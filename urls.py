from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from touglates.views import popup_closer
from . import views

app_name = "tougcomsys"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("tougcomsys:homepage"))),
    path("homepage/", views.HomePage.as_view(), name="homepage"),
    path("page/<int:page>/", views.HomePage.as_view(), name="page"),
    path("article/<int:pk>/", views.ArticleDetail.as_view(), name="article"),
    path(
        "article/<int:pk>-<slug:slug>/", views.ArticleDetail.as_view(), name="article"
    ),
    path("article/list/", views.ArticleList.as_view(), name="article_list"),
    path(
        "article/<int:pk>/update/",
        views.ArticleUpdate.as_view(),
        name="article_update",
    ),
    path(
        "article/<int:pk>/update/page/<int:page>/",
        views.ArticleUpdate.as_view(),
        name="article_update",
    ),
    path("article/create/", views.ArticleCreate.as_view(), name="article_create"),
    path(
        "article/image/create/",
        views.ImageCreate.as_view(),
        name="article_image_create",
        kwargs={"popup": "popup"},
    ),
    path(
        "article/<int:pk>/articleeventdates/",
        views.ArticleArticleEventDates.as_view(),
        name="article_articleeventdates",
    ),
    path(
        "article/<int:pk>/placements/",
        views.ArticlePlacements.as_view(),
        name="article_placements",
    ),
    path(
        "article/<int:pk>/comment/create/",
        views.CommentCreate.as_view(),
        name="comment_create",
    ),
    path(
        "comment/<int:to>/comment/create/",
        views.CommentCreate.as_view(),
        name="comment_create",
    ),
    path(
        "article/<int:pk>/subscription/create/",
        views.SubscriptionCreate.as_view(),
        name="subscription_create",
    ),
    path(
        "article/<int:pk>/content/",
        views.ArticleContent.as_view(),
        name="article_content_only",
    ),
    path(
        "subscription/<int:pk>/delete/",
        views.SubscriptionDelete.as_view(),
        name="subscription_delete",
    ),
    path(
        "comment/<int:pk>/delete/", views.CommentDelete.as_view(), name="comment_delete"
    ),
    path(
        "ical_event/<str:ical_url>/<str:uid>/",
        views.IcalEventView.as_view(),
        name="ical_event",
    ),
    path("ical_text/0/", views.get_ical_text, name="ical_text"),
    path("ical_text/<int:pk>/", views.get_ical_text, name="ical_text"),
    path("ical_event/<str:uuid>/", views.ical_detail_view, name="ical_detail"),
    path(
        "popup_closer/<str:app_name>/<str:model_name>/<int:pk>/",
        popup_closer,
        name="popup_closer",
    ),
]
