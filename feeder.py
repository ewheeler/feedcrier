#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
import irclib
from fetcher import *
import time
import math

MAX = 160

class FeedCrier():
    def __init__(self, host="irc.freenode.net", port=6667,
                        nick="rapidsms-news", channels=["#mepemepe"], frequency=30):
        self.host = host
        self.port = port
        self.nick = nick 
        self.channels = channels 
        self.frequency = frequency
        self.irc = irclib.IRC()
        self.message_waiting = []

    def start(self):
        ''' Instantiates Fetcher and starts running things '''
        fetcher = Fetcher()
        self.run(fetcher)

    def connect(self):
        ''' Connects to IRC channels '''
        self.server = self.irc.server()
        try:
            self.server.connect(self.host, self.port, self.nick)
            for channel in self.channels:
                print("Joining %s on %s" % (channel, self.host))
                self.server.join(channel)
                time.sleep(10)
        except Exception, e:
            print e

    def run(self, fetcher):
        ''' Checks for new items, connects to IRC channel and sends items
            whenever they are found '''
        while True:
            self.message_waiting = Fetcher.go(fetcher)
            if self.message_waiting:
                print('%d new items' % len(self.message_waiting))
                # connect to channel if we have new feed items
                self.connect()
                while len(self.message_waiting) > 0:
                    # send each item and pause to prevent flooding
                    msg = self.message_waiting.pop()
                    self.outgoing(msg)
                    self.irc.process_once(timeout=5.0)
                print("Leaving %s" % (self.host))
                self.server.disconnect()
            time.sleep(self.frequency)
        
    def outgoing(self, msg):
        ''' Queues and sends item to IRC channel, chunking if necessary '''
        #TODO support sending to several channels
        channel = self.channels[0]

        #TODO should we remove linebreaks or send pieces separately?
        msg = msg.replace("\n", " ")

        print(msg + ' (' + str(len(msg)) + ')')
        if len(msg) > MAX:
            # split into several messages to send separately
            # if its longer than MAX
            for chunk in self.chunk(msg):
                self.server.privmsg(channel, chunk)
                self.irc.process_once(timeout=5.0)
        else:
            self.server.privmsg(channel, msg)

    def chunk(self, msg):
        ''' Splits a message into n chunks no larger than MAX '''
        chunks = []
        num_chunks = int(math.ceil(len(msg)/float(MAX)))
        print(num_chunks)
        for n in range(num_chunks):
            chunks.append(msg[(n*MAX):((n+1)*MAX)])
        return chunks

if __name__ == "__main__":
    FeedCrier.start(FeedCrier())
    while True:
        time.sleep(1)
