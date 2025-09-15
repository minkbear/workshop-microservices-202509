# main.py
import os
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Import the OTLP Exporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Import Prometheus Instrumentator
from prometheus_fastapi_instrumentator import Instrumentator

# Instrument psycopg2 for database tracing
import psycopg2
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
Psycopg2Instrumentor().instrument()


# Create an OTLPSpanExporter
# This will send traces to the OTel Collector at the specified endpoint.
# The default endpoint is http://localhost:4318/v1/traces, which we'll use.
# read from environment variable or config in real scenarios
trace_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
otlp_exporter = OTLPSpanExporter(
    endpoint=trace_endpoint
)

provider = TracerProvider()
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)


@app.get("/")
def read_root():
    return {"message": "Hello, Python service"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Get data from postgresql database with psycopg2
@app.get("/articles")
def read_articles():
    try:
        conn = psycopg2.connect(
            dbname="demo",
            user="user",
            password="password",
            host="db",
            port="5432",
            sslmode="disable"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        articles = cursor.fetchall()
    except psycopg2.Error as e:
        return {"error": f"Database error: {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return {"articles": articles}