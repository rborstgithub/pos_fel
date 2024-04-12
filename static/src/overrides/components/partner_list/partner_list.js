/** @odoo-module */
 
import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";


patch(PartnerListScreen.prototype, {
    async getNewPartners() {
        let result = await super.getNewPartners();
        if (!result.length) {
            result = await this.rpc({
                model: 'pos.session',
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
});
