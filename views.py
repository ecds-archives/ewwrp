import os
import re

from forms import *
from models import *

from itertools import chain

from settings import COLLECTIONS, DEFAULT_COLLECTION, DEFAULT_ORDERING

from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

''' Helper methods for views '''
def isInt(n):
    ''' Check if a string can be converted to an int or not '''
    try:
        if not n:
            return False
        int(n)
        return True
    except ValueError:
        return False

def getIntRange(n):
	m = re.search(r'^(?P<start>\d+)to(?P<end>\d+)$',n)
	if m:
		return m
	else:
		return False

def safeRange(r, a, b):
	''' Returns r[a:b] in a safe way '''
	lr = len(r)
	if a < 0: a = 0
	if b < 0: b = 0
	if a >= lr: a = lr-1
	if b >= lr: b = lr-1
	if a > b: return r[b:a]
	return r[a:b]

def makeURL(**kwargs):
    return '?' + '&'.join("{!s}={!s}".format(key,val) for (key,val) in kwargs.items())

def importantContextValues(app):
    ''' Values that should be available from any template '''
    return {'app': COLLECTIONS[app], 'collections': COLLECTIONS, 'can_sort_by': (('Author','author'), ('Title','title')), 'res_per_page': ((10,10), (20,20), (50,50))}
''' End helper methods '''

def page(request, doc_id, page, app=DEFAULT_COLLECTION):
    ''' Display a specific page '''
    context = {'app': COLLECTIONS[app]}
    context['page_in_collection'] = 'page'
    document = Documents.docs.get(id=doc_id)
    context['document'] = document
    if page != 'contents':
        # Get list of ids in order
        ids = Pages.pages.filter(doc_id__in=doc_id)
        
        ### NEED A WAY TO SPECIFY SPECIFIC DOC_ID
        
        id_list = [i.id for i in ids]
        
        # Position of current id
        position = id_list.index(page)
        
        # Get ID of prev and next pages
        if position > 0:
            context['prev_id'] = id_list[position-1]
        if position+1 < len(id_list):
            context['next_id'] = id_list[position+1]
        
        # Get the current page
        docpage = Pages.pages.get(id=page)
        context['docpage'] = docpage
        
        # Apply xsl transform
        formatted = docpage.xsl_transform(filename=os.path.join('file:///' + settings.BASE_DIR, 'ewwrp', 'static', 'xsl', 'tei.xsl'))
        context['formatted'] = formatted.serialize()
    context['page'] = page
    return render_to_response('page.html',context,context_instance=RequestContext(request))

def index(request, app=DEFAULT_COLLECTION):
    ''' Home page '''
    context = importantContextValues(app)
    context['page_in_collection'] = 'index'
    return render_to_response('index.html',context,context_instance=RequestContext(request))

def about(request, app=DEFAULT_COLLECTION):
    ''' About page - just a regular html file '''
    context = importantContextValues(app)
    context['page_in_collection'] = 'about'
    return render_to_response('about.html',context,context_instance=RequestContext(request))

def essays(request, app=DEFAULT_COLLECTION):
    ''' Essays - still need to make this work, but it should be quick '''
    context = importantContextValues(app)
    context['page_in_collection'] = 'essays'
    return render_to_response('index.html',context,context_instance=RequestContext(request))

