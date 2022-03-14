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
    AwardsResource, AwardsResourceConfig
from invenio_vocabularies.contrib.awards.services import \
    AwardsService, AwardsServiceConfig


@pytest.fixture(scope="module")
def extra_entry_points():
    """Extra entry points to load the mock_module features."""
    return {
        "invenio_db.models": [
            "awards = invenio_vocabularies.contrib.awards.models",
        ],
        "invenio_jsonschemas.schemas": [
            "awards = \
                invenio_vocabularies.contrib.awards.jsonschemas",
        ],
        "invenio_search.mappings": [
            "awards = \
                invenio_vocabularies.contrib.awards.mappings",
        ]
    }


@pytest.fixture(scope="function")
def award_full_data():
    """Full award data."""
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
            "en": "Test award"
        },
        "number": "B1000",
        "funder": {
            "id": "funder-1"
        }
    }


@pytest.fixture(scope='module')
def service():
    """Awards service object."""
    return AwardsService(config=AwardsServiceConfig)


@pytest.fixture(scope="module")
def resource(service):
    """Awards resource object."""
    return AwardsResource(AwardsResourceConfig, service)


@pytest.fixture(scope="module")
def base_app(base_app, resource, service):
    """Application factory fixture.

    Registers awards' resource and service.
    """
    base_app.register_blueprint(resource.as_blueprint())
    registry = base_app.extensions['invenio-records-resources'].registry
    registry.register(service, service_id='awards-service')
    yield base_app
