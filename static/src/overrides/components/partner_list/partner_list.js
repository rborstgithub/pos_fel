/** @odoo-module */
 
import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(PartnerListScreen.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
    },
    async getNewPartners() {
        let result = await super.getNewPartners();
        if (!result.length) {
            result = await this.orm.silent.call("pos.session", "crear_partner_con_datos_sat", [this.pos.company.id, this.state.query]);

            if (result.length) {
                this.state.selectedPartner = result[0];
                this.confirm();
            }
        }
        return result;
    }
});
