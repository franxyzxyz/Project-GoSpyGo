# the code below is adapted from
# https://github.com/crossbario/autobahn-python/blob/master/examples/twisted/websocket/echo/client.py
# license provided in the paragraphs preceding
################################################################################

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import grovepi
import json
import time
import atexit
import robotcalls

HOST = 'pacific-mountain-2023.herokuapp.com'
PORT = 80

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        # message is string
        message = payload

        # this is the ROBOT_ID, which matches the user_id defined in postgres
        # change for different users/robots
        # logic should be refactored in future versions
        ROBOT_ID = 1

        print("Message from Rails is " + message)

        # string -> json
        # IMPT: all keys AND strings converted to unicode by json.loads()
        request = json.loads(message)

        # refer to messages.json for message format
        # only process message if request came from OWN USER (add logic)
        if (request[u'requester'] == u'user') and (request[u'user_id'] == ROBOT_ID):
            requestUnicodeKey = request[u'sensor_type']
            result = robotcalls.dispatcher[requestUnicodeKey]()
            # # update request with robot reading
            request[u'reading'] = result
            request[u'requester'] = "robot"

            # # dumps json -> string
            reply = json.dumps(request)
            self.sendMessage(reply)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://" + HOST + ":" + str(PORT), debug=True)
    factory.protocol = MyClientProtocol

    reactor.connectTCP(HOST, PORT, factory)
    reactor.run()
