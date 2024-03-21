"""Add fucking pk

Revision ID: bc8a4d89646f
Revises: 327528894dc8
Create Date: 2024-03-21 12:30:12.789963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc8a4d89646f'
down_revision: Union[str, None] = '327528894dc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temp_schedule',
    sa.Column('fucking_unneeded_pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('flat', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('was_sent', sa.Boolean(), nullable=True),
    sa.Column('start_offset', sa.Integer(), nullable=True),
    sa.Column('end_offset', sa.Integer(), nullable=True),
    sa.Column('target_temp', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('fucking_unneeded_pk')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('temp_schedule')
    # ### end Alembic commands ###
