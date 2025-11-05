import logging

def setup_logging():
    # Basic logging ( not appropriate for big applications )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
