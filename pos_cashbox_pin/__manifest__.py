# Copyright 2019 Artem Rafailov <https://it-projects.info/team/Ommo73>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Pin Request for Open CashBox from POS""",
    "summary": """The module allows to open Cashbox/Cashdrawer from POS through input pin""",
    "category": "Point of Sale",
    # "live_test_url": "http://apps.it-projects.info/shop/product/pos-cashbox?version=10.0",
    "images": ['images/pos_cashbox_main.png'],
    "version": "11.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Artem Rafailov",
    "support": "pos@it-projects.info",
    "website": "https://it-projects.info/team/Ommo73",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        "point_of_sale",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/pos_cashbox_pins_template.xml",
    ],
    "qweb": [
        "views/pos_cashbox_pins_view.xml",
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,

    "demo_title": "Pin Request for Open CashBox from POS",
    "demo_addons": [
    ],
    "demo_addons_hidden": [
    ],
    "demo_url": "pos-cashbox",
    "demo_summary": "The module allows to open the CashBox from POS",
    "demo_images": [
        "images/pos_cashbox_main.png",
    ]
}
