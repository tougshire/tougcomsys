from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from touglates.views import window_closer
from . import views

app_name = 'tougcomsys'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('tougcomsys:homepage'))),
    path('homepage/', views.HomePage.as_view(), name='homepage'),
    path('page/<int:page>/', views.HomePage.as_view(), name='page'),
    path('article/<slug:slug>/', views.ArticleDetail.as_view(), name='article'),
    path('_/article/create/', views.ArticleCreate.as_view(), name='article_create'),
    path('_/article/image/create/', views.ImageCreate.as_view(), name='article_image_create', kwargs={'popup':'popup'}),
    path('article/<slug:article>/comment/create/', views.CommentCreate.as_view(), name='comment_create'),
    path('comment/<int:to>/comment/create/', views.CommentCreate.as_view(), name='comment_create'),
    path('article/<slug:article>/subscription/create/', views.SubscriptionCreate.as_view(), name='subscription_create'),
    path('subscription/<int:pk>/delete/', views.SubscriptionDelete.as_view(), name='subscription_delete'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    path('ical_event/<str:ical_url>/<str:uid>/', views.IcalEventView.as_view(), name='ical_event'),
    path('ical_text/0/', views.get_ical_text, name='ical_text'),
    path('ical_text/<int:pk>/', views.get_ical_text, name='ical_text'),
    path('ical_event/<str:uuid>/', views.ical_detail_view, name='ical_detail'),
    path('window_closer/<str:app_name>/<str:model_name>/<int:pk>/', window_closer, name='window_closer')

]   
