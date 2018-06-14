#!/usr/bin/python
"""WebSocket CLI interface."""
import sys
import json
from twisted.application import strports # pip install twisted
from twisted.application import service
from twisted.internet    import protocol
from twisted.python      import log
from twisted.web.server  import Site
from twisted.web.static  import File

from txws import WebSocketFactory # pip install txws
import redis
import requests
redisServer = redis.StrictRedis()

class Protocol(protocol.Protocol):
    def connectionMade(self):
        from twisted.internet import reactor
        log.msg("launch a new process on each new connection")
        self.pp = ProcessProtocol()
        self.pp.factory = self
        #reactor.spawnProcess(self.pp, sys.executable,
         #                    [sys.executable, '-u', 'client.py'])
    def dataReceived(self, data):
        self._send(data)
        self.pp._sendback(data)
        response = json.loads(data)
        headers = {'Content-type': 'application/json'}
        url = 'http://localhost:8031/realtime_stats/'
        res = requests.post(url, json=response, headers=headers)
        if res.status_code!=200:
            log.msg("failed request to django server")

    def connectionLost(self, reason):
        return
        #self.pp.transport.loseConnection()

    def _send(self, data):
        self.transport.write(data) # send back


class ProcessProtocol(protocol.ProcessProtocol):
    def connectionMade(self):
        log.msg("connectionMade")
    def outReceived(self, data):
        log.msg("send stdout back %r" % data)
        self._sendback(data)
    def errReceived(self, data):
        log.msg("send stderr back %r" % data)
        self._sendback(data)
    def processExited(self, reason):
        log.msg("processExited")
    def processEnded(self, reason):
        log.msg("processEnded")

    def _sendback(self, data):
        self.factory._send(data)


application = service.Application("ws-cli")

_echofactory = protocol.Factory()
_echofactory.protocol = Protocol
strports.service("tcp:8081:interface=0.0.0.0",
                 WebSocketFactory(_echofactory)).setServiceParent(application)
