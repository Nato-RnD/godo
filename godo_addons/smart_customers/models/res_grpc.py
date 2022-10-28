import string
from odoo import api, fields, models, _, SUPERUSER_ID
import grpc
from .services import contract_service_pb2_grpc, contract_service_pb2
from concurrent import futures
from .grpc_server import *
_logger = logging.getLogger(__name__)


class ResGrpc(models.Model): 
    _name = 'res.grpc'
    _description = 'GRPC for Sync'

    name = fields.Char(string="gRPC service")

    def grpc_woker(self):
        with api.Environment.manage():
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            contract_service_pb2_grpc.add_AccountSyncServicer_to_server(AccountSyncServicer(self.env.cr), server)
            _logger.info('Starting server. Listening on port %s.' % 9999)
            server.add_insecure_port('[::]:%s' % 9999)
            # grpc_servers.update({self.id: server})
            server.start()
            server.wait_for_termination()


    def __init__(self, pool, cr):
        t = threading.Thread(name="%s.Bus" % 'GRPC', target=self.grpc_woker)
        t.daemon = True
        t.start()
        super().__init__(pool, cr)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    _description = _('GRPC Server')

    name = fields.Char(string='Name')
    listen_port = fields.Integer(string='Listening Port') 
    state = fields.Selection([('running', 'Running'), ('stopped', 'Stopped')], string='Status',
                             default='stopped')

    _sql_constraints = [
        ('listen_port_uniq', 'unique (listen_port)', 'The listen port must be unique !')
    ]

    def grpc_woker(self):
        with api.Environment.manage():
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            base_pb2_grpc.add_ProductsServicer_to_server(ProductServicer(self.env.cr), server)
            _logger.info('Starting server. Listening on port %s.' % self.listen_port)
            server.add_insecure_port('[::]:%s' % self.listen_port)
            grpc_servers.update({self.id: server})
            server.start()
            server.wait_for_termination()

    def action_start(self):
        self.write({'state': 'running'})
        t = threading.Thread(name="%s.Bus" % self.name, target=self.grpc_woker)
        t.daemon = True
        t.start()

    def action_stop(self):
        self.write({'state': 'stopped'})
        if grpc_servers.get(self.id, False):
            _logger.info('Stopping server on port %s.' % self.listen_port)
            grpc_servers.get(self.id).stop(0)




