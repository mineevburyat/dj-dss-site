from django import forms
from .models import Image as ImageMedia

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageMedia
        fields = ('slug', 'title', 'caption', 'alt_txt')
        