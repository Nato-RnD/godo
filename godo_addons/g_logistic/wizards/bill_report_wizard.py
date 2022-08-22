from odoo import api, models, fields, _

class BillReportWizard(models.TransientModel):
    _name = "godo.bill.report.wizard"
    _description = "Bill Report Wizard" 

    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')

    def bill_report_print(self):
        data = {
            'form': self.read()[0]
        }
        report_action = self.env.ref('g_logistic.action_bill_report').report_action(self, data=data)

        return report_action
