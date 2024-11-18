from django.forms import ModelForm, forms, BooleanField

from catalog.models import Product, Version

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name,  fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ("owner",)

    forbidden_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in self.forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(
                    f"Название продукта не может содержать слово: {word}"
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in self.forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(
                    f"Описание продукта не может содержать слово: {word}"
                )
        return description


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = "__all__"


class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ("is_published", "description", "category")