"""empty message

Revision ID: 87eca0538053
Revises: ebab1388de9d
Create Date: 2019-06-13 20:28:16.298293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87eca0538053'
down_revision = 'ebab1388de9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('map_register_modified_by_fkey', 'map_register', type_='foreignkey')
    op.drop_column('map_register', 'modified_by')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('map_register', sa.Column('modified_by', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('map_register_modified_by_fkey', 'map_register', 'users', ['modified_by'], ['id'])
    # ### end Alembic commands ###
