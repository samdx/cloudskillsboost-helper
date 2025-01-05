import os
import re


def util_replace_special_chars(text_to_replace: str) -> str:
    """
    Remove special characters from the given text.
    This to make sure when a path is created, it doesn't contain any special characters.
    :param text_to_replace:
    :return str:
    """
    return (text_to_replace
            .replace(',', '')
            .replace('/', ' ')
            .replace(':', '')
            .replace(' - ', ' ')
            .replace(' ', '-'))


def util_replace_quote_marks(text_to_replace: str) -> str:
    """
    Replace the common quotation marks with their Unicode equivalents.
    :rtype: str
    :param text_to_replace:
    :return:
    Reference: https://www.babelstone.co.uk/Unicode/whatisit.html
    """

    return (text_to_replace
            .replace(u'\u201C', u"\u0022")  # “ to "
            .replace(u'\u201D', u'\u0022')  # ” to "
            .replace(u'\u2019', u"\u0027")  # ’ to '
            .replace(u'\u2018', u"\u0027")  # ‘ to '
            )


def util_strip_html_tags(text: str) -> str:
    """
    Strip out HTML tags from the given text.\n
    :param text: The text to process.
    :return: The text without HTML tags.
    """
    return re.sub(r'<.*?>', '', text)
