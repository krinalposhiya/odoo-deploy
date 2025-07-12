
from odoo import models, fields, api
import re

class MyModel(models.Model):
    _name = 'video.gallary'  # replace with your actual model name
    _description = 'Model with YouTube Video Preview'

    # youtube_url = fields.Char("YouTube URL")
    # video_preview = fields.Html("Video Preview", compute="_compute_video_preview", sanitize=False)

    # @api.depends('youtube_url')
    # def _compute_video_preview(self):
    #     for record in self:
    #         video_id = ""
    #         if record.youtube_url:
    #             # Extract video ID from YouTube link
    #             match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_\-]{11})", record.youtube_url)
    #             if match:
    #                 video_id = match.group(1)
    #         if video_id:
    #             record.video_preview = f'''
    #             <iframe width="560" height="315" 
    #                     src="https://www.youtube.com/embed/{video_id}" 
    #                     frameborder="0" allowfullscreen></iframe>
    #             '''
    #         else:
    #             record.video_preview = "<p>Invalid or no YouTube link provided.</p>"

    name = fields.Char("Title")
    youtube_url = fields.Char("YouTube URL")
    product_id = fields.Many2one('product.template', string="Product")
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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
