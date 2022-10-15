"""empty message

Revision ID: 0fcef44238e5
Revises: 
Create Date: 2022-10-15 09:49:08.032086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fcef44238e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'commentaire', type_='foreignkey')
    op.create_foreign_key(None, 'commentaire', 'personne', ['client_id'], ['id'])
    op.create_unique_constraint(None, 'entreprises', ['nomEntreprise'])
    op.alter_column('message', 'lienPhoto',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('message', 'lienVideo',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.drop_constraint(None, 'publication', type_='foreignkey')
    op.create_foreign_key(None, 'publication', 'personne', ['exposant_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'publication', type_='foreignkey')
    op.create_foreign_key(None, 'publication', 'exposant', ['exposant_id'], ['id'])
    op.alter_column('message', 'lienVideo',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('message', 'lienPhoto',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.drop_constraint(None, 'entreprises', type_='unique')
    op.drop_constraint(None, 'commentaire', type_='foreignkey')
    op.create_foreign_key(None, 'commentaire', 'client', ['client_id'], ['id'])
    # ### end Alembic commands ###