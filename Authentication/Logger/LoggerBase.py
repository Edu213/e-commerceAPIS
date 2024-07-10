import logging as log

def configure_logger():
    """
    Configures the logger with specified settings.

    Sets the logging level to DEBUG, and defines a custom format for log messages.
    Additionally, adds two handlers: one for writing log messages to a file named 'zonama-webservices',
    and another for printing log messages to the console.

    Args:
        None

    Returns:
        None
    """

    log.basicConfig(
        level=log.DEBUG,
        format='%(asctime)s: %(levelname)s [%(filename)s: %(lineno)s] %(message)s',
        datefmt='%I:%M:%S %p',
        handlers=[
            log.FileHandler('zonama-webservices'),
            log.StreamHandler()
        ]
    )

if __name__ == '__main__':
    configure_logger()
    
    # Example log messages
    log.debug('Test debug')
    log.info('Test info')
    log.warning('Test warning')
    log.error('Test error')
    log.critical('Test critical')
