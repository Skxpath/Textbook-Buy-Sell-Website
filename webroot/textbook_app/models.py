from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django import forms

MAX_ISBN_DIGITS = 13
MAX_PRICE_DOLLAR_DIGITS = 4
PRICE_CENTS_DIGITS = 2

class Textbook(models.Model):
    isbn = models.DecimalField('ISBN', max_digits=MAX_ISBN_DIGITS, decimal_places=0, primary_key=True)
    title = models.CharField('Book Title', max_length=200)
    author = models.CharField('Author', max_length=200)
    description = models.TextField('Description')

class TextbookForm(ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Textbook
        fields = '__all__'

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
    # Forms a many-to-one relationship between users and ads
    # i.e. an ad belongs to only one user, but a user can have many ads
    # When a user's account is deleted, delete all of their ads too
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # We want to ensure that every ad is associated with a Textbook, so all ads for a textbook can be found together
    book = models.ForeignKey(Textbook, on_delete=models.CASCADE)

class AdForm(ModelForm):
    class Meta:
        model = Ad
        exclude = ['poster', 'book']



