/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { ReprintReceiptButton } from "@point_of_sale/app/screens/ticket_screen/reprint_receipt_button/reprint_receipt_button";

patch(ReprintReceiptButton.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
    },
    async click() {        
        if (!this.props.order) {
            return;
        }
        
        const [savedOrder] = await this.orm.searchRead(
            "pos.order",
            [["id", "in", [this.props.order.server_id]]],
            [
                "firma_fel",
                "serie_fel",
                "numero_fel",
                "certificador_fel",
            ],
        );

        this.props.order.fel = {
            firma_fel: '',
            serie_fel: '',
            numero_fel: '',
            certificador_fel: '',
            precio_total_descuento: 0,
        }

        if (savedOrder) {
            this.props.order.fel.firma_fel = savedOrder.firma_fel;
            this.props.order.fel.serie_fel = savedOrder.serie_fel;
            this.props.order.fel.numero_fel = savedOrder.numero_fel;
            this.props.order.fel.certificador_fel = savedOrder.certificador_fel;

            let precio_total_descuento = 0;
            let precio_total_positivo = 0;

            this.props.order.get_orderlines().forEach(function(linea) {
                if (linea.price * linea.quantity > 0) {
                    precio_total_positivo += linea.price * linea.quantity;
                } else if (linea.price * linea.quantity < 0) {
                    precio_total_descuento += Math.abs(linea.price * linea.quantity);
                }
            });

            this.props.order.fel.precio_total_descuento = precio_total_descuento;
            
            let descuento_porcentaje_fel = precio_total_descuento / precio_total_positivo;
            this.props.order.get_orderlines().forEach(function(linea) {
                if (linea.price * linea.quantity > 0) {
                    linea.descuento_porcentaje_fel = descuento_porcentaje_fel * 100;
                    linea.descuento_nominal_fel = linea.price * linea.quantity * descuento_porcentaje_fel;
                } else if (linea.price * linea.quantity < 0) {
                    linea.descuento_porcentaje_fel = 100;
                    linea.descuento_nominal_fel = linea.price * linea.quantity;
                }
            });
        }
        return super.click(...arguments);
    },
});
