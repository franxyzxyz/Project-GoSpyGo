###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

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
    ROBOT_ID = 11

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        # message is string
        message = payload

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
