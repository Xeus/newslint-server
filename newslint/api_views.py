# Create your views here.
from django.http import HttpResponse, Http404
import json
from django.shortcuts import get_object_or_404
from linter.lib.newslint.newslint import newslint
from linter.models import Clipping, ClippingForm, PUBLICATIONS
from django.utils import timezone
from settings import API_PREFIX, DATE_FORMAT
import logging
from django.views.decorators.csrf import csrf_exempt


api_logger = logging.getLogger('api')
logger = logging.getLogger('django')


def get_api_links_dict(request):
    return {
        'help': 'http://' + request.get_host() + '/' + API_PREFIX + 'help/',
        'clippings_list': 'http://' + request.get_host() + '/' + API_PREFIX + 'clippings/',
        'specific_clipping': 'http://' + request.get_host() + '/' + API_PREFIX + 'clipping/1/',
        'lint and save a clipping (via POST)': 'http://' + request.get_host() + '/' + API_PREFIX + 'post/',
    }


def get_user_ip(ip):
    if ip != None:
        return ip
    else:
        return 'no-IP'


def index(request):
    data = {
        'current_url': request.build_absolute_uri(),
        'api_links': get_api_links_dict(request)
    }

    api_logger.info('INFO: index (' + get_user_ip(request.META.get('REMOTE_ADDR')) + ')')

    return HttpResponse(json.dumps(data), content_type='json')


def list(request):
    try:
        clippings = Clipping.objects.all().order_by('-added')
    except Clipping.DoesNotExist:
        raise Http404
    clippings_decoded = []
    for c in clippings:
        c.added = c.added.strftime(DATE_FORMAT)
        c.published = c.published.strftime(DATE_FORMAT)
        c._state = None
        clippings_decoded.append(c.__dict__)
    data = {
        'current_url': request.build_absolute_uri(),
        'clippings_list': clippings_decoded,
        'title': 'list of public news clippings',
        'api_links': get_api_links_dict(request)
    }
    return HttpResponse(json.dumps(data), content_type='json')


@csrf_exempt
def lint_and_save(request):
    content = request.POST.get('content', '')
    clipping = Clipping()
    f = ClippingForm(request.POST, instance=clipping)
    if f.is_valid():
        result = newslint(content)
        clipping.id = None
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
            'api_links': get_api_links_dict(request)
        }
        data['status'] = 'saved to database'
        data['result']['total'] = data['result']['professionalism'] + data['result']['nonpartisanship'] + data['result']['credibility']
        clipping_obj = f.save(commit=False)
        if clipping_obj.published == None:
            clipping_obj.published = timezone.now()
        clipping_obj.save()
        data['permanent_url'] = 'http://' + request.get_host() + '/' + API_PREFIX + 'clipping/' + str(clipping.id)
        api_logger.info('linter (' + get_user_ip(request.META.get('REMOTE_ADDR')) + ')')
        logger.info('text linted and saved to database')
    else:
        data = {
            'current_url': request.build_absolute_uri(),
            'error_message': "You didn't enter the form correctly.",
            'content': request.POST.get('content', ''),
            'api_links': get_api_links_dict(request)
        }
        api_logger.info('linter (' + get_user_ip(request.META.get('REMOTE_ADDR')) + ')')
        logger.error('form not valid')
    return lint_result(request, data)


def lint_result(request, data={}):
    # import pprint
    # import copy
    # pp = pprint.PrettyPrinter(indent=2)
    # data2 = copy.copy(data)
    # data2['content'] = '[removed for brevity]'
    # pp.pprint(data2)
    # print(simplejson.dumps(data))
    data['title'] = 'linter results'
    return HttpResponse(json.dumps(data), content_type='json')


@csrf_exempt
def linter(request):
    content = ''
    if request.method == 'GET':
        content = request.GET.get('content', '')
    elif request.method == 'POST':
        content = request.POST.get('content', '')
    result = newslint(content)
    data = {
        'current_url': request.build_absolute_uri(),
        'result': result.fail_points,
        'errors': result.errors,
        'warnings': result.warnings,
        'notices': result.notices,
        'content': content,
        'api_links': get_api_links_dict(request)
    }
    if request.method == 'POST' and request.POST.get('public') == 'true':
        data['status'] = 'saved to database'

    api_logger.info('linter (' + get_user_ip(request.META.get('REMOTE_ADDR')) + ')')
    logger.info('text linted')
    return HttpResponse(json.dumps(data), content_type='json')


def help(request):
    data = {
        'current_url': request.build_absolute_uri(),
        'example': {
            'post_format': {
                'header': 'x-www-form-urlencoded',
                'params': {
                    'content': 'your news text includes chris hayes',
                    'public': 'true',
                    'title': 'clipping title',
                    'publication': 'source publication',
                    'author': 'author name',
                    'url': 'url if online article',
                    'published': '10/12/13 (MM/DD/YY)'
                }
            },
            'response_format': {
                "errors": [],
                "warnings": [{
                    "message": "Some references to punditry are used",
                    "detail": "References to pundits, who give more lip service to politics and rumor than to subject matter expertise and objectivity, can undermine the veracity of a story.",
                    "evidence": "chris hayes"
                }],
                "url": "http://localhost:8000/api/v1/linter/",
                'api_links': get_api_links_dict(request),
                "content": "chris hayes",
                "result": {
                    "credibility": 1.0,
                    "nonpartisanship": 0,
                    "professionalism": 0
                },
                "status": "saved to database",
                "notices": []
            },
        },
        'api_links': get_api_links_dict(request)
    }

    api_logger.info('help (' + get_user_ip(request.META.get('REMOTE_ADDR')) + ')')
    return HttpResponse(json.dumps(data), content_type='json')


def detail(request, pk):
    clipping = get_object_or_404(Clipping, pk=pk)
    result = newslint(clipping.content)
    title = 'untitled clipping'
    if clipping.title != '':
        title = clipping.title
    data = {
        'current_url': request.build_absolute_uri(),
        'author': clipping.author,
        'url': clipping.url,
        'publication': clipping.publication,
        'added': clipping.added.strftime(DATE_FORMAT),
        'published': clipping.published.strftime(DATE_FORMAT),
        'errors': result.errors,
        'warnings': result.warnings,
        'notices': result.notices,
        'content': clipping.content,
        'permanent_url': 'http://' + request.get_host() + '/clipping/' + str(clipping.id),
        'api_url': 'http://' + request.get_host() + '/api/v1/clipping/' + str(clipping.id),
        'title': title,
        'result': result.fail_points,
        'api_links': get_api_links_dict(request)
    }
    return HttpResponse(json.dumps(data), content_type='json')
