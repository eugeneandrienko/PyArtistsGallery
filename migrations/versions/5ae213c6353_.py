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
    op.create_index(
        op.f('ix_pictures_path_to_image'),
        'pictures', ['path_to_image'], unique=False)
    op.create_index(
        op.f('ix_pictures_path_to_thumbnail'),
        'pictures', ['path_to_thumbnail'], unique=False)
    op.create_index(op.f('ix_pictures_name'), 'pictures', ['name'],
                    unique=False)
    op.create_index(op.f('ix_pictures_description'), 'pictures', ['description'],
                    unique=False)
    op.create_index(
        op.f('ix_pictures_upload_date'),
        'pictures',
        ['upload_date'],
        unique=False)
    op.create_index(op.f('ix_pictures_size'), 'pictures', ['size'], unique=False)


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
