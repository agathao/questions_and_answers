from django import template
import re
import unicodedata
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe, SafeData, mark_for_escaping
from django.utils.encoding import force_unicode
from django.utils.html import (conditional_escape, escapejs,
    escape, urlize as _urlize, linebreaks, strip_tags, avoid_wrapping,
    remove_tags, simple_email_re,word_split_re)
from django.utils.http import urlquote
import string

register = template.Library()

@register.filter(name='ellipses')
def ellipses(value, arg):
    original_string = value
    max_length = arg

    if len(original_string) <= max_length:
        return original_string
    else:
        return original_string[:max_length] + "..."
    
class Replacement(object):

    def __init__(self, replacement):
        self.replacement = replacement
        self.occurrences = []

    def __call__(self, match):
        self.matched = match.group(0)
        self.replaced = match.expand(self.replacement)
        print self.matched
        print self.replaced
        return self.replaced

@register.filter(name='replaceimage')
def replaceimage(value, autoescape=False):
    original_string = value
    repl = Replacement('<a rel="lightbox" href="\\1"><img class="contentimg" style="display:block; max-width:100%%;max-height:300px; padding-top:5px; margin-bottom:3px" src="\\1"></a>')
    return re.sub(r'(https?://.*[jpg|png|gif|JPG|PNG|GIF]$)', repl, original_string)

