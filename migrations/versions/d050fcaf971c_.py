"""empty message

Revision ID: d050fcaf971c
Revises: 2b99ccd8396d
Create Date: 2021-05-02 22:04:42.141339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd050fcaf971c'
down_revision = '2b99ccd8396d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('task', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
