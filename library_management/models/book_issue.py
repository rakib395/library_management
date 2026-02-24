from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class LibraryBookIssue(models.Model):
    _name = 'library.book.issue'
    _description = 'Book Issue Record'

    member_id = fields.Many2one('library.member', string='Member', required=True)
    book_id = fields.Many2one('library.book', string='Book', required=True, domain="[('available_copies', '>', 0)]")
    issue_date = fields.Date(string='Issue Date', default=fields.Date.today)
    expected_return_date = fields.Date(string='Expected Return Date')
    actual_return_date = fields.Date(string='Actual Return Date')
    days_overdue = fields.Integer(string='Days Overdue', compute='_compute_fines', store=True)
    fine_amount = fields.Float(string='Fine Amount', compute='_compute_fines', store=True)
    status = fields.Selection([
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    ], string='Status', default='issued')



    def action_return_book(self):
        for record in self:
            record.actual_return_date = date.today()
            record.status = 'returned'



    @api.depends('expected_return_date', 'actual_return_date', 'status')
    def _compute_fines(self):
        for record in self:
            overdue_days = 0
            check_date = record.actual_return_date or date.today()
            if record.expected_return_date and check_date > record.expected_return_date:
                delta = check_date - record.expected_return_date
                overdue_days = delta.days
            record.days_overdue = overdue_days
            record.fine_amount = overdue_days * 10.0



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            book = self.env['library.book'].browse(vals.get('book_id'))
            if book.available_copies < 1:
                raise ValidationError(_("Sorry! '%s' is currently out of stock.") % book.name)
            book.available_copies -= 1
        return super().create(vals_list)
    


    def write(self, vals):
        if 'status' in vals and vals['status'] == 'returned':
            for record in self:
                if record.status != 'returned':
                    record.book_id.available_copies += 1
        return super().write(vals)
    


    def get_overdue_count(self):
        return self.search_count([
            ('status', '=', 'issued'),
            ('expected_return_date', '<', fields.Date.today())
        ])
    


    def _cron_check_overdue(self):
        overdue_records = self.search([
            ('status', '=', 'issued'),
            ('expected_return_date', '<', fields.Date.today())
        ])
        for record in overdue_records:
            record.status = 'overdue'



    @api.depends('book_id', 'member_id')
    def _compute_display_name(self):
        for record in self:
            if record.book_id and record.member_id:
                record.display_name = f"{record.book_id.name} - {record.member_id.name}"
            else:
                record.display_name = "Book Issue"