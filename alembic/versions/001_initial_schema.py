"""initial schema

Revision ID: 001_initial
Revises:
Create Date: 2026-03-22

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == "sqlite"
    ts_default = sa.text("(datetime('now'))") if is_sqlite else sa.text("now()")
    bool_false = sa.text("0") if is_sqlite else sa.text("false")

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=ts_default,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["parent_id"], ["categories.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_slug"), "categories", ["slug"], unique=True)

    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tags_slug"), "tags", ["slug"], unique=True)

    op.create_table(
        "glossary_entries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("term", sa.String(length=500), nullable=False),
        sa.Column("definition", sa.Text(), nullable=False),
        sa.Column("slug", sa.String(length=500), nullable=False),
        sa.Column("related_terms", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=ts_default,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_glossary_entries_slug"), "glossary_entries", ["slug"], unique=True)

    op.create_table(
        "seo_records",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("page_url", sa.String(length=2048), nullable=False),
        sa.Column("indexed", sa.Boolean(), nullable=False, server_default=bool_false),
        sa.Column("last_crawled", sa.DateTime(timezone=True), nullable=True),
        sa.Column("issues", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_seo_records_page_url"), "seo_records", ["page_url"], unique=True)

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("slug", sa.String(length=500), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
            server_default=sa.text("'draft'"),
        ),
        sa.Column("seo_title", sa.String(length=500), nullable=True),
        sa.Column("seo_description", sa.Text(), nullable=True),
        sa.Column("featured_image", sa.String(length=2048), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=ts_default,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=ts_default,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_articles_slug"), "articles", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_articles_slug"), table_name="articles")
    op.drop_table("articles")
    op.drop_index(op.f("ix_seo_records_page_url"), table_name="seo_records")
    op.drop_table("seo_records")
    op.drop_index(op.f("ix_glossary_entries_slug"), table_name="glossary_entries")
    op.drop_table("glossary_entries")
    op.drop_index(op.f("ix_tags_slug"), table_name="tags")
    op.drop_table("tags")
    op.drop_index(op.f("ix_categories_slug"), table_name="categories")
    op.drop_table("categories")
