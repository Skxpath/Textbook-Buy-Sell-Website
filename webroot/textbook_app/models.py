from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django import forms
from django.utils import timezone

MAX_ISBN_DIGITS = 13
MAX_PRICE_DOLLAR_DIGITS = 4
PRICE_CENTS_DIGITS = 2

class Textbook(models.Model):
    isbn = models.DecimalField('ISBN', max_digits=MAX_ISBN_DIGITS, decimal_places=0, primary_key=True)
    title = models.CharField('Book Title', max_length=200)
    author = models.CharField('Author', max_length=200)
    description = models.TextField('Textbook Description', blank=True, default='')

# Adds bootstrap classes to all form fields by default
# snippet taken from hurlbz's answer here: https://stackoverflow.com/questions/19489699/how-to-add-class-id-placeholder-attributes-to-a-field-in-django-model-forms
class BaseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            #get current classes from Meta
            classes = self.fields[field].widget.attrs.get("class")
            if classes is not None:
                classes += " form-control"
            else:
                classes = "form-control"
            self.fields[field].widget.attrs.update({
                'class': classes
            })

class TextbookForm(BaseModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea)
    isbn = forms.IntegerField(min_value=0)

    class Meta:
        model = Textbook
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TextbookForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].widget.attrs.update({'v-model': 'textbookIsbn'})
        self.fields['title'].widget.attrs.update({'v-model': 'textbookTitle'})
        self.fields['author'].widget.attrs.update({'v-model': 'textbookAuthor'})

class TextbookFormNoIsbn(BaseModelForm):
    class Meta:
        model = Textbook
        exclude = ['isbn']

class Ad(models.Model):
    price = models.DecimalField(max_digits=MAX_PRICE_DOLLAR_DIGITS + PRICE_CENTS_DIGITS, decimal_places=PRICE_CENTS_DIGITS)
    MAX_BOOK_CONDITION_CODE_LENGTH = 4
    NEW = 'NEW'
    GOOD = 'GOOD'
    FAIR = 'FAIR'
    WORN = 'WORN'
    BAD = 'BAD'
    BOOK_CONDITIONS = (
        (NEW, 'New'),
        (GOOD, 'Good'),
        (FAIR, 'Fair'),
        (WORN, 'Worn'),
        (BAD, 'Bad'),
    )
    condition = models.CharField(
        max_length=MAX_BOOK_CONDITION_CODE_LENGTH,
        choices=BOOK_CONDITIONS,
        default=GOOD,
        blank=False
    )
    #Ad Description, to describe in more detail the ad itself, rather than the textbook.
    Ad_Description = models.TextField('Ad Description', blank=True, default='')
    # Forms a many-to-one relationship between users and ads
    # i.e. an ad belongs to only one user, but a user can have many ads
    # When a user's account is deleted, delete all of their ads too
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # We want to ensure that every ad is associated with a Textbook, so all ads for a textbook can be found together
    book = models.ForeignKey(Textbook, on_delete=models.CASCADE)

class AdForm(BaseModelForm):
    class Meta:
        model = Ad
        exclude = ['poster', 'book']

class Chat(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    # label = models.SlugField(unique=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages')
    user = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
