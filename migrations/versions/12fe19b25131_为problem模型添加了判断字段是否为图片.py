"""为Problem模型添加了判断字段是否为图片

Revision ID: 12fe19b25131
Revises: 610fca74390d
Create Date: 2020-04-20 11:41:14.706675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12fe19b25131'
down_revision = '610fca74390d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('problems', sa.Column('body_is_image', sa.Boolean(), nullable=True))
    op.add_column('problems', sa.Column('correct_answer_is_image', sa.Boolean(), nullable=True))
    op.add_column('problems', sa.Column('description_is_image', sa.Boolean(), nullable=True))
    op.add_column('problems', sa.Column('original_answer_is_image', sa.Boolean(), nullable=True))
    op.add_column('problems', sa.Column('title', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('problems', 'title')
    op.drop_column('problems', 'original_answer_is_image')
    op.drop_column('problems', 'description_is_image')
    op.drop_column('problems', 'correct_answer_is_image')
    op.drop_column('problems', 'body_is_image')
    # ### end Alembic commands ###
