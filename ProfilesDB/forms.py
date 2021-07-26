from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import ROLES


class CreateGroupForm(forms.Form):
    title = forms.CharField(label='Group title', max_length=50, min_length=3, initial='')
    private = forms.BooleanField(initial=False, required=False)
    min_level = forms.IntegerField(initial=1,
                                   validators=[MaxValueValidator(100), MinValueValidator(1)])
    role = forms.ChoiceField(choices=ROLES)

    def __init__(self, user, data=None):
        self.user = user
        super(CreateGroupForm, self).__init__(data=data)
        self.fields['title'].initial = user.username + "'s group"
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['private'].widget.attrs.update(
            {'class': 'form-check-input border-secondary',
             'style': 'background-color: #353B40;color: #efefef;width:25px;height:25px'})
        self.fields['min_level'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['role'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
