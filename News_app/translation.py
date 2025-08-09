from modeltranslation.translator import register, TranslationOptions, translator
from .models import New, Category


@register(New)
class NewTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)
# 2-usul
# translator.register(New, NewTranslationOptions)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)