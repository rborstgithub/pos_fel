# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

class PosOrder(models.Model):
    _inherit = 'pos.order'

    firma_fel = fields.Char('Firma FEL', related='account_move.firma_fel')
    serie_fel = fields.Char('Serie FEL', related='account_move.serie_fel')
    numero_fel = fields.Char('Numero FEL', related='account_move.numero_fel')
    certificador_fel = fields.Char('Certificador FEL', related='account_move.certificador_fel')
    
    def _get_invoice_lines_values(self, line_values, pos_order_line):
        res = super(PosOrder, self)._get_invoice_lines_values(line_values, pos_order_line)
        if pos_order_line.pack_lot_ids:
            lotes = ', '.join([l.lot_name for l in pos_order_line.pack_lot_ids if l.lot_name])
            res['name'] += ': '+lotes
        return res

    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()
        if self.refunded_order_ids and self.refunded_order_ids.account_move:
            res['factura_original_id'] = self.refunded_order_ids.account_move.id
            res['motivo_fel'] = 'Anulación'
        return res

