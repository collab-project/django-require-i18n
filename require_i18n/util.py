# Copyright Collab 2015

"""
Utilities.
"""

from tower import tweak_message

from pybabel_json.extractor import extract_json


def extract_tower_json(fileobj, keywords, comment_tags, options):
    """
    JSON Babel extractor.
    """
    for lineno, funcname, message, comments in (
            list(extract_json(fileobj, keywords, comment_tags, options))):

        message = tweak_message(message)

        yield lineno, funcname, message, comments
