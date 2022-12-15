from itertools import cycle

from sanic import Sanic
from sanic.log import logger
from sanic.response import redirect
from sanic_ext import validate

from auth import login
from config import config
from helpers import prepare_cdn_video_url, connect_to_db, close_db_connection, update_cdn_config, init_config, \
    get_cdn_config_repo, is_cdn_host
from models import BalancerParams
from repo import CDNConfigRepository

app = Sanic("balancer")
app.blueprint(login)
app.blueprint(config)


@app.before_server_start
async def init_server(application: Sanic, _):
    logger.info('Initialize server started')
    await init_config(application)
    await connect_to_db(application)

    application.ctx.is_cdn_host = is_cdn_host(application)
    application.ctx.cdn_config_repo = CDNConfigRepository(application.ctx.db_connection)
    application.ext.add_dependency(CDNConfigRepository, get_cdn_config_repo)

    await update_cdn_config(application)

    # await application.add_task(ping_cdn)
    logger.info('Initialize server stopped')


@app.before_server_stop
async def stop_server(application: Sanic, _):
    logger.info('Stop server started')
    await close_db_connection(application)
    logger.info('Stop server ended')


@app.route('/')
@validate(query=BalancerParams)
async def handler(request, query: BalancerParams):
    if not next(request.app.ctx.is_cdn_host):
        return redirect(query.video, status=301)
    return redirect(prepare_cdn_video_url(query.video, request.app.config.CDN_HOST), status=301)
