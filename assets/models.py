from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.core.exceptions import ValidationError
from private_storage.fields import PrivateFileField
from .helper_func import get_asset_preview_image_path, get_asset_path, get_asset_category_image_path
from taggit.managers import TaggableManager
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify
from django.utils.html import mark_safe
from django.templatetags.static import static
from .validators import asset_preview_image_validator
from django.urls import reverse_lazy

# Create your models here.
    
class Asset_Category(models.Model):
    
    name = models.CharField(
        max_length=200, 
        verbose_name='Category Name',
        unique = True,
    )
    
    slug = models.SlugField(
        verbose_name= ' Slug',
        unique= True,
    )
    
    image = ResizedImageField(
        # size=[720, 923], # aspect_ratio = 0.78:1
        # crop=['middle', 'center'],
        # quality=95,
        upload_to= get_asset_category_image_path,
        verbose_name= 'Asset Category Image',
        blank = True,
        null = True,
    )
    
    required_file_types = models.CharField(
        max_length= 1000,
        default='',
        verbose_name='Required File Types',
        help_text= 'file_type_1, file_type_2, file_type_3'
    )
    
    min_asset_size = models.DecimalField(
        verbose_name = 'Minimum Asset Size(MB)',
        decimal_places = 2,
        max_digits = 6,
    )
    
    max_asset_size = models.DecimalField(
        verbose_name = 'Maximum Asset Size(MB)',
        decimal_places = 2,
        max_digits = 6,
    )
    
    class Meta:
        verbose_name = "Asset Category"
        verbose_name_plural = "Asset Categories"
        ordering = ["name"]
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(args, kwargs)
    
    def clean(self,*args, **kwargs):
        if self.min_asset_size > self.max_asset_size:
            raise ValidationError(
                {'min_asset_size' : 'Minimum asset size can not be higher than Maximum asset size.'}
            )
        super().clean(*args, **kwargs)    

    @property
    def asset_category_image(self):
        if self.image:
            return mark_safe('<img src="/media/%s" width="150" />' % (self.image))
        else:
            return mark_safe('<img src="%s" width="150" />' % (static('images/no_image_H.png')))
    
    def __str__(self):
        return self.name

asset_status = {
    'draft' : 'Draft',
    'published' : 'Published',
    'rejected' : 'Rejected',
}

class Asset(models.Model):
    
    uuid = models.UUIDField(
        unique= True,
        default= uuid.uuid4,
        verbose_name= 'UUID',
    )
    
    user = models.ForeignKey(
        get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= 'User',
    ) 
    
    category = models.ForeignKey(
        Asset_Category,
        on_delete= models.CASCADE,
        verbose_name= 'Asset Category',
    )
    
    title = models.CharField(
        max_length= 120,
        verbose_name= "Asset Title",
    )
    
    meta_description = models.CharField(
        max_length=300,
        verbose_name= "Asset Meta Description",
    )
    
    description = models.TextField(
        verbose_name= "Asset Description",
        default= 'Asset Description',
        blank= True,
        null=True,
    )
    
    tags = TaggableManager(
        blank = True,
        ordering = ["name",],
        verbose_name='Asset Tags',
    )
    
    asset = PrivateFileField(
        upload_to = get_asset_path,
        verbose_name = "Asset"
    )
    
    size = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        default= 0,
        verbose_name= 'Asset Size',
    )
    
    file_type = models.CharField(
        max_length= 50,
        default= '',
        blank= True,
    )
     
    status = models.CharField(
        max_length= 100,
        choices= asset_status,
        default= 'draft',
        verbose_name= "Asset Status",
    )
    
    date_created = models.DateTimeField(
        auto_now_add= True,
        verbose_name= "Date Created",
    )
    
    date_updated = models.DateTimeField(
        auto_now= True,
        verbose_name= "Date Updated",
    )
    
    date_published = models.DateTimeField(
        verbose_name= 'Date Published',
        blank= True,
        null = True,
    )
    
    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ["-date_created"]
        
    def __str__(self):
        return str(self.user.username + ' - ' + self.title)
    
    def clean(self,*args, **kwargs):
        if self.file_type == "":
            raw_file_types = str(self.category.required_file_types).split(',')
            
            file_types = [x.strip() for x in raw_file_types]
            
            if str(self.asset.name).split('.')[-1] not in file_types:
                raise ValidationError(
                    {"asset" : f'Required file types : {file_types}'}, 
                )
        if self.status == 'published':
            if not len(self.title) >= 20:
                raise ValidationError(
                    {"title" : f'Title is too small, Min-20(yours-{len(self.title)})'}, 
                )
            if not len(self.meta_description) >= 50:
                raise ValidationError(
                    {"meta_description" : f'Meta Description is too small, Min-50(yours-{len(self.meta_description)})'}, 
                )
            if not len(self.description) >= 200:
                raise ValidationError(
                    {"description" : f'Description is too small, Min-200(yours-{len(self.description)})'}, 
                )
            if not self.tags.count() >= 2:
                raise ValidationError(
                    {"tags" : f'Minimum 2 tags are required(yours-{self.tags.count()})'}, 
                )
        super().clean(*args, **kwargs)

    @property
    def is_eligible_for_publish(self):
        if len(self.title) >= 20 and len(self.meta_description) >= 50 and len(self.description) >= 200 and self.tags.count() >= 2 and self.asset_preview_images.count() >= 3 and self.licenses.count() >= 2:
            return True
        return False
    
    @property
    def get_eligible_for_publish_dict(self):
        dic = dict()
        if not len(self.title) >= 20:
            dic['title'] = f'Title is too small, Min-20(yours-{len(self.title)})'
        if not len(self.meta_description) >= 50:
            dic['meta_description'] = f'Meta Description is too small, Min-50(yours-{len(self.meta_description)})'
        if not len(self.description) >= 200:
            dic['description'] = f'Description is too small, Min-200(yours-{len(self.description)})'
        if not self.tags.count() >= 2:
            dic['tags'] = f'Minimum 2 tags are required(yours-{self.tags.count()})'
        if not self.asset_preview_images.count() >= 3:
            dic['asset_preview_images'] = f'Minimum 3 preview images are required(yours-{self.asset_preview_images.count()})'
        if not self.licenses.count() >= 2:
            dic['licenses'] = f'Minimum 2 license are required(yours-{self.licenses.count()})'
        return dic
    
    @property
    def get_rating(self):
        if self.rating or self.rating == None:
            rating = self.rating or 0
            rating_list = [0,0,0,0,0, 0, 0]
            for i in range(1, int(rating) + 1):
                rating_list[i] = 1
            rating_list[6] = int(self.total_rating)
            rating_list[0] = round(float(rating),1)
            return rating_list
        # else:
        #     assetfeedback_obj = self.feedbacks.all().aggregate(rating = Avg('rating'))
        #     assetfeedback_objC = self.feedbacks.all().count()
        #     rating_list = [0,0,0,0,0, 0, 0]
        #     if assetfeedback_obj['rating']:
        #         for i in range(1, int(assetfeedback_obj['rating']) + 1):
        #             rating_list[i] = 1
        #         rating_list[6] = int(assetfeedback_objC)
        #         rating_list[0] = float(assetfeedback_obj['rating'])
        #     return rating_list

    def get_absolute_url(self): 
        return str(reverse_lazy("assets:asset_detail",kwargs={'uuid' : self.uuid}))
    
    
    def did_user_purchase(self, user_obj):
        from orders.models import Order_Items
        order_item_obj = Order_Items.objects.filter(asset = self, order__user = user_obj, order__order_status = 'success').order_by('-date_created').first()
        if order_item_obj:
            if not AssetFeedback.objects.filter(order = order_item_obj.order, user = user_obj,asset = self).exists():
                return order_item_obj
        return False
    
