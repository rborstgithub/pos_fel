# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import collections
import re

import requests
import logging
from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    def crear_partner_con_datos_sat(self, datos_cliente):
        query = datos_cliente[0]
        fields = datos_cliente[1]
        company_id = datos_cliente[2]

        company_id = self.env['res.company'].search([('id','=',company_id)])
        partners = self.env['res.partner'].search([('vat','=',query)])

        if company_id:
            # Si el partner no existe se crea y si ya existe, se devuelve el que ya existe
            if len(partners) == 0:
                datos_facturacion_fel = self._datos_sat(company_id, query)
                
                partner_dic = {
                    'name': datos_facturacion_fel['nombre'],
                    'vat': datos_facturacion_fel['nit'],
                }
                partner = self.create(partner_dic)
                return partner.read(fields)
            else:
                return partners.read(fields)
        else:
            return []
