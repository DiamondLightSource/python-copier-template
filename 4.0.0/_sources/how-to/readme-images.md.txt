# How to add images to the README

The contents of the `README.md` file may be presented in various places:

* Project homepage on GitHub
* Project documentation (if using Sphinx build)
* PyPI (if publishing there)

This places some limitations on including relative content as PyPI is only
provided with the content directly in `README.md` and not the surrounding
resources.

Additionally the Sphinx build uses the `docs` directory as the root of the build
meaning that included content is relative to that path.

A reference link in Markdown syntax can be used to allow images to be included
such that  a fixed image URL is used in the `README.md` itself which can be
overridden to a relative URL for the Sphinx build. This satisfies the three use
cases above.

Example of Markdown reference link:

```markdown
![Image alt text][reference]
```
with the `reference` defined (potentially elsewhere) as:

```markdown
[reference]: https://mydomain.com/myimage.png
```

## Example: Image Reference 

This example shows how to include an image (local to the repository) in the
`README.md` such that it will render in all three places mentioned above.

In the `README.md` a reference image link is placed at the location the image
should be rendered:

```markdown
![my example image][blueapi]
```

at the bottom of the `README.md`, link to a `raw.githubusercontent.com` URL.
This is placed below a comment:

```markdown
<!-- README only content. Anything below this line won't be included in index.md -->

[blueapi]: https://raw.githubusercontent.com/DiamondLightSource/blueapi/main/docs/images/blueapi.png
```

The absolute URL is used to allow PyPI to render the image. If PyPI is not
required a relative URL can be used which will work for GitHub rendering.

The `README.md` content is included in the Sphinx build (for example `index.md`)
but will stop when it reaches the comment:

````markdown
```{include} ../README.md
:end-before: <!-- README only content
```
````

After this include block the reference can be redefined to point to the local
image, relative to the root of the Spinx build:

```markdown
[blueapi]: images/blueapi.png
```

This ensures that a frozen version of the image at the time the docs are built
is used for the documentation rather than an image on a branch.

Note that if using a `raw.githubusercontent.com` URL pointing to an image on a
branch, e.g:
```
https://raw.githubusercontent.com/DiamondLightSource/blueapi/main/docs/images/blueapi.png
```
it is possible that the image will be removed or change over time. This would
affect the content displayed on PyPI, even for releases already made.

To mitigate this it may be desired to point to fixed versions of such assets,
via a commit hash or a tag URL. For example an image at a specific tag:
```
https://raw.githubusercontent.com/DiamondLightSource/blueapi/0.4.0/docs/images/blueapi.png
```
or an image at a specific commit:
```
https://raw.githubusercontent.com/DiamondLightSource/blueapi/7bbc94e0d61da2a4ce4de6a1285c4cc0e4ba67f2/docs/images/blueapi.png
```
This may incur a prohibitive maintenance cost, in constantly updating references
when releases are made, so use of these fixed images is left as a per-project
decision.


## Example: Logo

A logo may also be added to the `README.md`. 


Given that the `README.md` layout has not been drastically changed from the
template, the following HTML image style code may be placed at the very top of
`README.md`:
```html
<img src="https://raw.githubusercontent.com/DiamondLightSource/blueapi/main/docs/images/blueapi-logo.svg"
     style="background: none" width="120px" height="120px" align="right">
```

The width and height may be adjusted to suit the particular project logo.
