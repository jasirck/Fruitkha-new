from django import forms
from .models import myprodect


class prodectsForm(forms.ModelForm):
    prodect_image1 = forms.FileField(required=False)
    prodect_image2 = forms.FileField(required=False)
    prodect_image3 = forms.FileField(required=False)

    class Meta:
        model = myprodect
        fields = [
            "price",
            "prodect_name",
            "category",
            "description",
            "quantity",
            "variant",
            "prodect_image1",
            "prodect_image2",
            "prodect_image3",
        ]
