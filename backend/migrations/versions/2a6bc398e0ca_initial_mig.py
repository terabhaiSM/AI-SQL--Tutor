"""Initial mig

Revision ID: 2a6bc398e0ca
Revises: fffa7ad835bc
Create Date: 2024-06-17 12:16:51.328411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a6bc398e0ca'
down_revision = 'fffa7ad835bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=500), nullable=False),
    sa.Column('topic', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('topic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('level', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=500), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workspace',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('last_access_date', sa.DateTime(), nullable=True),
    sa.Column('workspace_topics', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('sampledatabase_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workspace_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workspace_id', sa.Integer(), nullable=False),
    sa.Column('workspace_practice_seq', sa.Integer(), nullable=False),
    sa.Column('question_desc_json', sa.JSON(), nullable=False),
    sa.Column('answer_desc', sa.String(length=500), nullable=False),
    sa.Column('correct_boolean', sa.Boolean(), nullable=True),
    sa.Column('feedback_from_AI_json', sa.JSON(), nullable=True),
    sa.Column('AI_rating', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workspace_details')
    op.drop_table('workspace')
    op.drop_table('answer')
    op.drop_table('user')
    op.drop_table('topic')
    op.drop_table('question')
    # ### end Alembic commands ###
