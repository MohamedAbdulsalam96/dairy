
frappe.ui.form.on("Sales Order", {
	validate: function(frm) {        
        // var otm = frappe.model.get_value("Dairy Settings","Dairy Settings","morning_locking_time");
       
        frappe.model.get_value('Dairy Settings', {'name': 'Dairy Settings'}, 'morning_locking_time', function(d)
        {
            
            
            var otm = d.morning_locking_time;  
            var td = frappe.datetime.add_days(frappe.datetime.get_today(),1);
            if (frm.doc.delivery_shift == 'Morning') 
            {            
                if(frm.doc.delivery_date == frappe.datetime.get_today())
                {
                    frappe.validated = false;
                    frappe.throw(__('Order locking time is over'));
                    
                }            
                
                if(frm.doc.delivery_date == td)
                {
                    if(frm.doc.current_time > otm)
                    {
                        frappe.validated = false;
                        frappe.throw(__('Order locking time is over'));
                    }

                }

            }
        });

        frappe.model.get_value('Dairy Settings', {'name': 'Dairy Settings'}, 'evening_locking_time', function(e)
        {
            
            
            var ote = e.evening_locking_time;  
            
            if(frm.doc.delivery_shift == 'Evening')
            {
                if(frm.doc.delivery_date == frappe.datetime.get_today())
                {
                    if(frm.doc.current_time > ote)
                    {
                        frappe.validated = false;
                        frappe.throw(__('Order locking time is over'));
                    }
                }
            }
        });
    }
});