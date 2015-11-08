from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import json
import time

HOST = ''
PORT = 80

class MyClientProtocol(WebSocketClientProtocol):
    ROBOT_ID = 11

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        message = payload
        print("Message from Rails is " + message)

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
