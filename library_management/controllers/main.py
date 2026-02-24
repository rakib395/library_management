from odoo import http
from odoo.http import request

class LibraryWebsite(http.Controller):

    @http.route(['/library/books'], type='http', auth="public", website=True)
    def library_books(self, search='', **post):
        domain = [('available_copies', '>', 0)]
        if search:
            domain += ['|', ('name', 'ilike', search), ('author', 'ilike', search)]
        
        books = request.env['library.book'].sudo().search(domain)
        
        return request.render("library_management.books_catalog_template", {
            'books': books,
            'search': search,
        })

    @http.route(['/library/book/<int:book_id>'], type='http', auth="public", website=True)
    def library_book_detail(self, book_id, **post):
        book = request.env['library.book'].sudo().browse(book_id)
        if not book.exists():
            return request.not_found()
            
        return request.render("library_management.book_detail_template", {
            'book': book,
            'main_object': book,
        })

    @http.route(['/library/member/portal'], type='http', auth="user", website=True)
    def library_member_portal(self, **post):
        user = request.env.user
        
        
        member = request.env['library.member'].sudo().search([
            ('partner_id', '=', user.partner_id.id)
        ], limit=1)
        
        
        if not member:
            return request.make_response(
                "<html><body><h1>Member Record Not Found</h1><p>Please link Mitchell Admin to a Member record in the Odoo Backend.</p></body></html>",
                headers=[('Content-Type', 'text/html')]
            )
            
        issue_history = request.env['library.book.issue'].sudo().search([
            ('member_id', '=', member.id)
        ])
        
        return request.render("library_management.member_portal_template", {
            'member': member,
            'issues': issue_history,
        })