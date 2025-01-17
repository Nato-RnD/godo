# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CalendarAlarm(models.Model):
    _inherit = 'calendar.alarm'

    alarm_type = fields.Selection(selection_add=[
        ('sms', 'SMS Text Message')
    ], ondelete={'sms': 'set default'})
    sms_template_id = fields.Many2one(
        'sms.template', string="SMS Template",
        domain=[('model', 'in', ['calendar.event'])],
        compute='_compute_sms_template_id', readonly=False, store=True,
        help="Template used to render SMS reminder content.")

    @api.depends('alarm_type', 'mail_template_id')
    def _compute_sms_template_id(self):
        for alarm in self:
            if alarm.alarm_type == 'sms' and not alarm.sms_template_id:
                alarm.sms_template_id = self.env['ir.model.data']._xmlid_to_res_id('calendar_sms.sms_template_data_calendar_reminder')
            elif alarm.alarm_type != 'sms' or not alarm.sms_template_id:
                alarm.sms_template_id = False
