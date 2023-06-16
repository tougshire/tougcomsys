from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = 'tougcomsys'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('tougcomsys:homepage'))),
    path('homepage/', views.HomePage.as_view(), name='homepage'),
    path('article/<slug:slug>/', views.ArticleDetail.as_view(), name='article'),
    path('ical_text/0/', views.get_ical_text, name='ical_text'),
    path('ical_text/<int:pk>/', views.get_ical_text, name='ical_text'),
    path('ical_event/<str:uuid>/', views.ical_detail_view, name='ical_detail'),

    # path('page/<slug:slug>/', views.PageDetail.as_view(), name='page'),
    # path('event/<slug:slug>/', views.EventDetail.as_view(), name='event')

]   
