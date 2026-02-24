# -*- coding: utf-8 -*-
# Part of Mehedi Hasan Rakib. See LICENSE file for full copyright and licensing details.
{

    'name': 'Library Management System',
    'version': '1.0',
    'summary': 'A simple tool to manage books, members, and library records.',
    'sequence': 2,
    'description':"""
        This module helps you to:
        1. Keep a list of all library books.
        2. Save information about library members.
        3. Track which book is issued to which member.
        4. Calculate late fees (fines) automatically.
    """,
    'category':'Library',
    'author':'MindSynth',
    'website': 'https://xyz.com',
    'license': 'LGPL-3',
    
    'depends':['base', 'mail', 'web', 'report_xlsx', 'website'],

   'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/cron_data.xml',
        'data/demo_data.xml', 
        'views/menu.xml',
        'views/book_views.xml',
        'views/member_views.xml',
        'views/book_issue_views.xml',
        'views/category_views.xml',
        'wizard/book_issue_wizard_view.xml',   
        'wizard/book_return_wizard_view.xml', 
        'wizard/member_renewal_wizard_view.xml',
        'wizard/report_wizard_view.xml', 
        'report/library_reports.xml',
        'report/book_issue_report.xml',
        'views/templates.xml',
        'views/menu.xml',                      
    ],


    'assets': {
        'web.assets_frontend': [
            'library_management/static/src/css/style.css',
            'library_management/static/src/js/autocomplete.js',
        ],
    },



    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}