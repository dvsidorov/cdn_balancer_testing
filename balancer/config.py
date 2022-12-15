import os

from sanic import Blueprint
from sanic import json
from sanic import Request
from sanic_ext import validate

from models import CDNConfig
from repo import CDNConfigRepository
from auth import protected


class BalancerConfig:
    KEEP_ALIVE = True

    MS_DB_HOST = os.getenv('BALANCER_MS_DB_HOST', 'db-mysql')
    MS_DB_PORT = os.getenv('BALANCER_MS_DB_PORT', 3306)
    MS_DB_NAME = os.getenv('BALANCER_MS_DB_NAME', 'balancer_db')
    MS_DB_USER = os.getenv('BALANCER_MS_DB_USER', 'balancer')
    MS_DB_PASS = os.getenv('BALANCER_MS_DB_PASS', 'balancer')

    SECRET = os.getenv('BALANCER_SECRET', 'KEEP_IT_SECRET_KEEP_IT_SAFE')


config = Blueprint("config", url_prefix="/config")


@config.route('/', methods=['POST'])
@protected
@validate(json=CDNConfig)
async def config_create(request: Request,
                        body: CDNConfig,
                        cdn_config_repo: CDNConfigRepository):
    await cdn_config_repo.insert__cdn_settings(location=body.location, settings=body.settings)
    return json('OK', status=201)


@config.route('/', methods=['PUT'])
@protected
@validate(json=CDNConfig)
async def config_update(request: Request,
                        body: CDNConfig,
                        cdn_config_repo: CDNConfigRepository):
    await cdn_config_repo.update__cdn_settings__by_location(location=body.location, settings=body.settings)
    return json('OK', status=200)


@config.route('/', methods=['DELETE'])
@protected
@validate(json=CDNConfig)
async def config_delete(request:Request,
                        body: CDNConfig,
                        cdn_config_repo: CDNConfigRepository):
    await cdn_config_repo.delete__cdn_settings__by_location(location=body.location)
    return json('OK', status=200)
