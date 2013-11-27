from linter.models import Clipping
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from linter.lib.newslint.newslint import newslint as newslint
from django.core.urlresolvers import reverse


def index(request):
    try:
        clippings = Clipping.objects.all().order_by('-added')[:5]
    except Clipping.DoesNotExist:
        raise Http404
    data = {
        'clippings_list': clippings
    }
    return render(request, 'clippings/index.html', data)


def detail(request, pk):
    clipping = get_object_or_404(Clipping, pk=pk)
    result = newslint(clipping.content)
    data = {
        'clipping': clipping,
        'result': result.fail_points
    }
    return render(request, 'clippings/detail.html', data)
