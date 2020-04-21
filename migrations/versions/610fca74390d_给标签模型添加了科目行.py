"""给标签模型添加了科目行

Revision ID: 610fca74390d
Revises: 4f8ad9c22eba
Create Date: 2020-04-19 14:32:09.170417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '610fca74390d'
down_revision = '4f8ad9c22eba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('subject_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tags', 'subjects', ['subject_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags', type_='foreignkey')
    op.drop_column('tags', 'subject_id')
    # ### end Alembic commands ###
