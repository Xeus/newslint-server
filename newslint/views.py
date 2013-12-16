from linter.lib.newslint.newslint import newslint
from linter.models import Clipping, ClippingForm, PUBLICATIONS
from django.shortcuts import render
from datetime import datetime
from api_views import API_PREFIX


def index(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS,
        'page': 'index',
        'title': 'read between the lines'
    }
    return render(request, 'index.html', data)


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
            'help': 'http://' + request.get_host() + '/' + API_PREFIX + 'help'
        }
        data['result']['total'] = data['result']['professionalism'] + data['result']['nonpartisanship'] + data['result']['credibility']
        return lint_result(request, data)
    else:
        print(f.errors)
        return render(request, 'index.html', {
            'error_message': "You didn't enter the form correctly.",
        })


def lint_result(request, data={}):
    # import pprint
    # import copy
    # pp = pprint.PrettyPrinter(indent=2)
    # data2 = copy.copy(data)
    # data2['content'] = '[removed for brevity]'
    # pp.pprint(data2)
    # print(simplejson.dumps(data))
    data['title'] = 'linter results'
    return render(request, 'result.html', data)


def input_clipping(request):
    data = {
        'title': 'lint some text :: newslint',
        'PUBLICATIONS': PUBLICATIONS
    }
    return render(request, 'input.html', data)


def about(request):
    data = {
        'page': 'about',
        'title': 'about'
    }
    return render(request, 'about.html', data)
