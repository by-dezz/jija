from jija import router
from .views import *


routes = [
    router.Endpoint('/', IndexView),
]