from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
        {
        "label":_("Milk Entry"),
        "items": [
            {
              "type": "doctype",
              "name": "Milk Entry",
              "label": _("Milk Entry"),
              "description": _("Milk Entry."),
              "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "Milk Rate",
                "label": _("Milk Rate"),
                "description": _("Milk Rate"),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "Raw Milk Sample",
                "label": _("Raw Milk Sample"),
                "description": _("Raw Milk Sample"),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "Route Master",
                "label": _("Route Master"),
                "description": _("Route Master"),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "Van Collection",
                "label": _("Van Collection"),
                "description": _("Van Collection"),
                "onboard": 1,
            },
            
          ]
      },

      {
        "label":_("Field Order"),
        "items": [
            {
                "type": "doctype",
              	"name": "Field Order",
                "label": _("Field Order"),
                "description": _("Field Order."),
                "onboard": 1,
            },
            
	        ]
      },

      {
        "label":_("Order Book"),
        "items": [
           	{
             	  "type": "doctype",
              	"name": "Order Book",
                "label": _("Order Book"),
                "description": _("Order Book."),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "Sales Order",
                "label": _("Sales Order"),
                "description": _("Sales Order."),
                "onboard": 1,
            },
            {
                "type": "doctype",
                "name": "Quotation",
                "label": _("Quotation"),
                "description": _("Quotation"),
                "onboard": 1,
            },
          ]
      },


            {
                  "label": _("Settings"),
                  "items": [
                      {
                    	"type": "doctype",
                    	"name": "Dairy Settings",
                    	"label": _("Dairy Settings"),
                    	"description": _("Dairy Settings"),
                    	"onboard": 1,
                      },
                      {
                   	"type": "doctype",
                    	"name": "Member Master",
                    	"label": _("Member Master"),
                   	"description": _("Member Master"),
                    	"onboard": 1,
                      },
                      {
                    	"type": "doctype",
                    	"name": "Society Master",
                    	"label": _("Society Master"),
                    	"description": _("Society Master"),
                    	"onboard": 1,
                      },
                      {
                    	"type": "doctype",
                    	"name": "Member Category",
                    	"label": _("Member Category"),
                    	"description": _("Member Category"),
                    	"onboard": 1,
                      },

                  ]
          },

    ]
