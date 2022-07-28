from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    """Public Static Storage of DO Spaces."""

    location = 'static'
    default_acl = 'public-read'


class MediaRootS3Boto3Storage(S3Boto3Storage):
    """Public Media Storage of DO Spaces."""

    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
