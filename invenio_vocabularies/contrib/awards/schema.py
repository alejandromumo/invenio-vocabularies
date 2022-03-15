# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Awards schema."""

from flask_babelex import lazy_gettext as _
from functools import partial
from marshmallow import Schema, ValidationError, fields, validate, \
    validates_schema
from marshmallow_utils.fields import IdentifierSet, SanitizedUnicode
from marshmallow_utils.schemas import IdentifierSchema

from .config import award_schemes
from ..funders.schema import FunderRelationSchema
from ...services.schema import BaseVocabularySchema, i18n_strings


class AwardSchema(BaseVocabularySchema):
    """Award schema."""
    identifiers = IdentifierSet(fields.Nested(
        partial(
            IdentifierSchema,
            allowed_schemes=award_schemes,
            identifier_required=False
        )
    ))
    number = SanitizedUnicode(
        required=True,
        validate=validate.Length(min=1, error=_('Number cannot be blank.'))
    )
    funder = fields.Nested(FunderRelationSchema)


class AwardRelationSchema(Schema):
    """Award relation schema."""

    id = SanitizedUnicode()
    number = SanitizedUnicode()
    title = i18n_strings

    @validates_schema
    def validate_data(self, data, **kwargs):
        """Validate either id or number/title are present."""
        id_ = data.get("id")
        number = data.get("number")
        title = data.get("title")
        if (id_) or (number and title):
            pass
        else:
            raise ValidationError(
                    _("An existing id or number/title must be present."),
                    "awards"
            )


class FundingRelationSchema(Schema):
    """Funding schema."""

    funder = fields.Nested(FunderRelationSchema)
    award = fields.Nested(AwardRelationSchema)

    @validates_schema
    def validate_data(self, data, **kwargs):
        """Validate either funder or award is present."""
        funder = data.get('funder')
        award = data.get('award')
        if not funder and not award:
            raise ValidationError(
                {"funding": _("At least award or funder should be present.")})
