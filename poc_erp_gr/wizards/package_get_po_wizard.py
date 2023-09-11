# -*- coding: utf-8 -*-

import json
from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)



class PackageGetPoWizard(models.TransientModel):
    _name = 'package.get.po.wizard'
    _description = 'Package Get PO Wizard'
    
    # erp_po_no = fields.Char(erp_string='PO No.')
    # erp_gr_no = fields.Char(string='GR No.')
    json_popover = fields.Char('JSON data a', compute='_compute_json_popover')
    json_popover_b = fields.Char('JSON data b', compute='_compute_json_popover')

    def _compute_json_popover(self):
        _logger.error('----------------- g -----------------')
        _logger.error(self)
        _logger.error('----------------- g -----------------')
        row = [
            {
                'a': 1,
                'b': 10
            },
            {
                'a': 2,
                'b': 20
            }
        ]
        for r in row:
            self.json_popover_b = r['a']
            self.json_popover = r['b']
            # self.json_popover = json.dumps(row)
    
