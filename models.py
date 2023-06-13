from django.db import models
from datetime import datetime, date
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse

class Image(models.Model):
    title = models.CharField(
        'Title',
        max_length=100,
        help_text="The title of the image"
    )
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The user who uploaded this image"
    )
    created=models.DateTimeField(
        'created',
        auto_now_add=True,
        help_text="The date/time this image was created"
    )
    file = models.ImageField(
        null=True,
        blank=True,
        upload_to='gallery/',
        help_text='The file to be uploaded - can be blank if URL is entered and no file needs to be uploaded - Is removed once saved'
    )
    url = models.URLField(
        'URL',
        blank=True,
        help_text='The URL.  This will be overwritten if a file is uploaded'
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
        ordering = ('-created',)


class Placement(models.Model):
    SHOW_NO = 0
    SHOW_YES = 1
    SHOW_CHOICES = [
        (SHOW_NO, "No"),
        (SHOW_YES, "Yes"),
    ]

    title=models.CharField(
        'title',
        max_length=100,
        blank=True,
        help_text='The title to be displayed for this placement'
    )
    place_number = models.IntegerField(
        help_text="A number to help determine where posts of this placement appear the template."
    )
    show_author = models.IntegerField(
        'show author',
        choices = SHOW_CHOICES,
        default=SHOW_NO,
        help_text="If the author should be shown in the list of posts. This is just a flag - the template has to be coded appropriately for this to work"
    )
    show_created = models.IntegerField(
        choices = SHOW_CHOICES,
        default=SHOW_NO,
        help_text="If the creation date should be shown in the list of posts. This is just a flag - the template has to be coded appropriately for this to work"
    )

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ('place_number',)
    
#     
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
        (SHOW_COMPLY, "Use Placement Choice")
    ]
    headline = models.CharField(
        'Headline',
        max_length=100,
        help_text="The title or headline of the article"
    )
    subheadline = models.CharField(
        'Sub Headline',
        max_length=100,
        blank=True,
        help_text="The optional subtitle or subheadline of the article"
    )
    content_format = models.CharField(
        'content format',
        max_length=20,
        choices=(
            ('markdown', 'markdown'),
            ('html','html'),
        ),
        default='markdown',
        help_text="The format (or markup method) used for the content"
    )
    content = models.TextField(
        "content",
        blank=True,
        help_text="The content of the post"
    )
    summary_format = models.CharField(
        'summary format',
        max_length=20,
        choices=(
            ('same', 'same as content'),
            ('markdown', 'markdown'),
            ('html','html'),
        ),
        default='same',
        help_text="The format (or markup method) used for the summary"
    )
    summary = models.TextField(
        "summary",
        blank=True,
        help_text="A shorter version of the content"
    )
    readmore = models.CharField(
        'read more text',
        max_length=30,
        default = 'Read More', 
        blank=True,
        help_text='The text to use for the "read more" link '
    )
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who created ths article"
    )
    show_author = models.IntegerField(
        'show author',
        choices=SHOW_CHOICES,
        default=SHOW_COMPLY,
        help_text="If the author should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work"
    )
    show_updated = models.IntegerField(
        'show updated',
        choices=SHOW_CHOICES,
        default=SHOW_COMPLY,
        help_text="If the updated date should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work"
    )
    created_date=models.DateTimeField(
        'created',
        auto_now_add=True,
        help_text="The date/time this article was created"
    )
    updated_date=models.DateTimeField(
        'updated',
        auto_now=True,
        help_text="The date/time this article was created"
    )
    sortable_date=models.DateTimeField(
        'sortable date',
        default=datetime.now,
        null=True,
        help_text="The modifiable date used for sorting, normally used only if this is a post, and in the admin panel for pages.  Later dates normally appear list earlier dates"
    )
    sticky=models.BooleanField(
        'sticky',
        default=False,
        help_text='If this post is stuck to the top. This is used before sortable date'
    )
    draft_status = models.IntegerField(
        "draft status",
        choices = [
            (DRAFT_STATUS_PUBLISHED, 'published'),
            (DRAFT_STATUS_ARCHIVED, 'archived'),
            (DRAFT_STATUS_DRAFT, 'draft'),
        ],
        default=0,
        help_text="If this post is a draft, which only displays in preview mode"
    )

    slug = models.SlugField(
        "slug",
        help_text = "The slug used to refer to this article"
    )

    def get_absolute_url(self): 
        return reverse("post_detail", kwargs={"slug": self.slug}) 

    def save(self, *args, **kwargs):   
        if not self.slug > "":
            self.slug = slugify(self.headline)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('tougcomsys:article', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-sticky', '-sortable_date',)

class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        help_text='The article to which the image is attached'
    )
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text = 'The image to add to the article'
    )
    shown_on_list = models.BooleanField(
        'shown on list',
        default=False,
        help_text='If this image should be displayed with this article\'s headline and summary on a list of articles'
    )
    shown_above_content = models.BooleanField(
        'shown above content',
        default=False,
        help_text='If this image should be displayed above the content in a detail view of the articles'
    )
    shown_below_content = models.BooleanField(
        'shown below content',
        default=False,
        help_text='If this image should be displayed below the content in a detail view of the articles'
    )
    is_featured = models.BooleanField(
        'is featured',
        default=False,
        help_text='If this image should be featured, for use in Social Media links'
    )
    list_image_attributes = models.CharField(
        "list image attributes",
        max_length=200,
        blank=True,
        help_text='The attributes (ie style="width:60%") for the image for if/when the image is displayed list content',
    )
    list_image_link = models.URLField(
        "list image link",
        blank=True,
        help_text='The link for the image if/when displayed list content',
    )
    list_image_link_attributes = models.CharField(
        "list image link attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for if/when the image is displayed list content',
    )

    above_content_image_attributes = models.CharField(
        "above content image attributes",
        max_length=200,
        blank=True,
        help_text='The attributes (ie style="width:60%") for the image for if/when the image is displayed in a list',
    )
    above_content_image_link = models.URLField(
        "above content image link",
        blank=True,
        help_text='The link for the image if/when displayed list content',
    )
    above_content_link_attributes = models.CharField(
        "above content link attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for if/when the image is displayed list content',
    )
    below_content_image_attributes = models.CharField(
        "below content image attributes",
        max_length=200,
        blank=True,
        help_text='The attributes (ie style="width:60%") for the image for if/when the image is displayed below content',
    )
    below_content_image_link = models.URLField(
        "below content image link",
        blank=True,
        help_text='The link for the image if/when displayed below content',
    )
    below_content_link_attributes = models.CharField(
        "below content link attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for if/when the image is displayed below content',
    )

