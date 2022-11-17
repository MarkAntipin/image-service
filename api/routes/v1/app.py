from backend_utils.server import Router, compile_routers

from api.routes.v1.handlers import images

routers = [
    Router(router=images.router, tags=['Images'], prefix='/images'),
]


v1_routers = compile_routers(
    routers=routers,
    root_prefix='/api/v1'
)
