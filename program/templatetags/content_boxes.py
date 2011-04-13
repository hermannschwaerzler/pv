# http://docs.djangoproject.com/en/1.2/howto/custom-template-tags/

from django import template
register = template.Library()

from program.models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic

@register.inclusion_tag('program/boxes/broadcastformat.html')
def broadcastformat():
    broadcastformats = BroadcastFormat.objects.all()
    return {'broadcastformats': broadcastformats}

@register.inclusion_tag('program/boxes/musicfocus.html')
def musicfocus():
    musicfoci = MusicFocus.objects.all()
    return {'musicfoci': musicfoci}

@register.inclusion_tag('program/boxes/showinformation.html')
def showinformation():
    showinformations = ShowInformation.objects.all()
    return {'showinformations': showinformations}

@register.inclusion_tag('program/boxes/showtopic.html')
def showtopic():
    showtopics = ShowTopic.objects.all()
    return {'showtopics': showtopics}