# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class PosOrder(models.Model):
    _inherit = 'pos.order'

    firma_fel = fields.Char('Firma FEL', related='account_move.firma_fel')
    serie_fel = fields.Char('Serie FEL', related='account_move.serie_fel')
    numero_fel = fields.Char('Numero FEL', related='account_move.numero_fel')
