# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test the award vocabulary service."""

import pytest
from invenio_pidstore.errors import PIDAlreadyExists, PIDDeletedError
from marshmallow.exceptions import ValidationError

from invenio_vocabularies.contrib.awards.api import Award


def test_simple_flow(app, db, service, identity, award_full_data):
    """Test a simple vocabulary service flow."""
    # Create it
    item = service.create(identity, award_full_data)
    number = item.number

    assert item.number == award_full_data['number']
    for k, v in award_full_data.items():
        assert item.data[k] == v

    # Read it
    read_item = service.read(identity, 'cern')
    assert item.number == read_item.number
    assert item.data == read_item.data

    # Refresh index to make changes live.
    Award.index.refresh()

    # Search it
    res = service.search(
        identity, q=f"number:{number}", size=25, page=1)
    assert res.total == 1
    assert list(res.hits)[0] == read_item.data

    # Update it
    data = read_item.data
    data['title']['en'] = 'New title'
    update_item = service.update(identity, number, data)
    assert item.number == update_item.number
    assert update_item['title']['en'] == 'New title'

    # Delete it
    assert service.delete(identity, number)

    # Refresh to make changes live
    Award.index.refresh()

    # Fail to retrieve it
    # - db
    pytest.raises(PIDDeletedError, service.read, identity, number)
    # - search
    res = service.search(
        identity, q=f"number:{number}", size=25, page=1)
    assert res.total == 0


def test_pid_already_registered(
    app, db, service, identity, award_full_data
):
    """Recreating a record with same id should fail."""
    service.create(identity, award_full_data)
    pytest.raises(
        PIDAlreadyExists, service.create, identity, award_full_data)


def test_extra_fields(app, db, service, identity, award_full_data):
    """Extra fields in data should fail."""
    award_full_data['invalid'] = 1
    pytest.raises(
        ValidationError, service.create, identity, award_full_data)
