# -*- coding: utf-8 -*-
import openerp
from openerp import models, fields, api
from datetime import datetime, date, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class FleetRentalDocumentRent(models.Model):
    _name = 'fleet_rental.document_rent'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('booked', 'Booked'),
        ('confirmed', 'Confirmed'),
        ('extended', 'Extended'),
        ('returned', 'Returned'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, default='draft')

    _inherits = {
                 'fleet_rental.document': 'document_id',
                 }

    document_id = fields.Many2one('fleet_rental.document', required=True,
            string='Related Document', ondelete='restrict',
            help='common part of all three types of the documents', auto_join=True)

    user_branch_id = fields.Many2one('fleet_branch.branch', default=lambda self: self.env.user.branch_id.id)

    document_return_id = fields.Many2one('fleet_rental.document_return')

    @api.onchange('vehicle_id')
    def on_change_vehicle_id(self):
        self.mapped('document_id')._compute_png()
        self.allowed_kilometer_per_day = self.vehicle_id.allowed_kilometer_per_day
        self.rate_per_extra_km = self.vehicle_id.rate_per_extra_km
        self.daily_rental_price = self.vehicle_id.daily_rental_price
        self.period_rent_price = self.total_rental_period * self.daily_rental_price

    @api.onchange('exit_datetime', 'return_datetime')
    def _onchange_dates(self):
        if self.exit_datetime and self.return_datetime:
            start = datetime.strptime(self.exit_datetime, DTF)
            end = datetime.strptime(self.return_datetime, DTF)
            self.total_rental_period = (end - start).days
            self.period_rent_price = self.total_rental_period * self.daily_rental_price

    @api.onchange('period_rent_price', 'extra_driver_charge', 'other_extra_charges')
    def _onchange_charges(self):
        self.total_rent_price = self.period_rent_price + self.extra_driver_charge + self.other_extra_charges

    @api.multi
    def action_view_invoice(self):
        return self.mapped('document_id').action_view_invoice()

    @api.multi
    def action_book(self):
        for rent in self:
            rent.state = 'booked'
            self.vehicle_id.state_id = self.env.ref('fleet.vehicle_state_booked')

    @api.multi
    def action_cancel_booking(self):
        for rent in self:
            rent.state = 'cancel'
            self.vehicle_id.state_id = self.env.ref('fleet.vehicle_state_active')

    @api.multi
    def action_confirm(self):
        for rent in self:
            rent.state = 'confirmed'

    @api.multi
    def action_create_return(self):
        document_return_obj = self.env['fleet_rental.document_return']
        for rent in self:
            rent.state = 'returned'
            self.vehicle_id.state_id = self.env.ref('fleet.vehicle_state_active')
            document_return = document_return_obj.create({
               'partner_id': rent.partner_id.id,
               'vehicle_id': rent.vehicle_id.id,
               'allowed_kilometer_per_day': rent.allowed_kilometer_per_day,
               'rate_per_extra_km': rent.rate_per_extra_km,
               'daily_rental_price': rent.daily_rental_price,
               'origin': rent.name,
               'exit_datetime': rent.exit_datetime,
               'type': 'return',
               'return_datetime': fields.Datetime.now(),
               'odometer_before': rent.odometer_before,
               })
            rent.write({'document_return_id': document_return.id})
            for r in rent.check_line_ids:
                for w in document_return.check_line_ids:
                    if r.item_id == w.item_id:
                        w.exit_check_yes = r.exit_check_yes
                        w.exit_check_no = r.exit_check_no
                        break

        return self.action_view_document_return(document_return.id)

    @api.multi
    def action_create_extend(self):
        document_rent_obj = self.env['fleet_rental.document_extend']
        for rent in self:
            self.vehicle_id.state_id = self.env.ref('fleet.vehicle_state_active')
            document_extend = document_rent_obj.create({
               'partner_id': rent.partner_id.id,
               'vehicle_id': rent.vehicle_id.id,
               'allowed_kilometer_per_day': rent.allowed_kilometer_per_day,
               'rate_per_extra_km': rent.rate_per_extra_km,
               'daily_rental_price': rent.daily_rental_price,
               'document_rent_id': rent.id,
               'origin': rent.name,
               'exit_datetime': rent.return_datetime,
               'type': 'extended_rent',
               'odometer_before': rent.odometer_before,
               })
            for r in rent.check_line_ids:
                for w in document_extend.check_line_ids:
                    if r.item_id == w.item_id:
                        w.exit_check_yes = r.exit_check_yes
                        w.exit_check_no = r.exit_check_no
                        break

        return self.action_view_document_extend(document_extend.id)

    @api.multi
    def action_view_document_return(self, document_return_id):
        action = self.env.ref('fleet_rental_document.fleet_rental_return_document_draft_act')
        form_view_id = self.env.ref('fleet_rental_document.fleet_rental_return_document_form').id

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        result['res_id'] = document_return_id
        return result

    @api.multi
    def action_view_document_extend(self, document_return_id):
        action = self.env.ref('fleet_rental_document.fleet_rental_document_extend_act')
        form_view_id = self.env.ref('fleet_rental_document.fleet_rental_document_extend_form').id

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [(form_view_id, 'form')],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        result['res_id'] = document_return_id
        return result

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet_rental.document_rent') or 'New'
        result = super(FleetRentalDocumentRent, self).create(vals)
        return result


class FleetRentalDocumentExtend(models.Model):
    _name = 'fleet_rental.document_extend'
    _inherit = 'fleet_rental.document_rent'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('booked', 'Booked'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, default='draft')

    @api.multi
    def action_submit(self):
        for rent in self:
            rent.state = 'booked'
            self.vehicle_id.state_id = self.env.ref('fleet.vehicle_state_booked')

    @api.multi
    def action_view_invoice(self):
        return self.mapped('document_id').action_view_invoice()
