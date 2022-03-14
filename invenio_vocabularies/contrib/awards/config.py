# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Vocabulary grants configuration."""

from flask import current_app
from flask_babelex import lazy_gettext as _
from invenio_records_resources.services import SearchOptions
from invenio_records_resources.services.records.components import DataComponent
from invenio_records_resources.services.records.params import \
    SuggestQueryParser
from werkzeug.local import LocalProxy

from ...services.components import PIDComponent

grant_schemes = LocalProxy(
     lambda: current_app.config["VOCABULARIES_GRANT_SCHEMES"]
)


class GrantsSearchOptions(SearchOptions):
    """Search options."""

    # QUESTION ask alex about what's useful for the domain
    # QUESTION mappings number either a text or keyword
    suggest_parser_cls = SuggestQueryParser.factory(
        fields=[
            'title.*^50',
            'title.*._2gram',
            'title.*._3gram',
            'number^10',
            'funder.name^5',
            'funder.name._2gram',
            'funder.name._3gram',
        ],
    )

    sort_default = 'bestmatch'

    sort_default_no_query = 'name'

    sort_options = {
        "bestmatch": dict(
            title=_('Best match'),
            fields=['_score'],  # ES defaults to desc on `_score` field
        ),
        # QUESTION ask alex about what's useful for the domain. Either number or nothing at all and assume defaults from SearchOptions parent object?
        "newest": dict(
            title=_('Newest'),
            fields=['-created'],
        ),
        "oldest": dict(
            title=_('Oldest'),
            fields=['created'],
        ),
    }


service_components = [
    # Order of components are important!
    DataComponent,
    PIDComponent,
]
