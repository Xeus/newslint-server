# Create your views here.
from django.http import HttpResponse, Http404
from django.utils import simplejson
from linter.lib.newslint.newslint import newslint
from linter.models import Clipping, ClippingForm, PUBLICATIONS
from django.utils import timezone


API_PREFIX = 'api/v1/'

def index(request):
    data = {
        'url': request.build_absolute_uri(),
        'api_links': {
            'help': 'http://' + request.get_host() + '/' + API_PREFIX + 'help',
            'clippings_list': 'http://' + request.get_host() + '/' + API_PREFIX + 'clippings',
            'specific_clipping': 'http://' + request.get_host() + '/' + API_PREFIX + 'clippings/1'
        }
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def linter(request):
    content = request.GET.get('q', '')
    result = newslint(content)
    data = {
        'url': request.build_absolute_uri(),
        'result': result.fail_points,
        'errors': result.errors,
        'warnings': result.warnings,
        'notices': result.notices,
        'content': content,
        'api_links': {
            'help': 'http://' + request.get_host() + '/' + API_PREFIX + 'help',
            'clippings_list': 'http://' + request.get_host() + '/' + API_PREFIX + 'clippings',
            'specific_clipping': 'http://' + request.get_host() + '/' + API_PREFIX + 'clippings/1'
        }
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def help(request):
    data = {
        'url': request.build_absolute_uri(),
        'api_links': {
            'help': 'http://' + request.get_host() + '/' + API_PREFIX + 'help',
            'clippings_list': 'http://' + request.get_host() + '/' + API_PREFIX + 'clippings',
            'specific_clipping': 'http://' + request.get_host() + '/' + API_PREFIX + 'clippings/1'
        }
    }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
