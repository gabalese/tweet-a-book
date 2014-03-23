import re
import os


def html_to_text(data):
    """
    Thanks Tamim Shahriar
    http://love-python.blogspot.it/2011/04/html-to-text-in-python.html

    The present is a slight modified version of that script. LOTS of room for improvement,
    but still functional (if you can't use a proper cleaner like the one in lxml.html).
    """

    # replace consecutive spaces into a single one
    data = " ".join(data.split())

    # get only the body content
    bodypat = re.compile(r'<body[^<>]*?>(.*?)</body>', re.I)
    result = re.findall(bodypat, data)
    data = result[0]

    # now remove the java script
    p = re.compile(r'<script[^<>]*?>.*?</script>')
    data = p.sub('', data)

    # remove the css styles
    p = re.compile(r'<style[^<>]*?>.*?</style>')
    data = p.sub('', data)

    # remove html comments
    p = re.compile(r'')
    data = p.sub('', data)

    # remove all the tags
    p = re.compile(r'<[^<]*?>')
    data = p.sub('', data)

    return data


def tokenize(line):
    """
    Very basic regexp pattern to find "tweetable sentences".
    The "sentence" is blatantly defined as "begins with a uppercase letter, goes on until the first full stop".
    *Very* rough, but works. Breaks on acronyms and stuff.
    """
    from settings import MIN_LENGTH, MAX_LENGTH  # Lazy import
    rephrase = re.compile(r'(?<!\w\s)[A-Z].{%d,%d}[!\?\.]' % (MIN_LENGTH, MAX_LENGTH))
    tokens = rephrase.findall(line)
    return tokens


def extract_tweets(epubfile):
    listtokens = []
    for k in epubfile.manifest:
        if k.attrib["media-type"] == "application/xhtml+xml":
            plaintext = html_to_text(epubfile.read(os.path.join(os.path.dirname(epubfile.opf_path), k.attrib["href"])))
            tokens = tokenize(plaintext)
            if len(tokens) > 0:
                listtokens.extend(tokens)
    return listtokens