from django.db import models
from django.utils.translation import gettext as _

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from core.models import MenuModel
from core.utils import items_pagination


class Home(Page):
    template = "blog/tpl_blog.html"

    def get_context(self, request, *args, **kwargs):
        context = super(Home, self).get_context(request, *args, **kwargs)
        context["blog_home"] = self
        context["categories"] = Category.objects.live()
        context["posts"] = items_pagination(self.get_posts(), request, count=7)
        return context

    def get_posts(self):
        return Post.objects.live().order_by("-first_published_at")

    subtitle = models.CharField(max_length=150, blank=True, default="")
    body = StreamField(
        [
            ("html", blocks.RawHTMLBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    seo_img = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image",
        help_text="Image for social media, size 1200×628 pixels",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("seo_img"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.Category"]

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blog")


class Category(Page, MenuModel):
    template = "blog/tpl_blog.html"

    def get_context(self, request, *args, **kwargs):
        context = super(Category, self).get_context(request, *args, **kwargs)
        context["blog_home"] = self.get_parent().specific
        context["category_id"] = self.id
        context["categories"] = Category.objects.live()
        context["posts"] = items_pagination(self.articles(), request, count=7)
        return context

    def articles(self):
        return Post.objects.live().child_of(self).order_by("-first_published_at")

    subtitle = models.CharField(max_length=150, blank=True, default="")
    body = StreamField(
        [
            ("html", blocks.RawHTMLBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    seo_img = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image",
        help_text="Image for social media, size 1200×628 pixels",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("seo_img"),
    ]

    settings_panels = Page.settings_panels + MenuModel.menu_panel

    parent_page_types = ["blog.Home"]
    subpage_types = ["blog.Post"]

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")


class Post(Page):
    template = "blog/tpl_post_page.html"

    body = StreamField(
        [
            ("text", blocks.RichTextBlock()),
            ("html", blocks.RawHTMLBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    seo_img = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Image"),
        help_text=_("Image for social media, size 1200×628 pixels"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("seo_img"),
    ]

    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
