"""empty message

Revision ID: f4937e2b6444
Revises: 6e2a6119acab
Create Date: 2024-10-20 19:30:26.609654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4937e2b6444'
down_revision = '6e2a6119acab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('ingredientes', sa.String(length=200), nullable=False),
    sa.Column('pasos', sa.String(), nullable=False),
    sa.Column('fecha_publicacion', sa.DateTime(), nullable=False),
    sa.Column('img_ilustrativa', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe')
    # ### end Alembic commands ###
