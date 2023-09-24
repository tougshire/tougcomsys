from datetime import date, datetime, timedelta
from typing import Any, Dict
from urllib.parse import urlencode
from django.apps import apps
from django.forms.models import BaseModelForm

import icalendar
import markdown as md
import recurring_ical_events
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, QueryDict
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from feeds.models import Post as FeedPost
from feeds.models import Source as FeedSource

from tougcomsys.forms import ArticleArticleEventDateFormSet, ArticleForm, ArticlePlacementFormSet, CommentForm, ImageForm
from tougcomsys.models import (Article, BlockedIcalEvent, Comment, ICal, Image, Menu,
                               Page, Placement, Subscription)
from tougshire_vistas.models import Vista
from tougshire_vistas.views import get_vista_queryset, make_vista_fields, vista_context_data

# ArticleImage, 

class TestError(Exception):
    pass

def events_from_icals( placement ):

    start_date = date.today() + timedelta( days=placement.event_list_start )
    end_date =   start_date + timedelta( days=placement.events_list_length )

    event_date_dict = {}

    blocked_ical_events = BlockedIcalEvent.objects.all()
    blocked_ical_uids = [ blocked_event.uuid for blocked_event in blocked_ical_events ]

    for ical in placement.ical_set.all():
    
        url = ical.url

        ical_string = requests.get(url).text
        calendar = icalendar.Calendar.from_ical(ical_string)
        ical_events = recurring_ical_events.of(calendar).between(start_date, end_date)

        for ical_event in ical_events:

            event_dict = {}
            event_dict['uid'] = str(ical_event['UID']) if ical_event.has_key('UID') else ''
            if not event_dict['uid'] > '':
                continue

            if event_dict['uid'] in blocked_ical_uids:

                blocks = blocked_ical_events.filter( uuid=event_dict['uid'] )

                if blocks.exists():
                    block = blocks.first()

                    article = block.display_instead
                    if not article:
                        continue

                    event_dict['slug'] = article.slug

                    event_dict['whendate'] = date( ical_event['DTSTART'].dt.year, ical_event['DTSTART'].dt.month, ical_event['DTSTART'].dt.day )
                    if isinstance( ical_event['DTSTART'].dt, datetime ):
                        event_dict['whentime'] = datetime( 100, 1, 1, ical_event['DTSTART'].dt.hour, ical_event['DTSTART'].dt.minute )
                    event_dict['enddate'] = date( ical_event['DTEND'].dt.year, ical_event['DTEND'].dt.month, ical_event['DTEND'].dt.day )
                    if isinstance( ical_event['DTEND'].dt, datetime ):
                        event_dict['endtime'] = datetime( 100, 1, 1, ical_event['DTEND'].dt.hour, ical_event['DTEND'].dt.minute )

                    event_dict['headline'] = article.headline 
                    event_dict['content'] = article.content

                    isokey = event_dict['whendate'].isoformat()

            else:

                event_dict['ical_url'] = url.replace('/', '_%2f_')
                event_dict['whendate'] = date( ical_event['DTSTART'].dt.year, ical_event['DTSTART'].dt.month, ical_event['DTSTART'].dt.day )
                if isinstance( ical_event['DTSTART'].dt, datetime ):
                    event_dict['whentime'] = datetime( 100, 1, 1, ical_event['DTSTART'].dt.hour, ical_event['DTSTART'].dt.minute )
                event_dict['enddate'] = date( ical_event['DTEND'].dt.year, ical_event['DTEND'].dt.month, ical_event['DTEND'].dt.day )
                if isinstance( ical_event['DTEND'].dt, datetime ):
                    event_dict['endtime'] = datetime( 100, 1, 1, ical_event['DTEND'].dt.hour, ical_event['DTEND'].dt.minute )
                 
                event_dict['headline'] = str(ical_event['SUMMARY'])
                event_dict['content'] = str(ical_event['DESCRIPTION']) if ical_event.has_key('DESCRIPTION') else ''

                isokey = event_dict['whendate'].isoformat()

            if isokey in event_date_dict:
                event_date_dict[ isokey ].append( event_dict )
            else:
                event_date_dict[ isokey ] = [ event_dict ]

    return event_date_dict

