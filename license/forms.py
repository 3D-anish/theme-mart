from django import forms
from .models import Asset_License, License

class AddAssetLicenseForm(forms.ModelForm):
    
    license = forms.ModelChoiceField(
        queryset=License.objects.none(),
        widget= forms.Select(attrs={"class" : "form-select"})
    )
    
    class Meta:
        model = Asset_License
        fields = [ 'asset', 'license', 'price']
        widgets = {
            "price" : forms.NumberInput(attrs={"class":"form-control","placeholder":"Price"}),
        }
    
    def save(self):
        asset = self.cleaned_data.get("asset")
        license = self.cleaned_data.get("license")
        price = self.cleaned_data.get("price")
        
        asset_license_obj = Asset_License.objects.create(
            asset = asset,
            license = license,
            price = price,
        )
        asset_license_obj.save()
        return asset_license_obj
        
class EditAssetLicenseForm(forms.ModelForm):
    license = forms.ModelChoiceField(
        queryset=License.objects.none(),
        widget= forms.Select(attrs={"class" : "form-select"})
    )
    
    class Meta:
        model = Asset_License
        fields = ['license', 'price']
        widgets = {
            "price" : forms.NumberInput(attrs={"class":"form-control","placeholder":"Price"}),
        }
