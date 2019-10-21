from django import forms
from . models import Chess
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
import os


class ChessForm(forms.ModelForm):
    gameName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your Game Name'}),
                            help_text='Type a Game name, so you can save and reload it!')

    activePlayer = forms.ChoiceField(choices=(('','--choose color--'), 
                                                    ('2','Black'), 
                                                    ('1','White'), ),
                                        help_text='Which color player are you?')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout('gameName', 'activePlayer',
                                Submit('save',
                                    'Start Game',
                                    css_class='btn-outline-info'))
        self.helper.form_class = 'form-horizontal'
        self.helper.labels_uppercase = True


    class Meta:
        model = Chess
        fields = ['gameName', 'activePlayer',]
        labels = {'activePlayer': 'Select Your Color',}


