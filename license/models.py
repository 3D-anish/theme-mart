from django.db import models
from assets.models import Asset, Asset_Category
from django.core.exceptions import ValidationError

# Create your models here.

class License_Term(models.Model):
    
    term_title = models.CharField(
        max_length=50,
        verbose_name= 'Term Title',
    )
    
    term_detail = models.CharField(
        max_length= 2000,
        verbose_name= "Term Detail",
    )
    
    class Meta:
        verbose_name = "License Term"
        verbose_name_plural = "License Terms"
        ordering = ["-pk"]
        
    def __str__(self):
        return self.term_title

class License(models.Model):
    
    license_names_choices = {
        'educational_license' : "Educational License",
        'personal_license' : "Personal License",
        'regular_license' : "Regular License",
        'extended_license' : "Extended License",
        'commercial_license' : "Commercial License",
    }
    
    name = models.CharField(
        max_length=100,
        choices=license_names_choices,
        verbose_name= 'License Name',
    )
    
    asset_category = models.ForeignKey(
        Asset_Category, 
        on_delete=models.CASCADE,
        verbose_name= "Asset Category",
    )
    
    license_terms = models.ManyToManyField(
        License_Term, 
        blank=False,
        verbose_name= "License Terms",
    )
    
    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"
        ordering = ["pk"]
    
    @property
    def total_license_terms(self):
        return str(self.license_terms.count())
    
    def clean(self,*args,**kwargs):
        if License.objects.filter(name = self.name , asset_category = self.asset_category).exclude(pk = self.pk).exists():
            raise ValidationError(
                {"asset_category" : f'Asset Category already have this license.'}, 
            )
        super().clean(*args, **kwargs)
    
    def __str__(self):
        return str(self.get_name_display() + ' - ' + self.asset_category.name)
    
class Asset_License(models.Model):
    
    asset = models.ForeignKey(
        Asset, 
        on_delete=models.CASCADE,
        related_name= 'licenses',
        verbose_name= 'Asset',
    )
    
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE,
        verbose_name= "License",
    )
    
    price = models.DecimalField(
        max_digits= 8, 
        decimal_places=2,
        verbose_name= "Price",
    )
    
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name= "Date Created",
    )
    
    class Meta:
        verbose_name = "Asset License"
        verbose_name_plural = "Asset Licenses"
        ordering = ["date_created"]
    
    def clean(self,*args,**kwargs):
        if Asset_License.objects.filter(asset = self.asset , license = self.license).exclude(pk = self.pk).exists():
            raise ValidationError(
                {"license" : f'Asset already have this license.'}, 
            )
        if self.asset.category != self.license.asset_category:
            raise ValidationError(
                {"license" : f'Asset can\'t have this license.'}, 
            )
        if self.price < 49:
            raise ValidationError(
                {'price' : 'Price must be higher than ₹49'},
            )
        if self.price > 100000:
            raise ValidationError(
                {'price' : 'Price must be less than ₹1,00,000'},
            )
        super().clean(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.asset.title + ' - ' + '(' +str(self.license) + ')')
