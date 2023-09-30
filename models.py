import re
from django.db import models
from datetime import datetime, date, timedelta
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models.functions import Upper
from django.core.exceptions import ValidationError
from feeds.models import Source


def plus_366():
    return date.today() + timedelta(days=366)


class Image(models.Model):
    title = models.CharField(
        "Title", max_length=100, help_text="The title of the image"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The user who uploaded this image",
    )
    created = models.DateTimeField(
        "created", auto_now_add=True, help_text="The date/time this image was created"
    )
    file = models.ImageField(
        null=True,
        blank=True,
        upload_to="gallery/",
        help_text="The file to be uploaded - can be blank if URL is entered and no file needs to be uploaded - Is removed once saved",
    )
    alt_text = models.CharField(
        "alt text",
        max_length=255,
        blank=True,
        help_text="The alternet text for the image",
    )

    url = models.URLField(
        "URL",
        blank=True,
        help_text="The URL.  This will be overwritten if a file is uploaded",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        update_url = False

        if self.file:
            update_url = True

        super().save(*args, **kwargs)

        if update_url:
            self.url = self.file.url
            self.file = None

        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created",)


class Page(models.Model):
    HOME_NO = 0
    HOME_YES = 1
    HOME_CHOICES = [
        (HOME_NO, "No"),
        (HOME_YES, "Yes"),
    ]

    name = models.CharField("name", max_length=30, help_text="The name of the page")

    is_home = models.IntegerField(
        choices=HOME_CHOICES,
        default=HOME_NO,
        help_text="If this is the home page.  Only one will be used as home page even if more than one is chosen",
    )

    def __str__(self):
        return "{}{}".format(self.name, " (Home)" if self.is_home else "")

    def get_absolute_url(self):
        return reverse("tougcomsys:page", kwargs={"page": self.pk})

    class Meta:
        ordering = (
            "-is_home",
            "pk",
        )


class Placement(models.Model):
    SHOW_NO = 0
    SHOW_YES = 1
    SHOW_CHOICES = [
        (SHOW_NO, "No"),
        (SHOW_YES, "Yes"),
    ]

    TYPE_ARTICLE_LIST = 0
    TYPE_EVENT_LIST = 1
    TYPE_FEED = 2
    TYPE_CHOICES = [
        (TYPE_ARTICLE_LIST, "Article List"),
        (TYPE_EVENT_LIST, "Event List"),
        (TYPE_FEED, "Feed"),
    ]

    COLUMNWIDTH_NARROW = "narrow"
    COLUMNWIDTH_WIDE = "wide"
    COLUMNWIDTH_CHOICES = [(COLUMNWIDTH_NARROW, "Narrow"), (COLUMNWIDTH_WIDE, "Wide")]

    FONT_SIZE_XLARGE = "xl"
    FONT_SIZE_LARGE = "l"
    FONT_SIZE_MEDIUM = "m"
    FONT_SIZE_SMALL = "s"
    FONT_SIZE_XSMALL = "xs"
    FONT_SIZE_CHOICES = (
        (FONT_SIZE_XLARGE, "XL"),
        (FONT_SIZE_LARGE, "L"),
        (FONT_SIZE_MEDIUM, "M"),
        (FONT_SIZE_SMALL, "S"),
        (FONT_SIZE_XSMALL, "XS"),
    )
    type = models.IntegerField(
        "type", choices=TYPE_CHOICES, help_text="The type of placement"
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The page on which this placement should appear",
    )
    title = models.CharField(
        "title",
        max_length=100,
        blank=True,
        help_text="The title to be displayed for this placement",
    )
    place_number = models.IntegerField(
        help_text="A number to help determine where posts of this placement appear the template."
    )
    column_width = models.CharField(
        "column width",
        max_length=20,
        blank=True,
        null=True,
        choices=COLUMNWIDTH_CHOICES,
        default=COLUMNWIDTH_NARROW,
        help_text="The width of the column. The template may ingore this setting either completely or for certain media types",
    )
    font_size = models.CharField(
        "font size",
        default="m",
        choices=FONT_SIZE_CHOICES,
        max_length=8,
        help_text="The relative font size. The template may ingore this setting either completely or for certain media types",
    )
    show_title = models.IntegerField(
        "show title",
        choices=SHOW_CHOICES,
        default=SHOW_YES,
        help_text="If the title of the list should be shown. This is just a flag - the template has to be coded appropriately for this to work",
    )
    show_author = models.IntegerField(
        "show author",
        choices=SHOW_CHOICES,
        default=SHOW_NO,
        help_text="If the author should be shown in the list of posts. This is just a flag - the template has to be coded appropriately for this to work",
    )
    show_created = models.IntegerField(
        "show created date",
        choices=SHOW_CHOICES,
        default=SHOW_NO,
        help_text="If the creation date should be shown in the list of posts. This is just a flag - the template has to be coded appropriately for this to work",
    )
    event_list_start = models.IntegerField(
        "event list start",
        default=0,
        help_text="For event lists, the start date of the event list, in days relative to the current date",
    )
    events_list_length = models.IntegerField(
        "event list length",
        default=366,
        help_text="For event lists, length in days of the list",
    )

    def __str__(self):
        return "{} on page {}".format(self.title, self.page)

    class Meta:
        ordering = (
            "page",
            "place_number",
        )


class Article(models.Model):
    DRAFT_STATUS_PUBLISHED = 7
    DRAFT_STATUS_ARCHIVED = 3
    DRAFT_STATUS_DRAFT = 0

    SHOW_NO = 0
    SHOW_YES = 1
    SHOW_COMPLY = 2
    SHOW_CHOICES = [
        (SHOW_NO, "No"),
        (SHOW_YES, "Yes"),
        (SHOW_COMPLY, "Use Placement Choice"),
    ]
    IMAGE_LOCATION_TOP = "top"
    IMAGE_LOCATION_SIDE = "side"
    IMAGE_LOCATION_BOTTOM = "bottom"
    IMAGE_LOCATION_CHOICES = [
        (IMAGE_LOCATION_TOP, "top only"),
        (IMAGE_LOCATION_SIDE, "side or top"),
        (IMAGE_LOCATION_BOTTOM, "bottom only"),
    ]
    COMMENTS_ALLOW = 1
    COMMENTS_NONE = 0
    COMMENTS_CLOSED = -1
    COMMENTS_CHOICES = [
        (COMMENTS_ALLOW, "allow"),
        (COMMENTS_NONE, "none"),
        (COMMENTS_CLOSED, "closed"),
    ]

    headline = models.CharField(
        "Headline", max_length=100, help_text="The title or headline of the article"
    )
    subheadline = models.CharField(
        "Sub Headline",
        max_length=100,
        blank=True,
        help_text="The optional subtitle or subheadline of the article",
    )
    content_format = models.CharField(
        "content format",
        max_length=20,
        choices=(
            ("markdown", "markdown"),
            ("html", "html"),
        ),
        default="markdown",
        help_text="The format (or markup method) used for the content",
    )
    content = models.TextField(
        "content", blank=True, help_text="The content of the post"
    )
    hashtags = models.CharField(
        "hashtags",
        max_length=100,
        blank=True,
        help_text="Hashtags, separated by spaces",
    )
    list_image = models.ForeignKey(
        Image,
        verbose_name="list view image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="list_image",
        help_text="The image to show in list view ",
    )
    list_image_location = models.CharField(
        "list view image location",
        max_length=20,
        choices=IMAGE_LOCATION_CHOICES,
        default=IMAGE_LOCATION_CHOICES[0],
        help_text="The location of the image. This is just a flag which indicates a preference",
    )
    detail_image = models.ForeignKey(
        Image,
        verbose_name="detail image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="detail_image",
        help_text="The image to show in detail view ",
    )
    detail_image_location = models.CharField(
        "detail view image location",
        max_length=20,
        choices=IMAGE_LOCATION_CHOICES,
        default=IMAGE_LOCATION_CHOICES[0],
        help_text="The location of the image. This is just a flag which indicates a preference",
    )
    featured_image = models.ForeignKey(
        Image,
        verbose_name="featured image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="featured_image",
        help_text="The image to show in links to this article, where supported ",
    )

    summary_format = models.CharField(
        "summary format",
        max_length=20,
        choices=(
            ("same", "same as content"),
            ("markdown", "markdown"),
            ("html", "html"),
        ),
        default="same",
        help_text="The format (or markup method) used for the summary",
    )
    summary = models.TextField(
        "summary", blank=True, help_text="A shorter version of the content"
    )
    readmore = models.CharField(
        "read more text",
        max_length=30,
        default="Read More",
        blank=True,
        help_text='The text to use for the "read more" link ',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who created ths article",
    )
    descriptive_date = models.CharField(
        "descriptive date",
        max_length=50,
        blank=True,
        help_text='A descriptive date, such as "New Year\s Day", or "The Third Monday Each Month". Always use this for recurring ical events',
    )
    show_author = models.IntegerField(
        "show author",
        choices=SHOW_CHOICES,
        default=SHOW_COMPLY,
        help_text="If the author should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work",
    )
    show_updated = models.IntegerField(
        "show updated",
        choices=SHOW_CHOICES,
        default=SHOW_COMPLY,
        help_text="If the updated date should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work",
    )
    created_date = models.DateTimeField(
        "created", auto_now_add=True, help_text="The date/time this article was created"
    )
    updated_date = models.DateTimeField(
        "updated", auto_now=True, help_text="The date/time this article was created"
    )
    draft_status = models.IntegerField(
        "draft status",
        choices=[
            (DRAFT_STATUS_PUBLISHED, "published"),
            (DRAFT_STATUS_ARCHIVED, "archived"),
            (DRAFT_STATUS_DRAFT, "draft"),
        ],
        default=0,
        help_text="If this post is a draft, which only displays in preview mode",
    )
    allow_comments = models.IntegerField(
        "allow comments",
        choices=COMMENTS_CHOICES,
        default=0,
        help_text="If comments are allowed",
    )
    slug = models.SlugField(
        "slug",
        max_length=150,
        blank=True,
        help_text="A URL friendly representation - usually a variation of the headline",
    )

    def save(self, *args, **kwargs):
        if not self.slug > "":
            self.slug = slugify(self.headline)
        hashtag_list = re.split("\s*[\s;,]\s*", self.hashtags)
        self.hashtags = " ".join(
            [tag if tag[:1] == "#" else "#" + tag for tag in hashtag_list]
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        if self.slug:
            return reverse(
                "tougcomsys:article", kwargs={"pk": self.pk, "slug": self.slug}
            )
        else:
            return reverse("tougcomsys:article", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-created_date",)


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        help_text="The article which is to be placed on the site",
    )
    in_reply_to = models.ForeignKey(
        "Comment",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The comment to which this comment is a reply",
    )
    in_reply_to_author_str = models.CharField(
        "in reply to author",
        max_length=50,
        blank=True,
        help_text="The author of the comment to which this comment is a reply",
    )
    in_reply_to_created_date = models.TextField(
        "in reply to created",
        blank=True,
        null=True,
        help_text="The date of the comment to which this comment is a reply",
    )

    in_reply_to_text = models.TextField(
        "in reply to",
        blank=True,
        help_text="The text of the comment to which this comment is a reply",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The user who wrote the comment",
    )
    created_date = models.DateField(
        auto_now_add=True, help_text="The date the comment was created"
    )
    comment_text = models.TextField("comment", help_text="The text of the comment")

    def __str__(self):
        return "[{}: {}] {}".format(
            self.created_date, self.author, self.comment_text[:50]
        )

    class Meta:
        ordering = ("created_date",)


class Subscription(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        help_text="The article to which the subscriber is subscribed",
    )
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="The subscriber to the article",
    )

    def __str__(self):
        return "{}->{}".format(self.subscriber, self.article)


class ArticlePlacement(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        help_text="The article which is to be placed on the site",
    )
    placement = models.ForeignKey(
        Placement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The placement on the template (for events - no placement indicates event should be on any calendar)",
    )
    expiration_date = models.DateField(
        "expiration date",
        null=True,
        blank=True,
        help_text="The date that this article should be removed from this placement",
    )
    sortable_date = models.DateTimeField(
        "sortable date",
        default=datetime.now,
        null=True,
        help_text="The modifiable date used for sorting posts, Later dates normally appear list earlier dates",
    )
    sticky = models.BooleanField(
        "sticky",
        default=False,
        help_text="If this post is stuck to the top. This is used before sortable date",
    )

    class Meta:
        ordering = ("article",)


class ArticleEventdate(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        help_text="If the article is an event, the article to which this event date belongs",
    )
    whendate = models.DateField(
        "date", help_text="If the article is an event, the date of the event"
    )
    whentime = models.TimeField(
        "time", blank=True, null=True, help_text="The start time of the event"
    )
    timelen = models.IntegerField(
        "length(minutes)",
        default=0,
        help_text="The length of time for the event in minutes",
    )

    def __str__(self):
        return "{} -> {}".format(self.article, self.whendate)

    class Meta:
        ordering = ("whendate", "-whentime", "article")


class ICal(models.Model):
    name = models.CharField(
        "name",
        max_length=50,
        blank=True,
        help_text="An optional name to be given to this calendar.",
    )
    url = models.URLField("url", help_text="The URL of the external calendar")
    placement = models.ForeignKey(
        Placement,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"type": Placement.TYPE_EVENT_LIST},
        help_text="The placement which should display this ical",
    )

    def __str__(self):
        return self.name if self.name > "" else self.url


