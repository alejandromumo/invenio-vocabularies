# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Vocabulary awards."""

from invenio_records_resources.factories.factory import RecordTypeFactory

from ...records.pidprovider import PIDProviderFactory
from ...records.systemfields import BaseVocabularyPIDFieldContext
from ...services.permissions import PermissionPolicy
from .config import AwardsSearchOptions, service_components
from .schema import AwardSchema

record_type = RecordTypeFactory(
    "Award",
    # Data layer
    pid_field_kwargs={
        "create": False,
        "provider": PIDProviderFactory.create(pid_type='gra'),
        "context_cls": BaseVocabularyPIDFieldContext,
    },
    schema_version="1.0.0",
    schema_path="local://awards/award-v1.0.0.json",
    # Service layer
    service_schema=AwardSchema,
    search_options=AwardsSearchOptions,
    service_components=service_components,
    permission_policy_cls=PermissionPolicy,
    # Resource layer
    endpoint_route='/awards',
)
