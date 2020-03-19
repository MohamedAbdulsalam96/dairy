// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Route Master', {
	 onload: function(frm){
        frm.set_query('dest_warehouse', function(doc) {
            return {
                filters: {
                    "is_dcs":0,
                    "is_group":0,
                    "company":frappe.defaults.get_user_default("Company"),
                    "disabled":0
                }
            };
        });
        frm.set_query('source_warehouse', function(doc) {
            return {
                filters: {
                    "is_dcs":0,
                    "is_group":0,
                    "company":frappe.defaults.get_user_default("Company"),
                    "disabled":0
                }
            };
        });


        frm.set_query('driver', function(doc) {
            return {
                filters: {
                    "status":["=","Active"]
                }
            };
        });
        frm.trigger('set_property');

    },
    set_property: function(frm) {
         if(frm.doc.route_type =="Buying")
         {
            frm.set_df_property("dest_warehouse", "reqd", 1);
            frm.set_df_property("dest_warehouse", "hidden",0);

            frm.set_df_property("source_warehouse", "reqd", 0);
            frm.set_df_property("source_warehouse", "hidden",1);
         }
         else
         {
            frm.set_df_property("dest_warehouse", "reqd", 0);
            frm.set_df_property("dest_warehouse", "hidden",1);

            frm.set_df_property("source_warehouse", "reqd", 1);
            frm.set_df_property("source_warehouse", "hidden",0);
         }
    },
    route_type :function(frm){
        frm.trigger('set_property');
    },

//	refresh: function(frm) {
//	    if (frm.doc.docstatus===1) {
//            frm.add_custom_button(__("Add / Edit Prices"), function() {
//                frappe.route_options = {
//                    "price_list": frm.doc.name
//                };
//                frappe.set_route("Report", "Item Price");
//            }, "fa fa-money");
//		},
//	}

});