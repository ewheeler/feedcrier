#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
#import web
import irclib
from gitirc import *
import time


class FwdIRC():
    def __init__(self, host="irc.freenode.net", port=6667,
                        nick="rapidsms-news", channels=["#rapidsms"]):
        self.host = host
        self.port = port
        self.nick = nick 
        self.channels = channels 
        self.irc = irclib.IRC()
        self.message_waiting = []

    def start(self):
        self.server = self.irc.server()
        self.server.connect(self.host, self.port, self.nick)

        for channel in self.channels:
            print("Joining %s on %s" % (channel, self.host))
            self.server.join(channel)

        gi = GitIRC()
        self.run(gi)

    def run(self, gi):
        self.message_waiting = GitIRC.go(gi)
        if self.message_waiting:
            while len(self.message_waiting) > 0:
                msg = self.message_waiting.pop()
                self.outgoing(msg)
                self.irc.process_once(timeout=5.0)
        time.sleep(30)
        self.run(gi)
        
    def outgoing (self, msg):
        channel = self.channels[0]
        self.server.privmsg(channel, msg)

if __name__ == "__main__":
    #web.run(urls, globals())
    FwdIRC.start(FwdIRC())
    while True:
        time.sleep(1)
