import string
from odoo import api, fields, models, _, SUPERUSER_ID
import grpc
from .services import contract_service_pb2_grpc, contract_service_pb2
from concurrent import futures
from .grpc_server import *
_logger = logging.getLogger(__name__)
grpc_servers = {}


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings' 

    service_name = fields.Char(string='Name', config_parameter='smart_customers.service_name')
    listen_port = fields.Integer(string='Listening Port', config_parameter='smart_customers.listen_port') 
    state = fields.Selection([('running', 'Running'), ('stopped', 'Stopped')], string='Status',
                             default='stopped', config_parameter='smart_customers.state')

    # _sql_constraints = [
    #     ('listen_port_uniq', 'unique (listen_port)', 'The listen port must be unique !')
    # ]
    
    @api.onchange('state')
    def state_onchange(self):
        if self.state  == 'running':
            self.action_start()
        else:
            self.action_stop()

    def grpc_woker(self):
        with api.Environment.manage():
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            contract_service_pb2_grpc.add_AccountSyncServicer_to_server(AccountSyncServicer(self.env.cr), server)
            _logger.info('Starting server. Listening on port %s.' % self.listen_port)
            server.add_insecure_port('[::]:%s' % self.listen_port)
            grpc_servers.update({self.id: server})
            server.start()
            server.wait_for_termination()

    def action_start(self):
        # self.write({'state': 'running'})
        self.env['ir.config_parameter'].sudo().set_param('smart_customers.state','running')
        t = threading.Thread(name="%s.Bus" % self.service_name, target=self.grpc_woker)
        t.daemon = True
        t.start()

    def action_stop(self):
        self.env['ir.config_parameter'].sudo().set_param('smart_customers.state','stopped')
        if grpc_servers.get(self.id, False):
            _logger.info('Stopping server on port %s.' % self.listen_port)
            grpc_servers.get(self.id).stop(0)
 

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            service_name = str(self.env['ir.config_parameter'].sudo().get_param('smart_customers.service_name')),
            listen_port = int(self.env['ir.config_parameter'].sudo().get_param('smart_customers.listen_port')),
            state = self.env['ir.config_parameter'].sudo().get_param('smart_customers.state')
        )
        return res
 
    @api.model
    def set_values(self):
        
        param = self.env['ir.config_parameter'].sudo() 

        param.set_param('smart_customers.service_name', self.service_name)
        param.set_param('smart_customers.listen_port',int( self.listen_port))
        param.set_param('smart_customers.state', self.state)
        super(ResConfigSettings, self).set_values()
        
 



