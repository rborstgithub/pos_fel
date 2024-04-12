/** @odoo-module */

import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";

import { formatDateTime } from "@web/core/l10n/dates";

import { onWillStart } from "@odoo/owl";

patch(OrderReceipt.prototype, {
    setup() {
        super.setup();
        this._fel = {firma_fel: '', serie_fel: '', numero_fel: '', certificador_fel: '', fecha_pedido: '', precio_total_descuento: 0};
        
        onWillStart(async () => {
            const env = this.receiptEnv;
            const fel = this._fel;
            const orderlines = this._receiptEnv.orderlines;

            const [order] = await this.rpc(
                {
                    model: 'pos.order',
                    method: 'search_read',
                    args: [[['pos_reference', '=', env.order.name]], ["firma_fel", "serie_fel", "numero_fel", "certificador_fel", "date_order"]],
                },
                {
                    timeout: 5000,
                    shadow: true,
                }
            );

            if (order) {
                fel.firma_fel = order.firma_fel;
                fel.serie_fel = order.serie_fel;
                fel.numero_fel = order.numero_fel;
                fel.certificador_fel = order.certificador_fel;
                fel.fecha_pedido = formatDateTime(order.date_order);

                let precio_total_descuento = 0;
                let precio_total_positivo = 0;

                orderlines.forEach(function(linea) {
                    if (linea.price * linea.quantity > 0) {
                        precio_total_positivo += linea.price * linea.quantity;
                    } else if (linea.price * linea.quantity < 0) {
                        precio_total_descuento += Math.abs(linea.price * linea.quantity);
                    }
                });

                fel.precio_total_descuento = precio_total_descuento;
                
                let descuento_porcentaje_fel = precio_total_descuento / precio_total_positivo;
                orderlines.forEach(function(linea) {
                    if (linea.price * linea.quantity > 0) {
                        linea.descuento_porcentaje_fel = descuento_porcentaje_fel * 100;
                        linea.descuento_nominal_fel = linea.price * linea.quantity * descuento_porcentaje_fel;
                    } else if (linea.price * linea.quantity < 0) {
                        linea.descuento_porcentaje_fel = 100;
                        linea.descuento_nominal_fel = linea.price * linea.quantity;
                    }
                });
            }
        });
    },
    
    get fel() {
        return this._fel;
    }
});