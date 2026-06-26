import os
import yaml 
import logging
import logging_loki
from fastapi import FastAPI, Request
from warehouse.routers import items, orders
from warehouse.db import init_db
from contextlib import asynccontextmanager
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
# добавляем трейсы
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor

@asynccontextmanager
async def lifespan(app: FastAPI):
  await init_db()
  yield

requests_by_ip = Counter("requests_by_ip",
                         "amount of requests by ip",
                         labelnames=["client_ip"]
)



logger = logging.getLogger("warehouse_logger")
logger.setLevel(logging.INFO) # to show not only errors and warns
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

if os.getenv("CI") != "true":
    handler = logging_loki.LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "fastapi_warehouse"},
    version="1", # version is now required
)
    logger.addHandler(handler)

app = FastAPI(lifespan=lifespan)
# сбор метрик для прометеуса
Instrumentator().instrument(app).expose(app)

# настройка трейсов opentelemetry
resource = Resource.create({"service.name": "fastapi_warehouse"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# экспортер собранных трейсов в контейнер с Tempo
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4318/v1/traces")

# отправляем данные пачками
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)

# добавляем отслеживание HTTP и SQL запросов
FastAPIInstrumentor.instrument_app(app)
SQLite3Instrumentor().instrument()

@app.get("/")
async def main_page():
    return {"desc": "here is warehouse app main page"}

@app.middleware("http")
async def get_clien_ip(request: Request, call_next):
    if request.client:
        client_ip = request.client.host
    else:
        client_ip = "unknown"

    requests_by_ip.labels(client_ip=client_ip).inc()

    logger.info(f"Connection recieved: {request.method} {request.url.path} \
                with client ip {client_ip}",
                extra={"tags": {
                    "endpoint": request.url.path,
                    "method": request.method,
                    "ip": client_ip
                }})

    response = await call_next(request)

    if response.status_code >= 400:
        logger.error(f"Connection failed on endpoint {request.url.path} \
                     with status {response.status_code}, \
                     client ip {client_ip}",
                     extra={"tags":{
                        "endpoint": request.url.path,
                        "method": request.method,
                        "response_code": response.status_code,
                        "ip": client_ip
                     }})
    else:
        logger.info(f"Connection successful on endpoint {request.url.path} \
                     client ip {client_ip}",
                     extra={"tags":{
                        "endpoint": request.url.path,
                        "ip": client_ip,
                        "response_code": response.status_code,
                     }})

    return response

def my_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    with open("openapi.yml", "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = my_openapi

app.include_router(items.router)
app.include_router(orders.router)