def events_from_articles( placement, do_preview=False ):

    start_date = date.today() + timedelta( days=placement.event_list_start )
    end_date =   start_date + timedelta( days=placement.events_list_length )

    event_date_dict = {}

    if do_preview:
        articleplacements = placement.articleplacement_set.filter( Q(article__draft_status=Article.DRAFT_STATUS_PUBLISHED) | Q(article__draft_status=Article.DRAFT_STATUS_DRAFT) )
    else:
        articleplacements = placement.articleplacement_set.filter( article__draft_status=Article.DRAFT_STATUS_PUBLISHED) 

    for articleplacement in articleplacements:
    
        for event_date in articleplacement.article.articleeventdate_set.all():

            if event_date.whendate >= start_date and event_date.whendate <= end_date:

                event_dict = {}
                event_dict['whendate'] = event_date.whendate
                event_dict['whentime'] = event_date.whentime
                event_dict['endtime'] = event_date.whendate + timedelta( minutes=event_date.timelen )
                event_dict['slug'] = articleplacement.article.slug
                event_dict['headline'] = articleplacement.article.headline
                event_dict['content'] = articleplacement.article.content

                isokey = event_dict['whendate'].isoformat()
                if isokey in event_date_dict:
                    event_date_dict[ isokey ].append( event_dict )
                else:
                    event_date_dict[ isokey ] = [ event_dict ]

    return event_date_dict            

def ical_from_events( placement, do_preview=False ):
    ical_text = 'BEGIN:VCALENDAR\n'
    placementarticles = placement.articleplacement_set.all()
    for placementarticle in placementarticles:
        article = placementarticle.article
        eventdates = article.articleeventdate_set.all()
        if eventdates.exists():
            for eventdate in eventdates:
                ical_text = ical_text + 'BEGIN:VEVENT\n'
                ical_text = ical_text + 'DTSTAMP:{}\n'.format( date.today().isoformat() )
                ical_text = ical_text + 'UID:{}\n'.format( article.pk )
                ical_text = ical_text + 'SUMMARY:{}\n'.format( article.headline )

                if eventdate.whentime is not None:
                    ical_text = ical_text + 'DTSTART:{}{}{}T{}{}{}\n'.format( eventdate.whendate.year, eventdate.whendate.month, eventdate.whendate.day, eventdate.whentime.hour, eventdate.whentime.minute, 00 )  
                else:
                    ical_text = ical_text + 'DTSTART:{}{}{}\n'.format( eventdate.whendate.year, eventdate.whendate.month, eventdate.whendate.day )
                ical_text = ical_text + 'END:VEVENT\n'

    ical_text = ical_text + 'END:VCALENDAR\n'

    return ical_text            
            

def event_date_dict( placement, do_preview=False ):

    ical_dict = events_from_icals( placement )
    article_dict = events_from_articles( placement, do_preview )

    new_dict = ical_dict

    for key, events in article_dict.items():

        if key in new_dict:
            new_dict[ key ] = new_dict[ key ] + events 
        else:
            new_dict[ key ] = events

    new_dict = dict(sorted( new_dict.items() ) )
    return new_dict

def single_event_date_dict( url, uid ):

    blocked_ical_events = BlockedIcalEvent.objects.all()
    blocked_ical_uids = [ blocked_event.uuid for blocked_event in blocked_ical_events ]

    ical_string = requests.get(url).text
    calendar = icalendar.Calendar.from_ical(ical_string)
    ical_events = recurring_ical_events.of(calendar).all()

    event_dict = {}

    for ical_event in ical_events:

        event_dict['uid'] = str(ical_event['UID']) if ical_event.has_key('UID') else ''
        if not event_dict['uid'] == uid:
            continue

        if event_dict['uid'] in blocked_ical_uids:

            blocks = blocked_ical_events.filter( uuid=event_dict['uid'] )

            if blocks.exists():
                block = blocks.first()

                article = block.display_instead
                if not article:
                    continue

                event_dict['slug'] = article.slug

                event_dict['whendate'] = date( ical_event['DTSTART'].dt.year, ical_event['DTSTART'].dt.month, ical_event['DTSTART'].dt.day )
                if isinstance( ical_event['DTSTART'].dt, datetime ):
                    event_dict['whentime'] = datetime( 100, 1, 1, ical_event['DTSTART'].dt.hour, ical_event['DTSTART'].dt.minute )
                event_dict['enddate'] = date( ical_event['DTEND'].dt.year, ical_event['DTEND'].dt.month, ical_event['DTEND'].dt.day )
                if isinstance( ical_event['DTEND'].dt, datetime ):
                    event_dict['endtime'] = datetime( 100, 1, 1, ical_event['DTEND'].dt.hour, ical_event['DTEND'].dt.minute )

                event_dict['headline'] = article.headline 
                event_dict['content'] = article.content

        else:

            event_dict['whendate'] = date( ical_event['DTSTART'].dt.year, ical_event['DTSTART'].dt.month, ical_event['DTSTART'].dt.day )
            if isinstance( ical_event['DTSTART'].dt, datetime ):
                event_dict['whentime'] = datetime( 100, 1, 1, ical_event['DTSTART'].dt.hour, ical_event['DTSTART'].dt.minute )
            event_dict['enddate'] = date( ical_event['DTEND'].dt.year, ical_event['DTEND'].dt.month, ical_event['DTEND'].dt.day )
            if isinstance( ical_event['DTEND'].dt, datetime ):
                event_dict['endtime'] = datetime( 100, 1, 1, ical_event['DTEND'].dt.hour, ical_event['DTEND'].dt.minute )
            
            event_dict['headline'] = str(ical_event['SUMMARY'])
            event_dict['content'] = str(ical_event['DESCRIPTION']) if ical_event.has_key('DESCRIPTION') else ''

    return event_dict

    
