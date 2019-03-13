# -*- coding: utf-8 -*-
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import http
from odoo.http import request
from odoo.addons.website_portal.controllers.main import website_account


class PortalDebtHistory(website_account):

    @http.route(['/my/debt_history', '/my/debt_history/<int:limit>'], type='http', auth="user", website=True)
    def portal_my_debt_history(self, limit=10):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        if partner:
            debts = partner.debt_history(limit=limit)[partner.id]
            values.update({
                'history': debts['history'],
                'debts': [value for key, value in debts['debts'].iteritems()],
                'records_count': limit,
                'records_count_all': debts['records_count'],
            })

        return request.render("website_portal_debt_notebook.portal_my_debt_history", values)
