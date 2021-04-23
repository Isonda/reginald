import pytz

from datetime import datetime
from redis import StrictRedis

from log_handler import get_logger


client = StrictRedis(host="172.17.0.1")
logger = get_logger(__name__)
TIME_FORMAT = "%Y-%m-%d %I:%M %p"
TIMEZONE = pytz.timezone("America/Los_Angeles")


async def update_last_seen(user_id: str) -> bool:
    now = datetime.now(TIMEZONE).strftime(TIME_FORMAT)
    logger.info(now)
    return client.set(user_id, now)


async def get_last_seen(user_id: str) -> str:
    return client.get(user_id)
