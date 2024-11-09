'''
Created on 17/03/2020

@author: mmp
'''
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, HTML
from crispy_forms.helper import FormHelper
from django.urls import reverse

class LoginForm(AuthenticationForm):

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

		field_text= [
			('username', 'Universal User (UU) - Aveiro University', 'A valid user name from University of Aveiro', True),
			('password', 'Password', ' ', True),
		]

		for x in field_text:
			self.fields[x[0]].label = x[1]
			self.fields[x[0]].help_text = x[2]
			self.fields[x[0]].required = x[3]
			self.fields[x[0]].widget.attrs['class'] = "form-control"	### set field wide
		
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.layout = Layout(
				HTML('<p><strong>Please, use Firefox, Safari or Chrome browsers for better view experience.</strong></p>'),
				'username',
				'password',
				ButtonHolder(
					Submit('login', 'Login', css_class='btn-primary'),
					Button('cancel', 'Cancel', css_class='btn-secondary', onclick='window.location.href="{}"'.format(reverse('dashboard'))),
				)
			)


# 	def clean_username(self):
#		"""
#		To test the email address
#		"""
# 		username = self.data['username']
# 		if '@' in username:
# 			try:
# 				username = User.objects.get(email=username).username
# 			except User.DoesNotExist as e:
# 				raise ValidationError(
# 					self.error_messages['invalid_login'],
# 					code='invalid_login',
# 					params={'username':self.username_field.verbose_name},
# 				)
# 		return username
	
