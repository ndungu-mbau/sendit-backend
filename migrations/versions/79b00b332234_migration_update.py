"""migration update

Revision ID: 79b00b332234
Revises: a56d09292c16
Create Date: 2024-07-12 16:47:58.634652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79b00b332234'
down_revision = 'a56d09292c16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=110),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=40),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=110),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)

    # ### end Alembic commands ###
