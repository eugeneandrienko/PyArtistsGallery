"""empty message

Revision ID: 28cfe4f393f
Revises: 5ae213c6353
Create Date: 2015-07-13 17:43:02.291108

"""

# revision identifiers, used by Alembic.
revision = '28cfe4f393f'
down_revision = '5ae213c6353'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuration', sa.Column('gallery_description', sa.String(), nullable=False,
                                             server_default='Default description'))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('configuration', 'gallery_description')
    ### end Alembic commands ###
