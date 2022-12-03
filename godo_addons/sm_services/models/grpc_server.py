import grpc
from .services import contract_service_pb2_grpc, contract_service_pb2
from odoo import api, fields, models, _, SUPERUSER_ID, registry
from odoo.exceptions import Warning, UserError
import logging, threading
from google.protobuf.json_format import MessageToDict 
_logger = logging.getLogger(__name__)


class AccountSyncServicer (contract_service_pb2_grpc.AccountSyncServicer):
    def __init__(self, cr): 
        self.env = api.Environment(cr, SUPERUSER_ID, {}) 

    def AccountSyncMethod(self, request, context):
        _logger.info('System received a request to get product info!') 
        response = contract_service_pb2.AccountSyncResponse()
        _logger.info(request) 
        
        data = MessageToDict(request,preserving_proto_field_name=True)
        data['name'] = '%s [%s %s - %s]' % (data['profile_code'], data['last_name'], data['first_name'], data['user_name'])
        

        with api.Environment.manage():
            with registry(self.env.cr.dbname).cursor() as new_cr:
                new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                
                 
                account =  new_env['res.account'].browse(0)
                account.create(data) 
                try:
                    new_cr.commit()
                    response.synced = True 
                except Exception:
                    new_cr.rollback()
                    response.synced = False  
                
        return response
    
   