# Project for testing QDrant vector db.

This project embed memories and save into QDrant.
There is an option to search and delete the memories.

# Observability

This project uses Open Telemetry in order to enable Distributed Tracing for the app.
https://realpython.com/fastapi-opentelemetry/
Observability with OTEL is based on 3 concepts:
https://opentelemetry.io/docs/concepts/observability-primer/
logs, traces and metrics
Logs are timestamped messages from the system.
Traces are used to observe the path taken by a request. Traces are composed one span or a chain of spans. 
    Spans are more structured messages, which contain logs and a metadata. 
Metrics enable aggregating application information such as number of calls or response times.

Modern FastAPI already brings everything required for opentelemetry, only variable setting is required for configuring otel endpoints