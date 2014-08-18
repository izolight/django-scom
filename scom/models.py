#####################################
#                                   #
# Models fuer SCOM Aktionsplan      #
#                                   #
# Author: Gabor Tanz                #
# Changed: 13.08.2014               #
#                                   #
#####################################

from django.db import models


class Funktion(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class OS(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name


class Server(models.Model):
	name = models.CharField(max_length=30)
	ip = models.IPAddressField()
	funktion = models.ForeignKey(Funktion, null=True)
	is_virtual = models.BooleanField(default=True)
	os = models.ForeignKey(OS, null=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']	


class Source(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Alert(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Operator(models.Model):
	name = models.CharField(max_length=4)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Status(models.Model):
	STATI = (('O','Offen'),('G', 'Geschlossen'))
	name = models.CharField(max_length=1,choices=STATI,default='O')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Stati'
		ordering = ['name']


class Vorfall(models.Model):
	datum = models.DateField()
	operator = models.ForeignKey(Operator)
	server = models.ForeignKey(Server)
	source = models.ForeignKey(Source)
	alert = models.ForeignKey(Alert)
	status = models.ForeignKey(Status)

	def __str__(self):
		return str(self.server) + '-' + str(self.source) + '-' + str(self.alert)

	class Meta:
		verbose_name_plural = 'Vorfaelle'


class Aktion(models.Model):
	datum = models.DateField()
	operator = models.ForeignKey(Operator)
	name = models.TextField()
	vorfall = models.ForeignKey(Vorfall)

	def __str__(self):
		return self.name