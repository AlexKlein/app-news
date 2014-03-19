from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import News, Text

class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'latest_news_list'

    def get_queryset(self):
        """
        Return the last five published news (not including those set to be
        published in the future).
        """
        return News.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = News
    template_name = 'news/detail.html'
    def get_queryset(self):
        """
        Excludes any news that aren't published yet.
        """
        return News.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = News
    template_name = 'news/results.html'

def reads(request, news_id):
    p = get_object_or_404(News, pk=news_id)
    try:
        selected_text = p.text_set.get(pk=request.POST['text'])
    except (KeyError, Text.DoesNotExist):
        # Redisplay the news voting form.
        return render(request, 'news/detail.html', {
            'news': p,
            'error_message': "You didn't select a News.",
        })
    else:
        selected_text.reads += 1
        selected_text.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('news:results', args=(p.id,)))
