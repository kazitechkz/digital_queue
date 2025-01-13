from redis import Redis

from app.infrastructure.config import app_config


def get_redis_client():
    """
    Создаем экземпляр клиента Redis.
    """
    return Redis(
        host=app_config.redis_host,
        port=app_config.redis_port,
        password=app_config.redis_password,
        db=app_config.redis_db,
        decode_responses=True,
    )


redis_client = get_redis_client()
