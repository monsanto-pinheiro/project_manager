'''
Created on 20/03/2020

@author: mmp
'''

from django_auth_ldap.backend import LDAPBackend
from django_auth_ldap.backend import _LDAPUser

class LDAPBackendEx(LDAPBackend):
	
	def authenticate(self, request, username=None, password=None):
		ldap_user = _LDAPUser(self, username=username + ("" if username.endswith("@ua.pt") else "@ua.pt"))
		user = ldap_user.authenticate(password)
		return user
	


	

