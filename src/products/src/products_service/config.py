# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import os
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.boto3 import Boto3Instrumentation
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DDB_TABLE_PRODUCTS              = os.environ.get('DDB_TABLE_PRODUCTS', 'products')
    DDB_TABLE_CATEGORIES            = os.environ.get('DDB_TABLE_CATEGORIES', 'categories')
    DDB_TABLE_PERSONALISED_PRODUCTS = os.environ.get('DDB_TABLE_PERSONALISED_PRODUCTS', 'personalisedproducts')
    CACHE_PERSONALISED_PRODUCTS     = os.environ.get('CACHE_PERSONALISED_PRODUCTS', "True") == "True"
    IMAGE_ROOT_URL                  = os.environ.get('IMAGE_ROOT_URL')
    WEB_ROOT_URL                    = os.environ.get('WEB_ROOT_URL')
    DATA_DIR                        = os.environ.get('DATA_DIR', '/src/data')
    CATEGORY_DATA                   = os.path.join(DATA_DIR, os.environ.get('CATEGORY_DATA', "categories.yaml"))
    PRODUCT_DATA                    = os.path.join(DATA_DIR, os.environ.get('PRODUCT_DATA', "products.yaml"))
    AWS_DEFAULT_REGION              = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    COGNITO_USER_POOL_ID            = os.environ.get('COGNITO_USER_POOL_ID', 'xxxx')

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG                           = True
    DDB_ENDPOINT_OVERRIDE           = os.environ.get('DDB_ENDPOINT_OVERRIDE')

class ProductionConfig(Config):
    DEBUG                           = False

    @staticmethod
    def init_app(app):
        # Set up OpenTelemetry
        resource = Resource(attributes={
            SERVICE_NAME: "Products Service"
        })
        
        # Initialize tracing and an exporter that can send data to AWS X-Ray
        provider = TracerProvider(resource=resource)
        processor = BatchSpanProcessor(OTLPSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        
        # Instrument Flask
        FlaskInstrumentor().instrument_app(app)
        
        # Instrument requests library
        RequestsInstrumentor().instrument()
        
        # Instrument AWS SDK
        Boto3Instrumentation().instrument()

config = {
    'Development': Development,
    'Production': ProductionConfig
}