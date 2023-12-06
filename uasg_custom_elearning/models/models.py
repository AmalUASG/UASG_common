from odoo import models, fields, api
from odoo.http import request
import re
from odoo.addons.http_routing.models.ir_http import slug, url_for
from markupsafe import Markup

class Slides(models.Model):

    _inherit = [ 'slide.slide']

    video_source_type = fields.Selection(selection_add=[
        ('other', 'Other')],
        string='Video Source', compute="_compute_video_source_type")



    @api.depends('video_url')
    def _compute_video_source_type(self):
        for slide in self:
            video_source_type = False
            youtube_match = re.match(self.YOUTUBE_VIDEO_ID_REGEX, slide.video_url) if slide.video_url else False
            if youtube_match and len(youtube_match.groups()) == 2 and len(youtube_match.group(2)) == 11:
                video_source_type = 'youtube'
            if slide.video_url and not video_source_type and re.match(self.GOOGLE_DRIVE_DOCUMENT_ID_REGEX, slide.video_url):
                video_source_type = 'google_drive'
            vimeo_match = re.search(self.VIMEO_VIDEO_ID_REGEX, slide.video_url) if slide.video_url else False
            if not video_source_type and vimeo_match and len(vimeo_match.groups()) == 3:
                video_source_type = 'vimeo'
            else : 
                video_source_type = 'other'

            slide.video_source_type = video_source_type                               

    @api.depends('slide_category', 'google_drive_id', 'video_source_type', 'youtube_id')
    def _compute_embed_code(self):
        request_base_url = request.httprequest.url_root if request else False
        for slide in self:
            base_url = request_base_url or slide.get_base_url()
            if base_url[-1] == '/':
                base_url = base_url[:-1]

            embed_code = False
            embed_code_external = False
            if slide.slide_category == 'video':
                if slide.video_source_type == 'youtube':
                    query_params = urls.url_parse(slide.video_url).query
                    query_params = query_params + '&theme=light' if query_params else 'theme=light'
                    embed_code = Markup('<iframe src="//www.youtube-nocookie.com/embed/%s?%s" allowFullScreen="true" frameborder="0"></iframe>') % (slide.youtube_id, query_params)
                elif slide.video_source_type == 'google_drive':
                    embed_code = Markup('<iframe src="//drive.google.com/file/d/%s/preview" allowFullScreen="true" frameborder="0"></iframe>') % (slide.google_drive_id)
                elif slide.video_source_type == 'vimeo':
                    if '/' in slide.vimeo_id:
                        # in case of privacy 'with URL only', vimeo adds a token after the video ID
                        # the embed url needs to receive that token as a "h" parameter
                        [vimeo_id, vimeo_token] = slide.vimeo_id.split('/')
                        embed_code = Markup("""
                            <iframe src="https://player.vimeo.com/video/%s?h=%s&badge=0&amp;autopause=0&amp;player_id=0"
                                frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>""") % (
                                vimeo_id, vimeo_token)
                    else:
                        self.embed_code = self.video_url
                elif slide.video_source_type == 'other':

                    embed_code = slide.video_url
            elif slide.slide_category in ['infographic', 'document'] and slide.source_type == 'external' and slide.google_drive_id:
                embed_code = Markup('<iframe src="//drive.google.com/file/d/%s/preview" allowFullScreen="true" frameborder="0"></iframe>') % (slide.google_drive_id)
            elif slide.slide_category == 'document' and slide.source_type == 'local_file':
                slide_url = base_url + url_for('/slides/embed/%s?page=1' % slide.id)
                slide_url_external = base_url + url_for('/slides/embed_external/%s?page=1' % slide.id)
                base_embed_code = Markup('<iframe src="%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>')
                embed_code = base_embed_code % (slide_url, 315, 420)
                embed_code_external = base_embed_code % (slide_url_external, 315, 420)

            slide.embed_code = embed_code
            slide.embed_code_external = embed_code_external or embed_code

class SlideChannel(models.Model):

    _inherit="slide.channel"

    all_companies = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company')