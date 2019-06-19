# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _create_mo(self):
        route_mto = self.env.ref('mrp.route_warehouse0_manufacture')
        route_manufacture = self.env.ref('stock.route_warehouse0_mto')

        def filter_line(l):
            consu = l.product_id.type in ['product', 'consu'] 
            zero = not float_is_zero(l.qty, precision_rounding=l.product_id.uom_id.rounding)
            #Make sure the product has both mto and produce route otherwise don't need to produce it directly from the pos
            produce = route_mto in l.product_id.route_ids and route_manufacture in l.product_id.route_ids
            return consu and zero and produce

        
        for order in self:
            mo_model = self.env['mrp.production']
            mrp_product = self.env['mrp.product.produce']
            for line in order.lines.filtered(filter_line):
                #Cannot produce if there is no bom, take the first bom
                if not line.product_id.bom_ids:
                    _logger.warning("Need a bom for product %s in order to generate a MO from the POS" % line.product_id.id)
                
                #Create directly the MO
                mo = mo_model.create({
                    'product_id': line.product_id.id,
                    'product_qty': line.qty,
                    'bom_id': line.product_id.bom_ids.ids[0],
                    'product_uom_id': line.product_id.uom_id.id,
                    'origin': order.name, #Keep track of the pos order that generate the MO
                })
                #Launch wizard Product: 1 create, 2 call onchange, 3 call the button
                wizard_default = mrp_product.with_context(active_id=mo.id).default_get([
                    'serial', 
                    'production_id', 
                    'product_id',
                    'product_qty',
                    'product_uom_id',
                ])
                wizard = mrp_product.create(wizard_default)
                wizard._onchange_product_qty()
                wizard.do_produce()
                #mark the MO as done
                mo.button_mark_done()

    def create_picking(self):
        """Create a picking for each order and validate it."""

        #First create mo to have the product to produce in stock and remove components from the stock
        self._create_mo()
        #Call super to create a picking for the final product (and other product) to move it to customer location
        return super().create_picking()
