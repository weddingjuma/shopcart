from django import forms
from shopcart.catalog.models import Product, Category
from shopcart.cart.models import CartItem
from django.forms.widgets import CheckboxSelectMultiple

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']
        
        
class productForm(forms.Form):
    name = forms.CharField(label='Name')
    price = forms.IntegerField()
    old_price = forms.IntegerField()
    quantity = forms.IntegerField()
    description = forms.CharField(widget = forms.Textarea)
    photo = forms.ImageField(required=False)
    categories = forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple(attrs={'class':'format'}), queryset = Category.objects.all())
    
    
    
class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2',
        'class':'quantity', 'maxlength':'5'}),
        error_messages={'invalid':'Please enter a valid quantity.'},
        min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())
    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)
    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data
