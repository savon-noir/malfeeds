MalFeeds
========

MalFeeds is a python library to enable python developpers to easily manage malware feeds and blacklists.

The framework is composed of the following parts:

- malfeeds/engines: the low-level generic and specific engines collecting data
- malfeeds/objects: the high-level objects exposed for the developpers to manage feeds data
- malfeeds/feeds: the user's defined configuration of the feeds he wants to enable/create

MalFeeds Engines
----------------

The purpose of the engines is to enable developpers not to worry anymore on how to collect data. Engines will collect data and create MalFeeds objects easily manipulable.

Currently, MalFeeds supports the following engine types:

- HTTP lines feed (engine name: mallinesfeed)
- RSS feed (engine name: malrssfeed)
- CSV feed (engine name: malcsvfeed)
- TCP Wrappers host.deny file (engine name: maltcpdfeed)
- Snort-file feed (engine name: malsnortfeed)

The following are in the scope of developement line:
- Local files data streaming
- HPFeeds connector to integrate with honeypots data
- Multi-line feed

MalFeeds Objects
----------------

MalFeeds includes different objects, provided with an API which enable the developper to correlate the collected information, store it or export it.

Currently, MalFeeds is provided with the following object types:

- MalFeedsCollection: is a collection of malware feeds
- MalFeeds: the feed itself, containing an header and feed entries (IOC)
- MalFeedEntry: an IOC described through the MalFeeds API

The purpose of these object is to offer a clear and easy to use API to manipulate feeds data and to provide output plugins for this data.

As of today, no plugins have been developped but the following are planned:

- Redis
- ElasticSearch
- SQL
- Styx XML export

MalFeeds Feeds
--------------

Feeds are .ini files containing the configuration of the different feeds to enable and manage through MalFeeds. It should be the only configuration required to any user of the lib.

This ini files **must** contain the following attributes:

- **engine**: this is where you define the name of the engine to be used to collect the data
- **feedurl**: URL or URI where to collect data
- **type**: Data type, only the following types are supported so far: ip, domain, url, asn, country, coordinates
- **enabled**: set to 1 or 0 to enable or disable feed

Addtiionally, the following attributes **could** be specified in the feed configuration file:

- **title**: title for the feed
- **description**: description for the feed
- **publisher**: publisher/creator of the feed
- **rights**: licensing and authorization specific field, as specified by the feed creator
- **extended**: specific for rss feeds having additional data specified in rssfeed.description field (see malwaredomainlist and malc0de). Set to 1 or 0.

Dependencies
-------------

Following packages need to be installed:

- feedparser
- idstools

How to run it
-------------

A very light MalFeedCollection factory is coded in module malfeedsfactory.py. It simply creates a MalFeedsCollection object containing all the enabled MalFeeds.
Have a look at it.

Code Status
-----------

Still under "heavy" dev, help/pull requests/comments welcome.

Please note:

- Only the basis is there so far
- API is far from complete
- No output plugins exists yet
