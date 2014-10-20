"""empty message

Revision ID: 1b618132b035
Revises: None
Create Date: 2014-10-10 12:21:40.135390

"""

# revision identifiers, used by Alembic.
revision = '1b618132b035'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_number', sa.String(length=64), nullable=False),
    sa.Column('application_type', sa.String(length=50), nullable=False),
    sa.Column('request_details', sa.TEXT(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('work_queue', sa.String(length=100), nullable=True),
    sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('submitted_by', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cases')
    ### end Alembic commands ###