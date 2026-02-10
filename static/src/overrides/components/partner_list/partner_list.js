/** @odoo-module */
 
import { PartnerList } from "@point_of_sale/app/screens/partner_list/partner_list";
import { patch } from "@web/core/utils/patch";

patch(PartnerList.prototype, {
    async getNewPartners() {
        let result = await super.getNewPartners();
        if (result.length <= 0) {
            const partner_id = await this.pos.data.silentCall("pos.session", "crear_partner_con_datos_sat", [this.pos.company.id, this.state.query]);
            if (partner_id) {
                result = await this.pos.data.searchRead("res.partner", [['id','=',partner_id]], [], {});
            }
        }
        return result;
    }
});
