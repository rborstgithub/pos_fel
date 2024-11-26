/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";

patch(ReceiptScreen.prototype, {
    setup() {
        super.setup();
        if (!this.currentOrder.fel.firma_fel) {
            this.currentOrder.fel.contingencia_fel = true;
            
            // Es necesario volver a guardar la orden. Por qué la orden se guarda
            // al hacer el push_order al servidor. Y no se modifica al hace cambios.
            if (this.pos.db.get_order(this.currentOrder.uid)) {
                this.pos.db.add_order(this.currentOrder.export_as_JSON());
            }
        }
    }
});