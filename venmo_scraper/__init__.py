import logging

__version__ = '0.1.0'

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    level=logging.INFO)
