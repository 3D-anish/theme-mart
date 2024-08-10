from django import forms
from .models import Orders

class EditOrderDetailForm(forms.ModelForm):
    
    class Meta:
        model = Orders
        fields = ['user_full_name', 'user_phonenumber','address_line_1','address_line_2', 'address_area', 'address_city', 'address_state', 'address_pincode', 'gst_number']
        widgets = {
            "user_full_name" : forms.TextInput(attrs={"class":"form-control","placeholder":"Full Name"}),
            "user_phonenumber" : forms.TextInput(attrs={"class":"form-control","placeholder":"Phone Number"}),
            "address_line_1" : forms.TextInput(attrs={"class":"form-control","placeholder":"Address Line 1"}),
            "address_line_2" : forms.TextInput(attrs={"class":"form-control","placeholder":"Address Line 2"}),
            "address_area" : forms.TextInput(attrs={"class":"form-control","placeholder":"Area"}),
            "address_city" : forms.TextInput(attrs={"class":"form-control","placeholder":"City"}),
            "address_state" : forms.TextInput(attrs={"class":"form-control","placeholder":"State"}),
            "address_pincode" : forms.TextInput(attrs={"class":"form-control","placeholder":"PinCode"}),
            "gst_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"GST Number(optional)"}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_full_name'].required = True
        self.fields['user_phonenumber'].required = True
        self.fields['address_line_1'].required = True
        self.fields['address_line_2'].required = True
        self.fields['address_area'].required = True
        self.fields['address_city'].required = True
        self.fields['address_state'].required = True
        self.fields['address_pincode'].required = True
        self.fields['gst_number'].required = False