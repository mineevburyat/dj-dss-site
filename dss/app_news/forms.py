from django import forms
from .models import ImageMedia

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageMedia
        fields = ('slug', 'title', 'caption', 'alt_txt')
        