from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import re

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Char(string='Name', required=True)

    partner_id = fields.Many2one('res.partner', string='Related Partner', ondelete='cascade')

    member_number = fields.Char(string='Member ID', readonly=True, copy=False, default='New')

    email = fields.Char(string='Email')

    phone = fields.Char(string='Phone')

    address = fields.Text(string='Address')

    membership_start_date = fields.Date(string='Start Date', default=fields.Date.today)

    membership_expiry_date = fields.Date(string='Expiry Date')

    status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired')
    ], string='Status', compute='_compute_status', store=True, default='active')

    issue_count = fields.Integer(compute='_compute_issue_count')


    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, record.email):
                    raise ValidationError(_("Invalid Email Format! Please enter a valid email (e.g., rakib@gmail.com)."))


    @api.constrains('phone')
    def _check_phone_number(self):
        for record in self:
            if record.phone:
                if not record.phone.isdigit():
                    raise ValidationError(_("Phone number must contain only digits!"))
                
                if len(record.phone) != 11:
                    raise ValidationError(_("Phone number must be exactly 11 digits long!"))


    @api.depends('membership_expiry_date')
    def _compute_status(self):
        today = fields.Date.today()
        for record in self:
            if record.membership_expiry_date and record.membership_expiry_date < today:
                record.status = 'expired'
            else:
                record.status = 'active'


    def _compute_issue_count(self):
        for record in self:
            record.issue_count = self.env['library.book.issue'].search_count([
                ('member_id', '=', record.id)
            ])


    def action_renew_membership(self):
        for record in self:
            if record.membership_expiry_date:
                record.membership_expiry_date += timedelta(days=180)
            else:
                record.membership_expiry_date = fields.Date.today() + timedelta(days=180)


    def action_view_issued_books(self):
        return {
            'name': 'Issued Books',
            'type': 'ir.actions.act_window',
            'res_model': 'library.book.issue',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }


    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email must be unique!')
    ]


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('member_number', 'New') == 'New':
                vals['member_number'] = self.env['ir.sequence'].next_by_code('library.member.sequence') or 'New'
        return super().create(vals_list)