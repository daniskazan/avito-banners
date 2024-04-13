import datetime as dt
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint, func, orm, types


class BaseORMModel(orm.DeclarativeBase):
    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=func.now())
    updated_at: orm.Mapped[dt.datetime] = orm.mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class BannerORM(BaseORMModel):
    __tablename__ = "banners"

    content: orm.Mapped[dict] = orm.mapped_column(types.JSON)
    is_active: orm.Mapped[bool] = orm.mapped_column(default=False)
    feature_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("features.id"))

    feature: orm.Mapped["FeatureORM"] = orm.relationship(  # noqa
        lazy="joined", back_populates="banners"
    )
    tags: orm.Mapped[list["TagORM"]] = orm.relationship(  # noqa
        lazy="joined",
        back_populates="banners",
        secondary="banners_tags",
        cascade="all, delete",
        passive_deletes=True,
    )
    versions: orm.Mapped[list["BannerVersionHistory"]] = orm.relationship(
        lazy="joined", back_populates="banner"
    )

    def __repr__(self):
        return f"BannerORM ID-{self.id}"


class TagORM(BaseORMModel):
    __tablename__ = "tags"

    tag_name: orm.Mapped[str]

    banners: orm.Mapped[list["BannerORM"]] = orm.relationship(
        lazy="joined",
        back_populates="tags",
        secondary="banners_tags",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"TagORM ID-{self.id}"


class FeatureORM(BaseORMModel):
    __tablename__ = "features"

    feature_name: orm.Mapped[str]

    banners: orm.Mapped[list["BannerORM"]] = orm.relationship(
        "BannerORM", lazy="joined", back_populates="feature"
    )

    def __repr__(self):
        return f"FeatureORM ID-{self.id}"


class BannerTagORM(BaseORMModel):
    """
    m2m banners-tags association table;
    """

    __tablename__ = "banners_tags"
    __table_args__ = (
        UniqueConstraint("banner_id", "tag_id", name="banner_id_tag_id_uniq"),
    )
    banner_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("banners.id", ondelete="CASCADE"),
    )
    tag_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
    )

    banner: orm.Mapped["BannerORM"] = orm.relationship(
        lazy="joined", cascade="all, delete"
    )
    tag: orm.Mapped["TagORM"] = orm.relationship(lazy="joined", cascade="all, delete")

    def __repr__(self):
        return f"BannerTagORM ID-{self.id}"


class BannerVersionHistory(BaseORMModel):
    __tablename__ = "banner_version_history"

    version: orm.Mapped[uuid.UUID] = orm.mapped_column(default=uuid.uuid4)
    banner_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("banners.id"))

    tag_ids: orm.Mapped[list[int]] = orm.mapped_column(types.ARRAY(types.INTEGER))
    feature_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("features.id"))
    content: orm.Mapped[dict] = orm.mapped_column(types.JSON)

    banner: orm.Mapped["BannerORM"] = orm.relationship(back_populates="versions")
