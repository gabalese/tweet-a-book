import re
from settings import MAX_LENGHT, MIN_LENGHT


def html_to_text(data):

    # replace consecutive spaces into a single one
    data = " ".join(data.split())

    # get only the body content
    bodyPat = re.compile(r'<body[^<>]*?>(.*?)</body>', re.I)
    result = re.findall(bodyPat, data)
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
    rephrase = re.compile(r'(?<!\w\s)[A-Z].{%d,%d}[!\?\.]' % (MIN_LENGHT, MAX_LENGHT))
    tokens = rephrase.findall(line)
    return tokens
