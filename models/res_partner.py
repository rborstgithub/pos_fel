# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
import logging

class Partner(models.Model):
    _inherit = 'res.partner'

    def crear_partner_con_datos_sat(self, datos_cliente):
        query = datos_cliente[0]
        company_id = datos_cliente[1]

        company_id = self.env['res.company'].search([('id','=',company_id)])

        if company_id:
            datos_facturacion_fel = self._datos_sat(company_id, query)
            
            partner_dic = {
                'name': datos_facturacion_fel['nombre'],
                'vat': datos_facturacion_fel['nit'],
            }
            partner = self.create(partner_dic)
            params = self._loader_params_res_partner()
            return partner.read(params['search_params']['fields'])
        else:
            return []
