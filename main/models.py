from django.db import models
from django.utils.html import mark_safe
from .helper_func import get_home_banner_path

# Create your models here.

class HomeBanner(models.Model):
    
    banner = models.ImageField(
        upload_to= get_home_banner_path,
        verbose_name= "Banner"
    )
    
    link = models.URLField(
        verbose_name= 'URL'
    )
    
    link_text = models.CharField(
        max_length= 50,
        verbose_name= 'Link Button Text',
    )
    
    h1_title = models.CharField(
        max_length= 100,
        verbose_name= 'H1 Title',
        blank= True,
        null= True,
    )
    
    h4_title = models.CharField(
        max_length= 100,
        verbose_name= 'H4 Title',
        blank= True,
        null= True,
    )
    
    date_created = models.DateTimeField(
        auto_now_add= True,
    )
    
    @property
    def banner_preview(self):
        if self.banner:
            return mark_safe('<img src="/media/%s" width="500"  />' % (self.banner))
        else:
            return mark_safe('<p>Add New Banner</p>')
    
    class Meta:
        verbose_name = "Home Banner"
        verbose_name_plural = "Home Banners"
        ordering = ["date_created"]
    
    def __str__(self) -> str:
        return str(self.h1_title) + ' - ' + str(self.link)
