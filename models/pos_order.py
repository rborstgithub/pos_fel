# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

class PosOrder(models.Model):
    _inherit = 'pos.order'

    firma_fel = fields.Char('Firma FEL', related='account_move.firma_fel')
    serie_fel = fields.Char('Serie FEL', related='account_move.serie_fel')
    numero_fel = fields.Char('Numero FEL', related='account_move.numero_fel')
    certificador_fel = fields.Char('Certificador FEL', related='account_move.certificador_fel')
    comercial = fields.Char(string='Asesor', compute="_obtener_comercial")
    usuario = fields.Char(string='Usuario', compute="_obtener_usuario")

    def _obtener_comercial(self):
        self.comercial = ''
        if self.lines[0] and self.lines[0].sale_order_origin_id and self.lines[0].sale_order_origin_id.user_id:
            self.comercial = self.lines[0].sale_order_origin_id.user_id.name

    def _obtener_usuario(self):
        self.usuario = ''
        if self.user_id:
            self.usuario = self.user_id.name

    def _prepare_invoice_line(self, order_line):
        res = super(PosOrder, self)._prepare_invoice_line(order_line)
        if order_line.pack_lot_ids:
            lotes = ', '.join([l.lot_name for l in order_line.pack_lot_ids if l.lot_name])
            res['name'] += ': '+lotes
        return res

    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()
        if self.refunded_orders_count == 1 and self.refunded_order_ids.account_move:
            res['factura_original_id'] = self.refunded_order_ids.account_move.id
            res['motivo_fel'] = 'Anulación'
        if self.refunded_order_ids and self.refunded_order_ids[0].account_move:
            res['factura_original_id'] = self.refunded_order_ids[0].account_move.id
            res['motivo_fel'] = 'Anulación'
        return res

