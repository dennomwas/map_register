"""empty message

Revision ID: 828aa4e4e6bf
Revises: 
Create Date: 2019-06-11 23:53:42.697757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '828aa4e4e6bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email_address', sa.String(length=100), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('map_register',
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('serial_no', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('map_name', sa.String(length=100), nullable=False),
    sa.Column('area', sa.String(length=100), nullable=False),
    sa.Column('locality', sa.String(length=100), nullable=False),
    sa.Column('map_type', sa.String(length=100), nullable=False),
    sa.Column('lr_no', sa.String(length=100), nullable=True),
    sa.Column('fr_no', sa.String(length=100), nullable=True),
    sa.Column('sheet_no', sa.String(length=100), nullable=True),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('map_register')
    op.drop_table('users')
    # ### end Alembic commands ###