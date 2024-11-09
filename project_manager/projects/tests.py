from django.test import TestCase
from constants.constants_test_case import ConstantsTestsCase
from constants.meta_key_values import MetaKeyAndValue
from django.contrib.auth.models import User
from .models import Research, Institute, Specie, ProjectType, Project, MetaKeyProjects
from .manage_database import ManageDatabase
import datetime
# Create your tests here.

class testsReferenceFiles(TestCase):
	
	constantsTestsCase = ConstantsTestsCase()
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass

	def test_serialize(self):
		
		try:
			user = User.objects.get(username=ConstantsTestsCase.TEST_USER_NAME)
		except User.DoesNotExist:
			user = User()
			user.username = ConstantsTestsCase.TEST_USER_NAME
			user.is_active = False
			user.password = ConstantsTestsCase.TEST_USER_NAME
			user.save()
	
		test_name = "Name_test1"
		test_mail = "Name_test1 email"
		test_phone = "Name_test1 phone"
		Research.objects.create(name=test_name, email=test_mail, phone=test_phone, owner=user)
		research = Research.objects.get(name=test_name)
		Institute.objects.create(name=test_name, abbreviation=test_mail, city=test_phone, owner=user)
		institute = Institute.objects.get(name=test_name)
		Specie.objects.create(name=test_name, owner=user)
		specie = Specie.objects.get(name=test_name)
		
		abbreviation_xpto = "xpto"
		project_type = "project_type"
		ProjectType.objects.create(name=project_type, abbreviation=abbreviation_xpto, owner=user)
		project_type = ProjectType.objects.get(name=project_type, abbreviation=abbreviation_xpto)
		abbreviation_xpto_2 = "xpto.xpto"
		project_type_2 = "project_type_2"
		ProjectType.objects.create(name=project_type_2, abbreviation=abbreviation_xpto_2, owner=user)
		project_type_2 = ProjectType.objects.get(name=project_type_2, abbreviation=abbreviation_xpto_2)
		
		project = Project()
		project.description = "description _10"
		project.owner = user
		project.research = research
		project.institute = institute
		project.specie = specie
		project.project_type = project_type
		project.start_date = datetime.date.today()
		project.reference = project.get_project_reference()
		project.save()
		
		self.assertTrue(project.to_json().startswith('[{"model": "projects.project", "pk":'))
		
	def test_encrypted_fields(self):
		
		try:
			user = User.objects.get(username=ConstantsTestsCase.TEST_USER_NAME)
		except User.DoesNotExist:
			user = User()
			user.username = ConstantsTestsCase.TEST_USER_NAME
			user.is_active = False
			user.password = ConstantsTestsCase.TEST_USER_NAME
			user.save()
		
		test_name = "Name_test1"
		test_mail = "Name_test1 email"
		test_phone = "Name_test1 phone"
		Research.objects.create(name=test_name, email=test_mail, phone=test_phone, owner=user)
		research = Research.objects.get(name=test_name)
		self.assertEqual(research.name, test_name)
		self.assertEqual(research.email, test_mail)
		self.assertEqual(research.phone, test_phone)
		research = Research.objects.get(email=test_mail)
		self.assertEqual(research.name, test_name)
		self.assertEqual(research.email, test_mail)
		self.assertEqual(research.phone, test_phone)
		research = Research.objects.get(phone=test_phone)
		self.assertEqual(research.name, test_name)
		self.assertEqual(research.email, test_mail)
		self.assertEqual(research.phone, test_phone)
		
		try:
			research = Research.objects.get(phone="rese_tett  teet te  et")
			self.fail("Must fail")
		except Research.DoesNotExist:
			pass


		## Institute
		Institute.objects.create(name=test_name, abbreviation=test_mail, city=test_phone, owner=user)
		research = Institute.objects.get(name=test_name)
		self.assertEqual(research.name, test_name)
		self.assertEqual(research.abbreviation, test_mail)
		self.assertEqual(research.city, test_phone)
		research = Institute.objects.get(abbreviation=test_mail)
		self.assertEqual(research.name, test_name)
		self.assertEqual(research.abbreviation, test_mail)
		self.assertEqual(research.city, test_phone)
		research = Institute.objects.get(city=test_phone)
		self.assertEqual(research.name, test_name)
		self.assertEqual(research.abbreviation, test_mail)
		self.assertEqual(research.city, test_phone)
		
		try:
			research = Institute.objects.get(name="rese_tett  teet te  et")
			self.fail("Must fail")
		except Institute.DoesNotExist:
			pass


	def test_get_reference_name_project(self):
		
		manage_database = ManageDatabase()
		
		try:
			user = User.objects.get(username=ConstantsTestsCase.TEST_USER_NAME)
		except User.DoesNotExist:
			user = User()
			user.username = ConstantsTestsCase.TEST_USER_NAME
			user.is_active = False
			user.password = ConstantsTestsCase.TEST_USER_NAME
			user.save()

		try:
			user_2 = User.objects.get(username=ConstantsTestsCase.TEST_USER_NAME_2)
		except User.DoesNotExist:
			user_2 = User()
			user_2.username = ConstantsTestsCase.TEST_USER_NAME_2
			user_2.is_active = False
			user_2.password = ConstantsTestsCase.TEST_USER_NAME
			user_2.save()

		test_name = "Name_test1"
		test_mail = "Name_test1 email"
		test_phone = "Name_test1 phone"
		Research.objects.create(name=test_name, email=test_mail, phone=test_phone, owner=user)
		research = Research.objects.get(name=test_name)
		Institute.objects.create(name=test_name, abbreviation=test_mail, city=test_phone, owner=user)
		institute = Institute.objects.get(name=test_name)
		Specie.objects.create(name=test_name, owner=user)
		specie = Specie.objects.get(name=test_name)
		
		abbreviation_xpto = "xpto"
		project_type = "project_type"
		ProjectType.objects.create(name=project_type, abbreviation=abbreviation_xpto, owner=user)
		project_type = ProjectType.objects.get(name=project_type, abbreviation=abbreviation_xpto)
		abbreviation_xpto_2 = "xpto.xpto"
		project_type_2 = "project_type_2"
		ProjectType.objects.create(name=project_type_2, abbreviation=abbreviation_xpto_2, owner=user)
		project_type_2 = ProjectType.objects.get(name=project_type_2, abbreviation=abbreviation_xpto_2)

		project = Project()
		project.description = "description _1"
		project.owner = user
		project.research = research
		project.institute = institute
		project.specie = specie
		project.project_type = project_type
		project.start_date = datetime.date.today()
		project.reference = project.get_project_reference()
		project.save()

		project = Project()
		project.description = "description _2"
		project.owner = user
		project.research = research
		project.institute = institute
		project.specie = specie
		project.project_type = project_type
		project.start_date = datetime.date.today()
		project.reference = project.get_project_reference()
		project.save()
		manage_database.set_project_metakey(project, user,\
				MetaKeyAndValue.META_KEY_project_create, MetaKeyAndValue.META_VALUE_Success,
				project.to_json())
		
		project = Project()
		project.description = "description _3"
		project.owner = user
		project.research = research
		project.institute = institute
		project.specie = specie
		project.project_type = project_type
		project.start_date = datetime.date.today()
		project.reference = project.get_project_reference()
		project.save()

		####
		vect_out_reference = []
		for project in list(Project.objects.filter(project_type=project_type)):
			vect_out_reference.append(project.reference)
		self.assertEqual("xpto.2020.s3", vect_out_reference[0])
		self.assertEqual("xpto.2020.s2", vect_out_reference[1])
		self.assertEqual("xpto.2020.s1", vect_out_reference[2])


		project = Project()
		project.description = "description _4"
		project.owner = user_2
		project.research = research
		project.institute = institute
		project.specie = specie
		project.project_type = project_type
		project.start_date = datetime.date.today()
		project.reference = project.get_project_reference()
		project.save()
		for project in list(Project.objects.filter(project_type=project_type)):
			self.assertEqual("xpto.2020.s4", project.reference)
			break
		
		project = Project.objects.get(description="description _2")
		project.project_type = project_type_2
		project.reference = project.get_project_reference()
		project.save()
		manage_database.set_project_metakey(project, user,\
				MetaKeyAndValue.META_KEY_project_update, MetaKeyAndValue.META_VALUE_Success,
				project.to_json())
		
		project_key = manage_database.get_project_metakey_last(project, MetaKeyAndValue.META_KEY_project_update)
		self.assertTrue(project_key.description.find("description _2"))
		
		vect_out_reference = []
		for project in list(Project.objects.all()):
			vect_out_reference.append(project.reference)
		self.assertEqual("xpto.2020.s1", vect_out_reference[0])
		self.assertEqual("xpto.2020.s3", vect_out_reference[1])
		self.assertEqual("xpto.2020.s4", vect_out_reference[2])
		self.assertEqual("xpto.xpto.2020.s1", vect_out_reference[3])
		
		project = Project.objects.get(description="description _2")
		project.project_type = project_type_2
		project.reference = project.get_project_reference()
		project.save()
		
		vect_out_reference = []
		for project in list(Project.objects.all()):
			vect_out_reference.append(project.reference)
		self.assertEqual("xpto.2020.s1", vect_out_reference[0])
		self.assertEqual("xpto.2020.s3", vect_out_reference[1])
		self.assertEqual("xpto.2020.s4", vect_out_reference[2])
		self.assertEqual("xpto.xpto.2020.s1", vect_out_reference[3])
		
		project_update = Project.objects.get(description="description _2")
		project_update.description = "description_2_description_2"
		project_update.project_type = project_type
		project_update.reference = project_update.get_project_reference()
		project_update.save()
		manage_database.set_project_metakey(project_update, user,\
				MetaKeyAndValue.META_KEY_project_update, MetaKeyAndValue.META_VALUE_Success,
				project.to_json())
		
		vect_out_reference = []
		for project in list(Project.objects.all()):
			vect_out_reference.append(project.reference)
		self.assertEqual("xpto.2020.s1", vect_out_reference[0])
		self.assertEqual("xpto.2020.s3", vect_out_reference[1])
		self.assertEqual("xpto.2020.s4", vect_out_reference[2])
		self.assertEqual("xpto.2020.s5", vect_out_reference[3])
		
		project = Project()
		project.description = "description _5"
		project.owner = user_2
		project.research = research
		project.institute = institute
		project.specie = specie
		project.project_type = project_type
		project.start_date = datetime.date.today() + datetime.timedelta(days=356)
		project.reference = project.get_project_reference()
		project.save()
		manage_database.set_project_metakey(project, user,\
				MetaKeyAndValue.META_KEY_project_create, MetaKeyAndValue.META_VALUE_Success,
				project.to_json())
		
		vect_out_reference = []
		for project in list(Project.objects.all()):
			vect_out_reference.append(project.reference)
		self.assertEqual("xpto.2021.s1", vect_out_reference[0])
		self.assertEqual("xpto.2020.s1", vect_out_reference[1])
		self.assertEqual("xpto.2020.s3", vect_out_reference[2])
		self.assertEqual("xpto.2020.s4", vect_out_reference[3])
		self.assertEqual("xpto.2020.s5", vect_out_reference[4])
		
		project_key = manage_database.get_project_metakey_last(project_update, MetaKeyAndValue.META_KEY_project_update)
		self.assertTrue(project_key.description.find("description_2_description_2"))
		self.assertEqual(3, MetaKeyProjects.objects.filter(project=project_update).count())
		self.assertEqual(2, MetaKeyProjects.objects.filter(project=project_update, 
				meta_tag__name=MetaKeyAndValue.META_KEY_project_update).count())





