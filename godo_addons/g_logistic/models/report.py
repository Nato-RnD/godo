from odoo import models,fields,api

class BillReport(models.AbstractModel):
    _name="godo.bill.report"

    @api.model
    def report_action(self, docids, data=None):
        self.ensure_one()
        print ("Da goi khi load")