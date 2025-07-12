
from odoo import models, fields,api,_
from odoo.exceptions import ValidationError,UserError
import base64
import mimetypes
import os
import re
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_equipment = fields.Boolean(string='Equipment')


    pro_type = fields.Selection([
        ('machine', 'Machine'),
        ('tool', 'Tool'),
    ], string="Type", default='machine')

    brochure_file = fields.Binary('Brochure File', attachment=True)
    brochure_filename = fields.Char('Brochure Filename')
    brochure_description = fields.Text('Brochure Description')
    
    image_1 = fields.Image("Image 1")
    image_2 = fields.Image("Image 2")
    image_3 = fields.Image("Image 3")
    image_4 = fields.Image("Image 4")
   
    # custom_categ_id = fields.Many2one('custom.product.category', string="Category")
    partner_history_ids = fields.One2many(
        'product.detail.history',
        'product_template_id',
        string='Customer History'
    )

    def restrict_user(self):
        raise ValidationError("You are not allowed to Create/Update Products")

    # @api.model
    # def create(self, values):
    #     ctx = self._context
    #     restrict = ctx.get('user_restrict')
    #     if restrict:
    #         res = super(ProductTemplate, self).create(values)
    #         if not self.env.user.has_group('vd_product_gallary.can_modify_products'):
    #             self.restrict_user()
    #         return res
    #     else:
    #         return super(ProductTemplate, self).create(values)

    # def write(self, values):
    #     ctx = self._context
    #     restrict = ctx.get('user_restrict')
    #     if restrict:
    #         res = super(ProductTemplate, self).write(values)
    #         if not self.env.user.has_group('vd_product_gallary.can_modify_products'):
    #             self.restrict_user()
    #         return res
    #     else:
    #         return super(ProductTemplate, self).write(values)

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)

        # Handle YouTube URL
        if vals.get('youtube_url'):
            self.env['video.gallary'].create({
                'name': product.name,
                'youtube_url': product.youtube_url,
                'product_id': product.id,
            })
        return product

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        for record in self:
            # Brochure handling
            if vals.get('brochure_file') and vals.get('brochure_filename'):
                attachment = self.env['ir.attachment'].create({
                    'name': vals.get('brochure_filename'),
                    'type': 'binary',
                    'datas': vals.get('brochure_file'),
                    'res_model': self._name,
                    'res_id': record.id,
                    'mimetype': 'application/pdf',
                })
                record.message_post(
                    body=_("Brochure uploaded: %s") % attachment.name,
                    attachment_ids=[attachment.id]
                )
            if vals.get('youtube_url'):
                gallery = self.env['video.gallary'].search([('product_id', '=', record.id)], limit=1)
                if gallery:
                    gallery.write({
                        'youtube_url': vals['youtube_url'],
                        'name': record.name,
                    })
                else:
                    self.env['video.gallary'].create({
                        'name': record.name,
                        'youtube_url': vals['youtube_url'],
                        'product_id': record.id,
                    })
        return res

    # @api.model
    # def create(self, vals):
    #     # Check if user has manager access
    #     if not self.env.user.has_group('vd_product_gallary.group_product_gallery_manager'):
    #         print('---------crate------------------')
    #         raise UserError("Only a Manager is allowed to Create Products.")

    #     product = super(ProductTemplate, self).create(vals)

    #     # Handle YouTube URL
    #     if vals.get('youtube_url'):
    #         self.env['video.gallary'].create({
    #             'name': product.name,
    #             'youtube_url': product.youtube_url,
    #             'product_id': product.id,
    #         })

    #     return product

    # def write(self, vals):
    #     # Check if user has manager access
    #     if not self.env.user.has_group('vd_product_gallary.group_product_gallery_manager'):
    #         print('---------write------------------')
    #         raise UserError("Only a Manager is allowed to Update Products.")

    #     res = super(ProductTemplate, self).write(vals)

    #     for record in self:
    #         # Brochure file handling
    #         if vals.get('brochure_file') and vals.get('brochure_filename'):
    #             attachment = self.env['ir.attachment'].create({
    #                 'name': vals.get('brochure_filename'),
    #                 'type': 'binary',
    #                 'datas': vals.get('brochure_file'),
    #                 'res_model': self._name,
    #                 'res_id': record.id,
    #                 'mimetype': 'application/pdf',
    #             })
    #             record.message_post(
    #                 body=_("Brochure uploaded: %s") % attachment.name,
    #                 attachment_ids=[attachment.id]
    #             )

    #         # YouTube URL handling
    #         if vals.get('youtube_url'):
    #             gallery = self.env['video.gallary'].search([('product_id', '=', record.id)], limit=1)
    #             if gallery:
    #                 gallery.write({
    #                     'youtube_url': vals['youtube_url'],
    #                     'name': record.name,
    #                 })
    #             else:
    #                 self.env['video.gallary'].create({
    #                     'name': record.name,
    #                     'youtube_url': vals['youtube_url'],
    #                     'product_id': record.id,
    #                 })

    #     return res

    # def unlink(self):
    #     if self.env.user.has_group('vd_product_gallary.group_product_gallery_user'):
    #         raise UserError("Only a Manager can create product gallery records.")
    #     return super(ProductTemplate, self).unlink()



    def action_open_whatsapp_wizard(self):
        print("=======================a")
        self.ensure_one()
        currency_symbol = self.currency_id.symbol
        # message = f"*Product Details*\n" \
        #         f"Name: {self.name}\n" \
        #         f"Price: ₹{self.list_price}\n" \
        #         f"Category: {self.categ_id.name}\n" \
        #         f"Product Type: {self.pro_type}"
        
        message = f"*Product Details*\n\n" \
              f"Name: {self.name}\n" \
              f"Price: ₹{self.list_price}\n\n" \
              f"YouTube Link: {self.youtube_url if self.youtube_url else 'N/A'}\n"

        view_id = self.env.ref('vd_product_gallary.view_whatsapp_wizard_form').id  # ✅ Replace your_module_name
        print("view_id=============",view_id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Send WhatsApp',
            'res_model': 'whatsapp.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_message': message,
            }
        }


    # def write(self, vals):
    #     res = super(ProductTemplate, self).write(vals)

    #     for record in self:
    #         if vals.get('brochure_file') and vals.get('brochure_filename'):
    #             # Attach brochure to chatter
    #             attachment = self.env['ir.attachment'].create({
    #                 'name': vals.get('brochure_filename'),
    #                 'type': 'binary',
    #                 'datas': vals.get('brochure_file'),
    #                 'res_model': self._name,
    #                 'res_id': record.id,
    #                 'mimetype': 'application/pdf',
    #             })
    #             record.message_post(
    #                 body=_("Brochure uploaded: %s") % attachment.name,
    #                 attachment_ids=[attachment.id]
    #             )
    #     return res

  
    
    def action_view_videos(self):
        """Action to view videos in kanban/form"""
        self.ensure_one()
        return {
            'name': 'Product Videos',
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment',
            'view_mode': 'kanban,list,form',
            'domain': [
                ('res_model', '=', 'product.template'),
                ('res_id', '=', self.id),
                ('mimetype', 'ilike', 'video/')
            ],
            'context': {
                'default_res_model': 'product.template',
                'default_res_id': self.id,
            }
        }

    youtube_url = fields.Char("YouTube Video URL")
    video_preview = fields.Html("Video Preview", compute="_compute_video_preview", sanitize=False)

    @api.depends('youtube_url')
    def _compute_video_preview(self):
        for rec in self:
            video_id = ""
            if rec.youtube_url:
                match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_\-]{11})", rec.youtube_url)
                if match:
                    video_id = match.group(1)
            if video_id:
                rec.video_preview = f'''
                    <iframe width="280" height="160"
                            src="https://www.youtube.com/embed/{video_id}"
                            frameborder="0" allowfullscreen></iframe>
                '''
            else:
                rec.video_preview = "<p style='color:red;'>No valid YouTube link.</p>"

    # @api.model
    # def create(self, vals):
    #     product = super().create(vals)
    #     if vals.get('youtube_url'):
    #         self.env['video.gallary'].create({
    #             'name': product.name,
    #             'youtube_url': product.youtube_url,
    #             'product_id': product.id,
    #         })
    #     return product

    # def write(self, vals):
    #     # Call the superclass write method
    #     res = super(ProductTemplate, self).write(vals)

    #     for record in self:
    #         # Handle brochure attachment
    #         if vals.get('brochure_file') and vals.get('brochure_filename'):
    #             attachment = self.env['ir.attachment'].create({
    #                 'name': vals.get('brochure_filename'),
    #                 'type': 'binary',
    #                 'datas': vals.get('brochure_file'),
    #                 'res_model': self._name,
    #                 'res_id': record.id,
    #                 'mimetype': 'application/pdf',
    #             })
    #             record.message_post(
    #                 body=_("Brochure uploaded: %s") % attachment.name,
    #                 attachment_ids=[attachment.id]
    #             )

    #         # Handle YouTube URL for video gallery
    #         if vals.get('youtube_url'):
    #             gallery = self.env['video.gallary'].search([('product_id', '=', record.id)], limit=1)
    #             if gallery:
    #                 gallery.write({
    #                     'youtube_url': vals['youtube_url'],
    #                     'name': record.name,
    #                 })
    #             else:
    #                 self.env['video.gallary'].create({
    #                     'name': record.name,
    #                     'youtube_url': vals['youtube_url'],
    #                     'product_id': record.id,
    #                 })

    #     return res

    # def write(self, vals):
    #     res = super().write(vals)
    #     for rec in self:
    #         if vals.get('youtube_url'):
    #             # Update or create related gallery
    #             gallery = self.env['video.gallary'].search([('product_id', '=', rec.id)], limit=1)
    #             if gallery:
    #                 gallery.write({
    #                     'youtube_url': vals['youtube_url'],
    #                     'name': rec.name,
    #                 })
    #             else:
    #                 self.env['video.gallary'].create({
    #                     'name': rec.name,
    #                     'youtube_url': vals['youtube_url'],
    #                     'product_id': rec.id,
    #                 })
    #     return res

