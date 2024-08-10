from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import uuid

class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Password"}),
        validators=[validate_password,],
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Confirm Password"}),
    )
    class Meta:
        model = get_user_model()
        fields = ["username","email","password","confirm_password"]
        widgets = {
            "username": forms.TextInput(attrs={"class" : 'form-control','placeholder': 'Username',}),
            "email": forms.EmailInput(attrs={"class" : 'form-control','placeholder': 'Email Address',}),
        }
        
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if not self.has_error("password"):
            if password != confirm_password:
                self.add_error('confirm_password',"Password and Confirm Password do not match.")
        return cleaned_data
    
    def save(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user_obj = get_user_model().objects.create(
            username = username,
            email = email,
        )
        user_obj.is_active = False
        user_obj.is_verified = False
        user_obj.uuid = uuid.uuid4()
        user_obj.set_password(password)
        user_obj.save()
        user_obj.send_verification_link()
        
class ChangePasswordForm(forms.Form):
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class" : "form-control","placeholder":"Current Password"}),
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"New Password"}),
        validators=[validate_password,],
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Confirm New Password"}),
    )
    
    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        if current_password == new_password:
            self.add_error("new_password","Current password and new password are same")
        if not self.has_error("new_password"):
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password',"New Password and Confirm New Password do not match.")
        return cleaned_data
    
    def save(self,user_obj):
        user_obj.set_password(self.cleaned_data['new_password'])
        user_obj.save()

class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'phone_number', 'full_name','profile_image', 'address_line_1','address_line_2', 'address_area', 'address_city', 'address_state', 'address_pincode', 'gst_number']
        widgets = {
            "username" : forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}),
            "phone_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"Phone Number"}),
            "full_name" : forms.TextInput(attrs={"class":"form-control","placeholder":"Full Name"}),
            "profile_image" : forms.FileInput(attrs={"class":"form-control",}),
            "address_line_1" : forms.TextInput(attrs={"class":"form-control","placeholder":"Address Line 1"}),
            "address_line_2" : forms.TextInput(attrs={"class":"form-control","placeholder":"Address Line 2"}),
            "address_area" : forms.TextInput(attrs={"class":"form-control","placeholder":"Area"}),
            "address_city" : forms.TextInput(attrs={"class":"form-control","placeholder":"City"}),
            "address_state" : forms.TextInput(attrs={"class":"form-control","placeholder":"State"}),
            "address_pincode" : forms.TextInput(attrs={"class":"form-control","placeholder":"PinCode"}),
            "gst_number" : forms.TextInput(attrs={"class":"form-control","placeholder":"GST Number(optional)"}),
        }
        
class ResetPasswordForm(forms.Form):
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"New Password"}),
        validators=[validate_password,],
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Confirm New Password"}),
    )
    
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        if not self.has_error("new_password"):
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password',"New Password and Confirm New Password do not match.")
        return cleaned_data
    
    def save(self,user_obj):
        user_obj.uuid = None
        user_obj.set_password(self.cleaned_data["new_password"])
        user_obj.save()
