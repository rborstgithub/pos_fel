# -*- encoding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PosSession(models.Model):
    _inherit = 'pos.session'

    def action_pos_session_close(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        for session in self:
            if session.config_id.invoice_journal_id and session.config_id.invoice_journal_id.generar_fel:
                # No deben existir pedidos sin factura asociada y que no estén cancelados o que no tenga valor cero
                pedidos_sin_facturar = session.order_ids.filtered(lambda order: not order.account_move and (order.state not in ['cancel'] or not order.currency_id.is_zero(order.amount_total)))

                # No deben existir pedidos facturados con valor diferente de cero y validados que no tengan firma
                pedidos_sin_firmar = session.order_ids.filtered(lambda order: order.account_move and not order.currency_id.is_zero(order.amount_total) and order.account_move.state == 'posted' and not order.account_move.firma_fel)

                if len(pedidos_sin_facturar) > 0:
                    raise ValidationError(f'Tiene pedidos sin factura ({', '.join(pedidos_sin_facturar.mapped('name'))}), no puede cerrar sesión mientras no haya facturado todos los pedidos.')
                
                if len(pedidos_sin_firmar) > 0:
                    raise ValidationError(f'Tiene pedidos con facturas sin firmar ({', '.join(pedidos_sin_firmar.mapped('name'))}), no puede cerrar sesión mientras no haya firmado todos los pedidos.')

        return super().action_pos_session_close(balancing_account, amount_to_balance, bank_payment_method_diffs)

    @api.model
    def crear_partner_con_datos_sat(self, company_id, vat):
        if company_id:
            company = self.env['res.company'].search([('id','=',company_id)])
            partners = self.env['res.partner'].search([('vat','=',vat)], limit=1)

            # Si el partner no existe se crea y si ya existe, se devuelve el que ya existe
            if len(partners) == 0:
                datos_facturacion_fel = self.env['res.partner'].obtener_datos_facturacion_fel(company, vat)
                if datos_facturacion_fel['nombre'] and datos_facturacion_fel['nit']:
                    partner_dic = {
                        'name': datos_facturacion_fel['nombre'],
                        'vat': datos_facturacion_fel['nit'],
                    }
                    new_partner = self.env['res.partner'].sudo().create(partner_dic)
                    return new_partner.id
                else:
                    return []
            else:
                return partners.id
        else:
            return []
