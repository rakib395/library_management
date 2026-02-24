from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    isbn = fields.Char(string='ISBN', required=True)
    author = fields.Char(string='Author', required=True)
    publisher = fields.Char(string='Publisher')
    publication_date = fields.Date(string='Publication Date')
    total_copies = fields.Integer(string='Total Copies', default=1)
    available_copies = fields.Integer(string='Available Copies', default=1)
    image = fields.Binary(string='Cover Image')
    description_text = fields.Text(string='Description')
    
    status = fields.Selection([
        ('active', 'Active'),
        ('archived', 'Archived')
    ], string='Status', default='active', copy=False)
    
    category_id = fields.Many2one('library.category', string='Category')

    _sql_constraints = [
        ('unique_isbn', 'unique(isbn)', 'The ISBN must be unique!'),
    ]

   
    @api.depends('name', 'isbn', 'author')
    def _compute_display_name(self):
        for record in self:
            if record.isbn and record.author:
                record.display_name = f"[{record.isbn}] {record.name} - {record.author}"
            else:
                record.display_name = record.name


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('name', operator, name), ('author', operator, name), ('isbn', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
    


    def write(self, vals):
        if 'total_copies' in vals and vals['total_copies'] < 0:
            raise ValidationError(_("Total copies cannot be negative!"))
        return super(LibraryBook, self).write(vals)
    


    def unlink(self):
        for record in self:
            active_issues = self.env['library.book.issue'].search([
                ('book_id', '=', record.id),
                ('status', '=', 'issued')
            ])
            if active_issues:
                raise ValidationError(_("You cannot delete a book that is currently issued to a member."))
        return super(LibraryBook, self).unlink()
    


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': _("%s (Copy)") % (self.name),
            'isbn': f"{self.isbn}_copy",
        })
        return super(LibraryBook, self).copy(default)