# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged
from odoo.tests.common import Form


@tagged('post_install', '-at_install')
class TestPurchaseToInvoice(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls):
        super(TestPurchaseToInvoice, cls).setUpClass()
        uom_unit = cls.env.ref('uom.product_uom_unit')
        uom_hour = cls.env.ref('uom.product_uom_hour')
        cls.product_order = cls.env['product.product'].create({
            'name': "Zed+ Antivirus",
            'standard_price': 235.0,
            'list_price': 280.0,
            'type': 'consu',
            'uom_id': uom_unit.id,
            'uom_po_id': uom_unit.id,
            'purchase_method': 'purchase',
            'default_code': 'PROD_ORDER',
            'taxes_id': False,
        })
        cls.service_deliver = cls.env['product.product'].create({
            'name': "Cost-plus Contract",
            'standard_price': 200.0,
            'list_price': 180.0,
            'type': 'service',
            'uom_id': uom_unit.id,
            'uom_po_id': uom_unit.id,
            'purchase_method': 'receive',
            'default_code': 'SERV_DEL',
            'taxes_id': False,
        })
        cls.service_order = cls.env['product.product'].create({
            'name': "Prepaid Consulting",
            'standard_price': 40.0,
            'list_price': 90.0,
            'type': 'service',
            'uom_id': uom_hour.id,
            'uom_po_id': uom_hour.id,
            'purchase_method': 'purchase',
            'default_code': 'PRE-PAID',
            'taxes_id': False,
        })
        cls.product_deliver = cls.env['product.product'].create({
            'name': "Switch, 24 ports",
            'standard_price': 55.0,
            'list_price': 70.0,
            'type': 'consu',
            'uom_id': uom_unit.id,
            'uom_po_id': uom_unit.id,
            'purchase_method': 'receive',
            'default_code': 'PROD_DEL',
            'taxes_id': False,
        })

    def test_vendor_bill_delivered(self):
        """Test if a order of product invoiced by delivered quantity can be
        correctly invoiced."""
        purchase_order = self.env['purchase.order'].with_context(tracking_disable=True).create({
            'partner_id': self.partner_a.id,
        })
        PurchaseOrderLine = self.env['purchase.order.line'].with_context(tracking_disable=True)
        pol_prod_deliver = PurchaseOrderLine.create({
            'name': self.product_deliver.name,
            'product_id': self.product_deliver.id,
            'product_qty': 10.0,
            'product_uom': self.product_deliver.uom_id.id,
            'price_unit': self.product_deliver.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        pol_serv_deliver = PurchaseOrderLine.create({
            'name': self.service_deliver.name,
            'product_id': self.service_deliver.id,
            'product_qty': 10.0,
            'product_uom': self.service_deliver.uom_id.id,
            'price_unit': self.service_deliver.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        purchase_order.button_confirm()

        self.assertEqual(purchase_order.invoice_status, "no")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 0.0)

        purchase_order.order_line.qty_received = 5
        self.assertEqual(purchase_order.invoice_status, "to invoice")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 5)
            self.assertEqual(line.qty_invoiced, 0.0)

        purchase_order.action_create_invoice()
        self.assertEqual(purchase_order.invoice_status, "invoiced")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 5)

    def test_vendor_bill_ordered(self):
        """Test if a order of product invoiced by ordered quantity can be
        correctly invoiced."""
        purchase_order = self.env['purchase.order'].with_context(tracking_disable=True).create({
            'partner_id': self.partner_a.id,
        })
        PurchaseOrderLine = self.env['purchase.order.line'].with_context(tracking_disable=True)
        pol_prod_order = PurchaseOrderLine.create({
            'name': self.product_order.name,
            'product_id': self.product_order.id,
            'product_qty': 10.0,
            'product_uom': self.product_order.uom_id.id,
            'price_unit': self.product_order.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        pol_serv_order = PurchaseOrderLine.create({
            'name': self.service_order.name,
            'product_id': self.service_order.id,
            'product_qty': 10.0,
            'product_uom': self.service_order.uom_id.id,
            'price_unit': self.service_order.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        purchase_order.button_confirm()

        self.assertEqual(purchase_order.invoice_status, "to invoice")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 10)
            self.assertEqual(line.qty_invoiced, 0.0)

        purchase_order.order_line.qty_received = 5
        self.assertEqual(purchase_order.invoice_status, "to invoice")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 10)
            self.assertEqual(line.qty_invoiced, 0.0)

        purchase_order.action_create_invoice()
        self.assertEqual(purchase_order.invoice_status, "invoiced")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 10)

    def test_vendor_bill_delivered_return(self):
        """Test when return product, a order of product invoiced by delivered
        quantity can be correctly invoiced."""
        purchase_order = self.env['purchase.order'].with_context(tracking_disable=True).create({
            'partner_id': self.partner_a.id,
        })
        PurchaseOrderLine = self.env['purchase.order.line'].with_context(tracking_disable=True)
        pol_prod_deliver = PurchaseOrderLine.create({
            'name': self.product_deliver.name,
            'product_id': self.product_deliver.id,
            'product_qty': 10.0,
            'product_uom': self.product_deliver.uom_id.id,
            'price_unit': self.product_deliver.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        pol_serv_deliver = PurchaseOrderLine.create({
            'name': self.service_deliver.name,
            'product_id': self.service_deliver.id,
            'product_qty': 10.0,
            'product_uom': self.service_deliver.uom_id.id,
            'price_unit': self.service_deliver.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        purchase_order.button_confirm()

        purchase_order.order_line.qty_received = 10
        purchase_order.action_create_invoice()
        self.assertEqual(purchase_order.invoice_status, "invoiced")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 10)

        purchase_order.order_line.qty_received = 5
        self.assertEqual(purchase_order.invoice_status, "to invoice")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, -5)
            self.assertEqual(line.qty_invoiced, 10)
        purchase_order.action_create_invoice()
        self.assertEqual(purchase_order.invoice_status, "invoiced")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 5)

    def test_vendor_bill_ordered_return(self):
        """Test when return product, a order of product invoiced by ordered
        quantity can be correctly invoiced."""
        purchase_order = self.env['purchase.order'].with_context(tracking_disable=True).create({
            'partner_id': self.partner_a.id,
        })
        PurchaseOrderLine = self.env['purchase.order.line'].with_context(tracking_disable=True)
        pol_prod_order = PurchaseOrderLine.create({
            'name': self.product_order.name,
            'product_id': self.product_order.id,
            'product_qty': 10.0,
            'product_uom': self.product_order.uom_id.id,
            'price_unit': self.product_order.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        pol_serv_order = PurchaseOrderLine.create({
            'name': self.service_order.name,
            'product_id': self.service_order.id,
            'product_qty': 10.0,
            'product_uom': self.service_order.uom_id.id,
            'price_unit': self.service_order.list_price,
            'order_id': purchase_order.id,
            'taxes_id': False,
        })
        purchase_order.button_confirm()

        purchase_order.order_line.qty_received = 10
        purchase_order.action_create_invoice()
        self.assertEqual(purchase_order.invoice_status, "invoiced")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 10)

        purchase_order.order_line.qty_received = 5
        self.assertEqual(purchase_order.invoice_status, "invoiced")
        for line in purchase_order.order_line:
            self.assertEqual(line.qty_to_invoice, 0.0)
            self.assertEqual(line.qty_invoiced, 10)

    def test_vendor_severals_bills_and_multicurrency(self):
        """
        This test ensures that, when adding several PO to a bill, if they are expressed with different
        currency, the amount of each AML is converted to the bill's currency
        """
        PurchaseOrderLine = self.env['purchase.order.line']
        PurchaseBillUnion = self.env['purchase.bill.union']
        ResCurrencyRate = self.env['res.currency.rate']
        usd = self.env.ref('base.USD')
        eur = self.env.ref('base.EUR')
        purchase_orders = []

        ResCurrencyRate.create({'currency_id': usd.id, 'rate': 1})
        ResCurrencyRate.create({'currency_id': eur.id, 'rate': 2})

        for currency in [usd, eur]:
            po = self.env['purchase.order'].with_context(tracking_disable=True).create({
                'partner_id': self.partner_a.id,
                'currency_id': currency.id,
            })
            pol_prod_order = PurchaseOrderLine.create({
                'name': self.product_order.name,
                'product_id': self.product_order.id,
                'product_qty': 1,
                'product_uom': self.product_order.uom_id.id,
                'price_unit': 1000,
                'order_id': po.id,
                'taxes_id': False,
            })
            po.button_confirm()
            pol_prod_order.write({'qty_received': 1})
            purchase_orders.append(po)

        move_form = Form(self.env['account.move'].with_context(default_move_type='in_invoice'))
        move_form.purchase_vendor_bill_id = PurchaseBillUnion.browse(-purchase_orders[0].id)
        move_form.purchase_vendor_bill_id = PurchaseBillUnion.browse(-purchase_orders[1].id)
        move = move_form.save()
        amls = move.line_ids.filtered(lambda l: l.account_internal_group == 'expense')

        self.assertEqual(move.amount_total, 1500)
        self.assertEqual(move.currency_id, usd)
        self.assertEqual(len(amls), 2)
        self.assertEqual(amls[0].amount_currency, 1000)
        self.assertEqual(amls[1].amount_currency, 500)

    def test_product_price_decimal_accuracy(self):
        self.env.ref('product.decimal_price').digits = 3
        self.env.company.currency_id.rounding = 0.01

        po = self.env['purchase.order'].with_context(tracking_disable=True).create({
            'partner_id': self.partner_a.id,
            'order_line': [(0, 0, {
                'name': self.product_a.name,
                'product_id': self.product_a.id,
                'product_qty': 12,
                'product_uom': self.product_a.uom_id.id,
                'price_unit': 0.001,
                'taxes_id': False,
            })]
        })
        po.button_confirm()
        po.order_line.qty_received = 12

        move_form = Form(self.env['account.move'].with_context(default_move_type='in_invoice'))
        move_form.purchase_vendor_bill_id = self.env['purchase.bill.union'].browse(-po.id)
        move = move_form.save()

        self.assertEqual(move.amount_total, 0.01)

    def test_vendor_bill_analytic_account_default_change(self):
        """ Tests whether, when an analytic account rule is set, and user changes manually the analytic account on
        the po, it is the same that is mentioned in the bill.
        """
        analytic_account_default = self.env['account.analytic.account'].create({'name': 'default'})
        analytic_account_manual = self.env['account.analytic.account'].create({'name': 'manual'})

        self.env['account.analytic.default'].create({
            'analytic_id': analytic_account_default.id,
            'product_id': self.product_order.id,
        })

        po_form = Form(self.env['purchase.order'].with_context(tracking_disable=True))
        po_form.partner_id = self.partner_a
        with po_form.order_line.new() as po_line_form:
            po_line_form.name = self.product_order.name
            po_line_form.product_id = self.product_order
            po_line_form.product_qty = 1.0
            po_line_form.price_unit = 10
            po_line_form.account_analytic_id = analytic_account_manual

        purchase_order = po_form.save()
        purchase_order.button_confirm()
        purchase_order.action_create_invoice()

        aml = self.env['account.move.line'].search([('purchase_line_id', '=', purchase_order.order_line.id)])
        self.assertRecordValues(aml, [{'analytic_account_id': analytic_account_manual.id}])

    def test_multicompany_partner_bank(self):
        """ Test that in a multiple company environment, the bank account of the invoice
            is the one corresponding to the active company. """
        company_a = self.env.user.company_id
        company_b = self.env['res.company'].create({
            'name': 'Company B',
        })
        self.env.ref('l10n_generic_coa.configurable_chart_template')._load(15.0, 15.0, company_b)

        partner = self.env['res.partner'].create({
            'name': 'AAAAA',
        })
        partner_bank_a = self.env['res.partner.bank'].create({
            'acc_number': "BE01 23456789 10",
            'partner_id': partner.id,
            'company_id': company_a.id,
            'acc_type': 'bank'
        })
        partner_bank_b = self.env['res.partner.bank'].create({
            'acc_number': "BE10 98765432 10",
            'partner_id': partner.id,
            'company_id': company_b.id,
            'acc_type': 'bank'
        })
        partner.bank_ids = [partner_bank_a.id, partner_bank_b.id]

        PurchaseOrder = self.env['purchase.order'].with_context(tracking_disable=True)
        po_a = PurchaseOrder.with_company(company_a).create({
            'partner_id': partner.id,
            'company_id': company_a.id,
            'currency_id': company_a.currency_id.id,
            'date_order': '2019-01-01',
        })
        po_b = PurchaseOrder.with_company(company_b).create({
            'partner_id': partner.id,
            'company_id': company_b.id,
            'currency_id': company_b.currency_id.id,
            'date_order': '2019-01-01',
        })

        vals_pol = {
            'name': self.product_deliver.name,
            'product_id': self.product_deliver.id,
            'product_qty': 10.0,
            'product_uom': self.product_deliver.uom_id.id,
            'price_unit': self.product_deliver.list_price,
            'order_id': po_a.id,
            'taxes_id': False,
        }
        PurchaseOrderLine = self.env['purchase.order.line'].with_context(tracking_disable=True)
        PurchaseOrderLine.create(vals_pol)
        vals_pol['order_id'] = po_b.id
        PurchaseOrderLine.create(vals_pol)

        po_a.button_confirm()
        po_b.button_confirm()

        po_a.order_line.qty_received = po_b.order_line.qty_received = 10

        po_a.with_company(company_a).action_create_invoice()
        po_b.with_company(company_b).action_create_invoice()

        self.assertEqual(po_a.invoice_ids.company_id, company_a)
        self.assertEqual(po_a.invoice_ids.partner_bank_id, partner_bank_a)

        self.assertEqual(po_b.invoice_ids.company_id, company_b)
        self.assertEqual(po_b.invoice_ids.partner_bank_id, partner_bank_b)