def condensify( value ):
    return slugify( value ).replace('-','')

def get_menu_items( page ):
    menus = []
    for menuobject in Menu.objects.filter( page=page ):
        menu = [{'href':menuitem.url, 'label':menuitem.label} for menuitem in menuobject.menuitem_set.all() ]
        menus.append(menu)
    return menus

def get_page(request):

    try:
        page = Page.objects.get(pk=request.session.get('page'))
    except:
        try:
            page = Page.objects.first()
        except:
            page = None

    return page


class IcalEventView(TemplateView):

    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'ical_event.html')

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        if 'ical_url' in self.kwargs:
            ical_url = self.kwargs.get('ical_url').replace( '_%2f_', '/')
        else:
            return context_data 

        if 'uid' in self.kwargs:
            uid = self.kwargs.get('uid')
        else:
            return context_data 

        page = get_page(self.request)
        if page:
            context_data['menus'] = get_menu_items( page )

        context_data['article'] = single_event_date_dict( ical_url, uid ) 

        return context_data


class HomePage(TemplateView):

    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'homepage.html')

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        page = Page.objects.first()
        if 'page' in self.kwargs:
            page = Page.objects.get(pk=self.kwargs.get('page'))

        if page is None:
            return context_data
 
        context_data['menus'] = get_menu_items( page )

        # Remember the page so if an article or ical event is clicked, the menu displayed will be the same menu displayed for thsi view
        self.request.session['page'] = page.pk

        context_data['placement_types'] = {}
        for placement_type in Placement.TYPE_CHOICES:
            context_data['placement_types'][ condensify( placement_type[1] ) ] = placement_type[0]

        context_data['font_sizes'] = {}
        for font_size in Placement.FONT_SIZE_CHOICES:
            context_data['font_sizes'][ condensify( font_size[1] ) ] = font_size[0]

        do_preview = self.request.user.is_staff == True and self.request.GET.get('preview').lower() == "true"[:len(self.request.GET.get('preview'))].lower() if 'preview' in self.request.GET else False

        if do_preview:
            placements = Placement.objects.filter( page=page ).order_by('place_number')
        else:
            placements = Placement.objects.filter( page=page ).order_by('place_number')

        context_data['placements'] = []

        for placement in placements:

            if placement.type == Placement.TYPE_ARTICLE_LIST:
                if do_preview:
                    placement.count = placement.articleplacement_set.filter(Q(article__draft_status=Article.DRAFT_STATUS_PUBLISHED) | Q(article__draft_status=Article.DRAFT_STATUS_DRAFT)).count()
                    placement.articleplacements = placement.articleplacement_set.filter(Q(article__draft_status=Article.DRAFT_STATUS_PUBLISHED) | Q(article__draft_status=Article.DRAFT_STATUS_DRAFT))
                else:
                    placement.count = placement.articleplacement_set.filter(article__draft_status=Article.DRAFT_STATUS_PUBLISHED).count()
                    placement.articleplacements = placement.articleplacement_set.filter(article__draft_status=Article.DRAFT_STATUS_PUBLISHED)

                for articleplacement in placement.articleplacements:

                    date_count = articleplacement.article.articleeventdate_set.count()

                    if date_count == 1:
                        articleplacement.article.date = articleplacement.article.articleeventdate_set.first().whendate
                    else:
                        for article_eventdate in articleplacement.article.articleeventdate_set.all():
                            if article_eventdate.whendate < date.today():
                                articleplacement.article.prev_date = article_eventdate.whendate
                            if article_eventdate.whendate > date.today():
                                articleplacement.article.next_date = article_eventdate.whendate
                                break
                    
                    articleplacement.article.date_count = date_count

                    if articleplacement.article.summary == '':
                        articleplacement.article.summary = articleplacement.article.content
                    if articleplacement.article.summary == '__none__':
                        articleplacement.article.summary = ''
                    if articleplacement.article.content_format == 'markdown':
                        articleplacement.article.content = md.markdown(articleplacement.article.content, extensions=['markdown.extensions.fenced_code'])
                    if articleplacement.article.summary_format == 'markdown' or ( articleplacement.article.summary_format == 'same' and articleplacement.article.content_format == 'markdown' ):
                        articleplacement.article.summary = md.markdown(articleplacement.article.summary, extensions=['markdown.extensions.fenced_code'])

                    if articleplacement.article.summary != articleplacement.article.content and articleplacement.article.readmore > '':
                        articleplacement.article.show_readmore = True
                    else:
                        articleplacement.article.show_readmore = False

                    if articleplacement.article.show_author == Article.SHOW_COMPLY:
                        articleplacement.article.show_author = placement.show_author
                    if articleplacement.article.show_updated == Article.SHOW_COMPLY:
                        articleplacement.article.show_updates = placement.show_created  

            elif placement.type == Placement.TYPE_EVENT_LIST:

                placement.events = event_date_dict( placement, do_preview ) 

            elif placement.type == Placement.TYPE_FEED:
                placement.feedposts = FeedPost.objects.filter( source__in=[feedsource.source.pk for feedsource in placement.feedsource_set.all()] ).order_by('-created') 

            context_data['placements'].append(placement)

        return context_data

