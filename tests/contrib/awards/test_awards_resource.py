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
    award_full_data_too["number"] = "other"
    res = client.post(
        f"{prefix}", headers=h, data=json.dumps(award_full_data_too))
    assert res.status_code == 403

    res = client.put(
        f"{prefix}/cern", headers=h, data=json.dumps(award_full_data))
    assert res.status_code == 403

    res = client.delete(f"{prefix}/cern")
    assert res.status_code == 403


def test_awards_get(client, example_award, h, prefix):
    """Test the endpoint to retrieve a single item."""
    id_ = example_award.id

    res = client.get(f"{prefix}/{id_}", headers=h)
    assert res.status_code == 200
    assert res.json["id"] == id_
    # Test links
    assert res.json["links"] == {
        "self": "https://127.0.0.1:5000/api/awards/cern"
    }


def test_awards_search(client, example_award, h, prefix):
    """Test a successful search."""
    res = client.get(prefix, headers=h)

    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["sortBy"] == "title"


def _create_awards(service, identity):
    """Create dummy awards with similar names/acronyms/titles."""
    awards = [
        {
            "name": "CERN",
            "title": {
                "en": "European Organization for Nuclear Research",
                "fr": "Conseil Européen pour la Recherche Nucléaire"
            }
        },
        {
            "name": "OTHER",
            "title": {
                "en": "CERN"
            }
        },
        {
            "name": "CERT",
            "title": {
                "en": "Computer Emergency Response Team",
                "fr": "Équipe d'Intervention d'Urgence Informatique"
            }
        },
        {
            "name": "Northwestern University",
            "title": {
                "en": "Northwestern University",
            }
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

    # Should show 2 results, but id=cern as first due to name sorting
    res = client.get(f"{prefix}?suggest=CERN", headers=h)
    assert res.status_code == 200
    assert res.json["hits"]["total"] == 2
    assert res.json["hits"]["hits"][0]["name"] == "CERN"
    assert res.json["hits"]["hits"][1]["name"] == "OTHER"

    # Should show 1 result
    res = client.get(f"{prefix}?suggest=nucléaire", headers=h)
    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["hits"]["hits"][0]["name"] == "CERN"

    # Should show 2 results, but id=nu as first due to name
    res = client.get(f"{prefix}?suggest=nu", headers=h)
    assert res.status_code == 200
    assert res.json["hits"]["total"] == 1
    assert res.json["hits"]["hits"][0]["id"] == "cern"  # due to nucleaire
