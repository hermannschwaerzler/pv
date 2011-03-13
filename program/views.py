from django.views.generic.list import ListView

from models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic

from datetime import datetime, timedelta

class ShowListView(ListView):
    context_object_name = 'show_list'
    model = Show

    def get_context_data(self, **kwargs):
        context = super(ShowListView, self).get_context_data(**kwargs)

        context['broadcastformat_list'] = BroadcastFormat.objects.all()
        context['musicfocus_list'] = MusicFocus.objects.all()
        context['showinformation_list'] = ShowInformation.objects.all()
        context['showtopic_list'] = ShowTopic.objects.all()

        return context
    
class RecommendationsView(ListView):
    context_object_name = 'recommendations'
    template_name = 'program/recommendations.html'

    def get_queryset(self):
        now = datetime.now()
        in_one_week = now + timedelta(weeks=1)

        return Note.objects.filter(status=1, timeslot__start__range=(now, in_one_week))[:10]