from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.customers import router as customers_router
from app.api.health import router as health_router
from app.api.products import router as products_router
from app.api.test_orders import router as test_orders_router
from app.api.test_plans import router as test_plans_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(customers_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(test_orders_router, prefix="/api")
app.include_router(test_plans_router, prefix="/api")
