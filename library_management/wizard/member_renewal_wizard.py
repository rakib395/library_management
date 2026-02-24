from odoo import models, fields, api

class MemberRenewalWizard(models.TransientModel):
    _name = 'member.renewal.wizard'
    _description = 'Wizard to Renew Member Subscriptions'


    member_ids = fields.Many2many('library.member', string="Select Members", required=True)


    new_expiry_date = fields.Date(string="New Expiry Date", required=True, default=fields.Date.today)


    def action_renew_membership(self):

        for member in self.member_ids:
            member.write({
                'membership_expiry_date': self.new_expiry_date,
                'status': 'active'
            })


        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Membership renewed successfully for selected members!',
                'sticky': False,
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }