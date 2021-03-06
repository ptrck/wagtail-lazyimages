
# Wagtail Lazy Images


Template tags that generate tiny blurry placeholder images alongside your wagtail images in order to lazy-load them medium.com style.


## Installing


Install using pip:
    ```
    pip install wagtail-lazyimages
    ```

## Usage

1. Add `wagtail_lazyimages` to your `INSTALLED_APPS` setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'wagtail_lazyimages',
    ]
    ```

2. Load the `lazyimages_tags` template tag library in your template:
    ```
    {% load "lazyimages_tags" %}
    ```

3. Replace wagtail's `image` tag with `lazy_image` for images that should lazy load:
    ```
    {% lazy_image page.photo width-960 class="lazy" %}
    ```

    This template tag behaves just like wagtail's `image` tag with the exception that it generates an additional scaled down and blurred placeholder image. The URL of the placeholder image will appear in the `src` attribute of the image tag while the large version will be referenced in `data-src`:
    ```
    <img src="/path/to/placeholder-image.jpg" data-src"/path/to/image.jpg" class="lazy" />
    ```

4. In the front end: Implement the lazy loading functionality yourself or use a dedicated JavaScript library like [lozad.js](https://apoorv.pro/lozad.js):

    ```
    const observer = lozad('.lazy');
    observer.observe();
    ```


### Alternative attribute

If you want to use a different attribute for referencing the original image than `data-src` use the parameter `lazy_attr` for that:

    {% lazy_image page.photo width-960 lazy_attr="data-lazy-url" class="lazy" %}


### As syntax

If you need to assign the image data to a template variable using Django's `as` syntax, the URL of the placeholder image is stored in the `lazy_url` attribute:

    {% load "lazyimages_tags" %}

    {% lazy_image page.photo width-960 as img %}

    <img data-src="{{ img.url }}" src="{{ img.lazy_url }}" width="{{ img.width }}"
         height="{{ img.height }}" alt="{{ img.alt }}" />


### `attrs` shortcut

In case you need to use Wagtail's [`attrs shortcut`](https://docs.wagtail.io/en/stable/topics/images.html#the-attrs-shortcut) use `lazy_attrs` instead:

    {% load "lazyimages_tags" %}

    {% lazy_image page.photo width-960 as img %}

    <img {{ img.lazy_attrs }} class="custom-class" />
