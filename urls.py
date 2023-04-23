from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = 'tougcomsys'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('tougcomsys:homepage'))),
    path('homepage/', views.HomePage.as_view(), name='homepage'),
    path('article/<slug:slug>/', views.ArticleDetail.as_view(), name='article'),
    # path('page/<slug:slug>/', views.PageDetail.as_view(), name='page'),
    # path('event/<slug:slug>/', views.EventDetail.as_view(), name='event')

]   
