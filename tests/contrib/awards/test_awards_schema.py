# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test award schema."""

import pytest
from marshmallow import ValidationError

from invenio_vocabularies.contrib.awards.schema import AwardRelationSchema, \
    AwardSchema, FundingRelationSchema


#
# AwardRelationSchema
#
def test_valid_full(app, award_full_data):
    loaded = AwardSchema().load(award_full_data)
    assert award_full_data == loaded


def test_valid_minimal():
    valid_minimal = {
        "number": "B12321"
    }
    assert valid_minimal == AwardSchema().load(valid_minimal)


def test_invalid_no_number():
    invalid_no_number = {
        "identifiers": [
            {
                "identifier": "10.5281/zenodo.9999999",
                "scheme": "doi"
            }
        ]
    }
    with pytest.raises(ValidationError):
        data = AwardSchema().load(invalid_no_number)

#
# AwardRelationSchema
#


def test_valid_id():
    valid_id = {
        "id": "test",
    }
    assert valid_id == AwardRelationSchema().load(valid_id)


def test_valid_number_title():
    valid_data = {
        "number": "ABC-123",
        "title": {
            "en": "Test title."
        }
    }
    assert valid_data == AwardRelationSchema().load(valid_data)


def test_invalid_empty():
    invalid_data = {}
    with pytest.raises(ValidationError):
        data = AwardRelationSchema().load(invalid_data)


def test_invalid_number_type():
    invalid_data = {
        "number": 123
    }
    with pytest.raises(ValidationError):
        data = AwardRelationSchema().load(invalid_data)

#
# FundingRelationSchema
#


AWARD = {
    "title": {
        "en": "Some award"
    },
    "number": "100",
    "identifiers": [
        {
            "identifier": "10.5281/zenodo.9999999",
            "scheme": "doi"
        }
    ]
}

FUNDER = {
    "name": "Someone",
    "identifiers": [
        {
            "identifier": "10.5281/zenodo.9999999",
            "scheme": "doi"
        }
    ]
}


def test_valid_award_funding():
    valid_funding = {
        "award": AWARD
    }
    assert valid_funding == FundingRelationSchema().load(valid_funding)

    # Test a valid award with different representation
    valid_funding = {
        "award": {
            "id": "test-award-id"
        }
    }
    assert valid_funding == FundingRelationSchema().load(valid_funding)


def test_invalid_award_funding():
    invalid_funding = {
        "award": {
            "identifiers": [
                AWARD.get('identifiers')
            ]
        }
    }
    with pytest.raises(ValidationError):
        data = FundingRelationSchema().load(invalid_funding)


def test_valid_funder_funding():
    valid_funding = {
        "funder": FUNDER
    }
    assert valid_funding == FundingRelationSchema().load(valid_funding)

    # Test a valid funder with different representation
    valid_funding = {
        "funder": {
            "id": "test-funder-id"
        }
    }
    assert valid_funding == FundingRelationSchema().load(valid_funding)


def test_invalid_funder_funding():
    invalid_funding = {
        "funder": {
            "identifiers": [
                AWARD.get('identifiers')
            ]
        }
    }
    with pytest.raises(ValidationError):
        data = FundingRelationSchema().load(invalid_funding)


def test_valid_award_funder_funding():
    valid_funding = {
        "funder": FUNDER,
        "award": AWARD
    }
    assert valid_funding == FundingRelationSchema().load(valid_funding)


def test_invalid_empty_funding():
    invalid_funding = {}
    with pytest.raises(ValidationError):
        data = FundingRelationSchema().load(invalid_funding)
