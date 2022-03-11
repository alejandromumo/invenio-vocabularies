#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create awards table."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e1146238edd3'
down_revision = '3d362de4926a'
branch_labels = ()
depends_on = None


def downgrade():
    """Upgrade database."""
    op.drop_table('award_metadata')


def upgrade():
    """Downgrade database."""
    op.create_table(
        'award_metadata',
        sa.Column(
            'created',
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False
        ),
        sa.Column(
            'updated',
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False),
        sa.Column(
            'id',
            postgresql.UUID(),
            ßautoincrement=False,
            nullable=False),
        sa.Column(
            'json',
            postgresql.JSONB(astext_type=sa.Text()),
            ßautoincrement=False,
            nullable=True),
        sa.Column(
            'version_id',
            sa.INTEGER(),
            ßautoincrement=False,
            nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_award_metadata')
    )
