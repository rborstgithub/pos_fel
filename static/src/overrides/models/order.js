/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.fel = {
            firma_fel: '',
            serie_fel: '',
            numero_fel: '',
            certificador_fel: '',
            numero_acceso_fel: 0,
            contingencia_fel: false,
            precio_total_descuento: 0,
        }
        const max = 999999999;
        const min = 100000000;
        this.fel.numero_acceso_fel = Math.floor(Math.random() * (max - min + 1) + min);
    },
    wait_for_push_order() {
        return true;
    },
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.fel = this.fel;
        return result;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.numero_acceso_fel = this.fel.numero_acceso_fel;
        json.contingencia_fel = this.fel.contingencia_fel;
        return json;
    },
})