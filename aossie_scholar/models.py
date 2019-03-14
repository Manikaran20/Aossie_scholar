from django.db import models

# Create your models here.
class Author(models.Model):
	Title_name= models.CharField(max_length=500)
	Citations= models.CharField(max_length=50)
	CoAuthors= models.CharField(max_length=50)
	Normalized_citations= models.CharField(max_length=50)
	def __str__(self):
		return (self.Title_name)
