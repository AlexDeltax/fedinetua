from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel
from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page, Orderable

from core.models import MenuModel


class HomePage(Page):
    pass


class HeaderSection(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    text = blocks.RichTextBlock(features=["bold", "italic"])

    class Meta:
        icon = "openquote"
        label = "Header"
        template = "home/sections/tpl_header_section.html"


class Servers(Page, MenuModel):
    template = "home/tpl_servers_page.html"

    body = StreamField(
        [
            ("header", HeaderSection()),
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
        InlinePanel("server_instances", label=_("Instances")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("seo_img"),
    ]

    settings_panels = Page.settings_panels + MenuModel.menu_panel


class Instance(TimeStampedModel, Orderable):
    page = ParentalKey(
        Servers, on_delete=models.CASCADE, related_name="server_instances"
    )
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Image"),
        help_text=_("Image for instance"),
    )
    description = RichTextField(
        verbose_name=_("Description"),
        blank=True,
        default="",
        features=["bold", "italic"],
    )
    url = models.URLField()
    is_private = models.BooleanField(default=False)

    panels = [
        FieldPanel("title"),
        FieldPanel("image"),
        FieldPanel("description"),
        FieldPanel("url"),
        FieldPanel("is_private"),
    ]
