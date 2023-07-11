odoo.define('pos_fel.PartnerListScreen', function (require) {
    'use strict';
    
    const PartnerListScreen = require('point_of_sale.PartnerListScreen');
    const Registries = require('point_of_sale.Registries');

    const PosFELPartnerListScreen = (PartnerListScreen) => class PosFELPartnerListScreen extends PartnerListScreen {
        async getNewPartners() {
            let result = await super.getNewPartners();
            if (!result.length) {
                result = await this.rpc({
                    model: 'res.partner',
                    method: 'crear_partner_con_datos_sat',
                    args: [[], [this.state.query, this.env.pos.company.id]],
                }, {
                    timeout: 3000,
                    shadow: true,
                });

                if (result.length) {
                    this.state.selectedPartner = result[0];
                    this.confirm();
                } else {
                    await this.showPopup('ErrorPopup', {
                        title: 'NIT',
                        body: this.env._t('El NIT no fue encontrado'),
                    });
                }
            }
            return result;
        }
    };
    Registries.Component.extend(PartnerListScreen, PosFELPartnerListScreen);
    
    return PosFELPartnerListScreen;
    
});
