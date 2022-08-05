def setup_logging(logger, log_level, console=True):
    """ Function to help setup logging across all modules """

    # Set log level
    logger.setLevel(log_level)

    # Define Formatting: 
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

    # Log Output to CLI: 
    if console is True:
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger
