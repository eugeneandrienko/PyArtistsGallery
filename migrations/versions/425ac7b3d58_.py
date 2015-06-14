"""empty message

Revision ID: 425ac7b3d58
Revises: 2615e2b854
Create Date: 2015-06-01 23:34:49.724890

"""

# revision identifiers, used by Alembic.
revision = '425ac7b3d58'
down_revision = '2615e2b854'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('description', sa.String(), nullable=False, server_default=''))
    op.create_index(op.f('ix_pictures_description'), 'pictures', ['description'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pictures_description'), table_name='pictures')
    op.drop_column('pictures', 'description')
    ### end Alembic commands ###