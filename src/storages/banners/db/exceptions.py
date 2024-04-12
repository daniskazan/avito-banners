class BannerNotFoundException(Exception):
    pass


class BannersConsistenceBrokenException(Exception):
    pass


class BannerWithSuchTagAndFeatureAlreadyExists(Exception):
    pass


class TagNotFoundException(Exception):
    pass


class FeatureNotFoundException(Exception):
    pass