class ArticleDetail(DetailView):

    model = Article

    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'article.html')

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        page = get_page(self.request)

        if page:
            context_data['menus'] = get_menu_items( page )

        if self.object.content_format == 'markdown':
            self.object.content = md.markdown(self.object.content, extensions=['markdown.extensions.fenced_code'])
        if self.object.show_author == Article.SHOW_COMPLY:
            self.object.show_author = True
        if self.object.show_updated == Article.SHOW_COMPLY:
            self.object.show_updates = True  

        date_count = self.object.articleeventdate_set.count()

        if date_count == 1:
            context_data['date'] = self.object.articleeventdate_set.first().whendate
        else:
            for article_eventdate in self.object.articleeventdate_set.all():
                if article_eventdate.whendate < date.today():
                    context_data['prev_date'] = article_eventdate.whendate
                if article_eventdate.whendate > date.today():
                    context_data['next_date'] = article_eventdate.whendate
                    break
        
        context_data['date_count'] = date_count

        
        subscription = None
        if self.request.user.is_authenticated and self.object.allow_comments:
            try:
                subscription = Subscription.objects.get(article=self.get_object(), subscriber=self.request.user)
            except Subscription.MultipleObjectsReturned:
                subscriptions_delete = Subscription.objects.filter(article=self.get_object(), subscriber=self.request.user)[1:]
                for subscription in subscriptions_delete:
                    subscription.delete()
                subscription = Subscription.objects.get(article=self.get_object(), subscriber=self.request.user)
            except Subscription.DoesNotExist:
                pass

        context_data['subscription'] = subscription

        return context_data

