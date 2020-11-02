frappe.ui.form.on("Delivery Note", {
    setup: function(frm) {
		frm.add_fetch("route", "source_warehouse", "set_warehouse");
		frm.add_fetch("route", "price_list", "selling_price_list");
		frm.add_fetch("route", "transporter", "transporter");
	},
//	calculate_crate: function(frm){
//	console.log("******************************************");
////	    cur_frm.cscript.calculate_crate()
//	    frm.call({
//        method:"dairy.milk_entry.custom_delivery_note.calculate_crate",
//        args: {
//                doc: cur_frm
//              },
//        callback: function(r)
//            {
//               cur_frm.reload_doc();
//            }
//        });
//
//	},
	refresh: function(frm){
        if (frm.doc.docstatus==1) {
				frm.remove_custom_button("Delivery Trip", 'Create');
			}
	},
	onload: function(frm){
	    if(frm.doc.__islocal){
//	         frm.set_df_property("calculate_crate", "hidden",1);
	         frm.set_df_property("crate_count", "hidden",1);
	         frm.set_df_property("loose_crate_", "hidden",1);
	    }
	    frm.trigger('set_property');
	    frm.set_query('route', function(doc) {
            return {
                filters: {
                    "company":doc.company,
                     "route_type":"Milk Marketing",
                    "docstatus":1
                }
            };
        });
	},


    after_save: function(frm){
            frm.set_df_property("crate_count", "hidden",0);
	        frm.set_df_property("loose_crate_", "hidden",0);
	        cur_frm.reload_doc();
      },

	customer:function(frm){
        return cur_frm.call({
            method:"dairy.milk_entry.custom_delivery_note.get_route_price_list",
            args: {
                    doc_name: cur_frm.doc.customer
                  },
            callback: function(r)
                {
                   if(r.message)
                   {
                    frm.set_value("route",r.message.route);
                     frm.set_value("selling_price_list",r.message.p_list);
                     frm.set_value("set_warehouse",r.message.warehouse);
                   }
                }
        });
    },

    route: function(frm){
        frm.add_fetch("route", "transporter", "transporter");
    },
});


//cur_frm.cscript.calculate_crate = function(frm){
//    return cur_frm.call({
//        method:"dairy.milk_entry.custom_delivery_note.calculate_crate",
//        args: {
//                doc: cur_frm
//              },
//        callback: function(r)
//            {
//               cur_frm.reload_doc();
//            }
//    });
//}

//frappe.ui.form.on("Delivery Note Item", {
//	fat: function(frm,cdt,cdn) {
//	    console.log("****************************************fat");
//		var row = locals[cdt][cdn];
//		if (row.snf_clr){
//            frm.call({
//				method: 'dairy.milk_entry.custom_delivery_note.change_rate',
//				args: {
//					item_code: row.item_code,
//					warehouse: row.warehouse,
//					posting_date: frm.doc.posting_date,
//					fat: row.fat,
//					snf_clr: row.snf_clr
//				},
//				callback: function(r) {
//					if(r.message) {
//					    row.rate = r.message;
//					}
//				}
//			});
//		}
//
//	},
//	snf_clr: function(frm,cdt,cdn) {
//		var row = locals[cdt][cdn];
//		if (row.fat){
//		    frm.call({
//				method: 'dairy.milk_entry.custom_delivery_note.change_rate',
//				args: {
//					item_code: row.item_code,
//					warehouse: row.warehouse,
//					posting_date: frm.doc.posting_date,
//					fat: row.fat,
//					snf_clr: row.snf_clr
//				},
//				callback: function(r) {
//					if(r.message) {
//					    row.rate = r.message;
//					    frm.refresh();
//					}
//				}
//			});
//		}
//
//	},
//
//});