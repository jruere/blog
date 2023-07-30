AUTHOR = 'Javier Ruere'
SITENAME = 'Notes and Stuff'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Argentina/Buenos_Aires'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

OUTPUT_PATH = 'docs/'  # Required by GitHub Pages.
STATIC_PATHS = ['images/', 'extra/']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}}

PORT = 8000  # For development.
