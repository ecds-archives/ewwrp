import os
import re

from forms import *
from models import *

import time

from itertools import chain

from settings import COLLECTIONS, DEFAULT_COLLECTION, DEFAULT_ORDERING

from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import lxml.etree as ET

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
    ''' Values that should be available from any template. This is basically a work-around for managing apps '''
    return {'app': COLLECTIONS[app], 'collections': COLLECTIONS, 'can_sort_by': (('Author','author'), ('Title','title')), 'res_per_page': ((10,10), (20,20), (50,50))}

def makeTOC():
    ''' Creates a table of contents XML file'''
    docs = ET.Element('documents')
    alldocs = Docs.objects.all()
    for doc in alldocs:
        current = ET.SubElement(docs, 'document')
        ET.SubElement(current, 'title').text = doc.title
        ET.SubElement(current, 'id').text = doc.id
        ET.SubElement(current, 'author').text = doc.author
        ET.SubElement(current, 'collection').text = doc.collection
        ET.SubElement(current, 'language').text = doc.language
        ET.SubElement(current, 'ethnicity').text = doc.ethnicity
        ET.SubElement(current, 'form').text = doc.form
        ET.SubElement(current, 'genre').text = doc.genre
        ET.SubElement(current, 'geography').text = doc.geography
        ET.SubElement(current, 'date').text = doc.date
        k = ET.SubElement(current, 'keywords')
        for keyword in doc.keywords:
            ET.SubElement(k, 'term').text = keyword
    
    # Write the ElementTree to an XML document
    save_loc = os.path.join(settings.STATICFILES_DIRS[0], 'xml', 'table_of_contents.xml')
    f = open(save_loc, 'wb')
    f.write(ET.tostring(docs))
    f.close()
    return

def getPages(collection=None):
    tree = ET.parse(os.path.join(settings.STATICFILES_DIRS[0], 'xml', 'table_of_contents.xml'))
    root = tree.getroot()
    pages = []
    for item in root:
        d = {}
        for child in list(item):
            if child.tag == 'keywords':
                # Since keywords is a list
                d[child.tag] = ' '.join([c.text for c in child])
            else:
                d[child.tag] = child.text
        pages.append(d)
    return pages
''' End helper methods '''

def page(request, doc_id, page, app=DEFAULT_COLLECTION):
    ''' Display a specific page '''
    context = importantContextValues(app)
    context['page_in_collection'] = 'page'
    document = Docs.objects.get(id=doc_id)
    context['document'] = document
    if page != 'contents':
        # Create ordered list of all the divs
        id_list = [i.id for i in document.divs]
        
        # Position of current id
        position = id_list.index(page)
        
        # Get the current page
        docpage = document.divs[position]
        
        # Get ID of prev and next pages
        if position > 0:
            context['prev_id'] = id_list[position-1]
        if position+1 < len(id_list):
            context['next_id'] = id_list[position+1]
        
        # Get the current page
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
    
    results_per_page = 10
    
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
    
    if method == 'advanced':
        # If advanced, query fulltext terms
        # Parse for search options
        search_opts = {}
        if 'title' in form.cleaned_data and form.cleaned_data['title']:
            search_opts['title__fulltext_terms'] = form.cleaned_data['title']
        if 'author' in form.cleaned_data and form.cleaned_data['author']:
            search_opts['author__fulltext_terms'] = form.cleaned_data['author']
        if 'keyword' in form.cleaned_data and form.cleaned_data['keyword']:
            search_opts['fulltext_terms'] = form.cleaned_data['keyword']
        if 'collection' in form.cleaned_data and form.cleaned_data['collection']:
            if isinstance(form.cleaned_data['collection'],str):
                search_opts['collection__in'] = COLLECTIONS[form.cleaned_data['collection']]['name']
            elif isinstance(form.cleaned_data['collection'],list):
                search_opts['collection__in'] = [COLLECTIONS[m]['name'] for m in form.cleaned_data['collection']]

        # Get all documents, filter with search options, and order by score
        pageobjs = Docs.objects.filter(**search_opts).order_by('-fulltext_score')
    else:
        # If not advanced, run quick search
        pageobjs = getPages()
        print form.cleaned_data
        for key in form.cleaned_data:
            if form.cleaned_data[key]:
                val = form.cleaned_data[key].lower()
                val_parts = [x.strip() for x in val.split(' ')]
                for part in val_parts:
                    pageobjs = [k for k in pageobjs if key in k and isinstance(k[key], str) and part in k[key].lower()]
    
    # Create paginator safely
    paginator = Paginator(pageobjs, results_per_page)
    try:
        pages = paginator.page(current_page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    
    pages_formatted = []
    
    if method == 'advanced':
        # Create dictionary with desired properties
        for p in pages:
            pages_formatted.append({'form': p.form, 'language': p.language, 'author': p.author, 'title': p.title, 'collection': p.collection, 'date': p.date, 'keywords': ' '.join(p.keywords), 'genre': p.genre, 'id': p.id, 'ethnicity': p.ethnicity, 'geography': p.geography})
    else:
        pages_formatted = pages
    
    # Pass queries to context
    context['queries'] = queries # Current queries
    
    # Pass a bunch of variables to the template
    context['pages'] = pages_formatted
    context['paginator'] = pages
    
    # Render template
    return render_to_response('search.html',context,context_instance=RequestContext(request))

# This could use being updated
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
        
    results_per_page = 10
    
    # Read in pages from local XML file
    pageobjs = getPages()
    
    # Filtering based on collection
    if app != DEFAULT_COLLECTION:
        pageobjs = [p for p in pageobjs if p['collection'] == COLLECTIONS[app]['name']]
    
    options = {}
    
    # Summarize the collection
    for p in pageobjs:
        for key, val in p.iteritems():
            if not key in ['id','keywords','title','author',] and val:
                if not key in options:
                    options[key] = [val]
                elif not val in options[key]:
                    options[key].append(val)
            elif key in ['title','author',]:
                if val and len(val)>0 and val[0].isalpha():
                    if not key in options:
                        options[key] = [val[0]]
                    elif not val[0] in options[key]:
                        options[key].append(val[0])
    
    # Sort each option
    for key in options:
        options[key] = sorted(options[key])
    
    # Filter by value passed to user
    filt = request.GET.get('filter', False)
    val = request.GET.get('value', False)
    if filt and val:
        if filt in ['title', 'author']:
            pageobjs = [k for k in pageobjs if k[filt] and k[filt][0] == val]
        else:
            pageobjs = [k for k in pageobjs if k[filt] == val]
    
    # Sort pageobjs by title
    pageobjs = sorted(pageobjs, key=lambda k: k['title'])
    
    context['options'] = options
    
    # Pass the GET data, minus current page, to the context
    context['queries'] = queries
    
    paginator = Paginator(pageobjs, results_per_page)

    try:
        pages = paginator.page(current_page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    context['pages'] = pages
    context['paginator'] = pages

    return render_to_response('browse.html',context,context_instance=RequestContext(request))