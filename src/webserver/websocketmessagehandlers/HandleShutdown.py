
from AbstractHandler import AbstractHandler
import logging
logger = logging.getLogger(__name__)

class HandleShutdown( AbstractHandler ):

    def canHandle( self, message ):
        return 'SHUTDOWN' == message['type'].upper()


    def handle( self, message):

        self.AC3.shutdown()

    def stopHandling( self ):
        pass