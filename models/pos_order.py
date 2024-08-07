# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging
import re

class PosOrder(models.Model):
    _inherit = 'pos.order'

    firma_fel = fields.Char('Firma FEL', related='account_move.firma_fel')
    serie_fel = fields.Char('Serie FEL', related='account_move.serie_fel')
    numero_fel = fields.Char('Numero FEL', related='account_move.numero_fel')
    certificador_fel = fields.Char('Certificador FEL', related='account_move.certificador_fel')
    
    def _prepare_invoice_line(self, order_line):
        res = super(PosOrder, self)._prepare_invoice_line(order_line)
        if order_line.pack_lot_ids:
            lotes = ', '.join([l.lot_name for l in order_line.pack_lot_ids if l.lot_name])
            res['name'] += ': '+lotes
        return res

    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()
        
        partes = (self.pos_reference or 'Order 0-0-0').split('-');
        numero_acceso_fel = partes[0]+partes[2];
        numero_acceso_fel = int(re.sub(r'[^\d]+', '', numero_acceso_fel));
        
        res['numero_acceso_fel'] = numero_acceso_fel+140000000
        if self.pedido_origen_id and self.pedido_origen_id.account_move:
            res['factura_original_id'] = self.pedido_origen_id.account_move.id
            res['motivo_fel'] = 'Anulación'
        if self.refunded_order_ids and self.refunded_order_ids[0].account_move:
            res['factura_original_id'] = self.refunded_order_ids[0].account_move.id
            res['motivo_fel'] = 'Anulación'
        return res

