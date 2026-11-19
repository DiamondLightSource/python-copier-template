# How to embed Excalidraw diagrams

Start off by creating your diagram in <https://excalidraw.com>

```{raw} html
:file: ../images/excalidraw-example.svg
```

Click 'Save as image' and make sure the 'Embed scene' checkbox is enabled. this is required for loading your image back into Excalidraw should you wish to make changes later on. Name your file and export to SVG, saving it inside `docs/images`.

Add the following to embed it inside your documentation:

    ```{raw} html
    :file: ../images/my-diagram.excalidraw.svg
    ```

It is preferred to use the above convention over the image directive in order to retain the font used by Excalidraw.

Rebuild the docs and open the resulting html inside a browser.
