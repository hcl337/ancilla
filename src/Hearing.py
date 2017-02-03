from __future__ import division

import logging
import json
import time
import os
import copy
from threading import Timer, Thread

logger = logging.getLogger(__name__)


if 'raspberrypi' in os.uname()[1]:
    isRaspberryPi = True
else:
    import speech_recognition
    isRaspberryPi = False

class Hearing:
    '''
    The main class which represents the output of the system

    '''

    # Reference
    speech = None

    isEnabled = False

    recognizer = None

    importantWords = []

    callbacks = []

    MIN_TIME_AFTER_I_SPEAK_TO_LISTEN = 3


    def __init__(self, speech):
    	logger.info("Creating Hearing...")

        self.recognizer = speech_recognition.Recognizer()

        self.speech = speech

    def enable( self ):

        if self.isEnabled:
            raise Exception("Speeking is already enabled")

        self.isEnabled = True

        hearingThread = Thread(target=self.__hearingLoop)
        # Make sure it dies if the whole app dies
        hearingThread.setDaemon(True)
        # Need to actually start it running where it calls the update function
        hearingThread.start()



    def disable( self ):
    	isEnabled = False


    def subscribe( self, callback ):
        self.callbacks.append(callback)

    def addImportantWord( self, word ):
        self.importantWords.append( (word, 0.01) )


    def __hearingLoop( self ):

        while self.isEnabled:

            phrase = self.__listen( )

            logger.info("TimeSince AC3 last spoke:" + str(speech.timeSinceLastSpoke()))
            
            if speech.timeSinceLastSpoke() < MIN_TIME_AFTER_I_SPEAK_TO_LISTEN:
                logger.info("Heard something, but was speaking so it was AC3 talking: " + phrase)
                continue

            logger.info("I heard: " + phrase)
            
            for fn in self.callbacks:
                fn(phrase)

    
    def __listen( self ):

        logger.info("Starting to listen")
        with speech_recognition.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            logger.info("Stopped Listening")
        try:
            return self.recognizer.recognize_sphinx(audio )#, keyword_entries=self.importantWords )
            #return self.recognizer.recognize_google_cloud(audio, credentials_json='{"credentials_json":"AIzaSyBz2YFvh18iKTIei2s50Gk7XwDco1hxObo"}')
            # or: return recognizer.recognize_google(audio)
        except speech_recognition.UnknownValueError:
            print("Could not understand audio")
        except speech_recognition.RequestError as e:
            print("Recog Error; {0}".format(e))

        return ""