def search(request, method='basic', app=DEFAULT_COLLECTION):
    ''' Search for a document within a collection, using either basic or advanced search '''
    context = importantContextValues(app)
    
    # Determine whether or not to do an advanced search
    if method == 'advanced':
        context['page_in_collection'] = 'advsearch'
        context['advanced'] = True
        if request.GET: form = AdvancedSearchForm(request.GET)
        else: form = AdvancedSearchForm()
    else:
        context['page_in_collection'] = 'search'
        context['advanced'] = False
        if request.GET: form = SearchForm(request.GET)
        else: form = SearchForm()
    
    # Pass the form variable to the context instance
    context['form'] = form
    
    # If they didn't search yet, render the page as is
    if not request.GET or not form.is_valid():
        return render_to_response('search.html', context, context_instance=RequestContext(request))
    
    # Copy over the queries, e.g. current page number
    queries = request.GET.copy()
    # If the user is currently on a page other than the first one
    if 'current_page' in request.GET and isInt(request.GET['current_page']):
        current_page = int(request.GET['current_page'])
        del queries['current_page']
    else:
        current_page = 1
    
    # Determine if the user specified results per page
    if 'results_per_page' in request.GET and isInt(request.GET['results_per_page']):
        results_per_page = int(request.GET['results_per_page'])
    else:
        results_per_page = 10
    context['results_per_page'] = results_per_page
	
	# Parse for search options
    search_opts = {}
    if 'title' in form.cleaned_data and form.cleaned_data['title']:
        search_opts['title__fulltext_terms'] = form.cleaned_data['title']
    if 'author' in form.cleaned_data and form.cleaned_data['author']:
        search_opts['author__fulltext_terms'] = form.cleaned_data['author']
    if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
        search_opts['fulltext_terms'] = form.cleaned_data['keyword']
    
    # Get all documents, filter with search options, and order by score
    pageobjs = Documents.docs.filter(**search_opts).order_by('-fulltext_score')
    
    # If the user is in a collection other than the default collection
    if 'collection' in form.cleaned_data and form.cleaned_data['collection']:
        if isinstance(form.cleaned_data['collection'], str):
            pageobjs = pageobjs.filter(collection__in=COLLECTIONS[form.cleaned_data['collection']]['name'])
        elif isinstance(form.cleaned_data['collection'], list):
            pageobjs = pageobjs.filter(collection__in=[COLLECTIONS[m]['name'] for m in form.cleaned_data['collection']])
    
    # Order by user-specified criteria
    if 'sort_by' in request.GET and len(request.GET['sort_by'])>0:
        pageobjs = pageobjs.order_by(request.GET['sort_by'])
        context['sort_by'] = request.GET['sort_by']
    else:
        pageobjs = pageobjs.order_by(DEFAULT_ORDERING)
        context['sort_by'] = DEFAULT_ORDERING
    
    # Pass queries to context
    context['queries'] = queries # Current queries
    
    # Create paginator safely
    paginator = Paginator(pageobjs, results_per_page)
    try:
        pages = paginator.page(current_page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    
    # Pass a bunch of variables to the template
    context['num_pages'] = len(pageobjs)
    context['pages'] = pages
    
    # Render template
    return render_to_response('search.html',context,context_instance=RequestContext(request))

def browse(request, app=DEFAULT_COLLECTION):
    ''' Browse the collection '''
    context = importantContextValues(app)
    context['page_in_collection'] = 'browse'
    
    # Copy GET info over to a variable
    queries = request.GET.copy()
    
    # If the user is on a certain page, get that page and remove it from the query; otherwise, default to first page
    if 'current_page' in request.GET and isInt(request.GET['current_page']):
        current_page = int(request.GET['current_page'])
        del queries['current_page']
    else:
        current_page = 1
    
    # If the user specified the number of results per page, use that. Default to 10.
    if 'results_per_page' in request.GET and isInt(request.GET['results_per_page']):
        results_per_page = int(request.GET['results_per_page'])
    else:
        results_per_page = 10
    context['results_per_page'] = results_per_page
    
    # Get all the documents in the current collection
    if app != DEFAULT_COLLECTION:
        pageobjs = Documents.docs.filter(collection=COLLECTIONS[app]['name'])
    else:
        # If in the default collection don't filter
        pageobjs = Documents.docs
    
    # Order by user-specified criteria
    if 'sort_by' in request.GET and len(request.GET['sort_by'])>0:
        pageobjs = pageobjs.order_by(request.GET['sort_by'])
        context['sort_by'] = request.GET['sort_by']
    else:
        pageobjs = pageobjs.order_by(DEFAULT_ORDERING)
        context['sort_by'] = DEFAULT_ORDERING

    # Pass the GET data, minus current page, to the context
    context['queries'] = queries
        
    pageobjs = pageobjs.all()
    paginator = Paginator(pageobjs, results_per_page)

    try:
        pages = paginator.page(current_page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    context['num_pages'] = len(pageobjs)
    context['pages'] = pages

    return render_to_response('browse.html',context,context_instance=RequestContext(request))