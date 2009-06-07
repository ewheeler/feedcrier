#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
import feedparser
from stripper import *

class Fetcher:
    feed = 'https://github.com/rapidsms.private.atom?token=1e5ad8f275bdd03a163488732863171f'
    items = []

    def tidy(self, item):
        ''' Returns a tidy unicode version of the desired information
            from a feed item. You may need to customize this code, which
            is meant for github newsfeeds. '''
        body = stripHTML(item.content[0].value).strip().replace("&quot;", "\"")
        pretty = u'  %s  |  %s  ' % (item.title, body)
        return pretty

    def fetch(self):
        ''' Parses feed and returns items not found in the 
            items list (i.e., returns new items)'''
        def fresh(i): return i not in self.items
        return filter(fresh, feedparser.parse(self.feed).entries)

    def go(self):
        ''' Returns a list of tidy unicode representations of new feed items. '''
        print '======== FETCHING FEED ========='
        new_items = []
        for item in self.fetch():
            # add tidy version of item to list
            new_items.append(self.tidy(item))
            # add item to list of old items
            self.items.append(item)
        return new_items

if __name__ == "__main__":
    Fetcher.go(Fetcher())