class BlockedIcalEvent(models.Model):
    name = models.CharField(
        "name",
        max_length=50,
        blank=True,
        help_text="An optional name to be given to this event.",
    )

    ical = models.ForeignKey(
        ICal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The ical of the event to be blocked",
    )

    uuid = models.CharField(
        "uuid",
        max_length=264,
        help_text="The UUID of the external event to be supressed",
    )

    display_instead = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Display this article instead of the actual ICAL event, on the date of the ical event",
    )

    def __str__(self):
        return self.name if self.name > "" else self.uuid


class FeedSource(models.Model):
    placement = models.ForeignKey(
        Placement,
        on_delete=models.CASCADE,
        null=True,
        help_text="The placement on the template on which this feed should be displayed",
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        help_text="The source (set up in the Feeds app)",
    )

    def __str__(self):
        return self.source.feed_url


class Menu(models.Model):
    DRAFT_STATUS_PUBLISHED = 7
    DRAFT_STATUS_NO_PREVIEW = 5
    DRAFT_STATUS_DRAFT = 0
    DRAFT_STATUS_CHOICES = [
        (DRAFT_STATUS_PUBLISHED, "Published"),
        (DRAFT_STATUS_NO_PREVIEW, "No Preview"),
        (DRAFT_STATUS_DRAFT, "Draft"),
    ]

    name = models.CharField(max_length=30, help_text="The name of the menu")
    page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The page on which this menu should be displayed",
    )
    menu_number = models.IntegerField(
        "menu number",
        help_text="A number to help determine the place of the menu in the template. For the default template, 0 is the pace for a top menu and 1 is the place a side menu",
    )
    draft_status = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES,
        default=DRAFT_STATUS_DRAFT,
        help_text="The status of this menu.",
    )

    def __str__(self):
        return "{} on page {}".format(self.name, self.page)

    class Meta:
        ordering = ("page", "menu_number")


