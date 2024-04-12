import datetime as dt

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
        lazy="joined", back_populates="banners", secondary="banners_tags"
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
        ForeignKey("banners.id"),
    )
    tag_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey("tags.id"),
    )

    banner: orm.Mapped["BannerORM"] = orm.relationship(lazy="joined")
    tag: orm.Mapped["TagORM"] = orm.relationship(lazy="joined")

    def __repr__(self):
        return f"BannerTagORM ID-{self.id}"
