from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'age', 'gender', 'ethnicity', 'traits', 'background', 'type_story', 'personality', 'year']

class GameChoiceForm(forms.Form):
    custom_choice = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your custom choice here', 'maxlength': '100'})
    )

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)

