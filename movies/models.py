from django.db import models

# Create your models here.
class Movie(models.Model):
    Not_Rated = 0
    Rating = (
        (0 , Not_Rated) ,
        (1 , 1),
        (2 , 2),
        (3 , 3),
        (4 , 4),
        (5 , 5)
    )

    Type = (
       ('Free' , 'Free') ,
       ('Paid' , 'Paid')
    )

    name = models.CharField( max_length=140)
    story = models.TextField(default="")
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=Rating , default=Not_Rated)
    type = models.CharField(choices=Type , max_length=5)
    watch_time = models.PositiveIntegerField()
    website = models.URLField(blank=True, max_length=200)
    most_watched = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = ("Movie")
        verbose_name_plural = ("Movies")

    def __str__(self):
        return self.name


