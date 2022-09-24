from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


class TagInlineFormset(BaseInlineFormSet):
    def clean(self):
        main = 0
        for form in self.forms:
            if form.cleaned_data['is_main']:
                main += 1
            if main > 1:
                raise ValidationError('Основным может быть только один раздел')
        if not main:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class TegsInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = TagInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text']
    inlines = [TegsInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
