from odoo import models

class MemberXlsx(models.AbstractModel):
    _name = 'report.library_management.report_member_xlsx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, members):

        sheet = workbook.add_worksheet('Library Report')


        title_format = workbook.add_format({
            'bold': True, 
            'align': 'center', 
            'valign': 'vcenter', 
            'font_size': 16
        })

        header_format = workbook.add_format({
            'bold': True, 
            'align': 'center', 
            'valign': 'vcenter', 
            'bg_color': '#D3D3D3', 
            'border': 1
        })

        sub_header_format = workbook.add_format({
            'bold': True, 
            'align': 'center', 
            'valign': 'vcenter', 
            'bg_color': '#E9E9E9', 
            'border': 1
        })

        data_format = workbook.add_format({
            'align': 'center', 
            'valign': 'vcenter', 
            'border': 1
        })

        left_data_format = workbook.add_format({
            'align': 'left', 
            'valign': 'vcenter', 
            'border': 1
        })


        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:F', 18)
        sheet.set_column('G:G', 12)
        sheet.set_column('H:H', 35)


        sheet.merge_range('A2:H2', 'Mindsynth Technologies', title_format)


        sheet.merge_range('A4:A5', 'SL.', header_format)

        sheet.merge_range('B4:B5', 'Book Name', header_format)

        sheet.merge_range('C4:C5', 'Member Name', header_format)

        sheet.merge_range('D4:F4', 'Issue Schedule', header_format)
        sheet.write('D5', 'Issue Date', sub_header_format)
        sheet.write('E5', 'Expected Return', sub_header_format)
        sheet.write('F5', 'Duration (Days)', sub_header_format)

        sheet.merge_range('G4:G5', 'Status', header_format)

        sheet.merge_range('H4:H5', 'Fine', header_format)


        row = 5
        sl_no = 1


        for member in members:

            issues = self.env['library.book.issue'].search([('member_id', '=', member.id)])
            
            if not issues:
                sheet.write(row, 0, sl_no, data_format)
                sheet.write(row, 1, 'No Issue Found', left_data_format)
                sheet.write(row, 2, member.name, left_data_format)
                sheet.write(row, 3, '-', data_format)
                sheet.write(row, 4, '-', data_format)
                sheet.write(row, 5, '-', data_format)
                sheet.write(row, 6, member.status or 'N/A', data_format)
                sheet.write(row, 7, '-', left_data_format)
                
                row += 1
                sl_no += 1

            else:
                for line in issues:
                    sheet.write(row, 0, sl_no, data_format)
                    
                    sheet.write(row, 1, line.book_id.name if line.book_id else '', left_data_format)
                    
                    sheet.write(row, 2, member.name, left_data_format)
                    
                    issue_dt = line.issue_date.strftime('%d-%b-%Y') if line.issue_date else ''
                    expect_dt = line.expected_return_date.strftime('%d-%b-%Y') if line.expected_return_date else ''
                    
                    sheet.write(row, 3, issue_dt, data_format)
                    sheet.write(row, 4, expect_dt, data_format)
                    sheet.write(row, 5, line.days_overdue or 0, data_format)
                    
                    sheet.write(row, 6, line.status or '', data_format)
                    
                    sheet.write(row, 7, f"Fine Amount: {line.fine_amount}", left_data_format)
                    
                    row += 1
                    sl_no += 1