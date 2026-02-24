from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BookIssueWizard(models.TransientModel):
    _name = 'book.issue.wizard'
    _description = 'Wizard to Issue Multiple Books'


    member_id = fields.Many2one('library.member', string="Member", required=True)

    issue_date = fields.Date(string="Issue Date", default=fields.Date.today)

    expected_return_date = fields.Date(string="Expected Return Date", required=True)
    
    book_ids = fields.Many2many('library.book', string="Books to Issue", 
                                domain=[('available_copies', '>', 0)])


    def action_issue_books(self):

        if not self.book_ids:
            raise ValidationError(_("Please select at least one book!"))


        for book in self.book_ids:

            self.env['library.book.issue'].create({
                'member_id': self.member_id.id,
                'book_id': book.id,
                'issue_date': self.issue_date,
                'expected_return_date': self.expected_return_date,
                'status': 'issued'
            })
        
        return {'type': 'ir.actions.act_window_close'}