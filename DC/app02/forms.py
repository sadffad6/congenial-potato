from django.forms import forms, ModelForm, PasswordInput
from .models import UserInfo

class loginForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'password':
                field.widget = PasswordInput(render_value=False, attrs={"class": "form-control", "placeholder": name})
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": name}
