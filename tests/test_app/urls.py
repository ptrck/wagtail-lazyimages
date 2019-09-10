from django.conf.urls import include, url

try:
    # Wagtail 2.x
    from wagtail.core import urls as wagtail_urls
except ImportError:
    # Wagtail 1.x
    from wagtail.wagtailcore import urls as wagtail_urls


urlpatterns = [
    url(r'', include(wagtail_urls)),
]
