"""atualizando voo

Revision ID: cf9861d5e762
Revises: 3243a0c89c10
Create Date: 2024-11-02 18:08:23.950764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf9861d5e762'
down_revision: Union[str, None] = '3243a0c89c10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('voos', sa.Column('preco', sa.Integer(), nullable=True))
    op.add_column('voos', sa.Column('imagem_companhia', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('voos', 'imagem_companhia')
    op.drop_column('voos', 'preco')
    # ### end Alembic commands ###
