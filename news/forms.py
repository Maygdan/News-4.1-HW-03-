from django import forms
from django.core.exceptions import ValidationError
from .badwords import BAD_WORDS as W

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=[
            'author',
            'title', 
            'text',
            'category',

      
        ]
        
    def clean(self):
            cleaned_data=super().clean()
            text=cleaned_data.get('text') 
            if text is not None and len(text)<100:
                raise ValidationError({
                    'text':'Текст не может быть менее 100 символов'
                })
            if any([j in str(text) for j in W]):
                 raise ValidationError('Текст не должен содержать подобные выражения')
            
            title=cleaned_data.get('title') 

            if title==text:
                raise ValidationError({
                'text':'Название не должно быть индентично тексту'
                                       })
            if any([j in str(title) for j in W]):
                 raise ValidationError({'title':'Название не должно содеражать ругательства'})
            
                 
            
            return cleaned_data
# qwertyuiopasdfghjklzxcvbnmqwertyuiop
# qwertyuiopasdfghjklzxcvbnmqwertyuiop
