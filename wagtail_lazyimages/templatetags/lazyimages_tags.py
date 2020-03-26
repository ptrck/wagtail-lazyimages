from io import BytesIO

from django import template
from django.core.files.base import ContentFile
from django.forms.utils import flatatt
from PIL import Image, ImageFilter

try:
    # Wagtail 2.x
    from wagtail.images.shortcuts import get_rendition_or_not_found
    from wagtail.images.templatetags.wagtailimages_tags import image, ImageNode
except ImportError:
    # Wagtail 1.x
    from wagtail.wagtailimages.shortcuts import get_rendition_or_not_found
    from wagtail.wagtailimages.templatetags.wagtailimages_tags import image, ImageNode

register = template.Library()


def _generate_placeholder_image(rendition, path, storage):
    with Image.open(storage.open(rendition.file.name, "rb")) as img:
        img_format = img.format
        img.thumbnail([128, 128])

        # Gaussian filter needs RGB(A) so we convert anything else to RGB first
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        lazy_img = img.filter(ImageFilter.GaussianBlur(3))

        lazy_img_io = BytesIO()
        lazy_img.save(lazy_img_io, format=img_format)
        cf = ContentFile(lazy_img_io.getvalue(), path)
        storage.save(path, cf)


def _get_placeholder_url(rendition):
    storage = rendition.image._meta.get_field("file").storage
    if not storage.exists(rendition.file.name):
        return

    lazy_img_path = "{}_lazy.{}".format(*rendition.file.name.rsplit(".", 1))
    lazy_url = rendition.url.replace(rendition.file.name, lazy_img_path)

    if not storage.exists(lazy_img_path):
        _generate_placeholder_image(rendition, lazy_img_path, storage)

    return lazy_url


class LazyImageNode(ImageNode):
    def render(self, context):
        image = self.image_expr.resolve(context)
        if not image:
            return ""

        rendition = get_rendition_or_not_found(image, self.filter)
        rendition.lazy_url = _get_placeholder_url(rendition)

        lazy_attr = str(self.attrs.pop("lazy_attr", '"data-src"'))[1:-1]
        lazy_attrs = {"src": rendition.lazy_url, lazy_attr: rendition.url}

        if self.output_var_name:
            attrs = dict(rendition.attrs_dict, **lazy_attrs)
            rendition.lazy_attrs = flatatt(attrs)
            context[self.output_var_name] = rendition
            return ""

        return rendition.img_tag(lazy_attrs)


@register.tag(name="lazy_image")
def lazy_image(parser, token):
    node = image(parser, token)
    return LazyImageNode(
        node.image_expr,
        node.filter_spec,
        attrs=node.attrs,
        output_var_name=node.output_var_name,
    )
