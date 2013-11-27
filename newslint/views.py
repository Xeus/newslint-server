# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from linter.lib.newslint.newslint import newslint
from linter.models import Clipping, ClippingForm, PUBLICATIONS
from django.shortcuts import render
from datetime import datetime


def index(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS
    }
    return render(request, 'index.html', data)


def linter(request):
    content = 'test block'
    result = newslint(content)
    data = {
        'url': 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'],
        'result': result.fail_points,
        'errors': result.errors,
        'warnings': result.warnings,
        'notices': result.notices,
        'content': content
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def lint_clipping(request):
    f = ClippingForm(request.POST)
    print(request.POST)
    if f.is_valid():
        content = request.POST['content']
        result = newslint(content)
        test = Clipping(request.POST)
        test.added = datetime.now()
        data = {
            'url': 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'],
            'errors': result.errors,
            'warnings': result.warnings,
            'notices': result.notices,
            'result': result.fail_points,
            'content': content
        }
        return lint_result(request, data)
    else:
        print(f.errors)
        return render(request, 'index.html', {
            'error_message': "You didn't enter the form correctly.",
        })


def lint_result(request, data={}):
    return render(request, 'result.html', data)


def api_help(request):
    api_prefix = '/api/v1'
    data = {
        'url': 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'],
        'api_links': {
            'help': 'http://' + request.META['HTTP_HOST'] + api_prefix + '/help',
            'clippings_list': 'http://' + request.META['HTTP_HOST'] + api_prefix + '/clippings',
            'specific_clipping': 'http://' + request.META['HTTP_HOST'] + api_prefix + '/clippings/1'
        }
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def input_clipping(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS
    }
    return render(request, 'input.html', data)
