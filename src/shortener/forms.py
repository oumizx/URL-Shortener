from django import forms
from .validators import validate_dot_com, validate_url


class SubmitUrlForm(forms.Form):
    url = forms.CharField(
        label='Submit URL',
        validators=[validate_url, ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Long URL",
                "class": "form-control"
            }
        )
    )



    # def clean(self):
    #     cleaned_data = super(SubmitUrlForm, self).clean()

    # def clean_url(self):
    #     url = self.cleaned_data['url']
    #     #print(url)
    #     url_validator = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise forms.ValidationError("Invalid URL for this field")
    #     return url
