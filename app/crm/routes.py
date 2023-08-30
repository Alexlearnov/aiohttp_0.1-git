from aiohttp.web import Application
from app.crm.views import index         # создали в ручную

def setup_routes(app: Application):
    app.router.add_get("/index", index)     # функция по руту вызывает нашу функцмю представления страницы