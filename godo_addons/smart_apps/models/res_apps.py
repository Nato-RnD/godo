from re import S
import time
from odoo import models, fields, api, _
import luhn
import random
import math
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class ResApps(models.Model): 
    _name = 'res.apps' 
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('Smart App')
    
    STATUS_SELECTION = [
        ('draft', 'Draft'),  # method action_pos_session_open
        ('activated', 'Activated'),               # method action_pos_session_closing_control
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')  # method action_pos_session_close
    ]
    
    app_code = fields.Char(string="Apps Code")
    name = fields.Char(string="Apps Name", required=True )
    app_version = fields.Char(string = 'App Version', max_leghth = 3)
    app_icon = fields.Binary(string='App Icon')
    registered_date = fields.Datetime(string="Registered Date")
    private_key = fields.Text(string="Private Key")
    public_key = fields.Text(string="Public Key" )
    status = fields.Selection(STATUS_SELECTION, string='Status', default='draft')
    
 
    
    
    @api.model
    def create(self, vals):
        if not self.id:
            #Dinh dang app code YYMM XXX C RRR C 
            # YY = year with rear 2 digits, MM is month with 2 digits, C is checksum with luhn alt, RRR as random 3 digits
            _temp_code = '%s%s%s' % (datetime.now().strftime('%y'), datetime.now().strftime('%m'), vals.get('app_version','001'))
            _pre_luhn = luhn.append(_temp_code)
            _random_code = "{:03d}".format(math.ceil(random.random() * 1000))
            vals['app_version'] = vals.get('app_version','001')
            vals['app_code'] = luhn.append('%s%s' % (_pre_luhn, _random_code)) 
            vals['registered_date'] = time.strftime('%Y-%m-%d')
            pri, pub = self.rsa_generator()
            vals['private_key'] = pri
            vals['public_key'] = pub
        
        res = super(ResApps, self).create(vals) 
        return res
    
    
    def rsa_generator(self) :
        # generate private/public key pair
        key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=1024)

        # get public key in OpenSSH format
        public_key = key.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
       
        # get private key in PEM container format
        pem = key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        # decode to printable strings
        private_key_str = pem.decode('utf-8')
        public_key_str = public_key.decode('utf-8')
        return private_key_str,public_key_str 