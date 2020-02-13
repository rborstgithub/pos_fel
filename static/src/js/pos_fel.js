odoo.define('pos_fel.pos_fel', function (require) {
"use strict";

var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');

var core = require('web.core');
var rpc = require('web.rpc');

var QWeb = core.qweb;

screens.ReceiptScreenWidget.include({
    render_receipt: function(){
        var order = this.pos.get_order();
        var self = this;

        console.log(order);

        rpc.query({
            model: 'pos.order',
            method: 'search_read',
            args: [[['pos_reference', '=', order.name]], ["firma_fel", "serie_fel", "numero_fel"]],
        }, {
            timeout: 3000,
        }).then(function (orders) {
            console.log(orders);
            if (orders.length > 0) {
                var env = self.get_receipt_render_env();
                env['firma_fel'] = orders[0].firma_fel;
                env['serie_fel'] = orders[0].serie_fel;
                env['numero_fel'] = orders[0].numero_fel;
                self.$('.pos-receipt-container').html(QWeb.render('OrderReceipt', env));
            }
        });
    }
})

// var _super_posmodel = models.PosModel.prototype;
// models.PosModel = models.PosModel.extend({
//     push_and_invoice_order: function(order){
//         var self = this;
//         var invoiced = _super_posmodel.push_and_invoice_order.apply(this, arguments);
//         invoiced.then(function(order_server_id) {
//             rpc.query({
//                     model: 'pos.order',
//                     method: 'search_read',
//                     args: [[['id', '=', order_server_id[0]]], ["firma_fel", "serie_fel", "numero_fel"]],
//                 }, {
//                     timeout: 3000,
//                 }).then(function (orders) {
//                     if (orders.length > 0) {
//                         self.get_order().firma_fel = orders[0].firma_fel
//                         self.get_order().serie_fel = orders[0].serie_fel
//                         self.get_order().numero_fel = orders[0].numero_fel
//                     }
//                 });
//         });
//         return invoiced;
//     }
// })

});
