from typing import Any
from django import forms
from .models import Asset, Asset_Preview_Images, AssetFeedback
from taggit.forms import TagWidget

class CreateAssetForm(forms.ModelForm):
    
    class Meta:
        model = Asset
        fields = [ 'title', 'category', 'meta_description', 'tags', 'asset', 'user']
        widgets = {
            "title" : forms.TextInput(attrs={"class":"form-control","placeholder":"Title"}),
            "category" : forms.Select(attrs={"class":"form-select form-select-lg",}),
            "meta_description" : forms.TextInput(attrs={"class":"form-control","placeholder":"Meta Description"}),
            "tags" : TagWidget(attrs={"class":"form-control","placeholder":"Tags"}),
            "asset" : forms.FileInput(attrs={"class":"form-control"}),
        }
    
    def clean(self):
        cleaned_data = super(CreateAssetForm, self).clean()
        asset = cleaned_data.get("asset")
        category = cleaned_data.get("category")

        asset_size = round((asset.size / 1048576),2)
        min_size = category.min_asset_size
        max_size = category.max_asset_size
        
        if asset_size > max_size or asset_size < min_size:
            self.add_error('asset',f'Invalid  asset size, Min - {min_size}MB & Max - {max_size}MB and yours - {asset_size}MB')
        
        return cleaned_data
    
    def save(self):
        title = self.cleaned_data.get("title")
        category = self.cleaned_data.get("category")
        meta_description = self.cleaned_data.get("meta_description")
        tags = self.cleaned_data.get("tags")
        asset = self.cleaned_data.get("asset")
        user = self.cleaned_data.get("user")
        
        asset_obj = Asset.objects.create(
            title = title,
            category = category,
            meta_description = meta_description,
            user = user,
        )
        if tags:
            for i in tags:
                asset_obj.tags.add(i.strip())
        asset_obj.asset = asset
        asset_obj.size = round((asset.size / 1048576),2)
        asset_obj.file_type = str(asset.name).split('.')[-1]
        asset_obj.save()
        return asset_obj.pk
        
class EditAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [ 'title', 'meta_description', 'description', 'tags']
        widgets = {
            "title" : forms.TextInput(attrs={"class":"form-control","placeholder":"Title"}),
            "meta_description" : forms.TextInput(attrs={"class":"form-control","placeholder":"Meta Description"}),
            "description" : forms.Textarea(attrs={"class":"form-control","placeholder":"Description"}),
            "tags" : TagWidget(attrs={"class":"form-control","placeholder":"tags"}),
        }
        
class AddPreviewImageForm(forms.ModelForm):
    
    class Meta:
        model = Asset_Preview_Images
        fields = [ 'image', 'asset']
        widgets = {
            "image" : forms.FileInput(attrs={"class":"form-control"}),
        }
    
    def save(self):
        image = self.cleaned_data.get("image")
        asset = self.cleaned_data.get("asset")
        asset_preview_image_obj = Asset_Preview_Images.objects.create(
            asset = asset,
        )
        asset_preview_image_obj.image = image
        asset_preview_image_obj.save()
        return asset_preview_image_obj

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = AssetFeedback
        fields = ['order', 'user', 'asset', 'rating', 'feedback']
        widgets = {
            "feedback" : forms.Textarea(attrs={"class":"form-control","placeholder":"Feedback","rows" : "3"}),
            "order" : forms.HiddenInput(),
            "user" : forms.HiddenInput(),
            "asset" : forms.HiddenInput(),
        }
