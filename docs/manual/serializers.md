## Serializer
Serializers are used to convert and validate data from request a format that can be transmitted over the wire.
Best practice is to create a serializers in `serializers.py` in your app.

```python
from jija import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.fields.IntegerField()
    name = serializers.fields.CharField()
```

## Field
In serializers you can use fields to validate and convert data.
Fields are processing validators and converters data if it need.
You can create your own field by inheriting from `jija.serializers.fields.Field`.

```python
class MyField(IntegerField):
    validators = (*IntegerField.validators, MyValidator)
```


## Validator
Validators are used to validate data.
It will convert data to python type and check it.
If data is not valid, it will raise `jija.serializers.exceptions.ValidationError`.