class ArticleList(ListView):

    permission_required = 'sdcpeople.view_person'
    model = Article

    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'article_list.html')

    def setup(self, request, *args, **kwargs):

        self.vista_settings={
            'max_search_keys':5,
            'fields':[],
        }

        self.vista_settings['fields'] = make_vista_fields(Article, field_names=[
            'headline',
            'draft_status',
            'articleplacement__placement'
        ])

        if 'by_value' in kwargs and 'by_parameter' in kwargs:

            self.vista_get_by = QueryDict(urlencode([
                ('filter__fieldname__0', [kwargs.get('by_parameter')]),
                ('filter__op__0', ['exact']),
                ('filter__value__0', [kwargs.get('by_value')]),
                ('order_by', ['name_last', 'name_common', ]),
                ('paginate_by',self.paginate_by),
            ],doseq=True) )


        self.vista_defaults = QueryDict(urlencode([
            ('filter__fieldname__0', ['draft_status']),
            ('filter__op__0', ['exact']),
            ('filter__value__0', [Article.DRAFT_STATUS_PUBLISHED]),
            ('order_by', ['updated_date', 'headline', ]),
            ('paginate_by',self.paginate_by),
        ],doseq=True),mutable=True )

        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = super().get_queryset()

        self.vistaobj = {'querydict':QueryDict(), 'queryset':queryset}

        return get_vista_queryset( self )

    def get_paginate_by(self, queryset):

        if 'paginate_by' in self.vistaobj['querydict'] and isinstance(self.vistaobj['querydict']['paginate_by'], int):
            print('tp239i644', self.vistaobj['querydict']['paginate_by'])
            return self.vistaobj['querydict']['paginate_by']

        return super().get_paginate_by(queryset)

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        vista_data = vista_context_data(self.vista_settings, self.vistaobj['querydict'])


        context_data = {**context_data, **vista_data}
        context_data['vista_default'] = dict(self.vista_defaults)

        if self.request.user.is_authenticated:
            context_data['vistas'] = Vista.objects.filter(user=self.request.user, model_name='sdcpeople.Article').all() # for choosing saved vistas

        if self.request.POST.get('vista_name'):
            context_data['vista_name'] = self.request.POST.get('vista_name')

        context_data['count'] = self.object_list.count()

        return context_data


def get_ical_text(request, pk=0):
    if not pk > 0:
        return HttpResponse("-")
    ical = ICal.objects.get(pk=pk)
    return  HttpResponse(requests.get(ical.url).text)

def ical_detail_view(request, uuid):

    ical_calendars = []
    event_from_ical = {}

    for ical in ICal.objects.all():
        ical_string = requests.get(ical.url).text
        calendar = icalendar.Calendar.from_ical(ical_string)
        ical_calendars.append( calendar )


    for ical_calendar in ical_calendars:
        # for icalevent in recurring_ical_events.of(calendar).between( event_start_date, event_end_date ):
        for icalevent in recurring_ical_events.of(ical_calendar).all():
            dict_items = dict(icalevent.items())
            if dict_items["UID"] == uuid:

                event_from_ical['slug'] = ''
                event_from_ical['headline'] = str(icalevent["SUMMARY"])
                event_from_ical['summary'] = ''
                if 'DESCRIPTION' in dict_items:
                    event_from_ical['content'] = dict_items['DESCRIPTION']

                break

    return TemplateResponse( request, '{}/article.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR']), { "article": event_from_ical } )

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'comment_form.html')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if 'article' in self.kwargs:
            context_data['article'] = Article.objects.get(slug=self.kwargs.get('article'))
        if 'to' in self.kwargs:
            context_data['article'] = Comment.objects.get(pk=self.kwargs.get('to'))

        return context_data

    def get_initial(self):
        
        initial_data = super().get_initial()
        if 'article' in self.kwargs:
            initial_data['article'] = Article.objects.get(slug=self.kwargs.get('article'))
        if 'to' in self.kwargs:
            initial_data['article'] = Comment.objects.get(pk=self.kwargs.get('to'))
        return initial_data

    def form_valid(self, form):
        
        comment = form.save(commit=False)
        comment.author = self.request.user
        if comment.in_reply_to is not None:
            comment.in_reply_to_text = comment.in_reply_to.comment_text
            comment.in_reply_to_created_date = comment.in_reply_to.created_date
            comment.in_reply_to_author_str = str(comment.in_reply_to.author)

        form.save()

        if 'FROM_EMAIL' in settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]:
            from_email = settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['FROM_EMAIL']
        else:
            from_email = None
        

        for subscription in comment.article.subscription_set.all():
            try:
                send_mail(
                    settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['SITE_NAME'] + ' new comment',
                    comment.comment_text,
                    from_email,
                    [subscription.subscriber.email]
                )
            except Exception as e:
                print('{} {}'.format(type(e), e))

        return super().form_valid(form)

    def get_success_url(self):
        return reverse( 'tougcomsys:article', kwargs={'slug':self.object.article.slug} )

