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
        this.uuid_pos_fel = uuidv4();
    },
    wait_for_push_order() {
        return true;
    },
    export_for_printing(baseUrl, headerData) {
        const result = super.export_for_printing(...arguments);

        const lineas_pedido = this.getSortedOrderlines();
        
        result.orderlines.forEach((linea_recibo, indice) => {
            const linea_pedido = lineas_pedido[indice];
            const producto = linea_pedido.product_id;
            const nombre_linea_venta = linea_pedido.sale_order_line_id?.name || "";
            const nombre_producto = producto?.display_name || "";

            const nombre_producto_con_codigo = producto?.default_code
                    ? `[${producto.default_code}] ${nombre_producto}`
                    : nombre_producto;

            const nombre_linea_venta_sin_codigo = nombre_linea_venta.replace(/^\[[^\]]+\]\s*/, "");        
            const descripcion = nombre_producto && nombre_linea_venta_sin_codigo.startsWith(nombre_producto)
                    ? nombre_linea_venta_sin_codigo.slice(nombre_producto.length).trim()
                    : "";
        
            linea_recibo.productName = descripcion || nombre_producto_con_codigo;        
            linea_recibo.discount = "";        
            const cantidad = linea_pedido.get_quantity();
            const precio_unitario_con_descuento = cantidad
                    ? linea_pedido.get_price_with_tax() / cantidad
                    : 0;
        
            const simbolo_moneda = linea_pedido.currency?.symbol || "Q";        
            linea_recibo.unitPrice = `${simbolo_moneda} ${precio_unitario_con_descuento.toFixed(8)}`;
        });

        result.fel = {}
        result.fel['firma_fel'] = this.firma_fel;
        result.fel['serie_fel'] = this.serie_fel;
        result.fel['numero_fel'] = this.numero_fel;
        result.fel['certificador_fel'] = this.certificador_fel;
        result.fel['numero_acceso_fel'] = this.numero_acceso_fel;
        result.fel['contingencia_fel'] = this.contingencia_fel;
        result.fel['precio_total_descuento'] = this.precio_total_descuento || 0;
        result.is_to_invoice = this.is_to_invoice()
        return result;
    },
})