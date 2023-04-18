## How it works
In jija, middlewares are used to process requests before and after they are passed to the view.

In startup jija collecting middlewares from all apps and core app from `middlewares.py` in each app,
middlewares.py should contain a subclasses of `jija.middleware.Middleware`, it will be included in order of definition.
Request for subapp will be processed by middlewares from core app and subapp,
then if you want add some middleware for all apps you can add it to core app.

## Default middlewares
By default jija uses some middlewares: `jija.middlewares.print_request`.

## Creating a custom middleware
To create a custom middleware, you need to create `middlewares.py` in your app 
and add a class that inherits from `jija.middleware.Middleware` and implement the `handler` method.

```python
from jija import middleware

class MyMiddleware(middleware.Middleware):
    async def handler(self, request, handler):
        # add your logic here
        return await handler(request)
```
