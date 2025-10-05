"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-10-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('twofa_secret', sa.String(), nullable=True),
        sa.Column('timezone', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create sd_accounts table
    op.create_table('sd_accounts',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('sd_username', sa.String(), nullable=False),
        sa.Column('sd_token', sa.Text(), nullable=False),
        sa.Column('token_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_success', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('user_id')
    )

    # Create lineups table
    op.create_table('lineups',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('transport', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create user_lineups table
    op.create_table('user_lineups',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('lineup_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('user_id', 'lineup_id')
    )

    # Create stations table
    op.create_table('stations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('callsign', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('affiliate', sa.String(), nullable=True),
        sa.Column('is_hd', sa.Boolean(), nullable=True),
        sa.Column('logo_uri', sa.String(), nullable=True),
        sa.Column('logo_width', sa.Integer(), nullable=True),
        sa.Column('logo_height', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create lineup_stations table
    op.create_table('lineup_stations',
        sa.Column('lineup_id', sa.String(), nullable=False),
        sa.Column('station_id', sa.String(), nullable=False),
        sa.Column('channel', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('lineup_id', 'station_id')
    )

    # Create programs table
    op.create_table('programs',
        sa.Column('program_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('episode_title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('season', sa.Integer(), nullable=True),
        sa.Column('episode', sa.Integer(), nullable=True),
        sa.Column('original_air_date', sa.Date(), nullable=True),
        sa.Column('genres', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('advisories', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('cast', sa.JSON(), nullable=True),
        sa.Column('crew', sa.JSON(), nullable=True),
        sa.Column('md5', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('program_id')
    )
    op.create_index(op.f('ix_programs_title'), 'programs', ['title'])
    op.create_index(op.f('ix_programs_md5'), 'programs', ['md5'])

    # Create schedules table
    op.create_table('schedules',
        sa.Column('station_id', sa.String(), nullable=False),
        sa.Column('program_id', sa.String(), nullable=False),
        sa.Column('start_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_new', sa.Boolean(), nullable=True),
        sa.Column('live', sa.Boolean(), nullable=True),
        sa.Column('premiere', sa.Boolean(), nullable=True),
        sa.Column('finale', sa.Boolean(), nullable=True),
        sa.Column('audio', sa.String(), nullable=True),
        sa.Column('aspect', sa.String(), nullable=True),
        sa.Column('subtitles', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('station_id', 'program_id', 'start_utc')
    )
    op.create_index(op.f('ix_schedules_start_utc'), 'schedules', ['start_utc'])
    op.create_index(op.f('ix_schedules_end_utc'), 'schedules', ['end_utc'])

    # Create images table
    op.create_table('images',
        sa.Column('ref_id', sa.String(), nullable=False),
        sa.Column('program_id', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('aspect', sa.String(), nullable=True),
        sa.Column('uri', sa.String(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('ref_id')
    )
    op.create_index(op.f('ix_images_program_id'), 'images', ['program_id'])

    # Create favourites table
    op.create_table('favourites',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('program_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('user_id', 'program_id')
    )

    # Create rules table
    op.create_table('rules',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('type', sa.Enum('SERIES', 'KEYWORD', 'TEAM', name='ruletype'), nullable=False),
        sa.Column('query', sa.Text(), nullable=True),
        sa.Column('program_id', sa.String(), nullable=True),
        sa.Column('station_ids', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('new_only', sa.Boolean(), nullable=True),
        sa.Column('padding_pre', sa.Integer(), nullable=True),
        sa.Column('padding_post', sa.Integer(), nullable=True),
        sa.Column('keep_last', sa.Integer(), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rules_user_id'), 'rules', ['user_id'])

    # Create notifications table
    op.create_table('notifications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('rule_id', sa.UUID(), nullable=True),
        sa.Column('station_id', sa.String(), nullable=True),
        sa.Column('program_id', sa.String(), nullable=True),
        sa.Column('start_utc', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'])
    op.create_index(op.f('ix_notifications_rule_id'), 'notifications', ['rule_id'])

def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_table('rules')
    op.drop_table('favourites')
    op.drop_table('images')
    op.drop_table('schedules')
    op.drop_table('programs')
    op.drop_table('lineup_stations')
    op.drop_table('stations')
    op.drop_table('user_lineups')
    op.drop_table('lineups')
    op.drop_table('sd_accounts')
    op.drop_table('users')