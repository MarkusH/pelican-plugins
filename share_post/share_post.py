"""
Share Post
==========

This plugin adds share URL to article. These links are textual which means no
online tracking of your readers.
"""
from __future__ import unicode_literals

from bs4 import BeautifulSoup
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote as quote_inner

    def quote(content):
        return quote_inner(content.encode('utf-8'))

from pelican import signals, contents


def article_title(content):
    main_title = BeautifulSoup(content.title, 'html.parser').get_text().strip()
    return quote(main_title)


def article_url(content):
    site_url = content.settings['SITEURL']
    return quote('%s/%s' % (site_url, content.url))


def share_post(content):
    if isinstance(content, contents.Static):
        return
    title = article_title(content)
    url = article_url(content)

    tweet = '{quote}{title}{quote}{space}{url}'.format(
        quote=quote('"'), title=title, space=quote(' '), url=url,
    )
    facebook_link = 'http://www.facebook.com/sharer/sharer.php?s=100&amp;p%%5Burl%%5D=%s' % url
    gplus_link = 'https://plus.google.com/share?url=%s' % url
    twitter_link = 'http://twitter.com/home?status=%s' % tweet
    linkedin_link = 'https://www.linkedin.com/shareArticle?mini=true&url=%s&title=%s&source=%s' % (
        url, title, url
    )

    mail_link = 'mailto:?subject=%s&amp;body=%s' % (title, url)

    share_links = {
        'twitter': twitter_link,
        'facebook': facebook_link,
        'google-plus': gplus_link,
        'linkedin': linkedin_link,
        'email': mail_link
    }
    content.share_post = share_links


def register():
    signals.content_object_init.connect(share_post)
