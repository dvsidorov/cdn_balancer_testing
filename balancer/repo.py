import json
from typing import Any, Dict

from aiomysql import Connection
from aiomysql import DictCursor

from models import CDNConfig

QUERY__SEARCH__CDN_CONFIG__BY_LOCATION = """
    select location,
        settings
    from cdn_settings
    where location = %(location)s;
"""

QUERY__INSERT__CDN_CONFIG = """
    insert ignore into cdn_settings (location, settings)
    values (%(location)s, %(settings)s);
"""

QUERY__UPDATE__CDN_CONFIG__BY_LOCATION = """
    update cdn_settings
    set settings = %(settings)s
    where location = %(location)s;
"""

QUERY__DELETE__CDN_CONFIG__BY_LOCATION = """
    delete
    from cdn_settings
    where location = %(location)s;
"""


class MySQLBaseRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    @property
    def connection(self) -> Connection:
        return self._conn

    async def _fetch_row(self, query: str, *query_params: Any) -> Dict:
        async with self._conn.cursor(DictCursor) as cur:
            await cur.execute(query, *query_params)
            return await cur.fetchone()

    async def _execute(self, query: str, *query_params: Any) -> None:
        async with self._conn.cursor() as cur:
            await cur.execute(query, *query_params)


class CDNConfigRepository(MySQLBaseRepository):

    async def insert__cdn_settings(self, location: str, settings: dict):
        await self._execute(QUERY__INSERT__CDN_CONFIG, dict(location=location, settings=json.dumps(settings)))

    async def update__cdn_settings__by_location(self, location: str, settings: dict):
        await self._execute(QUERY__UPDATE__CDN_CONFIG__BY_LOCATION,
                            dict(location=location, settings=json.dumps(settings)))

    async def delete__cdn_settings__by_location(self, location: str):
        await self._execute(QUERY__DELETE__CDN_CONFIG__BY_LOCATION, dict(location=location))

    async def search__cdn_settings__by_location(self, location: str = 'default'):
        cdn_settings = await self._fetch_row(QUERY__SEARCH__CDN_CONFIG__BY_LOCATION, dict(location=location))
        if not cdn_settings:
            raise EntityListDoesNotExist(f"Config CDN settings not found")
        return CDNConfig(**cdn_settings)


class EntityListDoesNotExist(Exception):
    pass
