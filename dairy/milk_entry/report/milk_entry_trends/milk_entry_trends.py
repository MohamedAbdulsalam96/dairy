# Copyright (c) 2013, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate


def execute(filters=None):
    conditions = get_columns(filters, "Milk Entry")
    data = get_data(filters, conditions)
    return conditions["columns"], data

def get_columns(filters, trans):
	validate_filters(filters)

	# get conditions for based_on filter cond
	based_on_details = based_wise_columns_query(filters.get("based_on"), trans)

	print("===based_on_details",based_on_details)
	# get conditions for periodic filter cond
	period_cols, period_select = period_wise_columns_query(filters, trans)
	print("===period_cols", period_cols,"====period_select",period_select)

	# get conditions for grouping filter cond
	group_by_cols = group_wise_column(filters.get("group_by"))
	print("====group_by_cols",group_by_cols)

	columns = based_on_details["based_on_cols"] + period_cols + [_("Total(Qty)") + ":Float:120", _("Total(Amt)") + ":Currency:120"]
	if group_by_cols:
		columns = based_on_details["based_on_cols"] + group_by_cols + period_cols + \
			[_("Total(Qty)") + ":Float:120", _("Total(Amt)") + ":Currency:120"]

	conditions = {"based_on_select": based_on_details["based_on_select"], "period_wise_select": period_select,
		"columns": columns, "group_by": based_on_details["based_on_group_by"], "grbc": group_by_cols, "trans": trans,
		"addl_tables": based_on_details["addl_tables"], "addl_tables_relational_cond": based_on_details.get("addl_tables_relational_cond", "")}

	return conditions

def validate_filters(filters):
	for f in ["Fiscal Year", "Based On", "Period", "Company"]:
		if not filters.get(f.lower().replace(" ", "_")):
			frappe.throw(_("{0} is mandatory").format(f))

	if not frappe.db.exists("Fiscal Year", filters.get("fiscal_year")):
		frappe.throw(_("Fiscal Year: {0} does not exists").format(filters.get("fiscal_year")))

	if filters.get("based_on") == filters.get("group_by"):
		frappe.throw(_("'Based On' and 'Group By' can not be same"))

def get_data(filters, conditions):
	data = []
	inc, cond= '',''
	query_details =  conditions["based_on_select"] + conditions["period_wise_select"]

	posting_date = 't1.date'
	# if conditions.get('trans') in ['Sales Invoice', 'Purchase Invoice', 'Purchase Receipt', 'Delivery Note']:
	# 	posting_date = 't1.posting_date'
	# 	if filters.period_based_on:
	# 		posting_date = 't1.'+filters.period_based_on

	if conditions["based_on_select"] in ["t1.project,", "t2.project,"]:
		cond = ' and '+ conditions["based_on_select"][:-1] +' IS Not NULL'
	if conditions.get('trans') in ['Sales Order', 'Purchase Order']:
		cond += " and t1.status != 'Closed'"

	if conditions.get('trans') == 'Quotation' and filters.get("group_by") == 'Customer':
		cond += " and t1.quotation_to = 'Customer'"

	year_start_date, year_end_date = frappe.db.get_value("Fiscal Year",
		filters.get('fiscal_year'), ["year_start_date", "year_end_date"])

	if filters.get("group_by"):
		sel_col = ''
		ind = conditions["columns"].index(conditions["grbc"][0])

		# if filters.get("group_by") == 'Item':
		# 	sel_col = 't2.item_code'
		if filters.get("group_by") == 'dcs':
			sel_col = 't1.dcs_id'
		elif filters.get("group_by") == 'member':
			sel_col = 't1.member'
		elif filters.get("group_by") == 'shift':
			sel_col = 't1.shift'

		if filters.get('based_on') in ['dcs','milk_type']:
			inc = 1
		else :
			inc = 0

		data1 = frappe.db.sql(""" select %s from `tabMilk Entry` t1
					where  t1.company = %s and %s between %s and %s and
					t1.docstatus = 1 %s %s
					group by %s
				""" % (query_details,"%s",
					posting_date, "%s", "%s", conditions.get("addl_tables_relational_cond"), cond, conditions["group_by"]), (filters.get("company"),
					year_start_date, year_end_date),as_list=1)


		print("===data1",data1)
		for d in range(len(data1)):
			#to add blanck column
			dt = data1[d]
			dt.insert(ind,'')
			data.append(dt)

			#to get distinct value of col specified by group_by in filter
			row = frappe.db.sql("""select DISTINCT(%s) from `tab%s` t1
						where t1.company = %s and %s between %s and %s
						and t1.docstatus = 1 and %s = %s %s %s
					""" %
					(sel_col,  conditions["trans"],
						"%s", posting_date, "%s", "%s", conditions["group_by"], "%s", conditions.get("addl_tables_relational_cond"), cond),
					(filters.get("company"), year_start_date, year_end_date, data1[d][0]), as_list=1)

			for i in range(len(row)):
				des = ['' for q in range(len(conditions["columns"]))]

				#get data for group_by filter
				row1 = frappe.db.sql(""" select %s , %s from `tab%s` t1
							where t1.company = %s and %s between %s and %s
							and t1.docstatus = 1 and %s = %s and %s = %s %s %s
						""" %
						(sel_col, conditions["period_wise_select"], conditions["trans"],
							 "%s", posting_date, "%s","%s", sel_col,
							"%s", conditions["group_by"], "%s", conditions.get("addl_tables_relational_cond"), cond),
						(filters.get("company"), year_start_date, year_end_date, row[i][0],
							data1[d][0]), as_list=1)

				des[ind] = row[i][0]

				for j in range(1,len(conditions["columns"])-inc):
					des[j+inc] = row1[0][j]

				data.append(des)
	else:
		check = (""" select %s from `tab%s` t1
					where t1.company = %s and %s between %s and %s and
					t1.docstatus = 1 %s %s
					group by %s
				""" %(query_details, conditions["trans"],
					"%s", posting_date, "%s", "%s", cond, conditions.get("addl_tables_relational_cond", ""), conditions["group_by"]),
				(filters.get("company"), year_start_date, year_end_date))

		print("===check",check)

		data = frappe.db.sql(""" select %s from `tab%s` t1
					where t1.company = %s and %s between %s and %s and
					t1.docstatus = 1 %s %s
					group by %s
				""" %
				(query_details, conditions["trans"],
				 # , conditions["trans"], conditions["addl_tables"],
					"%s", posting_date, "%s", "%s", cond, conditions.get("addl_tables_relational_cond", ""), conditions["group_by"]),
				(filters.get("company"), year_start_date, year_end_date), as_list=1)

	return data

