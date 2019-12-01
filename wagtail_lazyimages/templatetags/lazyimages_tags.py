from io import BytesIO

from django import template
from django.core.files.base import ContentFile
from PIL import Image, ImageFilter

try:
    # Wagtail 2.x
    from wagtail.images.shortcuts import get_rendition_or_not_found
    from wagtail.images.templatetags.wagtailimages_tags import image, ImageNode
except ImportError:
    # Wagtail 1.x
    from wagtail.wagtailimages.shortcuts import get_rendition_or_not_found
    from wagtail.wagtailimages.templatetags.wagtailimages_tags import (
        image, ImageNode)

register = template.Library()


def _get_placeholder_url(rendition):
    storage = rendition.image._meta.get_field("file").storage
    if not storage.exists(rendition.file.name):
        return

    img = Image.open(storage.open(rendition.file.name, "rb"))
    img_format = img.format

    # Resize and blur image
    img.thumbnail([128, 128])

    if img.mode != "RGBA":
        img = img.convert("RGB")

    lazy_img = img.filter(ImageFilter.GaussianBlur(3))

    lazy_img_io = BytesIO()
    lazy_img.save(lazy_img_io, format=img_format)

    lazy_img_path = "{}_lazy.{}".format(*rendition.file.name.rsplit(".", 1))
    if not storage.exists(lazy_img_path):
        cf = ContentFile(lazy_img_io.getvalue(), lazy_img_path)
        lazy_img_path = storage.save(lazy_img_path, cf)

    return rendition.url.replace(rendition.file.name, lazy_img_path)


@register.simple_tag
def lazy_image_url(rendition):
    return _get_placeholder_url(rendition)


class LazyImageNode(ImageNode):
    def render(self, context):
        img_tag = super().render(context)
        image = self.image_expr.resolve(context)
        if not image:
            return ""
        rendition = get_rendition_or_not_found(image, self.filter)
        if img_tag:
            lazy_attr = str(self.attrs.pop('lazy_attr', '"data-src"'))[1:-1]
            attrs = {
                "src": _get_placeholder_url(rendition),
                lazy_attr: rendition.url,
            }
            for key in self.attrs:
                attrs[key] = self.attrs[key].resolve(context)
            img_tag = rendition.img_tag(attrs)
        return img_tag


@register.tag(name="lazy_image")
def lazy_image(parser, token):
    node = image(parser, token)
    return LazyImageNode(
        node.image_expr,
        node.filter_spec,
        attrs=node.attrs,
        output_var_name=node.output_var_name
    )
