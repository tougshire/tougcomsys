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
    
class Post(models.Model):
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

    title = models.CharField(
        'Title',
        max_length=100,
        help_text="The title of the thread"
    )
    list_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display above the title, and to use for social media graphs'
    )
    above_content_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display above the content, and to use for social media graphs',
        related_name="post_above_content_image"
    )
    above_content_image_attributes = models.CharField(
        "above content image attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie style="width:60%") for the image for the image displayed above content',
    )
    above_content_image_link = models.URLField(
        "above content image link",
        blank=True,
        help_text='The link for the image displayed above content',
    )
    above_content_link_attributes = models.CharField(
        "above content link attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for the image displayed above content',
    )
    below_content_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display below the content, and to use for social media graphs if no above_content image is set',
        related_name="post_below_content_image"
    )
    below_content_image_attributes = models.CharField(
        "below content image attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie style="width:60%") for the image for the image displayed below content',
    )
    below_content_image_link = models.URLField(
        "below content image link",
        blank=True,
        help_text='The link for the image displayed below content',
    )
    below_content_link_attributes = models.CharField(
        "below content link attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for the image displayed below content',
    )
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who created ths thread"
    )
    created=models.DateTimeField(
        'created',
        auto_now_add=True,
        help_text="The date/time this therad was created"
    )
    sortable_date=models.DateTimeField(
        'sortable date',
        default=datetime.now,
        null=True,
        help_text="The modifiable date used for sorting. This is the created date by default. To move a post up, select a future date."
    )
    sticky=models.BooleanField(
        'sticky',
        default=False,
        help_text='If this post is stuck to the top. This is used before sortable date'
    )
    show_author = models.IntegerField(
        'show author',
        choices=SHOW_CHOICES,
        default=SHOW_COMPLY,
        help_text="If the author should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work"
    )
    show_created = models.IntegerField(
        'show created',
        choices=SHOW_CHOICES,
        default=SHOW_COMPLY,
        help_text="If the creation date should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work"
    )
    placement=models.ForeignKey(
        Placement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The place on the home page"
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
        unique=True,
        help_text="The code that provides a character based ID for this page"
    )

    def get_absolute_url(self): 
        return reverse("post_detail", kwargs={"slug": self.slug}) 

    def save(self, *args, **kwargs):   
        if not self.slug > "":
            self.slug = slugify(self.title)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-sticky', '-sortable_date',)
    
class Event(models.Model):
    DRAFT_STATUS_PUBLISHED = 7
    DRAFT_STATUS_ARCHIVED = 3
    DRAFT_STATUS_DRAFT = 0

    title = models.CharField(
        'title',
        max_length=100,
        help_text="The title of the thread"
    )
    list_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display above the title, and to use for social media graphs'
    )
    above_content_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display above the content, and to use for social media graphs',
        related_name="event_above_content_image"
    )
    above_content_image_link = models.URLField(
        "above content image link",
        blank=True,
        help_text='The link for the image displayed above content',
    )
    above_content_image_attributes = models.CharField(
        "above content image attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie style="width:60%") for the image for the image displayed above content',
    )
    above_content_link_attributes = models.CharField(
        "above content link attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for the image displayed above content',
    )
    below_content_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display below the content, and to use for social media graphs if no above_content image is set',
        related_name="event_below_content_image"
    )
    below_content_image_attributes = models.CharField(
        "below content image attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie style="width:60%") for the image for the image displayed below content',
    )

    below_content_image_link = models.URLField(
        "below content image link",
        blank=True,
        help_text='The link for the image displayed below content',
    )
    below_content_link_attributes = models.CharField(
        "below content link attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for the image displayed below content',
    )
    starttime = models.TimeField(
        'starting',
        blank=True,
        null=True,
        help_text='The start time of the event'
    )
    lenmin = models.IntegerField(
        'length(minutes)',
        blank=True,
        default=0,
        help_text='How long the event lasts (0 indicates indefinite or unkown)'
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
        'content format',
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
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text = 'The post to use as the content and summary.  If selected, the post content and summary will be used instead of the event\'s content and summary'
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
        unique=True,
        help_text="The code that provides a character based ID for this page"
    )

    def get_absolute_url(self): 
        return reverse("event_detail", kwargs={"slug": self.slug}) 
    
    def save(self, *args, **kwargs):   
        if not self.slug > "":
            self.slug = slugify(self.title)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title

    class Meta:
        ordering=['starttime', 'lenmin']    

class EventDate(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        help_text="The event to which this date belongs"
    )
    whenday = models.DateField(
        'date',
        help_text="The date of the event"
    )

    def __str__(self):
        return '{} -> {}'.format(self.event, self.whenday)

    class Meta:
        ordering = ('whenday','event')

class Page(models.Model):
    DRAFT_STATUS_PUBLISHED = 7
    DRAFT_STATUS_ARCHIVED = 3
    DRAFT_STATUS_DRAFT = 0
    title = models.CharField(
        'Title',
        max_length=100,
        help_text="The title of the thread"
    )
    above_content_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display above the content, and to use for social media graphs',
        related_name="page_above_content_image"
    )
    above_content_image_link = models.URLField(
        "above content image link",
        blank=True,
        help_text='The link for the image displayed above content',
    )
    above_content_link_attributes = models.CharField(
        "above content attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for the image displayed above content',
    )
    below_content_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The image to display below the content, and to use for social media graphs if no above_content image is set',
        related_name="page_below_content_image"
    )
    below_content_image_link = models.URLField(
        "below content image link",
        blank=True,
        help_text='The link for the image displayed below content',
    )
    below_content_link_attributes = models.CharField(
        "below content attributes",
        max_length=70,
        blank=True,
        help_text='The attributes (ie target="_blank") for the link for the image displayed below content',
    )

    slug = models.SlugField(
        unique=True,
        help_text="The code that provides a character based ID for this page"
    )
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who created ths thread"
    )
    created=models.DateTimeField(
        'created',
        auto_now_add=True,
        help_text="The date/time this therad was created"
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
    list_order = models.CharField(
        max_length=1,
        blank=True,
        default='~',
        help_text="A character to determine the place on the list. Numbers are higher than capital letters, which are higher than small letters"
    )
    draft_status = models.IntegerField(
        "draft status",
        choices = [
            (DRAFT_STATUS_PUBLISHED, 'published'),
            (DRAFT_STATUS_ARCHIVED, 'archived'),
            (DRAFT_STATUS_DRAFT, 'draft'),
        ],
        default=0,
        help_text="If this page is a draft, which only displays in preview mode"
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self): 
        return reverse("page_detail", kwargs={"slug": self.slug}) 
    
    def save(self, *args, **kwargs):   
        if not self.slug > "":
            self.slug = slugify(self.title)
        super().save(*args, **kwargs) 

    class Meta:
        ordering = ('list_order', '-created',)

class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        help_text="The post which includes the image"
    )
    image = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text = "The image included in the post.  Optional if URL is set"
    )
    url = models.URLField(
        "URL",
        blank=True,
        help_text = "The URL of the image. Leave blank to use the Image field. URL will override the image field if URL is not blank"
    )
    slug = models.SlugField(
        "slug",
        help_text = "The slug used to refer to the image in this post (refer to the image with {{ img:my-image }}) if my-image is the slug"
    )

    def __str__(self):
        return self.slug