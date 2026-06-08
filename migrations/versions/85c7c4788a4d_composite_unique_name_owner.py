"""composite_unique_name_owner

Revision ID: 85c7c4788a4d
Revises: a76821be9d86
Create Date: 2026-06-07 10:41:07.806193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85c7c4788a4d'
down_revision = 'a76821be9d86'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Rename old table
    op.rename_table('tomato_variety', '_tomato_variety_old')
    
    # 2. Re-create tomato_variety table with composite constraint, dropping old unique constraint on name
    op.create_table('tomato_variety',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=100), nullable=True),
        sa.Column('size', sa.String(length=100), nullable=True),
        sa.Column('origin', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('fallback_image_url', sa.String(length=255), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('in_stock', sa.Boolean(), server_default='1', nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['owner_id'], ['person.id'], name='fk_tomato_variety_owner_id_person'),
        sa.UniqueConstraint('name', 'owner_id', name='uq_tomato_variety_name_owner')
    )
    
    # 3. Copy data
    op.execute('''
        INSERT INTO tomato_variety (id, name, category, color, size, origin, description, image_url, fallback_image_url, owner_id, in_stock)
        SELECT id, name, category, color, size, origin, description, image_url, fallback_image_url, owner_id, in_stock
        FROM _tomato_variety_old
    ''')
    
    # 4. Drop old table
    op.drop_table('_tomato_variety_old')


def downgrade():
    # 1. Rename current table
    op.rename_table('tomato_variety', '_tomato_variety_old')
    
    # 2. Re-create tomato_variety table with single unique constraint on name
    op.create_table('tomato_variety',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=100), nullable=True),
        sa.Column('size', sa.String(length=100), nullable=True),
        sa.Column('origin', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('fallback_image_url', sa.String(length=255), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('in_stock', sa.Boolean(), server_default='1', nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['owner_id'], ['person.id'], name='fk_tomato_variety_owner_id_person'),
        sa.UniqueConstraint('name')
    )
    
    # 3. Copy data
    op.execute('''
        INSERT INTO tomato_variety (id, name, category, color, size, origin, description, image_url, fallback_image_url, owner_id, in_stock)
        SELECT id, name, category, color, size, origin, description, image_url, fallback_image_url, owner_id, in_stock
        FROM _tomato_variety_old
    ''')
    
    # 4. Drop old table
    op.drop_table('_tomato_variety_old')

