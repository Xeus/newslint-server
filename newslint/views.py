from linter.lib.newslint.newslint import newslint
from linter.models import Clipping, ClippingForm, PUBLICATIONS
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from settings import DATE_FORMAT, API_PREFIX
from django.http import Http404
import logging

logger = logging.getLogger('django')
api_logger = logging.getLogger('api')


def index(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS,
        'page': 'index',
        'title': 'read between the lines'
    }
    return render(request, 'index.html', data)


def lint(request):
    data = {
        'PUBLICATIONS': PUBLICATIONS,
        'page': 'lint',
        'title': 'lint some text',
        'published_default': timezone.now()
    }
    return render(request, 'lint.html', data)


def lint_clipping(request):
    clipping = Clipping()
    content = request.POST.get('content', '')
    f = ClippingForm(request.POST, instance=clipping)
    if f.is_valid():
        result = newslint(content)
        clipping.id = None
        if clipping.published == None:
            clipping.published = timezone.now()
        data = {
            'author': clipping.author,
            'url': clipping.url,
            'publication': clipping.publication,
            'added': clipping.added.strftime(DATE_FORMAT),
            'published': clipping.published.strftime(DATE_FORMAT),
            'current_url': request.build_absolute_uri(),
            'errors': result.errors,
            'warnings': result.warnings,
            'notices': result.notices,
            'result': result.fail_points,
            'content': content,
            'public': False,
            'help': 'http://' + request.get_host() + '/' + API_PREFIX + 'help'
        }
        data['result']['total'] = data['result']['professionalism'] + data['result']['nonpartisanship'] + data['result']['credibility']
        logger.info('text linted')
        if request.POST.get('public') == 'on':
            clipping_obj = f.save(commit=False)
            if clipping_obj.published == None:
                clipping_obj.published = timezone.now()
            clipping_obj.save()
            data['permanent_url'] = 'http://' + request.get_host() + '/clipping/' + str(clipping.id)
            data['api_url'] = 'http://' + request.get_host() + '/api/v1/clipping/' + str(clipping.id)
            logger.info('form saved to database')
            data['public'] = True
        return lint_result(request, data)
    else:
        print(f.errors)
        logger.error('text failed to lint properly: ' + content)
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
        'PUBLICATIONS': PUBLICATIONS,
        'published_default': timezone.now()
    }
    return render(request, 'input.html', data)


def about(request):
    data = {
        'page': 'about',
        'title': 'about',
        'get_url': request.get_host() + '/' + API_PREFIX + 'linter/',
        'get_post_url': request.get_host() + '/' + API_PREFIX + 'post/',
    }
    return render(request, 'about.html', data)


def list(request):
    try:
        clippings = Clipping.objects.all().order_by('-added')[:30]
    except Clipping.DoesNotExist:
        raise Http404
    data = {
        'clippings_list': clippings,
        'title': 'list of public news clippings'
    }
    print(data)
    return render(request, 'list.html', data)


def detail(request, pk):
    clipping = get_object_or_404(Clipping, pk=pk)
    result = newslint(clipping.content)
    title = 'untitled clipping'
    if clipping.title != '':
        title = clipping.title
    data = {
        'author': clipping.author,
        'url': clipping.url,
        'publication': clipping.publication,
        'added': clipping.added.strftime(DATE_FORMAT),
        'published': clipping.published.strftime(DATE_FORMAT),
        'current_url': request.path,
        'public': True,
        'errors': result.errors,
        'warnings': result.warnings,
        'notices': result.notices,
        'content': clipping.content,
        'permanent_url': 'http://' + request.get_host() + '/clipping/' + str(clipping.id),
        'api_url': 'http://' + request.get_host() + '/api/v1/clipping/' + str(clipping.id),
        'title': title,
        'result': result.fail_points,
        'help': 'http://' + request.get_host() + '/' + API_PREFIX + 'help'
    }
    return render(request, 'detail.html', data)
