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


from datetime import datetime, date, timedelta
import icalendar
import recurring_ical_events
import requests

import markdown as md

# from tougcomsys.models import Event, EventDate, Page, Placement, Post, Article, ArticleEventdate, ArticleImage, ArticlePlacement
from tougcomsys.models import Article, ArticleEventdate, ArticleImage, ArticlePlacement, Image, Placement, Menu, ICal, BlockedIcalEvent

class HomePage(TemplateView):

    template_name = '{}/homepage.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR'])

    def get_context_data(self, **kwargs):

        do_preview = self.request.user.is_staff == True and self.request.GET.get('preview').lower() == "true"[:len(self.request.GET.get('preview'))].lower() if 'preview' in self.request.GET else False

        context_data = super().get_context_data(**kwargs)

        if do_preview:
            placements = Placement.objects.annotate(published_qty=Count("articleplacement", filter=( Q(articleplacement__article__draft_status=Article.DRAFT_STATUS_PUBLISHED) | Q(articleplacement__article__draft_status=Article.DRAFT_STATUS_DRAFT ) ) )).filter(published_qty__gte=1)
        else:
            placements = Placement.objects.annotate(published_qty=Count("articleplacement", filter=(Q(articleplacement__article__draft_status=Article.DRAFT_STATUS_PUBLISHED)))).filter(published_qty__gte=1)

        context_data['placements'] = []
        for placement in placements:


            if do_preview:
                placement.count = placement.articleplacement_set.filter(Q(article__draft_status=Article.DRAFT_STATUS_PUBLISHED) | Q(article__draft_status=Article.DRAFT_STATUS_DRAFT)).count()
                placement.articleplacements = placement.articleplacement_set.all().filter(Q(article__draft_status=Article.DRAFT_STATUS_PUBLISHED) )
            else:
                placement.count = placement.articleplacement_set.filter(article__draft_status=Article.DRAFT_STATUS_PUBLISHED).count()
                placement.articleplacements = placement.articleplacement_set.all().filter(article__draft_status=Article.DRAFT_STATUS_PUBLISHED)

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
                
                for articleimage in articleplacement.article.articleimage_set.all():
                    if articleimage.shown_on_list:
                        articleplacement.article.list_image = articleimage

            context_data['placements'].append(placement)

        if do_preview:
            article_event_dates = ArticleEventdate.objects.filter(whendate__gte=date.today()).filter(Q(article__draft_status=Article.DRAFT_STATUS_PUBLISHED) | Q(article__draft_status=Article.DRAFT_STATUS_DRAFT) )
        else:
            article_event_dates = ArticleEventdate.objects.filter(whendate__gte=date.today()).filter(article__draft_status=Article.DRAFT_STATUS_PUBLISHED)

        collated_article_event_dates={}

        ical_calendars = []
        ical_supressors = []
        for ical in ICal.objects.all():
            ical_string = requests.get(ical.url).text
            calendar = icalendar.Calendar.from_ical(ical_string)
            ical_calendars.append( calendar )

        for iscsupress in BlockedIcalEvent.objects.all():
            ical_supressors.append(iscsupress.uuid)

        for article_event_date in article_event_dates:

            event = article_event_date.article
            event.source_type = 'article'

            if event.summary == '':
                event.summary = event.content
            if event.summary == '__none__':
                event.summary = ''
            if event.content_format == 'markdown':
                event.content = md.markdown(event.content, extensions=['markdown.extensions.fenced_code'])
            if event.summary_format == 'markdown' or ( event.summary_format == 'same' and event.content_format == 'markdown' ):
                event.summary = md.markdown(event.summary, extensions=['markdown.extensions.fenced_code'])

            if event.summary != event.content and event.readmore > '':
                event.show_readmore = True 
            else:
                event.show_readmore = False

            isokey = article_event_date.whendate.isoformat()
            if isokey in collated_article_event_dates:
                collated_article_event_dates[isokey]['events'].append(event)
            else:
                collated_article_event_dates[isokey]={}
                collated_article_event_dates[isokey]['whendate'] = article_event_date.whendate
                collated_article_event_dates[isokey]['events'] = [ event ]


        for ical_calendar in ical_calendars:
            for icalevent in recurring_ical_events.of(calendar).between(date.today(), date.today() + timedelta( days=100 ) ):
                if icalevent["uid"] not in ical_supressors:

                    if icalevent["DTSTART"].dt.date() >= date.today():
                        isokey = icalevent["DTSTART"].dt.date().isoformat()

                        event_from_ical = {}
                        event_from_ical['source_type'] = 'ical'
                        event_from_ical['slug'] = ''
                        if 'UID' in dict(icalevent.items()):
                            event_from_ical['slug'] = str(dict(icalevent.items())['UID'])
                        event_from_ical['headline'] = icalevent["SUMMARY"]
                        event_from_ical['summary'] = ''
                        if 'DESCRIPTION' in dict(icalevent.items()):
                            event_from_ical['summary'] = dict(icalevent.items())['DESCRIPTION']

                        if isokey in collated_article_event_dates:
                            collated_article_event_dates[isokey]['events'].append(event_from_ical)
                        else:
                            collated_article_event_dates[isokey]={}
                            collated_article_event_dates[isokey]['whendate'] = icalevent["DTSTART"].dt.date()
                            collated_article_event_dates[isokey]['events'] = [ event_from_ical ]


        sorted_collated_article_event_dates = (sorted( collated_article_event_dates.items() ))
        collated_article_event_dates = {}

        for event in sorted_collated_article_event_dates:
            collated_article_event_dates[ event[0] ] = event[1]

        if do_preview:
            context_data['menus']=Menu.objects.filter(Q(draft_status=Menu.DRAFT_STATUS_PUBLISHED) | Q(draft_status=Menu.DRAFT_STATUS_DRAFT))
        else:
            context_data['menus']=Menu.objects.filter(Q(draft_status=Menu.DRAFT_STATUS_PUBLISHED) | Q(draft_status=Menu.DRAFT_STATUS_NO_PREVIEW))


        context_data['event_dates'] = collated_article_event_dates                                      

        return context_data
    

