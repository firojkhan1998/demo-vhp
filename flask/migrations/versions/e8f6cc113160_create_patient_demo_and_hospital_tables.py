"""Create patient, demo, and hospital tables

Revision ID: e8f6cc113160
Revises: 
Create Date: 2025-01-12 14:38:06.346445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f6cc113160'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospital',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hospital_name', sa.String(length=100), nullable=False),
    sa.Column('hospital_company_name', sa.String(length=100), nullable=False),
    sa.Column('hospital_email', sa.String(length=100), nullable=False),
    sa.Column('hospital_contact', sa.String(length=15), nullable=False),
    sa.Column('hospital_address', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient',
    sa.Column('patient_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patient_fname', sa.String(length=100), nullable=False),
    sa.Column('patient_lname', sa.String(length=100), nullable=False),
    sa.Column('patient_dob', sa.DateTime(), nullable=False),
    sa.Column('patient_aadhar', sa.Integer(), nullable=False),
    sa.Column('patient_email', sa.String(length=100), nullable=False),
    sa.Column('patient_contact', sa.String(length=15), nullable=False),
    sa.Column('patient_address', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('patient_id')
    )
    with op.batch_alter_table('demo', schema=None) as batch_op:
        batch_op.alter_column('contact',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=15),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('demo', schema=None) as batch_op:
        batch_op.alter_column('contact',
               existing_type=sa.String(length=15),
               type_=sa.INTEGER(),
               existing_nullable=False)

    op.drop_table('patient')
    op.drop_table('hospital')
    # ### end Alembic commands ###
