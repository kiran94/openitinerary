import logging
import os

from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry._logs import get_logger_provider, set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.grpc import GrpcAioInstrumentorClient, GrpcAioInstrumentorServer
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from openitinerary.version import __version__


def setup():
    resource = Resource.create(
        {
            "service.name": "oi-adapter",
            "service.version": __version__,
        }
    )

    EXPORT_INTERVAL_MS = int(os.environ.get("OTEL_EXPORTER_INTERVAL_MS", "15_000"))
    LOGGING_LEVEL = os.environ.get("OI_ADAPTER_LOGGING_LEVEL", "INFO").upper()
    LOGGING_LEVEL = logging.getLevelNamesMapping()[LOGGING_LEVEL]

    # Tracing
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    if LOGGING_LEVEL == logging.DEBUG:
        trace_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(trace_provider)

    # Metrics
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter(), export_interval_millis=EXPORT_INTERVAL_MS)],
    )
    metrics.set_meter_provider(meter_provider)

    # Logs
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    logger_handler = LoggingHandler(logger_provider=logger_provider)

    root_logger = logging.getLogger()
    root_logger.setLevel(LOGGING_LEVEL)
    root_logger.addHandler(logger_handler)
    set_logger_provider(logger_provider)


def setup_libraries(app: FastAPI):
    FastAPIInstrumentor.instrument_app(app)
    HTTPXClientInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    GrpcAioInstrumentorServer().instrument()
    GrpcAioInstrumentorClient().instrument()


def shutdown():
    metrics.get_meter_provider().shutdown()
    trace.get_tracer_provider().shutdown()
    get_logger_provider().shutdown()
