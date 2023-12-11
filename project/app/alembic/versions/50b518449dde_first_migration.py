"""First migration

Revision ID: 50b518449dde
Revises: 
Create Date: 2023-12-09 00:11:07.774722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '50b518449dde'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Patients',
    sa.Column('id_patient', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('email', sa.VARCHAR(length=50), nullable=False),
    sa.Column('address', sa.VARCHAR(length=50), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=50), nullable=False),
    sa.Column('document', mysql.LONGBLOB(), nullable=False),
    sa.PrimaryKeyConstraint('id_patient')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Patients')
    # ### end Alembic commands ###