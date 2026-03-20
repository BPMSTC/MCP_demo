"""Background task scheduler for periodic jobs."""

from time import sleep


def run_scheduler() -> None:
    jobs = ["sync-customers", "archive-events", "refresh-cache"]
    for job in jobs:
        print(f"Running job: {job}")
        sleep(0.1)


if __name__ == "__main__":
    run_scheduler()
