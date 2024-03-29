"""remove oirrelevant junk

Revision ID: e3af7a501d1d
Revises: ba01c94141b0
Create Date: 2024-03-13 11:51:38.845146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3af7a501d1d'
down_revision = 'ba01c94141b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client')
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_index('ix_transaction_id_client_destinaire')
        batch_op.drop_index('ix_transaction_id_client_originaire')

    op.drop_table('transaction')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('step', sa.INTEGER(), nullable=False),
    sa.Column('type', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=False),
    sa.Column('isFraud', sa.BOOLEAN(), nullable=False),
    sa.Column('id_client_destinaire', sa.INTEGER(), nullable=False),
    sa.Column('id_client_originaire', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.ForeignKeyConstraint(['id_client_destinaire'], ['client.id'], ),
    sa.ForeignKeyConstraint(['id_client_originaire'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.create_index('ix_transaction_id_client_originaire', ['id_client_originaire'], unique=False)
        batch_op.create_index('ix_transaction_id_client_destinaire', ['id_client_destinaire'], unique=False)

    op.create_table('client',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.Column('oldBalance', sa.INTEGER(), nullable=False),
    sa.Column('newBalance', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
