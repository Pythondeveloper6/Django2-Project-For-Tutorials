from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils import encoding
# Create your models here.

level_choices = (
        ("All Levels", "All Levels"),
        ("Beginner" , "Beginner"),
        ("Intermediate" , "Intermediate"),
        ("Expert" , "Expert"),
)


class Post(models.Model):
    title   = models.CharField(max_length=100 )
    slug    = models.SlugField(null=True , blank=True , allow_unicode=True)
    content = RichTextField()
    image   = models.ImageField(upload_to='blog_images' , blank=True , default="/blog_images/blog.jpg" )
    updated = models.DateTimeField(auto_now=True , auto_now_add=False)
    created = models.DateTimeField(auto_now=False , auto_now_add=True)
    active  = models.BooleanField(default=True)
    level   = models.CharField(max_length=25, choices=level_choices )
    tag     = models.CharField(max_length=50 )


    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})


    def split_tag(self):
        return self.tag.split(',')



    def save(self, *args , **kwargs):
        if not self.slug and self.title :
            self.slug = slugify(self.title)
        super(Post , self).save(*args , **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering =  ["-created" , "-updated"]
