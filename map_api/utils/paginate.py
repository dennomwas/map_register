from flask import request, url_for, jsonify
from flask_paginate import Pagination

# local imports
from config import Config


def paginate_items(query):
    page = request.args.get('page', 1, type=int)
    per_page = Config.PER_PAGE

    paginated_data = query.paginate(
        page=page,
        per_page=per_page)

    page_items = paginated_data.items
    if page_items:
        next_url = None
        previous_url = None

        if paginated_data.has_next:
            next_url = url_for('map_blueprint.mapregister',
                               page=paginated_data.next_num, _external=True)

        if paginated_data.has_prev:
            previous_url = url_for('map_blueprint.mapregister',
                                   page=paginated_data.prev_num, _external=True)

        # serialized_data = schema.dump(page_items, many=True).data

        return ({
            'previous_page': previous_url,
            'current_page': paginated_data.page,
            'next_page': next_url,
            'count': paginated_data.total,
            'pages': paginated_data.pages,
            'status': 200,
            'page_items': page_items
        })