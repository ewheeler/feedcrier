#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
import feedparser
from stripper import *

class Fetcher:
    feed = 'https://github.com/rapidsms.private.atom?token=1e5ad8f275bdd03a163488732863171f'
    items = []

    def fetch(self):
        def fresh(i): return i not in self.items
        return filter(fresh, feedparser.parse(self.feed).entries)

    def go(self):
        print '======== FETCHING FEED ========='
        new_items = []
        for item in self.fetch():
            body = stripHTML(item.content[0].value).strip().replace("&quot;", "\"")
            pretty = u'  THIS JUST IN: %s  |  %s  ' % (item.title, body)
            new_items.append(pretty)
            self.items.append(item)
        return new_items

if __name__ == "__main__":
    Fetcher.go(Fetcher())
