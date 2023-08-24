from django.db import models
from wagtailsvg.models import Svg
from wagtailsvg.edit_handlers import SvgChooserPanel
from wagtail.admin.panels import MultiFieldPanel, FieldPanel


class MenuModel(models.Model):
    menu_subtitle = models.CharField(max_length=200, default="")
    menu_icon = models.ForeignKey(
        Svg, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    menu_panel = [
        MultiFieldPanel(
            [
                FieldPanel("menu_subtitle"),
                SvgChooserPanel("menu_icon"),
            ],
            heading="Menu settings",
        ),
    ]

    class Meta:
        abstract = True