class ArticleCreate(PermissionRequiredMixin, CreateView):

    permission_required = "tougcomsys.add_article"  
    model = Article
    form_class = ArticleForm
    template_name = 'tougcomsys/editing/article_form.html'
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'article_form.html')

    def get_success_url(self):
        return reverse( 'tougcomsys:article_articleeventdates', kwargs={'pk':self.object.pk})

class ArticleUpdate(PermissionRequiredMixin, UpdateView):

    permission_required = "tougcomsys.change_article"  
    model = Article
    form_class = ArticleForm
    template_name = 'tougcomsys/editing/article_form.html'
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'article_form.html')

    def get_success_url(self):
        return reverse( 'tougcomsys:article_articleeventdates', kwargs={'pk':self.object.pk})

class ImageCreate(PermissionRequiredMixin, CreateView):

    permission_required = "tougcomsys.add_image"  
    model = Image
    form_class = ImageForm
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'Image_form.html')

    def get_initial(self):
        
        initial = super().get_initial()
        initial['author'] = self.request.user
        return initial

    def get_success_url(self):
        if 'popup' in self.kwargs:
            return reverse('tougcomsys:window_closer', kwargs={'pk':self.object.pk, 'app_name':'tougcomsys', 'model_name':'Image'})
        return reverse('tougcomsys:homepage')
    
class ArticleArticleEventDates(PermissionRequiredMixin, UpdateView):

    permission_required = "tougcomsys.change_article"  
    model=Article
    fields=[]
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'article_articleeventdates_form.html')

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        if self.request.POST:
            context_data['articleeventdates'] = ArticleArticleEventDateFormSet (self.request.POST, instance=self.get_object())
        else:
            context_data['articleeventdates'] = ArticleArticleEventDateFormSet (instance=self.get_object())

        return context_data

    def form_valid(self, form):
        valid_response = super().form_valid(form)

        articleeventdates = ArticleArticleEventDateFormSet (self.request.POST, instance=self.get_object())
        if articleeventdates.is_valid():
            articleeventdates.save()
            return valid_response
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse( 'tougcomsys:article_placements', kwargs={'pk':self.object.pk})

class ArticlePlacements(PermissionRequiredMixin, UpdateView):

    permission_required = "tougcomsys.change_article"  
    model=Article
    fields=[]
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'article_articleplacements_form.html')

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        if self.request.POST:
            context_data['placements'] = ArticlePlacementFormSet (self.request.POST, instance=self.get_object())
        else:
            context_data['placements'] = ArticlePlacementFormSet (instance=self.get_object())

        return context_data


    def form_valid(self, form):
        valid_response = super().form_valid(form)

        articleplacements = ArticlePlacementFormSet (self.request.POST, instance=self.get_object())
        if articleplacements.is_valid():
            articleplacements.save()
            return valid_response
        else:
            for form in articleplacements.forms:
                print('tp239nk16', form.errors )
            return super().form_invalid(form)


class SubscriptionCreate(CreateView):

    model = Subscription
    fields = ['article']
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'subscription_form.html')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if 'article' in self.kwargs:
            context_data['article'] = Article.objects.get(slug=self.kwargs.get('article'))
        return context_data

    def form_valid(self, form):
        subscription = form.save(commit=False)
        subscription.subscriber = self.request.user
        print(self.request.user)
        form.save()

        return super().form_valid(form)

    def get_initial(self):
        
        initial_data = super().get_initial()
        if 'article' in self.kwargs:
            initial_data['article'] = Article.objects.get(slug=self.kwargs.get('article'))

        return initial_data

    def get_success_url(self):
        return reverse( 'tougcomsys:article', kwargs={'slug':self.object.article.slug} )

class SubscriptionDelete(DeleteView):

    model = Subscription
    fields = ['article']
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'subscription_delete.html')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['article'] = self.object.article
        return context_data

    def get_success_url(self):
        return reverse( 'tougcomsys:article', kwargs={'slug':self.object.article.slug} )


class CommentDelete(LoginRequiredMixin, DeleteView):

    model = Comment
    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'comment_delete_confirm.html')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['article'] = self.object.article
        return context_data

    def form_valid(self, form):

        if self.request.user != self.object.author:
            messages.error(self.request, 'You can only delete your own comments')
            return super().form_invalid(form)

        return super().form_valid(form)


    def get_success_url(self):
        return reverse( 'tougcomsys:article', kwargs={'slug':self.object.article.slug} )

