import asyncio
import re
from urllib.parse import urlparse, urljoin

from sanic.log import logger
import aiomysql
from sanic import Sanic, Request

from config import BalancerConfig
from repo import CDNConfigRepository

video_server_name_pattern = re.compile(r"^(s\d{1,3})\..+\.\w+$")


def prepare_cdn_video_url(video_url: str, cdn_host: str = 'cdn.example.ru') -> str:
    a = urlparse(video_url)
    b = video_server_name_pattern.findall(a.netloc)
    if not b:
        raise ValueError('server name not found')
    return urljoin(f'https://{cdn_host}', f'{b[0]}/{a.path}')


async def connect_to_db(application: Sanic):
    application.ctx.db_connection = await aiomysql.connect(
        host=application.config.MS_DB_HOST,
        port=application.config.MS_DB_PORT,
        user=application.config.MS_DB_USER,
        password=application.config.MS_DB_PASS,
        db=application.config.MS_DB_NAME,
        autocommit=True,
    )


async def close_db_connection(application: Sanic):
    application.ctx.db_connection.close()


async def init_config(application: Sanic) -> None:
    application.update_config(BalancerConfig)


async def update_cdn_config(application: Sanic) -> None:
    default_cdn_config = await application.ctx.cdn_config_repo.search__cdn_settings__by_location()
    application.update_config(default_cdn_config.settings)


async def get_cdn_config_repo(request: Request) -> CDNConfigRepository:
    return request.app.ctx.cdn_config_repo


async def ping_cdn():
    while True:
        await asyncio.sleep(5)
        ...
        logger.info('Check CDN')
