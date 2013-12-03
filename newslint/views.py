# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from linter.lib.newslint.newslint import newslint
from linter.models import Clipping, ClippingForm, PUBLICATIONS
from django.shortcuts import render
from datetime import datetime

API_PREFIX = '/api/v1'


def index(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS
    }
    return render(request, 'index.html', data)


def linter(request):
    content = 'test block'
    result = newslint(content)
    data = {
        'url': request.path,
        'result': result.fail_points,
        'errors': result.errors,
        'warnings': result.warnings,
        'notices': result.notices,
        'content': content,
        'help': 'http://' + request.META['HTTP_HOST'] + API_PREFIX + '/help'
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
            'url': request.path,
            'errors': result.errors,
            'warnings': result.warnings,
            'notices': result.notices,
            'result': result.fail_points,
            'content': content,
            'help': 'http://' + request.META['HTTP_HOST'] + API_PREFIX + '/help'
        }
        return lint_result(request, data)
    else:
        print(f.errors)
        return render(request, 'index.html', {
            'error_message': "You didn't enter the form correctly.",
        })


def lint_result(request, data={}):
    import pprint, copy
    pp = pprint.PrettyPrinter(indent=2)
    data2 = copy.copy(data)
    data2['content'] = '[removed for brevity]'
    pp.pprint(data2)
    # print(simplejson.dumps(data))
    return render(request, 'result.html', data)


def api_help(request):
    data = {
        'url': request.path,
        'api_links': {
            'help': 'http://' + request.META['HTTP_HOST'] + API_PREFIX + '/help',
            'clippings_list': 'http://' + request.META['HTTP_HOST'] + API_PREFIX + '/clippings',
            'specific_clipping': 'http://' + request.META['HTTP_HOST'] + API_PREFIX + '/clippings/1'
        }
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def input_clipping(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS
    }
    return render(request, 'input.html', data)
