from django.db.models import Count, Q
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView,)
from django.views.generic.list import ListView

from datetime import datetime, date

import markdown as md

from tougcomsys.models import Event, EventDate, Page, Placement, Post

class HomePage(TemplateView):

    template_name = '{}/homepage.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR'])

    def get_context_data(self, **kwargs):

        do_preview = self.request.user.is_staff == True and self.request.GET.get('preview').lower() == "true"[:len(self.request.GET.get('preview'))].lower() if 'preview' in self.request.GET else False

        context_data = super().get_context_data(**kwargs)

        if do_preview:
            placements = Placement.objects.annotate(published_qty=Count("post", filter=( Q(post__draft_status=Post.DRAFT_STATUS_PUBLISHED) | Q(post__draft_status=Post.DRAFT_STATUS_DRAFT ) ) )).filter(published_qty__gte=1)
        else:
            placements = Placement.objects.annotate(published_qty=Count("post", filter=(Q(post__draft_status=Post.DRAFT_STATUS_PUBLISHED)))).filter(published_qty__gte=1)

        context_data['places'] = []
        for place in placements:


            if do_preview:
                place.count = place.post_set.filter(Q(draft_status=Post.DRAFT_STATUS_PUBLISHED) | Q(draft_status=Post.DRAFT_STATUS_DRAFT)).count()
                place.posts = place.post_set.all().filter(Q(draft_status=Post.DRAFT_STATUS_PUBLISHED) )
            else:
                place.count = place.post_set.filter(draft_status=Post.DRAFT_STATUS_PUBLISHED).count()
                place.posts = place.post_set.all().filter(draft_status=Post.DRAFT_STATUS_PUBLISHED)

            for post in place.posts:
                
                if post.summary == '':
                    post.summary = post.content
                if post.summary == '__none__':
                    post.summary = ''
                if post.content_format == 'markdown':
                    post.content = md.markdown(post.content, extensions=['markdown.extensions.fenced_code'])
                if post.summary_format == 'markdown' or ( post.summary_format == 'same' and post.content_format == 'markdown' ):
                    post.summary = md.markdown(post.summary, extensions=['markdown.extensions.fenced_code'])
                
            context_data['places'].append(place)

        if do_preview:
            event_dates = EventDate.objects.filter(whenday__gte=date.today()).filter(Q(event__draft_status=Event.DRAFT_STATUS_PUBLISHED) | Q(event__draft_status=Event.DRAFT_STATUS_DRAFT) )
        else:
            event_dates = EventDate.objects.filter(whenday__gte=date.today()).filter(event__draft_status=Event.DRAFT_STATUS_PUBLISHED)

        collated_event_dates={}
        for event_date in event_dates:

            event = event_date.event
            if event.post:
                if event.summary == '':
                    event.summary = event.post.summary
                if event.content == '':
                    event.content = event.post.content

            if event.summary == '':
                event.summary = event.content
            if event.summary == '__none__':
                event.summary = ''
            if event.content_format == 'markdown':
                event.content = md.markdown(event.content, extensions=['markdown.extensions.fenced_code'])
            if event.summary_format == 'markdown' or ( event.summary_format == 'same' and event.content_format == 'markdown' ):
                event.summary = md.markdown(event.summary, extensions=['markdown.extensions.fenced_code'])

            isokey = event_date.whenday.isoformat()
            if isokey in collated_event_dates:
                collated_event_dates[isokey]['events'].append(event)
            else:
                collated_event_dates[isokey]={}
                collated_event_dates[isokey]['whenday'] = event_date.whenday
                collated_event_dates[isokey]['events'] = [ event ]


        context_data['event_dates'] = collated_event_dates

        context_data['footer'] = settings.TOUGCOMSYS['FOOTER_CONTENT']

        return context_data
    
class PostDetail(DetailView):
    model=Post
    template_name = '{}/post.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR'])
    context_object_name = 'post'

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        post = self.get_object()

        print('tp234e800')
        if post.postimage_set.count() > 0:
            print('tp234d759', post.title)

        if post.summary == '':
            post.summary = post.content
        if post.summary == '__none__':
            post.summary = ''

        if post.content_format == 'markdown':
            post.content = md.markdown(post.content, extensions=['markdown.extensions.fenced_code'])

        if post.summary_format == 'markdown' or ( post.summary_format == 'same' and post.content_format == 'markdown' ):
            post.summary = md.markdown(post.summary, extensions=['markdown.extensions.fenced_code'])

        context_data['post'] = post



        context_data['footer'] = settings.TOUGCOMSYS['FOOTER_CONTENT']

        return context_data

class EventDetail(DetailView):
    model=Event
    template_name = '{}/event.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR'])
    context_object_name = 'event'

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        event = self.get_object()

        event_dates = {
            'past':[],
            'future':[],
            'only':False,
        }   
        for event_date in event.eventdate_set.all():
            if event_date.whenday < date.today():
                event_dates['past'].append(event_date.whenday)
            else:
                event_dates['future'].append(event_date.whenday)

        if event_dates['future']:
            event_dates['now_or_next'] = event_dates['future'].pop(0)
        if event_dates['future']:
            event_dates['next'] = event_dates['future'].pop(0)
        if event_dates['past']:
            event_dates['previous'] = event_dates['past'].pop()


        context_data['event_dates'] = event_dates
        
        if event.post:
            if event.summary == '':
                event.summary = event.post.summary
            if event.content == '':
                event.content = event.post.content
 
        if event.summary == '':
            event.summary = event.content
        if event.summary == '__none__':
            event.summary = ''
        if event.content_format == 'markdown':
            event.content = md.markdown(event.content, extensions=['markdown.extensions.fenced_code'])
        if event.summary_format == 'markdown' or ( event.summary_format == 'same' and event.content_format == 'markdown' ):
            event.summary = md.markdown(event.summary, extensions=['markdown.extensions.fenced_code'])
        context_data['event'] = event

        context_data['footer'] = settings.TOUGCOMSYS['FOOTER_CONTENT']

        return context_data

class PageDetail(DetailView):
    model=Page
    template_name = '{}/page.html'.format(settings.TOUGCOMSYS['TEMPLATE_DIR'])
    context_object_name = 'page'

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        page = self.get_object()
        if page.content_format == 'markdown':
            page.content = md.markdown(page.content, extensions=['markdown.extensions.fenced_code'])
        context_data['page'] = page

        context_data['footer'] = settings.TOUGCOMSYS['FOOTER_CONTENT']

        return context_data