class Menuitem(models.Model):
    label = models.CharField(
        "label",
        max_length=100,
        blank=True,
        help_text="The label of the menu item.  If left blank, the label of the link will be used",
    )

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        help_text="The menu to which this item is attached",
    )

    article = models.ForeignKey(
        Article,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The article that this item links to - can be blank if a page or URL is entered and no article needs to be chosen. Removed and replaced by URL of article or page when this link is saved.",
    )

    page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The page that this item links to - can be blank if article or URL is entered and no page needs to be chosen. Removed and replaced by URL of article or page when this link is saved.",
    )

    url = models.CharField(
        "URL",
        max_length=250,
        blank=True,
        help_text="The URL.  This will be overwritten if an article or page is chosen",
    )

    sort_name = models.CharField(
        max_length=20,
        blank=True,
        help_text="A name for sorting.  The item with the alphabetically earliest sort name is first",
    )

    def __str__(self):
        return "{} on menu {}".format(
            self.label,
            self.menu,
        )

    class Meta:
        ordering = (Upper("sort_name"),)

    def clean(self):
        if self.article and self.page:
            raise ValidationError(
                "A menu item can link to an article or page, but not both"
            )

    def save(self, *args, **kwargs):
        update_url = False

        if self.article or self.page:
            update_url = True

        if update_url:
            self.url = (
                self.article.get_absolute_url()
                if self.article is not None
                else self.page.get_absolute_url()
            )

        if not self.label > "":
            self.label = self.link.label
        if not self.sort_name > "":
            self.sort_name = slugify(self.label)

        super().save(*args, **kwargs)
