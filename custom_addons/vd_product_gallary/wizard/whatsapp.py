from odoo import models, fields
from urllib.parse import quote

class WhatsAppWizard(models.TransientModel):
    _name = 'whatsapp.wizard'
    _description = 'WhatsApp Wizard'

    phone_number = fields.Char('Phone Number', required=True)
    message = fields.Text('Message', required=True)

    def action_send_whatsapp(self):
        for wizard in self:
            encoded_message = quote(wizard.message)
            url = f'https://wa.me/{wizard.phone_number}?text={encoded_message}'
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }

