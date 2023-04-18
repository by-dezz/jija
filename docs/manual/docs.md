## Include
You need to init ``config.DocsConfig`` in ``settings.py``.

```python
config.DocsConfig()
```

And add ``views.DocMixin`` to view in ``apps/my_app/views.py``.

```python
class MyView(views.View, views.DocMixin): ...
```

After that you can open docs on ``http://127.0.0.1:8080/docs/``.
Only views with ``views.DocMixin`` will be included to docs.

## Custom url
If you want to change url of docs, you need to provide ``url`` arg to ``config.DocsConfig``.

```python
config.DocsConfig(url='/custom-docs')
```

## Adding fields
Fields will be added to the docs automatically if you add serializer to the view.
