/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    wait_for_push_order() {
        return true;
    },
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.fel = this.fel;
        console.log(this.fel);
        return result;
    }
})