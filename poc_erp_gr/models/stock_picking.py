from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests
import json

import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # new fields
    # inherit method
    def button_validate(self):
        _logger.error('========= validate ===============')
        _logger.error(self.id)
        _logger.error(self.note)
        if self.note == '<p>From Koprol</p>':
            res = super(StockPicking, self).button_validate()
            return res

        # http to koprol
        pickingId, pickingName = self._get_picking()
        if pickingId == 0:
            res = super(StockPicking, self).button_validate()
            return res

        config = self.env["erp.app"].search(
            [
                ('company_id', '=', self.company_id.id),
                ('app_name', '=', 'Picking Line'),
                ('method', '=', 'put')
            ],
            limit=1
        )

        headers = {
            "Content-Type": "application/jsonp",
            "access-token": config.api_key 
        }

        pickingLines = self._get_move_line(pickingName, config.app_url, headers)

        # loop move line
        _logger.error(pickingLines)
        for row in pickingLines:
            _logger.error(row['id'])
            data = json.dumps({
                'qty_done': row['product_qty']
            })

            self._set_move_line(row['id'], data, config.app_url, headers)

        self._set_validate(pickingId)
        # super
        res = super(StockPicking, self).button_validate()
        return res

    def _get_picking(self):
        _logger.error('----------------- get picking --------------')
        config = self.env["erp.app"].search(
            [
                ('company_id', '=', self.company_id.id),
                ('app_name', '=', 'Picking'),
                ('method', '=', 'get')
            ],
            limit=1
        )

        headers = {
            "Content-Type": "application/jsonp",
            "access-token": config.api_key 
        }
    
        url = "{0}?limit=1&fields=id,name&domain=ref_doc_no:=:{1}".format(config.app_url, self.name)
        _logger.error(url)

        res = requests.request("GET", url, data={},  headers=headers)
        _logger.error(res)
        resJson = res.json()
        _logger.error(resJson)
        if resJson['count'] < 1:
            return [0, '']

        return [resJson['data'][0]['id'], resJson['data'][0]['name']]

    def _get_move_line(self, pickingName, app_url, headers):
        _logger.error('----------------- get move line --------------')
    
        url = "{0}?fields=id,product_id,product_qty,qty_done,picking_id&domain=picking_id:=:{1}".format(app_url, pickingName)
        _logger.error(url)

        res = requests.request("GET", url, data={},  headers=headers)
        resJson = res.json()
        _logger.error(resJson)

        return resJson['data']
    
    def _set_move_line(self, lineId, data, app_url, headers):
        _logger.error('----------------- set move line --------------')
            
        url = "{0}/{1}".format(app_url, lineId)
        _logger.error(url)

        res = requests.request("PUT", url, data=data,  headers=headers)
        resJson = res.json()
        _logger.error(resJson)

        return resJson
    
    def _set_validate(self, pickingId):
        _logger.error('----------------- set validate --------------')
        if pickingId == 0:
            return
        
        config = self.env["erp.app"].search(
            [
                ('company_id', '=', self.company_id.id),
                ('app_name', '=', 'Picking'),
                ('method', '=', 'get')
            ],
            limit=1
        )

        headers = {
            "Content-Type": "application/jsonp",
            "access-token": config.api_key 
        }
            
        url = "{0}/{1}/button_validate".format(config.app_url, pickingId)
        _logger.error(url)

        data = json.dumps({
            "note": "From ERP"
        })

        res = requests.request("PATCH", url, data=data,  headers=headers)
        resJson = res.json()
        _logger.error(resJson)
        if res.status_code > 500:
                raise ValidationError(_(resJson['message']))

        return resJson
