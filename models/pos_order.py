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
        return super(PosOrder, self.with_context(generate_pdf=False))._generate_pos_order_invoice()
    
    def _prepare_invoice_vals(self):
        res = super()._prepare_invoice_vals()    
        res['numero_acceso_fel'] = self.numero_acceso_fel
        res['contingencia_fel'] = self.contingencia_fel
        res['uuid_pos_fel'] = self.uuid
        if self.refunded_order_id and self.refunded_order_id.account_move:
            res['factura_original_id'] = self.refunded_order_id.account_move.id
            res['motivo_fel'] = 'Anulación'
        return res