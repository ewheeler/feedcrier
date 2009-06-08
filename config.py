#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

feed_config = { 
    'name' : 'github', 
    'url' : 'https://github.com/username.private.atom?token=apitoken',
    'snippet' : 'item.content[0].value',
    'format' : "'  %s  |  %s  |  %s  |  %s' % (item.link, item.title, compact_body, when)"
}
