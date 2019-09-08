
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


### Image in context variable

If you need to assign the image data to a template variable using Django's `as` syntax, use the provided `lazy_image_url` template tag for getting just the URL of the placeholder image:

    {% load "lazyimages_tags" %}

    {% image page.photo width-960 as img %}

    <img data-src="{{ img.url }}" src="{% lazy_image_url img %}" width="{{ img.width }}"
         height="{{ img.height }}" alt="{{ img.alt }}" />


### Alternative attribute

If you want to use a different attribute for referencing the original image than `data-src` use the parameter `lazy_attr` for that:

    {% lazy_image page.photo width-960 lazy_attr="data-lazy-url" class="lazy" %}

