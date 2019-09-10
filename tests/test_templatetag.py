import tempfile
from django.template import Context, Template
from django.test import TestCase, override_settings
from PIL import Image as PImage

try:
    # Wagtail 2.x
    from wagtail.images.models import Image
    from wagtail.images.tests.utils import (
        get_test_image_file,
        get_test_image_file_jpeg
    )
except ImportError:
    # Wagtail 1.x
    from wagtail.wagtailimages.models import Image
    from wagtail.wagtailimages.tests.utils import (
        get_test_image_file,
        get_test_image_file_jpeg
    )


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class TestLazyImageTemplateTag(TestCase):
    def _generate_image(self, filetype):
        if filetype == "jpeg":
            image_file = get_test_image_file_jpeg(size=(1280, 720))
        else:
            image_file = get_test_image_file(size=(1280, 720))
        return Image.objects.create(title="Test", file=image_file)

    def _generate_rendition(self, filetype, filter_spec):
        image = self._generate_image(filetype)
        rendition = image.get_rendition(filter_spec)
        return (image, rendition)

    def _get_lazy_path(self, image_url):
        return "{}_lazy.{}".format(*image_url.rsplit(".", 1))

    def _verify_image_file(self, path):
        im = PImage.open(path)
        return im.verify()

    def test_tag_jpeg(self):
        image, rendition = self._generate_rendition("jpeg", "width-960")
        template = Template(
            "{% load lazyimages_tags %}"
            "{% lazy_image image width-960 %}"
        )
        rendered = template.render(Context({'image': image}))
        lazy_url = self._get_lazy_path(rendition.url)
        self.assertIn('data-src="{}"'.format(rendition.url), rendered)
        self.assertIn('src="{}"'.format(lazy_url), rendered)
        self._verify_image_file(self._get_lazy_path(rendition.file.path))

    def test_tag_png(self):
        image, rendition = self._generate_rendition("png", "width-960")
        template = Template(
            "{% load lazyimages_tags %}"
            "{% lazy_image image width-960 %}"
        )
        rendered = template.render(Context({'image': image}))
        lazy_url = self._get_lazy_path(rendition.url)
        self.assertIn('data-src="{}"'.format(rendition.url), rendered)
        self.assertIn('src="{}"'.format(lazy_url), rendered)

    def test_as_syntax(self):
        image, rendition = self._generate_rendition("jpeg", "width-960")
        template = Template(
            "{% load lazyimages_tags %}"
            "{% lazy_image image width-960 as img %}"
            "{% lazy_image_url img %}"
        )
        rendered = template.render(Context({'image': image}))
        self.assertIn(self._get_lazy_path(rendition.url), rendered)

    def test_lazy_attr(self):
        image, rendition = self._generate_rendition("jpeg", "width-960")
        template = Template(
            '{% load lazyimages_tags %}'
            '{% lazy_image image width-960 lazy_attr="data-orig-url" %}'
        )
        rendered = template.render(Context({'image': image}))
        lazy_url = self._get_lazy_path(rendition.url)
        self.assertIn('data-orig-url="{}"'.format(rendition.url), rendered)
        self.assertIn('src="{}"'.format(lazy_url), rendered)
        self.assertNotIn('lazy_attr', rendered)