class ArticleDetail(DetailView):
    model=Article
    template_name = '{}/article.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR'])
    context_object_name = 'article'

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        article = self.get_object()

        article_event_dates = {
            'past':[],
            'future':[],
            'only':False,
        }   
        for article_event_date in article.articleeventdate_set.all():
            if article_event_date.whendate < date.today():
                article_event_dates['past'].append(article_event_date.whendate)
            else:
                article_event_dates['future'].append(article_event_date.whendate)

        if article_event_dates['future']:
            article_event_dates['now_or_next'] = article_event_dates['future'].pop(0)
        if article_event_dates['future']:
            article_event_dates['next'] = article_event_dates['future'].pop(0)
        if article_event_dates['past']:
            article_event_dates['previous'] = article_event_dates['past'].pop()


        context_data['event_dates'] = article_event_dates

        for articleimage in article.articleimage_set.all():
            if articleimage.shown_above_content:
                article.above_content_image = articleimage
            if articleimage.shown_below_content:
                article.below_content_image = articleimage


        if article.summary == '':
            article.summary = article.content
        if article.summary == '__none__':
            article.summary = ''
        if article.content_format == 'markdown':
            article.content = md.markdown(article.content, extensions=['markdown.extensions.fenced_code'])
        if article.summary_format == 'markdown' or ( article.summary_format == 'same' and article.content_format == 'markdown' ):
            article.summary = md.markdown(article.summary, extensions=['markdown.extensions.fenced_code'])

        context_data['article'] = article
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
        for icalevent in recurring_ical_events.of(calendar).between(date.today(), date.today() + timedelta( days=100 ) ):

            dict_items = dict(icalevent.items())
            if dict_items["UID"] == uuid:

                event_from_ical['slug'] = ''
                event_from_ical['headline'] = icalevent["SUMMARY"]
                event_from_ical['summary'] = ''
                if 'DESCRIPTION' in dict_items:
                    event_from_ical['content'] = dict_items['DESCRIPTION']

                break

    return TemplateResponse( request, '{}/ical_event.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR']), { "event": event_from_ical } )   


