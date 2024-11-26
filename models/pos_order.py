# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

class PosOrder(models.Model):
    _inherit = 'pos.order'

    numero_acceso_fel = fields.Integer('Número de Accesso FEL')
    contingencia_fel = fields.Boolean('Contingencia FEL')
    firma_fel = fields.Char('Firma FEL', related='account_move.firma_fel')
    serie_fel = fields.Char('Serie FEL', related='account_move.serie_fel')
    numero_fel = fields.Char('Numero FEL', related='account_move.numero_fel')
    certificador_fel = fields.Char('Certificador FEL', related='account_move.certificador_fel')

    def _generate_pos_order_invoice(self):
        # No enviar PDF
        self = self.with_context(generate_pdf=False)
        return super(PosOrder, self)._generate_pos_order_invoice()
    
    def _get_invoice_lines_values(self, line_values, pos_order_line):
        res = super(PosOrder, self)._get_invoice_lines_values(line_values, pos_order_line)
        if pos_order_line.pack_lot_ids:
            lotes = ', '.join([l.lot_name for l in pos_order_line.pack_lot_ids if l.lot_name])
            res['name'] += ': '+lotes
        return res

    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()    
        res['numero_acceso_fel'] = self.numero_acceso_fel
        res['contingencia_fel'] = self.contingencia_fel
        if self.refunded_order_ids and self.refunded_order_ids.account_move:
            res['factura_original_id'] = self.refunded_order_ids.account_move.id
            res['motivo_fel'] = 'Anulación'
        return res

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        if ui_order.get('numero_acceso_fel'):
            res.update({'numero_acceso_fel': ui_order['numero_acceso_fel']})
        if ui_order.get('contingencia_fel'):
            res.update({'contingencia_fel': ui_order['contingencia_fel']})
        return res