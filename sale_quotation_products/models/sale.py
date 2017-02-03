# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from ast import literal_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def add_products_to_quotation(self):
        self.ensure_one()
        action_read = False
        actions = self.env.ref(
            'product.product_normal_action_sell')
        if actions:
            action_read = actions.read()[0]
            context = literal_eval(action_read['context'])
            context['sale_quotation_products'] = True
            context['pricelist'] = self.pricelist_id.display_name
            # we send company in context so it filters taxes
            context['company_id'] = self.company_id.id
            context['partner_id'] = self.partner_id.id
            action_read['context'] = context
            # action_read['view_mode'] = 'tree,form'
            action_read['name'] = _('Quotation Products')
        return action_read

    @api.multi
    def add_products(self, product_ids, qty):
        self.ensure_one()
        for product in self.env['product.product'].browse(product_ids):
            val = {
                'product_uom_qty': qty,
                'order_id': self.id,
                'product_id': product.id or False,
            }
            self.env['sale.order.line'].create(val)
