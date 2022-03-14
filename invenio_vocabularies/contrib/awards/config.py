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

    # QUESTION IS IT? it will search using title.* in 2/3  shingles
    # QUESTION ^100 is correct?
    suggest_parser_cls = SuggestQueryParser.factory(
        fields=[
            'title.*^100',
            'title.*._2gram',
            'title.*._3gram',
        ],
    )

    sort_default = 'bestmatch'

    sort_default_no_query = 'name'

    sort_options = {
        "bestmatch": dict(
            title=_('Best match'),
            fields=['_score'],  # ES defaults to desc on `_score` field
        ),
        # QUESTION removed sort option for title. This can be removed since that's the default behavior in parent's class. Is it ok?
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
