'''
Created on 19/03/2020

@author: mmp
'''
from django.test import TestCase
from utils.utils import Utils
from constants.constants_test_case import ConstantsTestsCase
from django.conf import settings
import os

class UtilsTest(TestCase):

	constantsTestsCase = ConstantsTestsCase()
	utils = Utils()

	def setUp(self):
		self.baseDirectory = os.path.join(settings.STATIC_ROOT, self.constantsTestsCase.MANAGING_TESTS)

	def tearDown(self):
		pass

	def test_paths(self):
		
		self.assertEqual("uploads/project_event/projectId_1/eventId_2/userId_3", self.utils.get_path_to_project_event_file(1, 2, 3))
		lst_data = self.utils.get_path_to_project_event_file_with_random(1, 2, 3).split('/')
		path_after_join = "/".join(lst_data[:-1])
		self.assertEqual("uploads/project_event/projectId_1/eventId_2/userId_3", path_after_join)
		
	def test_md5sum(self):
		file_to_test = os.path.join(self.baseDirectory, "md5sum", "TAT_P4_SE_2.pdf")
		self.assertTrue(os.path.exists(file_to_test))
		self.assertEqual("44f2b38ac0339b4fae020bbcf49cb405", self.utils.md5sum(file_to_test))



