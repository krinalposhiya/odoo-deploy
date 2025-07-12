import datetime
from odoo import http
from odoo.http import request
from odoo import models, fields, api, _
from operator import itemgetter
import itertools
import operator
from datetime import date, timedelta, datetime
from collections import defaultdict

class ProjectFilter(http.Controller):
    """The ProjectFilter class provides the filter option to the js.
    When applying the filter returns the corresponding data."""


    # @http.route('/product/dashboard/data', auth='public', type='json')
    # def get_product_categories(self, **kw):
    #     categories = request.env['product.category'].sudo().search([])
    #     result = []
    #     for cat in categories:
    #         result.append({
    #             'id': cat.id,
    #             'name': cat.name,
    #         })
    #     return {'categories': result}

    @http.route('/product/dashboard/data', auth='public', type='json')
    def get_product_categories(self, **kw):
        categories = request.env['product.category'].sudo().search([])
        result = []
        for cat in categories:
            result.append({
                'id': cat.id,
                'name': cat.name,
                'parent_id': cat.parent_id.id if cat.parent_id else False,
            })
        return {'categories': result}


    @http.route('/product/list/by/category', auth='public', type='json')
    def get_products_by_category(self, **kw):
        category_id = int(kw.get('category_id', 0))
        search_term = kw.get('search_term', '').strip()

        domain = [('is_equipment', '=', True)]

        if category_id:
            # Include child categories
            category = request.env['product.category'].sudo().browse(category_id)
            all_cats = category.child_id.ids + [category.id]
            domain.append(('categ_id', 'in', all_cats))

        if search_term:
            domain.append(('name', 'ilike', search_term))

        products = request.env['product.template'].sudo().search(domain)

        result = []
        for prod in products:
            result.append({
                'id': prod.id,
                'name': prod.name,
                'image': f"/web/image/product.template/{prod.id}/image_1920",
                'pro_type': prod.pro_type,
                'list_price': prod.list_price,
                'video_url': self._get_embed_url(prod.youtube_url),
                'image_1': f"/web/image/product.template/{prod.id}/image_1" if prod.image_1 else False,
                'image_2': f"/web/image/product.template/{prod.id}/image_2" if prod.image_2 else False,
                'image_3': f"/web/image/product.template/{prod.id}/image_3" if prod.image_3 else False,
                'image_4': f"/web/image/product.template/{prod.id}/image_4" if prod.image_4 else False,
                'brochure_url': prod.brochure_file and f"/web/content/product.template/{prod.id}/brochure_file/{prod.brochure_filename}" or False,
                'description': prod.description or '',
            })
        return {'products': result}

    def _get_embed_url(self, url):
        if not url:
            return ''
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return url



    @http.route('/product/open/add/history', type='json', auth='user')
    def open_add_history_wizard(self, product_id):
        product = request.env['product.template'].sudo().browse(int(product_id))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add History',
            'res_model': 'product.history.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': product.id,
            }
        }




