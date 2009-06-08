#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
from time import strftime, localtime
import re

import feedparser
from stripper import *

class Fetcher:
    feed = 'https://github.com/rapidsms.private.atom?token=1e5ad8f275bdd03a163488732863171f'
    items = []

    def tidy(self, item):
        ''' Returns a tidy unicode version of the desired information
            from a feed item. You may need to customize this code, which
            is meant for github newsfeeds. '''
        # remove all html markup
        body = stripHTML(item.content[0].value).strip().replace("&quot;", "\"")
        # replace many whitespaces with one space
        spaces = re.compile('\s+')
        compact_body = re.sub(spaces, " ", body)
        # make date readable
        when = strftime("%a, %d %b %Y %H:%M", item.published_parsed)
        # assemble a pretty string of nuggets from feed item
        pretty = u'  %s  |  %s  |  %s  |  %s' % (item.link, item.title, compact_body, when)
        return pretty

    def fetch(self):
        ''' Parses feed and returns items not found in the 
            items list (i.e., returns new items)'''
        def fresh(i): return i not in self.items
        return filter(fresh, feedparser.parse(self.feed).entries)

    def go(self):
        ''' Returns a list of tidy unicode representations of new feed items. '''
        when = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        print '======== FETCHING FEED (%s) =========' % when
        new_items = []
        for item in self.fetch():
            # add tidy version of item to list
            new_items.append(self.tidy(item))
            # add item to list of old items
            self.items.append(item)
        return new_items

if __name__ == "__main__":
    Fetcher.go(Fetcher())
