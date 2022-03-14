# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest

from invenio_vocabularies.contrib.awards.resources import \
    GrantsResource, GrantsResourceConfig
from invenio_vocabularies.contrib.awards.services import \
    GrantsService, GrantsServiceConfig


@pytest.fixture(scope="module")
def extra_entry_points():
    """Extra entry points to load the mock_module features."""
    return {
        "invenio_db.models": [
            "grants = invenio_vocabularies.contrib.grants.models",
        ],
        "invenio_jsonschemas.schemas": [
            "grants = \
                invenio_vocabularies.contrib.grants.jsonschemas",
        ],
        "invenio_search.mappings": [
            "grants = \
                invenio_vocabularies.contrib.grants.mappings",
        ]
    }


@pytest.fixture(scope="function")
def grant_full_data():
    """Full grant data."""
    return {
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
        "number": "B1000",
        "funder": {
            "id": "funder-1"
        }
    }


@pytest.fixture(scope='module')
def service():
    """Grants service object."""
    return GrantsService(config=GrantsServiceConfig)


@pytest.fixture(scope="module")
def resource(service):
    """Grants resource object."""
    return GrantsResource(GrantsResourceConfig, service)


@pytest.fixture(scope="module")
def base_app(base_app, resource, service):
    """Application factory fixture.

    Registers grants' resource and service.
    """
    base_app.register_blueprint(resource.as_blueprint())
    registry = base_app.extensions['invenio-records-resources'].registry
    registry.register(service, service_id='grants-service')
    yield base_app
