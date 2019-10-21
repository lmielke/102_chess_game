from django import forms
from . models import Article, Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from web_project.helper import MyHelper
import os


class PostCreateForm(forms.ModelForm):
    form_params = MyHelper.get_web_modes(None, os.environ.get('WEB_MODE', 'localhost:8000'))
    style_params = MyHelper.get_web_styles(None, os.environ.get('WEB_STYLE', '0'))
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': form_params['form_ph_1']}),
                            label=form_params['form_lbl_1'],
                            help_text=form_params['form_help_1'])
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': form_params['form_ph_2']}),
                            label=form_params['form_lbl_2'],
                            help_text=form_params['form_help_2'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout('title', 'content',
                                Submit('speichern',
                                    self.form_params['form_btn_text1'],
                                    css_class=self.style_params['form_btn_style1']))
        #self.helper.form_class = 'form-horizontal'
        self.helper.labels_uppercase = True


    class Meta:
        model = Post
        fields = ['title', 'content']



class ArticleCreateForm(forms.ModelForm):
    form_params = MyHelper.get_web_modes(None, os.environ.get('WEB_MODE', 'localhost:8000'))
    style_params = MyHelper.get_web_styles(None, os.environ.get('WEB_STYLE', '0'))
    # form fields are paraeterized here with labels and placeholder values
    importance = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 oder 2 oder 3'}),
                            label='Priorität')
    topic = forms.CharField(widget=forms.TextInput(attrs={'placeholder': form_params['form_ph_0']}),
                            label=form_params['form_lbl_0'])
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Überschrift ihres Artikels'}),
                            label='Überschrift')
    teaser = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Zusammenfassung', 'style': 'height: 5em;'}),
                            label='Zusammenfassung ihres Artikels',
                            help_text=form_params['form_help_1'],
                            max_length=200)
    img_capt = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Beschreiben Sie kurz ihr Bild?'}),
                            label='Bild Beschreibung')
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Es war einmal...',
                                                            'style': 'height: 15em;'}),
                            label='Hier können Sie ihren Text eingeben',
                            help_text='Achten sie auf eine angemessene Sprechweise!')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        print(f'in ArticleCreateForm with: {self.style_params}')
        self.helper.form_method = 'post'
        self.helper.layout = Layout('importance', 'topic', 'title', 'teaser', 'article_img', 'img_capt', 'content', Submit('speichern', self.form_params['form_btn_text1'], css_class=self.style_params['form_btn_style1']))
        #self.helper.form_class = 'form-horizontal'
        self.helper.labels_uppercase = True


    class Meta:
        model = Article
        fields = ['importance', 'topic', 'title', 'teaser', 'article_img', 'img_capt', 'content']

