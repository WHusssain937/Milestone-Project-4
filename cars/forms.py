from django import forms
from .models import Car, Brand


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brands = Brand.objects.all()
        brand_names = [(b.id, b.__str__()) for b in brands]

        self.fields['brand'].choices = brand_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
            