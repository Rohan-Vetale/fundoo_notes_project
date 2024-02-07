"""add middw

Revision ID: 510f03eec88e
Revises: 34a3eaeb34ea
Create Date: 2024-02-07 14:55:34.944277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '510f03eec88e'
down_revision: Union[str, None] = '34a3eaeb34ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request_logs',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('request_method', sa.String(), nullable=True),
    sa.Column('request_path', sa.String(), nullable=True),
    sa.Column('count', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_request_logs_id'), 'request_logs', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_request_logs_id'), table_name='request_logs')
    op.drop_table('request_logs')
    # ### end Alembic commands ###
