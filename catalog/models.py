from django.db import models
from django.template.defaultfilters import slugify
import os
import hashlib
import easy_thumbnails
from easy_thumbnails.fields import ThumbnailerImageField 
import datetime
from django.contrib.auth.models import *

# encoding: utf-8
# Create your models here.
def get_image_path(instance, filename):
	return os.path.join('photos', hashlib.md5(str(datetime.datetime.now)).hexdigest())

#categories models
class Category(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True, help_text='Unique value for product page URL, created from name.')
	description = models.TextField()
	is_active = models.BooleanField(default=True)
	meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='SEO keywords')
	meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'categories'
		ordering = ['-created_at']
		verbose_name_plural = 'Categories'
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		return ('catalog_category', (), { 'category_slug': self.slug })

#product models

class Product(models.Model):
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True,
help_text='Unique value for product page URL, created from name.')

	price = models.DecimalField(max_digits=9,decimal_places=2)
	old_price = models.DecimalField(max_digits=9,decimal_places=2,
blank=True,default=0.00)
	image = ThumbnailerImageField(upload_to = get_image_path, blank=True)
	is_active = models.BooleanField(default=True)
	is_bestseller = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	quantity = models.IntegerField()
	description = models.TextField()
	meta_keywords = models.CharField(max_length=255,
									help_text='Comma-delimited set of SEO keywords for meta tag')
	meta_description = models.CharField(max_length=255,
									help_text='Content for description meta tag')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(Category)
	user = models.ForeignKey(User)
	class Meta:
		db_table = 'products'
		ordering = ['-created_at']
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		return ('catalog_product', (), { 'product_slug': self.slug })
	def sale_price(self):
		if self.old_price > self.price:
			return self.price
		else:
			return None

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Product, self).save(*args, **kwargs)