from odoo import models, fields, api

class LibraryReportWizard(models.TransientModel):
    _name = 'library.report.wizard'
    _description = 'Library Report Wizard'

    member_id = fields.Many2one('library.member', string="Select Member", required=True)

    def action_print_pdf(self):
        return self.env.ref('library_management.action_report_book_issue_card').report_action(self.member_id)

    def action_print_excel(self):

        return self.env.ref('library_management.action_report_member_xlsx').report_action(self.member_id)