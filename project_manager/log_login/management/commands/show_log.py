'''
Created on Jan 5, 2018

@author: mmp
'''
from django.core.management import BaseCommand
from django.conf import settings
from log_login.models import LoginHistory

class Command(BaseCommand):
	'''
	classdocs
	'''
	help = "Show log of users."
	## logging
	
	def __init__(self, *args, **kwargs):
		super(Command, self).__init__(*args, **kwargs)
	
	def show_log_history(self):
		"""
		create a default user to link the default references...
		"""
		count = 1
		for log_history in LoginHistory.objects.order_by("-creation_date")[:25]:
			self.stdout.write("{: <5}) {: <25} {: <19} {: <6} {}".format(count, log_history.owner.username,
				log_history.creation_date.strftime(settings.DATETIME_FORMAT_FOR_TABLE),
				log_history.operation, log_history.ip))
			count += 1
		
	def handle(self, *args, **options):
		"""
		Start here
		"""
		self.stdout.write("Show log history...")
		self.show_log_history()
