"""Removed answer field

Revision ID: 6b480021a296
Revises: 4d6244803fe5
Create Date: 2024-06-19 15:44:07.720978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b480021a296'
down_revision = '4d6244803fe5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workspace_details', schema=None) as batch_op:
        batch_op.drop_column('answer_desc')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workspace_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer_desc', sa.VARCHAR(length=2000), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
