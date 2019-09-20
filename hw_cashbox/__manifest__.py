# -*- coding: utf-8 -*-
# Copyright 2019 Artem Rafailov <https://it-projects.info/team/Ommo73>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Hardware Cashbox""",
    "summary": """The module allows you to send signals to open the cashbox separately""",
    "category": "Point of Sale",
    # "live_test_url": "http://apps.it-projects.info/shop/product/pos-cashbox?version=10.0",
    "images": ['images/pos_cashbox_main.png'],
    "version": "10.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Artem Rafailov",
    "support": "pos@it-projects.info",
    "website": "https://it-projects.info/team/Ommo73",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        "hw_escpos",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
    ],
    "qweb": [
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}
