from django import forms
from django.utils.timezone import datetime
from .models import Cat

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields =['name',
                 'birth',
                 'description',
                 'picture',
                 'active']
        widgets = {
            'birth': forms.TextInput(attrs={'placeholder': 'Year of birth'}),
        }
    def clean_birth(self):
        birth = self.cleaned_data.get("birth")
        if birth < 2000 or birth > datetime.now().year:
            raise forms.ValidationError(" Not a valid year of birth")
        return birth