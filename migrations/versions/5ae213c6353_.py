"""empty message

Revision ID: 5ae213c6353
Revises: 3c73f5517a2
Create Date: 2015-07-01 16:08:50.298141

"""

# revision identifiers, used by Alembic.
revision = '5ae213c6353'
down_revision = '3c73f5517a2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_index('ix_pictures_path_to_image')
    op.drop_index('ix_pictures_path_to_thumbnail')
    op.drop_index('ix_pictures_name')
    op.drop_index('ix_pictures_description')
    op.drop_index('ix_pictures_upload_date')
    op.drop_index('ix_pictures_size')
    with op.batch_alter_table(
            'pictures',
            reflect_args=[sa.Column(
                'description',
                sa.VARCHAR())]
    ) as batch_op:
        batch_op.alter_column('description',
                              existing_type=sa.VARCHAR(),
                              nullable=True)


def downgrade():
    op.drop_index('ix_pictures_path_to_image')
    op.drop_index('ix_pictures_path_to_thumbnail')
    op.drop_index('ix_pictures_name')
    op.drop_index('ix_pictures_description')
    op.drop_index('ix_pictures_upload_date')
    op.drop_index('ix_pictures_size')
    with op.batch_alter_table(
            'pictures',
            reflect_args=[sa.Column(
                'description',
                sa.VARCHAR())]
    ) as batch_op:
        batch_op.alter_column('description',
                              existing_type=sa.VARCHAR(),
                              nullable=False)
