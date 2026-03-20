"""Runtime configuration for Service Hub sample."""


def load_settings() -> dict[str, str | int]:
    return {
        "service_name": "service-hub-api",
        "port": 8081,
        "environment": "demo",
    }
