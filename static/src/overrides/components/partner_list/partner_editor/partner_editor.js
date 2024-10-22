/** @odoo-module */

import { PartnerDetailsEdit } from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
import { patch } from "@web/core/utils/patch";

patch(PartnerDetailsEdit.prototype, {
    setup() {
        super.setup(...arguments);
        this.changes.nombre_facturacion_fel = this.props.partner.nombre_facturacion_fel;
        this.changes.nit_facturacion_fel = this.props.partner.nit_facturacion_fel;
    },
});