from django import forms
from .models import Seller

class CreateSellerForm(forms.ModelForm):
    
    class Meta:
        model = Seller
        fields = ['user', 'phone_number', 'bank_account_number', 'bank_account_ifsc_code', 'aadhar_card_number']
        widgets = {
            "phone_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"Phone Number"}),
            "bank_account_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"Bank Account Number"}),
            "bank_account_ifsc_code" : forms.TextInput(attrs={"class":"form-control","placeholder":"Bank Account IFSC Code"}),
            "aadhar_card_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"Aadhar Card Number"}),
        }
        
class EditSellerForm(forms.ModelForm):
    
    class Meta:
        model = Seller
        fields = ['phone_number', 'bank_account_number', 'bank_account_ifsc_code', 'aadhar_card_number']
        widgets = {
            "phone_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"Phone Number"}),
            "bank_account_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"Bank Account Number"}),
            "bank_account_ifsc_code" : forms.TextInput(attrs={"class":"form-control","placeholder":"Bank Account IFSC Code"}),
            "aadhar_card_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"Aadhar Card Number"}),
        }