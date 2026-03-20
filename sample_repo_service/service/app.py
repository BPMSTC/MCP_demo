"""Service entry point for the sample service repository."""

from config.settings import load_settings


def main() -> None:
    settings = load_settings()
    print(f"Starting {settings['service_name']} on port {settings['port']}")


if __name__ == "__main__":
    main()
