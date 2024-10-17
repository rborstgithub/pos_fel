# -*- encoding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PosSession(models.Model):
    _inherit = 'pos.session'

    def action_pos_session_validate(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        for session in self:
            if session.config_id.invoice_journal_id and session.config_id.invoice_journal_id.generar_fel:
                if len(session.order_ids.filtered(lambda order: order.state not in ['invoiced', 'cancel'] and order.amount_total > 0)) > 0:
                    raise ValidationError('Tiene pedidos sin factura, no puede cerrar sesión mientras no haya facturado todos los pedidos.')
                for order in session.order_ids.filtered(lambda order: order.state == 'invoiced' and order.amount_total > 0):
                    if order.account_move.state != 'open' and not order.account_move.firma_fel:
                        raise ValidationError('La factura del pedido {} no está firmada, por favor ingrese a la factura y validela para poder cerrar sesión.'.format(order.name))

        return super(PosSession, self).action_pos_session_validate(balancing_account, amount_to_balance, bank_payment_method_diffs)

    @api.model
    def crear_partner_con_datos_sat(self, query, company_id):
        company_id = self.env['res.company'].search([('id','=',company_id)])

        if company_id:
            datos_facturacion_fel = self.env['res.partner']._datos_sat(company_id, query)
            if datos_facturacion_fel['nombre']:
                partner_dic = {
                    'name': datos_facturacion_fel['nombre'],
                    'vat': datos_facturacion_fel['nit'],
                }
                partner = self.env['res.partner'].create(partner_dic)
                params = self._loader_params_res_partner()
                return partner.read(params['search_params']['fields'])
            else:
                return []
        else:
            return []
