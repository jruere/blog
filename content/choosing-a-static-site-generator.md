Title: Choosing a Static Site Generator
Date: 2015-10-06 23:44
Tags: web, indieweb, python

An article in my feed about some dude changing his static site generator reminded me of the subject.

This fellow mentioned Hakyll, which is written in Haskell. I'm always tempted to return to Haskell but lately I've grown so distanced from it that I have a hard time tweaking my own xmonad configuration... so no.

Since I remembered very little from my previous search, I restarted by asking DuckDuckGo for a "python static site generator" and found two interesting links. The first one a [list of Python site generators](https://wiki.python.org/moin/StaticSiteGenerator "Python Site Generators") and the second a ["leaderboard" of static site generators](https://www.staticgen.com/ "Leaderboard of Static Site Generators").

The first one was cool but didn't compare.

The second one also didn't compare but ranked them by some inane criteria. So I chose [Pelican](http://blog.getpelican.com/) which was the first of the Python generators by that criteria and it handles RSS, which is my only requirement.

It's installed as a normal Python package so I created a virtual env, pip installed it and... it failed on MarkupSafe. :(

Not a promising start but I re-created the virtual environment with Pypy 3 (2.4.0) instead of Python 3.5.0 and it worked. I guess MarkupSafe 0.23 has some speedups.c for Python 3.5.

N.B.: The docs tell to start the test server with `python -m pelican.server` in the quick-start but later recommend using the standard library server. Maybe it's to avoid Python 2 vs 3 issues?

When starting the dev server with `python -m pelican.server` it hangs? No! It just doesn't print the "Listening on port 8000..." I have come to expect.

The result looks sensible.

There's still a footer I'd like to remove but some other time.