class ProductDetailHistory(models.Model):
    _name = 'product.detail.history'
    _description = 'Product Detail Sharing History'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    product_template_id = fields.Many2one('product.template', string="Product", required=True)
    date_shared = fields.Datetime(string="Date Shared", default=fields.Datetime.now)
    shared_by = fields.Many2one('res.users', string="Shared By", default=lambda self: self.env.user)
    notes = fields.Text(string="Notes")


# models/product_video.py

# class IrAttachment(models.Model):
#     _inherit = 'ir.attachment'
    
#     # Video specific fields
#     video_duration = fields.Float(string='Duration (seconds)', help='Video duration in seconds')
#     video_format = fields.Char(string='Video Format', compute='_compute_video_format')
#     is_video = fields.Boolean(string='Is Video', compute='_compute_is_video', store=True)
#     file_size_mb = fields.Float(string='File Size (MB)', compute='_compute_file_size_mb')
    
#     @api.depends('mimetype')
#     def _compute_is_video(self):
#         for record in self:
#             record.is_video = record.mimetype and record.mimetype.startswith('video/') if record.mimetype else False
    
#     @api.depends('mimetype')
#     def _compute_video_format(self):
#         for record in self:
#             if record.mimetype and record.mimetype.startswith('video/'):
#                 record.video_format = record.mimetype.split('/')[-1].upper()
#             else:
#                 record.video_format = ''
    
