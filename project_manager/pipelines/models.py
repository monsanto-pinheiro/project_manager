from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create your models here.
class Pipeline(models.Model):

	class Meta:
		ordering = ['name', ]
		
	name = models.CharField(max_length=100, verbose_name='Name', db_index=True, unique=True)
	description = models.CharField(max_length=250, default='', verbose_name='Description')
	owner = models.ForeignKey(User, related_name='pipeline', on_delete=models.PROTECT)
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
	is_obsolete = models.BooleanField(default=False, verbose_name='Obsolete')
	is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')		## if this file was removed
	delete_date = models.DateTimeField(null=True, verbose_name='Delete Date')
	delete_owner = models.ForeignKey(User, related_name='delete_pipeline', blank=True, null=True, on_delete=models.PROTECT)
	
	def __str__(self):
		return self.name