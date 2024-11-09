'''
Created on Jan 5, 2018

@author: mmp
'''
from django.core.management import BaseCommand
from constants.constants import Constants
from django.contrib.auth.models import User

class Command(BaseCommand):
	'''
	classdocs
	'''
	help = "Load default references."
	## logging
	
	def __init__(self, *args, **kwargs):
		super(Command, self).__init__(*args, **kwargs)
	
	def create_default_user(self):
		"""
		create a default user to link the default references...
		"""
		self.__create_account(Constants.DEFAULT_USER, Constants.DEFAULT_USER_PASS, "notneed@notneed.com", False)


	def __create_account(self, user_name, password, email, b_active):
		"""
		try to create a default accounts
		"""
		try:
			user = User.objects.get(username=user_name)
			### great, the default user exist
		except User.DoesNotExist:
			
			self.stdout.write("Add user: {}".format(user_name))
			### need to create it
			user = User()
			user.username = user_name
			user.set_password(password)
			user.first_name = user_name
			user.email = email
			user.is_active = b_active
			user.is_staff = False
			user.is_superuser = False
			user.save()

		
	def handle(self, *args, **options):
		"""
		Start here
		"""
		self.stdout.write("Set default users...")
		self.create_default_user()

		self.stdout.write("End")
