import logging as log 

log.basicConfig(level=log.WARNING,
                format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                datefmt='%I:%M:%S %P',
                handlers = [
                    log.FileHandler('ProductManagementApi.log'),
                    log.StreamHandler()
                ])

if __name__ == '__main__':
    """
    Main entry point for testing different logginf levels
    
    This script demonstrates the logging levels available in the logging module:
    DEBUG, INFO, WARNING, ERROR, and CRITICAL. The configuration logs messages to  both a file 
    ProductManagementApi.log and the console
    """ 

    log.debug('Message level: DEBUG')
    log.info('Message level: INFO')
    log.warning('Message level: WARNING')
    log.error('Message level: ERROR')
    log.critical('Message level: CRITICAL')
