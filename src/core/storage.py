"""
S3-совместимое хранилище для медиа и документов.

Зачем отдельный слой:
- В dev: MinIO (локальный S3 в Docker)
- В prod: Selectel S3
- Меняется только URL в .env, код тот же

Все файлы (фото, видео, аудио, документы) хранятся в S3,
а в PostgreSQL — только ключ (путь) к файлу.

boto3 — стандартная библиотека AWS для работы с S3.
Работает с любым S3-совместимым хранилищем (MinIO, Selectel, Yandex, и т.д.)
"""

import uuid
from datetime import datetime

import boto3
import structlog
from botocore.config import Config

from src.core.config import settings

logger = structlog.get_logger()


class StorageService:
    """Сервис для работы с S3-хранилищем."""

    def __init__(self):
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(signature_version="s3v4"),
        )
        self._bucket = settings.S3_BUCKET_NAME

    def ensure_bucket(self) -> None:
        """Создать bucket если не существует. Вызывается при старте."""
        try:
            self._client.head_bucket(Bucket=self._bucket)
        except Exception:
            try:
                self._client.create_bucket(Bucket=self._bucket)
                logger.info("s3_bucket_created", bucket=self._bucket)
            except Exception as e:
                logger.error("s3_bucket_create_error", error=str(e))

    def generate_key(self, channel: str, content_type: str, extension: str) -> str:
        """
        Сгенерировать уникальный ключ для файла.

        Формат: {channel}/{year}/{month}/{day}/{uuid}.{ext}
        Пример: telegram/2026/03/17/a1b2c3d4.jpg
        """
        now = datetime.now()
        unique_id = uuid.uuid4().hex[:12]
        return f"{channel}/{now.year}/{now.month:02d}/{now.day:02d}/{unique_id}.{extension}"

    async def upload_bytes(self, key: str, data: bytes, content_type: str = "") -> str:
        """
        Загрузить файл в S3.

        Args:
            key: Путь в bucket (например "telegram/2026/03/17/abc123.jpg")
            data: Содержимое файла (байты)
            content_type: MIME-тип (например "image/jpeg")

        Returns:
            key — тот же ключ, для сохранения в БД
        """
        try:
            extra = {}
            if content_type:
                extra["ContentType"] = content_type

            self._client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=data,
                **extra,
            )
            logger.info("s3_upload_ok", key=key, size=len(data))
            return key
        except Exception as e:
            logger.error("s3_upload_error", key=key, error=str(e))
            raise

    async def download_bytes(self, key: str) -> bytes:
        """Скачать файл из S3."""
        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            return response["Body"].read()
        except Exception as e:
            logger.error("s3_download_error", key=key, error=str(e))
            raise

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """
        Получить временную ссылку на файл (для отображения в UI).

        Args:
            key: Путь к файлу в S3
            expires_in: Время жизни ссылки в секундах (по умолчанию 1 час)
        """
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=expires_in,
        )