class Asset_Preview_Images(models.Model):
    
    image = ResizedImageField(
        size=[720, 923], # aspect_ratio = 0.78:1
        crop=['middle', 'center'],
        quality=95,
        upload_to= get_asset_preview_image_path,
        verbose_name= 'Preview Image',
        validators = [asset_preview_image_validator,]
    )
    
    asset = models.ForeignKey(
        Asset,
        on_delete= models.CASCADE,
        related_name= 'asset_preview_images',
    )
    
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    
    def clean(self,*args, **kwargs):
        count = Asset_Preview_Images.objects.filter(asset = self.asset).count()
        if count >= 10:
            raise ValidationError(
                {"image" : f'You have already uploaded 10 preview images.'}, 
            )
        super().clean(*args, **kwargs)
    
    class Meta:
        verbose_name = "Asset Preview Image"
        verbose_name_plural = "Asset Preview Images"
        ordering = ["date_created"]
    
    @property
    def asset_preview_image_preview(self):
        if self.image:
            return mark_safe('<img src="/media/%s" width="200"  />' % (self.image))
        else:
            return mark_safe('<p>Add New Asset Preview Image</p>')
            
    def __str__(self):
        return str(self.asset.title)
    
class AssetFeedback(models.Model):
    order = models.ForeignKey(
        'orders.Orders',
        on_delete=models.CASCADE,
    )
    
    user = models.ForeignKey(
        get_user_model(),
        on_delete= models.CASCADE,
        verbose_name= 'User',
    )
    
    asset = models.ForeignKey(
        Asset,
        on_delete= models.CASCADE,
        verbose_name= 'Asset',
        related_name= 'feedbacks',
    )
    
    rating = models.IntegerField(
        default= 3,
        verbose_name= 'Rating',
    )
    
    feedback = models.TextField(
        verbose_name= 'Feedback',
    )
    
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name= 'Date Created'
    )
    
    def clean(self,*args, **kwargs):
        from orders.models import Order_Items
        order_item_obj = Order_Items.objects.filter(asset = self.asset,order = self.order, order__user = self.user, order__order_status = 'success').first()
        if not order_item_obj:
            raise ValidationError(
                {'feedback' : 'Can\'t give the feedback to unpurchased asset.'}
            )
        if AssetFeedback.objects.filter(order = self.order,user = self.user,asset = self.asset).exclude(pk = self.pk).exists():
            raise ValidationError(
                {'feedback' : 'Feedback is already given.'}
            )
        if self.rating > 5:
            raise ValidationError(
                {'rating' : 'Feedback rating can\'t be higher than 5.'}
            )
        if self.rating < 0:
            raise ValidationError(
                {'rating' : 'Feedback rating can\'t be lower than 0.'}
            )
        super().clean(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.asset.title} - {self.rating} - {self.user}"
    
    class Meta:
        verbose_name = "Asset Feedback"
        verbose_name_plural = "Asset Feedbacks"
        ordering = ["-date_created"]
