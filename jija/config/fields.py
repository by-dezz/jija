from jija.forms.fields import *


class SubclassValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if not issubclass(value, field.class_pattern):
            raise ValidationError(f'Value must be subclass of {field.class_pattern}, not {type(value)}', value)

        return value
    

class ClassField(Field):
    validators = [SubclassValidator]

    def __init__(self, *, class_pattern, **kwargs):
        self.class_pattern = class_pattern
        super().__init__(**kwargs)