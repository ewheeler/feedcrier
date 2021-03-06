#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
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
        if tag.lower() == 'a':
            #self._stripped.append(attrs[0][1])
            pass

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

