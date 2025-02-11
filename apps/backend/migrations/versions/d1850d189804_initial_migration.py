"""Initial migration

Revision ID: d1850d189804
Revises: 
Create Date: 2025-01-11 11:00:32.030154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1850d189804'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('gender', sa.String(), nullable=False))

    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.alter_column('release_date',
               existing_type=sa.DATE(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.alter_column('release_date',
               existing_type=sa.DATE(),
               nullable=True)

    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('age')

    # ### end Alembic commands ###
