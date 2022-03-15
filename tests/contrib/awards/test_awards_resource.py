# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test the award vocabulary resource."""

import json
from copy import deepcopy

import pytest

from invenio_vocabularies.contrib.awards.api import Award


@pytest.fixture(scope="module")
def prefix():
    """API prefix."""
    return "awards"


@pytest.fixture()
def example_award(
    app, db, es_clear, identity, service, award_full_data
):
    """Example award."""
    award = service.create(identity, award_full_data)
    Award.index.refresh()  # Refresh the index

    return award


def test_awards_invalid(client, h, prefix):
    """Test invalid type."""
    # invalid type
    res = client.get(f"{prefix}/invalid", headers=h)
    assert res.status_code == 404


def test_awards_forbidden(
    client, h, prefix, example_award, award_full_data
):
    """Test invalid type."""
    # invalid type
    award_full_data_too = deepcopy(award_full_data)
    award_full_data_too["id"] = "other"
    res = client.post(
        f"{prefix}", headers=h, data=json.dumps(award_full_data_too))
    assert res.status_code == 403

    res = client.put(
        f"{prefix}/test_award", headers=h, data=json.dumps(award_full_data))
    assert res.status_code == 403

    res = client.delete(f"{prefix}/test_award")
    assert res.status_code == 403


def test_awards_get(client, example_award, h, prefix):
    """Test the endpoint to retrieve a single item."""
    id_ = example_award.id

    res = client.get(f"{prefix}/{id_}", headers=h)
    assert res.status_code == 200
    assert res.json["id"] == id_
    # Test links
    assert res.json["links"] == {
        "self": "https://127.0.0.1:5000/api/awards/test_award"
    }


def test_awards_search(client, example_award, h, prefix):
    """Test a successful search."""
    res = client.get(prefix, headers=h)

    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["sortBy"] == "newest"

    res = client.get(f"{prefix}?q=test_award", headers=h)

    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["sortBy"] == "bestmatch"


def _create_awards(service, identity):
    """Create dummy awards with similar ids/numbers/titles."""
    awards = [
        {
            "title": {
                "en": "European Organization for Nuclear Research",
                "fr": "Conseil Européen pour la Recherche Nucléaire"
            },
            "id": "cern-award",
            "number": "cern-123"
        },
        {
            "title": {
                "en": "Computer Emergency Response Team",
                "fr": "Équipe d'Intervention d'Urgence Informatique"
            },
            "id": "cert-award",
            "number": "cert-123"
        },
        {
            "title": {
                "en": "Northwestern University",
            },
            "id": "nu-award",
            "number": "nu-123"
        }
    ]
    for aff in awards:
        service.create(identity, aff)

    Award.index.refresh()  # Refresh the index


def test_awards_suggest_sort(
    app, db, es_clear, identity, service, client, h, prefix
):
    """Test a successful search."""
    _create_awards(service, identity)

    # Should show 1 result
    res = client.get(f"{prefix}?suggest=cern", headers=h)
    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["hits"]["hits"][0]["id"] == "cern-award"

    # Should show 1 result
    res = client.get(f"{prefix}?suggest=nucléaire", headers=h)
    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["hits"]["hits"][0]["id"] == "cern-award"

    # Should show 2 results, but id=cern-award as first due to number
    res = client.get(f"{prefix}?suggest=nu", headers=h)
    assert res.status_code == 200
    assert res.json["hits"]["total"] == 2
    assert res.json["hits"]["hits"][0]["id"] == "cern-award"
    assert res.json["hits"]["hits"][1]["id"] == "nu-award"

    # Should show 1 result
    res = client.get(f"{prefix}?suggest=University", headers=h)
    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["hits"]["hits"][0]["id"] == "nu-award"
