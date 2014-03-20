# Tweet-A-Book!
A little (Flask) webapp to find tweetable sentences inside of an EPUB format publication.

## Description
The task: I often have the need to find short quotes in a book, usually to help us promote a publication on social media. This tool does exactly this: takes an ePub book and spits out a list of potentially tweetable sentences from the book. Try it, a test instance is available at [tweet-a-book.alese.it](http://tweet-a-book.alese.it).

## How does this work?
The `tokenize` function does basically look for anything longer than 100 and shorter than 140 characters in each XHTML inside the epub. As you may guess, the algorithm can be improved in many ways. Want to help me? Look into `src/functions.py`.

## Requirements
The app depends on flask and [pyepub](https://github.com/gabalese/pyepub), which is included in a tuned version to comply with Heroku requirements (_id est_: no `lxml` dependencies).

## Copyright
Tweet-A-Book is released as an open source project under the MIT license (as in `LICENSE` textile).