#     @api.depends('file_size')
#     def _compute_file_size_mb(self):
#         for record in self:
#             record.file_size_mb = round(record.file_size / (1024 * 1024), 2) if record.file_size else 0.0
    
#     @api.constrains('mimetype', 'file_size')
#     def _check_video_constraints(self):
#         """Validate video files"""
#         for record in self:
#             if record.is_video:
#                 # Check file size (limit to 100MB)
#                 if record.file_size > 100 * 1024 * 1024:
#                     raise ValidationError('Video file size cannot exceed 100 MB')
                
#                 # Check video formats
#                 allowed_formats = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/webm']
#                 if record.mimetype not in allowed_formats:
#                     raise ValidationError(f'Video format {record.mimetype} is not supported. Allowed formats: MP4, AVI, MOV, WMV, WEBM')
    
#     def get_video_url(self):
#         """Get video streaming URL"""
#         self.ensure_one()
#         if self.is_video:
#             return f'/web/content/{self.id}'
#         return False
    
#     def get_video_thumbnail(self):
#         """Generate video thumbnail (placeholder method)"""
#         self.ensure_one()
#         if self.is_video:
#             # This would need additional library like opencv-python or ffmpeg
#             # For now returning a placeholder
#             return '/web/static/src/img/placeholder.png'
#         return False

