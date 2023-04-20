## View
Views are the main way to interact with the user.
They are responsible for rendering the data and handling the user's requests.

The `View` will be called when the user requests the path specified in the `Endpoint` class.
The `View` methods are creates by defining the `get`, `post`, `put`, `patch`, `delete` methods in the class.

We recommend to create a `views.py` file in each app directory.
The views are defined as classes that inherit from the `View` class. 
You can define default and async methods.

```python
from jija import views

class MyView(views.View):
    def get(self): ...
    async def post(self): ...
    async def delete(self): ...
```

If you will raise `jija.exceptions.ViewForceExit` in the view, the view will be stopped and the response will be returned.
```python
from jija import exceptions, response

...

if color == 'red':
    raise exceptions.ViewForceExit(response.JsonResponse({'status': 'ok'}))

...
```

## SerializedView
SerializerView is a subclass of the `View` class.
You can use the `SerializedView` class to serialize the data before processing it.

For add a serializer, you need to add arg to your method and annotate serializer class to it.
All data from serializer will be added to docs if it is enabled and `DocMixin` is added to the view.

```python
from jija import views, serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()

class MyView(views.SerializedView):
    def get(self, data: MySerializer):
        ...
```

## WSView
Websocket view.
It is a view that is called when the user connects to the websocket.
To create actions to incoming messages, you need to define the `on_message` method.
To send messages to the user, you need to use the `send` method.
You can redefine the `on_connect` and `on_error` methods to add actions when the user connects and disconnects from the websocket.

```python
from jija import views

class MyWS(views.WSView):
    def on_message(self, message):
        self.send(message)     
```

## DocMixin
DocMixin is a mixin that adds documentation to the view.
You can add a `DocMixin` to the view to add documentation to the view.
DocString of the view and of the method will be used as a description.

```python
from jija import views

class MyView(views.View, views.DocMixin):
    """This is view description."""""
    
    def get(self):
        """This is method description."""""
```
