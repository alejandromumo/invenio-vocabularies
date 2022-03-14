# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Grants JSONSchema tests."""

import pytest
from jsonschema.exceptions import ValidationError

from invenio_vocabularies.contrib.awards.api import Grant


@pytest.fixture(scope="module")
def schema():
    """Returns the schema location."""
    return "local://grants/grant-v1.0.0.json"


def validates(data):
    """Validates grant data."""
    Grant(data).validate()

    return True


def fails(data):
    """Validates grant data."""
    pytest.raises(ValidationError, validates, data)
    return True


def test_valid_full(appctx, schema):
    data = {
        "$schema": schema,
        "identifiers": [
            {"identifier": "03yrm5c26", "scheme": "ror"}
        ],
        "pid": {
            "pk": 1,
            "status": "R",
            "pid_type": "affid",
            "obj_type": "aff"
        },
        "title": {
            "en": "Test grant"
        },
        "number": "1000",
        "funder": {
            "id": "funder-1"
        }
    }

    assert validates(data)


def test_valid_empty(appctx, schema):
    # check there are no requirements at JSONSchema level
    data = {
        "$schema": schema
    }

    assert validates(data)


# only number is defined by the grant schema
# the rest are inherited and should be tested elsewhere


def test_fails_number(appctx, schema):
    data = {
        "$schema": schema,
        "number": 123
    }

    assert fails(data)