def get_mon(dt):
	return getdate(dt).strftime("%b")

def period_wise_columns_query(filters, trans):
	query_details = ''
	pwc = []
	bet_dates = get_period_date_ranges(filters.get("period"), filters.get("fiscal_year"))

	trans_date = 'date'
	if filters.get("period") != 'Yearly':
		for dt in bet_dates:
			get_period_wise_columns(dt, filters.get("period"), pwc)
			query_details = get_period_wise_query(dt, trans_date, query_details)
	else:
		pwc = [_(filters.get("fiscal_year")) + " ("+_("Qty") + "):Float:120",
			_(filters.get("fiscal_year")) + " ("+ _("Amt") + "):Currency:120"]
		query_details = " SUM(t1.volume), SUM(t1.total),"

	query_details += 'SUM(t1.volume), SUM(t1.total)'
	return pwc, query_details

def get_period_wise_columns(bet_dates, period, pwc):
	if period == 'Monthly':
		pwc += [_(get_mon(bet_dates[0])) + " (" + _("Volume") + "):Float:120",
			_(get_mon(bet_dates[0])) + " (" + _("Amt") + "):Currency:120"]
	else:
		pwc += [_(get_mon(bet_dates[0])) + "-" + _(get_mon(bet_dates[1])) + " (" + _("Volume") + "):Float:120",
			_(get_mon(bet_dates[0])) + "-" + _(get_mon(bet_dates[1])) + " (" + _("Amt") + "):Currency:120"]

def get_period_wise_query(bet_dates, trans_date, query_details):
	query_details += """SUM(IF(t1.%(trans_date)s BETWEEN '%(sd)s' AND '%(ed)s', t1.volume, NULL)),
					SUM(IF(t1.%(trans_date)s BETWEEN '%(sd)s' AND '%(ed)s', t1.total, NULL)),
				""" % {"trans_date": trans_date, "sd": bet_dates[0],"ed": bet_dates[1]}
	return query_details

@frappe.whitelist(allow_guest=True)
def get_period_date_ranges(period, fiscal_year=None, year_start_date=None):
	from dateutil.relativedelta import relativedelta

	if not year_start_date:
		year_start_date, year_end_date = frappe.db.get_value("Fiscal Year",
			fiscal_year, ["year_start_date", "year_end_date"])

	increment = {
		"Monthly": 1,
		"Quarterly": 3,
		"Half-Yearly": 6,
		"Yearly": 12
	}.get(period)

	period_date_ranges = []
	for i in range(1, 13, increment):
		period_end_date = getdate(year_start_date) + relativedelta(months=increment, days=-1)
		if period_end_date > getdate(year_end_date):
			period_end_date = year_end_date
		period_date_ranges.append([year_start_date, period_end_date])
		year_start_date = period_end_date + relativedelta(days=1)
		if period_end_date == year_end_date:
			break

	return period_date_ranges

def get_period_month_ranges(period, fiscal_year):
	from dateutil.relativedelta import relativedelta
	period_month_ranges = []

	for start_date, end_date in get_period_date_ranges(period, fiscal_year):
		months_in_this_period = []
		while start_date <= end_date:
			months_in_this_period.append(start_date.strftime("%B"))
			start_date += relativedelta(months=1)
		period_month_ranges.append(months_in_this_period)

	return period_month_ranges

def based_wise_columns_query(based_on, trans):
	based_on_details = {}

	# based_on_cols, based_on_select, based_on_group_by, addl_tables
	if based_on == "dcs":
		based_on_details["based_on_cols"] = ["DCS:Link/Warehouse:120"]
		based_on_details["based_on_select"] = "t1.dcs_id, "
		based_on_details["based_on_group_by"] = 't1.dcs_id '
		based_on_details["addl_tables"] = ''

	elif based_on == "milk_type":
		based_on_details["based_on_cols"] = ["Milk Type:Data:120"]
		based_on_details["based_on_select"] = "t1.milk_type,"
		based_on_details["based_on_group_by"] = 't1.milk_type'
		based_on_details["addl_tables"] = ''

	return based_on_details

def group_wise_column(group_by):
	print("=====group_by",group_by)
	if group_by:
		if group_by=="dcs":
			return [group_by + ":Link/Warehouse:120"]
		elif group_by=="member":
			return [group_by + ":Link/Member:120"]
		elif group_by=="shift":
			return [group_by + ":Data:80"]
	else:
		return []
















