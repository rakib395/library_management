from odoo import models, fields, api, _
from datetime import date

class BookReturnWizard(models.TransientModel):
    _name = 'book.return.wizard'
    _description = 'Wizard to Return Issued Books'


    member_id = fields.Many2one('library.member', string="Member", required=True)


    issue_id = fields.Many2one('library.book.issue', string="Select Issued Book", 
                                domain="[('member_id', '=', member_id), ('status', '!=', 'returned')]",
                                required=True)


    return_date = fields.Date(string="Return Date", default=fields.Date.today)


    fine_amount = fields.Float(string="Fine to Pay", readonly=True)


    @api.onchange('issue_id')
    def _onchange_issue_id(self):
        if self.issue_id:
            self.fine_amount = self.issue_id.fine_amount


    def action_process_return(self):
        self.issue_id.write({
            'actual_return_date': self.return_date,
            'status': 'returned'
        })

        return {'type': 'ir.actions.act_window_close'}