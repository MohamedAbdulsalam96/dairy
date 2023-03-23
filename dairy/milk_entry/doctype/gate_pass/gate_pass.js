// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Pass', {
     onload : function(frm){

        frm.set_query('route', function(doc) {
            return {
                filters: {
                    "company":doc.company,
                     "route_type":"Milk Marketing",
                    "docstatus":1,
                    "transporter":doc.transporter
                }
            };
        });

        frm.set_query('transporter', function() {
			return {
				filters: {
					'is_transporter': 1
				}
			}
		});
     },

	 refresh: function(frm) {
	        if(! frm.doc.__islocal){
	            frm.set_df_property("items_section", "hidden", 1);
				frm.set_df_property("merge_items", "read_only", frm.is_new() ? 0 : 1);
	        }
	        if( frm.doc.__islocal){
	            frm.set_df_property("item", "reqd", 1);
	            frm.set_df_property("merge_items", "hidden", 1);
	            frm.set_df_property("crate_count_section", "hidden", 1);
                frm.set_df_property("loose_crate_section", "hidden", 1);

	        }
	        else{
	            frm.set_df_property("merge_items", "hidden", 0);
	            frm.set_df_property("crate_count_section", "hidden", 0);
                frm.set_df_property("loose_crate_section", "hidden", 0);
	        }
	        if ((frm.is_new())) {
            if (frm.doc.docstatus===0) {
				frm.add_custom_button(__('Delivery Note'),
					function() {
						erpnext.utils.map_current_doc({
							method: "dairy.milk_entry.doctype.gate_pass.gate_pass.make_delivery_note",
							source_doctype: "Delivery Note",
							target: me.frm,
							setters: {
							posting_date: frm.doc.date || undefined,
							route: frm.doc.route || undefined,
							shift: frm.doc.shift || undefined,
							transporter: frm.doc.transporter || undefined
							},

							get_query_filters: {
								docstatus: 1,
								status: ["=", ["To Bill"]],
                                crate_gate_pass_done:0
							}
						})
//						frappe.msgprint({
//                            title: __('Note'),
//                            indicator: 'green',
//                            message: __('After getting item. Save the document to see item details...')
//                        });
					
					
					}, __("Get items from"));

					frm.add_custom_button(__('Sales Invoice'),
					function() {
						console.log('route^^^^^^^^^^^^^^^',frm.doc.route)
						erpnext.utils.map_current_doc({
							method: "dairy.milk_entry.doctype.gate_pass.gate_pass.make_sales_invoice",
							source_doctype: "Sales Invoice",
							target: me.frm,
							setters: {
							posting_date: frm.doc.date || undefined,
							route: frm.doc.route || undefined,
							delivery_shift: frm.doc.shift || undefined,
							transporter: frm.doc.transporter || undefined
							},

							get_query_filters: {
								docstatus: 1,
								status: ["=", ["To Bill"]],
                                // crate_gate_pass_done:0
							}
						})
//						frappe.msgprint({
//                            title: __('Note'),
//                            indicator: 'green',
//                            message: __('After getting item. Save the document to see item details...')
//                        });
					
					
					}, __("Get items from"));
			}
			}
	 },

    calculate_crate: function(frm){
            if(frm.doc.name  && frm.doc.gate_crate_cal_done != "Done"){
                return cur_frm.call({
                    method:"dairy.milk_entry.doctype.gate_pass.gate_pass.calculate_crate",
                    args: {
                            doc_name: cur_frm.doc.name
                          },
                    callback: function(r)
                        {
                           cur_frm.reload_doc();
                        }
                });
                }
        },


});

