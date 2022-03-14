# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Grant vocabulary resources."""

from .grants import record_type

GrantsResourceConfig = record_type.resource_config_cls

GrantsResource = record_type.resource_cls
