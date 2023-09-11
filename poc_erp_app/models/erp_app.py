from odoo import api, fields, models, _

class ErpApp(models.Model):
    _name = 'erp.app'
    _description = 'ERP App Integration'

    # _rec_name = 'company_id'
    _order = 'company_id ASC'

    # new fields
    company_id = fields.Many2one('res.company', 'Company')
    app_name = fields.Char(string='App Name')    
    app_url = fields.Char(string='App URL')
    method = fields.Selection(
        string='Method',
        selection=[
            ('get', 'get'),
            ('post', 'post'),
            ('put', 'put'),
            ('delete', 'delete')
        ]
    )
    api_key = fields.Char(
        string='Api Key',
    )    
    