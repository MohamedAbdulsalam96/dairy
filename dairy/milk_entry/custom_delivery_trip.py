from __future__ import unicode_literals
import frappe
from frappe import _
@frappe.whitelist()
def get_jinja_data(doc):
	res =frappe.db.sql("""
	select 
            ds.customer,ds.delivery_note,
            dn.route,
            dni.item_code,dni.item_name,dni.qty,dni.uom,dni.total_weight,dni.crate_count
        from
            `tabDelivery Trip` dt, `tabDelivery Stop` ds, `tabDelivery Note` dn, `tabDelivery Note Item` dni
        where 
            dt.docstatus =1 and dt.name = %(name)s and ds.parent = %(name)s and dn.name = ds.delivery_note and dni.parent = ds.delivery_note
             
             """,{"name":doc.name}, as_dict=True)

	return res

@frappe.whitelist()
def get_jinja_data_del_note(doc):
	res = frappe.db.sql("""
	select distinct(delivery_note) from `tabGate Pass Item` where parent = %(name)s """, {"name": doc.name}, as_dict=True)
	return res

@frappe.whitelist()
def del_note_details(del_note):
	res = frappe.db.sql("""
	select 
		name,customer_name,route
	from 
		`tabDelivery Note` where name = %(name)s """, {"name": del_note}, as_dict=True)
	return res

@frappe.whitelist()
def get_jinja_data_del_note_item(del_note):
	res = frappe.db.sql("""
	select 
		item_code,item_name,batch_no,uom,qty,free_qty,outgoing_count,incoming_count,crate_type
	from 
		`tabCrate Count Child` where parent = %(name)s """, {"name": del_note}, as_dict=True)
	return res

@frappe.whitelist()
def del_note_total(del_note):
	res = frappe.db.sql("""
		select 
			total_supp_qty,total_crate_qty,total_free_qty
		from 
			`tabDelivery Note` where name = %(name)s """, {"name": del_note}, as_dict=True)
	return res