class ArticlePlacement(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        help_text="The article which is to be placed on the site"
    )
    placement=models.ForeignKey(
        Placement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The placement on the home page"
    )

class ArticleEventdate(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        help_text="If the article is an event, the article to which this event date belongs"
    )
    whendate = models.DateField(
        'date',
        help_text="If the article is an event, the date of the event"
    )
    whentime = models.TimeField(
        'time',
        blank=True,
        null=True,
        help_text='The start time of the event'
    )
    timelen = models.IntegerField(
        'length(minutes)',
        default=0,
        help_text = 'The length of time for the event in minutes'
    )

    def __str__(self):
        return '{} -> {}'.format(self.article, self.whendate)

    class Meta:
        ordering = ('whendate', '-whentime', 'article')

class ICal(models.Model):
    name = models.CharField(
        'name',
        max_length=50,
        blank=True,
        help_text = 'An optional name to be given to this calendar.'
    )
    url = models.URLField(
        'url',
        help_text = 'The URL of the external calendar'
    )

    def __str__( self ):
        return self.name if self.name > '' else self.url
    
class BlockedIcalEvent(models.Model):

    name = models.CharField(
        'name',
        max_length=50,
        blank=True,
        help_text = 'An optional name to be given to this event.'
    )

    uuid = models.CharField(
        'uuid',
        max_length=264,
        help_text = 'The UUID of the external event to be supressed'
    )

    def __str__( self ):
        return self.name if self.name > '' else self.uuid

class Menu(models.Model):
    DRAFT_STATUS_PUBLISHED = 7
    DRAFT_STATUS_NO_PREVIEW = 5
    DRAFT_STATUS_DRAFT = 0
    DRAFT_STATUS_CHOICES =[
        ( DRAFT_STATUS_PUBLISHED, "Published" ),
        ( DRAFT_STATUS_NO_PREVIEW, "No Preview" ),
        ( DRAFT_STATUS_DRAFT, "Draft" )
    ]


    name = models.CharField(
        max_length=30,
        help_text='The name of the menu'
    )
    sort_name = models.SlugField(
        'sorting name',
        blank=True,
        help_text='A name for sorting.  The menu with the alphabetically earliest sort name is considered the main menu'
    )
    draft_status = models.IntegerField(
        choices = DRAFT_STATUS_CHOICES,
        default=DRAFT_STATUS_DRAFT,
        help_text='The status of this menu.'
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):   
        if not self.sort_name > "":
            self.sort_name = slugify(self.name)
        super().save(*args, **kwargs) 


class MenuLink(models.Model):
    label = models.CharField(
        'label',
        max_length=100,
        help_text="The default label when added to menus"
    )
    article = models.ForeignKey(
        Article,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='The article that this item links to - can be blank if URL is entered and no article needs to be chosen. Removed and replaced by URL of article when this link is saved.'
    )
    url = models.CharField(
        'URL',
        max_length=250,
        blank=True,
        help_text='The URL.  This will be overwritten if an article is chosen'
    )

    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        update_url = False

        if self.article:
            update_url = True

        super().save(*args, **kwargs)

        if update_url:
            self.url = self.article.get_absolute_url()
            self.file = None

        super().save(*args, **kwargs)

class Menuitem(models.Model):
    label = models.CharField(
        'label',
        max_length=100,
        blank=True,
        help_text='The label of the menu item.  If left blank, the label of the link will be used'
    )
    link = models.ForeignKey(
        MenuLink,
        null=True,
        on_delete=models.CASCADE,
        help_text = 'The link that this menu item links to'
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        help_text='The menu to which this item is attached'
    )
    sort_name = models.CharField(
        max_length=20,
        blank=True,
        help_text='A name for sorting.  The item with the alphabetically earliest sort name is first'
    )
    def __str__(self):
        return '{}=>{}'.format(self.menu, self.label)
    
    def save(self, *args, **kwargs):   
        if not self.label > "":
            self.label = self.link.label
        if not self.sort_name > "":
            self.sort_name = slugify(self.label)

        super().save(*args, **kwargs) 
