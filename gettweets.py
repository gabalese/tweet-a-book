from src.functions import tokenize, html_to_text
import os


def extract_tweets(epubfile):
    listtokens = []
    for k in epubfile.manifest:
        if k.attrib["media-type"] == "application/xhtml+xml":
            plaintext = html_to_text(epubfile.read(os.path.join(os.path.dirname(epubfile.opf_path), k.attrib["href"])))
            if len(tokenize(plaintext)) > 0:
                listtokens.extend(tokenize(plaintext))
    return listtokens
