'''
Created on 19/03/2020

@author: mmp
'''
from django.test import TestCase
from django.contrib.auth import authenticate


# https://github.com/django-auth-ldap/django-auth-ldap/blob/master/tests/tests.py
class LdapTest(TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass

# 	def test_ldap(self):
# 		alice = authenticate(username="alice", password="password")
# 		monsanto = authenticate(username="monsanto", password="passss") 		### must be wuth @ua.pt
# 
# 		self.assertIsNone(alice)
# 		try:
# 			self.assertIsNotNone(monsanto)
# 		except :
# 			print("You must set a real password to run this test.")
# 			return
# 		self.assertIs(monsanto.is_active, True)
# 		self.assertIs(monsanto.is_staff, True)
# 		self.assertIs(monsanto.is_superuser, True) 
# 		self.assertEqual("Miguel", monsanto.first_name) 
# 		self.assertEqual("Pinheiro", monsanto.last_name) 
# 		self.assertEqual("monsanto@ua.pt", monsanto.email) 
	


