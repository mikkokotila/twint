from twintel._methods.stream import stream
from twintel._methods.flatfile import flatfile
from twintel._methods.search import search
from twintel._methods.timeline import timeline

__version__ = "1.3.1"

# module level doc-string

__doc__ = """

twintel - Twitter data for signals intelligence
==============================================
**twintel** is a Python package that provides a
very high level abstraction layer to Twitter
API and provides the preprocessed results in a
pandas dataframe. The system have been built with
several concerns in mind:

- availability of key scores (influence, reach, etc)
- applicability of the data for neural networks
- identification of spam and other bots
- singleline commands for all four important methods:
   - streaming API for both keywords and users
   - REST API for for keywords
   - REST API for user timelines
   - Flatfile ingestion from JSON (from Twitter API)
 - all methods return identical dataframe
"""
