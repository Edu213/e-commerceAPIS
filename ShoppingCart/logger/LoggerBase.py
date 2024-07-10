import logging as log

log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s: %(levelname)s [%(filename)s: %(lineno)s] %(message)s',
    datefmt='%I:%M:%S %p',
    handlers=[
        log.FileHandler('logger/cart_api.log'),
        log.StreamHandler()
    ]
)

pymongo_logger = log.getLogger('pymongo')
pymongo_logger.setLevel(log.WARNING)

if __name__ == '__main__':
    log.debug('Test debug')
    log.info('Test info')
    log.warning('Test warning')
    log.error('Test error')
    log.critical('Test critical')