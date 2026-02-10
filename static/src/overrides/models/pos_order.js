/** @odoo-module */

import { uuidv4 } from "@point_of_sale/utils";
import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
        const max = 999999999;
        const min = 100000000;
        this.numero_acceso_fel = Math.floor(Math.random() * (max - min + 1) + min);
    },
    waitForPushOrder() {
        return true;
    },
})