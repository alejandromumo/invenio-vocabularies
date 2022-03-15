# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Awards API tests."""

from functools import partial

import pytest
from invenio_indexer.api import RecordIndexer
from invenio_search import current_search_client
from jsonschema import ValidationError as SchemaValidationError

from invenio_vocabularies.contrib.awards.api import Award


@pytest.fixture()
def search_get():
    """Get a document from an index."""
    return partial(
        current_search_client.get, Award.index._name, doc_type="_doc"
    )


@pytest.fixture()
def indexer():
    """Indexer instance with correct Record class."""
    return RecordIndexer(
        record_cls=Award,
        record_to_index=lambda r: (r.__class__.index._name, "_doc"),
    )


@pytest.fixture()
def example_award(db, award_full_data):
    """Example award."""
    awa = Award.create(award_full_data)
    Award.pid.create(awa)
    awa.commit()
    db.session.commit()
    return awa


def test_award_schema_validation(app, db, example_award):
    """Award schema validation."""
    # valid data
    awa = example_award

    assert awa.schema == "local://awards/award-v1.0.0.json"
    assert awa.pid
    assert awa.id

    # invalid data
    examples = [
        # title are objects of key/string.
        {"id": "cern", "title": "not a dict"},
        {"id": "cern", "title": {"en": 123}},
        # identifiers are objects of key/string.
        {"id": "cern", "identifiers": "03yrm5c26"},
        {"id": "cern", "identifiers": ["03yrm5c26"]},
        {"id": "cern", "identifiers": {"03yrm5c26"}},
        # number must be a string
        {"id": "cern", "number": 123},
        # funder must be an object
        {"id": "cern", "funder": 123}
    ]

    for ex in examples:
        pytest.raises(SchemaValidationError, Award.create, ex)


def test_award_indexing(
    app, db, es, example_award, indexer, search_get
):
    """Test indexing of an award."""
    # Index document in ES
    assert indexer.index(example_award)["result"] == "created"

    # Retrieve document from ES
    data = search_get(id=example_award.id)

    # Loads the ES data and compare
    awa = Award.loads(data["_source"])
    assert awa == example_award
    assert awa.id == example_award.id
    assert awa.revision_id == example_award.revision_id
    assert awa.created == example_award.created
    assert awa.updated == example_award.updated


def test_award_pid(app, db, example_award):
    """Test award pid creation."""
    awa = example_award

    assert awa.pid.pid_value == "test_award"
    assert awa.pid.pid_type == "awa"
    assert Award.pid.resolve("test_award")
