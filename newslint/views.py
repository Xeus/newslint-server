# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from linter.lib.newslint.newslint import newslint
from linter.models import Clipping, ClippingForm, PUBLICATIONS
from django.shortcuts import render
from datetime import datetime


def index(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS
    }
    return render(request, 'input.html', data)


def linter(request):
    content = 'chris hayes'
    result = newslint(content)
    data = {
        'url': 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'],
        'result': result.fail_points,
        'content': content
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def lint_clipping(request):
    f = ClippingForm(request.POST)
    if f.is_valid():
        content = request.POST['content']
        result = newslint(content)
        test = Clipping(request.POST)
        test.added = datetime.now()
        data = {
            'url': 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'],
            'result': result.fail_points,
            'content': content
        }
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    else:
        print(f.errors)
        return render(request, 'index.html', {
            'error_message': "You didn't enter the form correctly.",
        })


def input_clipping(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS
    }
    return render(request, 'input.html', data)
