from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # new field
    ref_doc_no = fields.Char(string='ERP Doc No.', store=True)
    integration_msg = fields.Char(string='Integration Message', store=True)

    # RFQ Confirm button to order
    def button_confirm(self):  
        # try:
        # self._set_msg('Cannot connect to ERP')
    
        config = self.env["erp.app"].search(
            [
                ('company_id', '=', self.company_id.id),
                ('app_name', '=', 'Purchase Order'),
                ('method', '=', 'post')
            ],
            limit=1
        )

        if config:
            headers = {
                "Content-Type": "application/jsonp",
                "access-token": config.api_key 
            }

            configPartner = self.env["erp.app"].search(
                [
                    ('company_id', '=', self.company_id.id),
                    ('app_name', '=', 'Partner'),
                    ('method', '=', 'get')
                ],
                limit=1
            )
            urlPartner = "{0}?limit=1&fields=id,name&domain=name:=:{1}".format(configPartner.app_url, self.partner_id.name)

            resPartner = requests.request("GET", urlPartner, data={},  headers=headers)

            if resPartner.status_code != 200:
                raise ValidationError(_("Cannot connect to ERP"))

            resPartnerJson = resPartner.json()
            if resPartnerJson['count'] == 0:
                self.update({'integration_msg': "Vendor not found in ERP"})
                raise ValidationError(_("Vendor '{0}' not found in ERP".format(self.partner_id.name)))

            # Branch
            configBranch = self.env["erp.app"].search(
                [
                    ('company_id', '=', self.company_id.id),
                    ('app_name', '=', 'Branch'),
                    ('method', '=', 'get')
                ],
                limit=1
            )
            urlBranch = "{0}?limit=1&fields=id&domain=code:=:{1}".format(configBranch.app_url, self.branch_id.code)

            resBranch = requests.request("GET", urlBranch, data={},  headers=headers)
            if resBranch.status_code != 200:
                self.update({'integration_msg': "Cannot connect to ERP 'branch'"})
                raise ValidationError(_("Cannot connect to ERP"))

            resBranchJson = resBranch.json()
            if resBranchJson['count'] == 0:
                self.update({'integration_msg': "Branch not found in ERP"})
                raise ValidationError(_("Branch '{0}' not found in ERP".format(self.branch_id.name)))
            
            # ==== PO ======
            # Cek Item

            # Order 
            reqUrl = config.app_url

            payload = json.dumps({
                "partner_id": resPartnerJson['data'][0]['id'],
                "branch_id": resBranchJson['data'][0]['id'],
                "state": "purchase",
                "date_order": str(self.date_order),
                "date_planned": str(self.date_planned),
                "date_approve": str(self.date_order)
            })
            _logger.error(payload)
            response = requests.request("POST", reqUrl, data=payload,  headers=headers)
            _logger.error(response)
            if response.status_code > 300:
                self.update({'integration_msg': "Cannot connect to ERP 'order'"})
                raise UserError(_("Cannot connect to ERP"))
            
            resOrder = response.json()
            if response.status_code == 401:
                self.update({'integration_msg': resOrder['message']})
                raise ValidationError(_(resOrder['message']))
            
            if resOrder['count'] == 0:
                self.update({'integration_msg': "Try again to confirm order"})
                raise ValidationError(_("Try again to confirm order"))
            
            # Order line
            statusLine = 0
            orderId = resOrder['data'][0]['id']
            for row in self.order_line:
                payloadLine = json.dumps({
                    "product_id": row.product_id.id,
                    "name": row.name,
                    "product_qty": row.product_qty,
                    "product_uom_qty": row.product_uom_qty,
                    "order_id": orderId,
                    "price_unit": row.price_unit
                    # "branch_id": row.branch_id.id
                })
                urlLine = reqUrl + ".line"
                _logger.error(payloadLine)
                responseLine = requests.request("POST", urlLine, data=payloadLine,  headers=headers)
                _logger.error(responseLine.json())
                if responseLine.status_code != 200:
                    return
                statusLine = 1
        
            # _logger.log(msg="Done")
            if statusLine == 1:
                self.update({
                    'integration_msg': 'OK',
                    'ref_doc_no': resOrder['data'][0]['name']
                })
                super(PurchaseOrder, self).button_confirm()
        else:
            raise UserError(_("Please config API Integration"))
        # except Exception as error:
        #     _logger.error(error)

    def _set_msg(self, msg):
        # self.ensure_one()
        self.update({'integration_msg': msg})
        return
    
