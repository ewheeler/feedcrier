#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
import feedparser
from HTMLParser import HTMLParser

def stripHTML(data):
    return HTMLStripper(data).stripped

class HTMLStripper(HTMLParser):

    def __init__(self, data):
        HTMLParser.__init__(self)
        self._stripped = []
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'br':
            self._stripped.append('\n')

    def handle_charref(self, name):
        try:
            if name.lower().startswith('x'):
                char = int(name[1:], 16)
            else:
                char = int(name)
            self._stripped.append(unichr(char))
        except Exception, error:
            pass 

    def handle_entityref(self, name):
        try:
            char = unichr(name2codepoint[name])
        except Exception, error:
            pass
            char = u'&%s;' % name
        self._stripped.append(char)

    def handle_data(self, data):
        self._stripped.append(data)

    @property
    def stripped(self):
        return ''.join(self._stripped)

class GitIRC:
    feed = 'https://github.com/rapidsms.private.atom?token=1e5ad8f275bdd03a163488732863171f'
    items = []

    def fetch(self):
        def fresh(i): return i not in self.items
        return filter(fresh, feedparser.parse(self.feed).entries)

    def go(self):
        print '======== HERE WE GO ========='
        new_items = []
        for item in self.fetch():
            body = stripHTML(item.content[0].value).strip().replace("&quot;", "\"")
            pretty = u'  THIS JUST IN: %s  |  %s  ' % (item.title, body)
            new_items.append(pretty)
            self.items.append(item)
        return new_items

if __name__ == "__main__":
    GitIRC.go(GitIRC())
