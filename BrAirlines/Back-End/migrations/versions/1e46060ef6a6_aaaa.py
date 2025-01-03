"""aaaa

Revision ID: 1e46060ef6a6
Revises: 
Create Date: 2024-11-04 17:05:57.425499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e46060ef6a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('passagens_id_voo_fkey', 'passagens', type_='foreignkey')
    op.drop_constraint('passagens_id_passageiro_fkey', 'passagens', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('passagens_id_passageiro_fkey', 'passagens', 'users', ['id_passageiro'], ['id'])
    op.create_foreign_key('passagens_id_voo_fkey', 'passagens', 'voos', ['id_voo'], ['id'])
    # ### end Alembic commands ###
