from typing import Any, Dict
from django.http import HttpResponse
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView,)
from django.views.generic.list import ListView
from django.template.response import TemplateResponse
from django.utils.text import slugify

from datetime import datetime, date, timedelta
import icalendar
import recurring_ical_events
import requests

import markdown as md

from tougcomsys.models import Article, ArticleEventdate, ArticlePlacement, Comment, Image, Page, Placement, Menu, ICal, BlockedIcalEvent
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

        page = Page.objects.first()
        if 'page' in self.kwargs:
            page = Page.objects.get(pk=self.kwargs.get('page'))

        if page is None:
            return context_data
 
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

            context_data['placements'].append(placement)

        return context_data


class ArticleDetail(DetailView):

    model = Article

    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'article.html')

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        page = Page.objects.first()
        if 'page' in self.kwargs:
            page = Page.objects.get(pk=self.kwargs.get('page'))

        if page is None:
            return context_data
 
        context_data['menus'] = get_menu_items( page )

        if self.object.content_format == 'markdown':
            self.object.content = md.markdown(self.object.content, extensions=['markdown.extensions.fenced_code'])
        if self.object.show_author == Article.SHOW_COMPLY:
            self.object.show_author = True
        if self.object.show_updated == Article.SHOW_COMPLY:
            self.object.show_updates = True  
        

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

class CommentCreate(CreateView):
    model=Comment
    model = Comment

    template_name = '{}/{}'.format(settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['TEMPLATE_DIR'], 'comment_form.html')

