from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Book Category'
    _parent_name = "parent_id"

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('library.category', string='Parent Category', ondelete='cascade')
    child_ids = fields.One2many('library.category', 'parent_id', string='Child Categories')