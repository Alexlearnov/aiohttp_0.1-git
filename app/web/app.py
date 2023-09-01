from aiohttp.web import Application as aiohttp_Application, run_app as aiohttp_run_app
from aiohttp.web import View as aiohttp_View, Request as siohttp_Request
from app.web.routes import setup_routes
from app.store.crm.accessor import CrmAccessor
from typing import Optional
from app.store import setup_accessors
from aiohttp_apispec import setup_aiohttp_apispec
from .middlewares import setup_middlewares
from .config import Config, setup_config

class Application(aiohttp_Application):
    config: Optional[Config] = None
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = None

class Request(siohttp_Request):
    @property
    def app(self) -> Application:
        return super().app()

class View(aiohttp_View):
    @property
    def request(self) -> Request:
        return super().request

app = Application()

def run_app():
    setup_config(app)
    setup_routes(app)
    setup_aiohttp_apispec(app, title="CRM Application", url="/docs/json", swagger_path="/docs")  # лучше после роутов так как сетапится с помощью роутов
    setup_middlewares(app)
    setup_accessors(app)
    aiohttp_run_app(app)