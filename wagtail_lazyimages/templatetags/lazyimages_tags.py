from io import BytesIO

from django import template
from django.core.files.base import ContentFile
from PIL import Image, ImageFilter
from wagtail.images.templatetags.wagtailimages_tags import image, ImageNode
from wagtail.images.shortcuts import get_rendition_or_not_found

register = template.Library()


def _get_placeholder_url(rendition):
    storage = rendition.image._meta.get_field("file").storage
    img = Image.open(storage.open(rendition.file.name, "rb"))

    # Resize and blur image
    img.thumbnail([128, 128])
    lazy_img = img.filter(ImageFilter.GaussianBlur(3))

    lazy_img_io = BytesIO()
    lazy_img.save(lazy_img_io, format=img.format)

    lazy_img_path = "{}_lazy.{}".format(*rendition.file.name.rsplit(".", 1))
    if not storage.exists(lazy_img_path):
        cf = ContentFile(lazy_img_io.getvalue(), lazy_img_path)
        lazy_img_path = storage.save(lazy_img_path, cf)

    return rendition.url.replace(rendition.file.name, lazy_img_path)


@register.filter
def lazy_image_url(rendition):
    return _get_placeholder_url(rendition)


class LazyImageNode(ImageNode):
    def render(self, context):
        img_tag = super().render(context)
        image = self.image_expr.resolve(context)
        rendition = get_rendition_or_not_found(image, self.filter)
        placeholder_url = _get_placeholder_url(rendition)
        if img_tag:
            img_tag = img_tag.replace(
                "src=", "src=\"{}\" data-src=".format(placeholder_url))
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
