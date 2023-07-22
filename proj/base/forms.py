from .models import Collection,Store,CustomUser,UserReview
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email','username','password1','password2')


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('email','name','phone','house','area','landmark','pincode','town','state','country')
        # exclude = ('password',)
        labels = {
            'email': 'Email',
            'name': 'Name',
            'phone': 'Phone',
            'house': 'House No,Flat No',
            'area': 'Area',
            'landmark': 'Landmark',
            'pincode': 'Pincode',
            'town': 'Town,City',
            'state': 'State',
            'country': 'Country',
        }
    
class SortForm(forms.Form):
    CHOICES = (
        ('prod_price', 'Price: Low to High'),
        ('-prod_price', 'Price: High to Low'),
    )

    sort_by = forms.ChoiceField(label='',choices=CHOICES, widget=forms.RadioSelect)
    
class FilterForm(forms.Form):
    CHOICES = (
        ('Viynls', 'Viynls'),
        ('Cassettes', 'Cassettes'),
        ('Posters', 'Posters'),
    )

    choice_by = forms.ChoiceField(label='',choices=CHOICES, widget=forms.RadioSelect)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'cont-textarea'}))



class ChangeDetailForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('name','phone','house','area','landmark','pincode','town','state','country')
        # exclude = ('password',)
        labels = {
            'name': 'Name',
            'phone': 'Phone',
            'house': 'House No,Flat No',
            'area': 'Area',
            'landmark': 'Landmark',
            'pincode': 'Pincode',
            'town': 'Town,City',
            'state': 'State',
            'country': 'Country',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True

class RatingInput(forms.RadioSelect):
    template_name = 'base/rating_input.html'  

class CustomerReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=RatingInput)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'txtarea', 'placeholder':'Write your review here ...'}))
    class Meta:
        model = UserReview
        fields = ['rating', 'message']