# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import logging

class PosOrder(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_new_partner(self, config_id, domain, offset):
        result = super().get_new_partner(config_id, domain, offset)
        config = self.env['pos.config'].browse(config_id)

        if len(result['res.partner']) == 0:
            vat_domain = [x for x in domain if x[0] == 'vat']

            if len(vat_domain):
                vat = vat_domain[0][2].replace('%', '')
                
                datos_facturacion_fel = self.env['res.partner'].obtener_datos_facturacion_fel(vat)
                if datos_facturacion_fel['nombre'] and datos_facturacion_fel['nit']:
                    partner_dic = {
                        'name': datos_facturacion_fel['nombre'],
                        'vat': datos_facturacion_fel['nit'],
                    }
                    new_partner = self.env['res.partner'].sudo().create(partner_dic)

                    result['res.partner'] = self._load_pos_data_read(new_partner, config)
                    result['account.fiscal.position'] = self.env['account.fiscal.position']._load_pos_data_read(new_partner.fiscal_position_id, config),
        
        return result

