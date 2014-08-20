# -*- coding: utf-8 -*-
#####################################
#                                   #
# Views fuer SCOM Aktionsplan        #
#                                   #
# Author: Gabor Tanz                #
# Changed: 13.08.2014               #
#                                   #
#####################################
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import re
from datetime import date
import json

import logging # fuer Debugging

from scom.models import *

logging.basicConfig()
logger = logging.getLogger(__name__) # fuer Debugging

# Hauptseite
def index(request):
	# Variablen fuer nur offene Vorfaelle und sortieren nach Datum auf defaults setzen
	showall = 'offen'
	sort = 'datum'
	caption = 'Offene Vorfälle'
	caption_filter = ''
	caption_sort = ''

	# Sortierbutton als Sortieroption setzen
	if 'sort' in request.POST:
		sort = request.POST['sort']
		caption_sort = ' sortiert nach %s' % sort
	# Pruefen ob alle oder offene angezeigt werden sollen
	if 'showall' in request.POST:
		showall = request.POST['showall']
	
	# Daten aus DB holen
	aktionen = Aktion.objects.all()
	servers = Server.objects.all()
	sources = Source.objects.all()
	alerts = Alert.objects.all()
	operators = Operator.objects.all()
	stati = Status.objects.all()
	vorfaelle = Vorfall.objects.all()

	# je nachdem welcher filter angeklick wurde
	if 'filter' in request.POST:
		filter = json.loads(request.POST['filter'])
		if 'Operator' in filter:
			operator = Operator.objects.get(id=filter['Operator'])
			vorfaelle = vorfaelle.filter(operator=operator)
			caption_filter = ' erfasst von %s' % operator
		elif 'Server' in filter:
			server = Server.objects.get(id=filter['Server'])
			vorfaelle = vorfaelle.filter(server=server)
			caption_filter = ' von Server %s' % server
		elif 'Source' in filter:
			source = Source.objects.get(id=filter['Source'])
			vorfaelle = vorfaelle.filter(source=source)
			caption_filter = ' von Source %s' % source
		elif 'Alert' in filter:
			alert = Alert.objects.get(id=filter['Alert'])
			vorfaelle = vorfaelle.filter(alert=alert)
			caption_filter = ' von Alert %s' % alert

	# dictionary fuer template
	dictionary = {
		"aktionen": aktionen,
		"servers": servers,
		"sources": sources,
		"alerts": alerts,
		"operators": operators,
		"stati": stati,
		"showall": showall,
	}

	# falls nur offene angezeigt werden sollen
	if showall == 'offen':
		vorfaelle = vorfaelle.filter(status=1).order_by(sort)
		caption = caption + caption_filter + caption_sort
		dictionary['vorfaelle'] = vorfaelle
		dictionary['caption'] = caption		
		return render(request, 'scom/scom.html', dictionary)
	# alle Vorfaelle
	else:
		vorfaelle = vorfaelle.order_by(sort)
		caption = "Alle Vorfaelle" + caption_filter + caption_sort
		dictionary['vorfaelle'] = vorfaelle
		dictionary['caption'] = caption
		return render(request, 'scom/scom.html', dictionary)	


# Serverliste
def servers(request):
	servers = Server.objects.all().order_by('ip')
	oss = OS.objects.all()
	funktionen = Funktion.objects.all()

	return render(request, 'scom/servers.html', {
		"servers": servers,
		"oss": oss,
		"funktionen": funktionen,
	})


# Serverfunktion zu Auswalliste erfassen
def add_funktion(request):
	funktion = request.POST['funktion']
	if len(funktion) == 0:
		messages.add_message(request, messages.INFO, 'Geben Sie eine Funktion ein')
		return redirect('../../servers')

	Funktion(name=funktion).save()
	return redirect('../../servers')


# OS zu Auswalliste erfassen
def add_os(request):
	os = request.POST['os']
	if len(os) == 0:
		messages.add_message(request, messages.INFO, 'Geben Sie ein OS ein')
		return redirect('../../servers')

	OS(name=os).save()
	return redirect('../../servers')


# bestehende Serverinfos updaten
def update_server(request, server_id):
	#Server aus db holen
	server = Server.objects.get(id=server_id)
	# Server updaten
	if request.method == 'POST':
		if get_server_data(request) is not None:
			name, ip, funktion, os, is_virtual = get_server_data(request)
			server.name = name		
			server.ip = ip
			server.funktion = funktion
			server.os = os
			server.is_virtual = is_virtual
			server.save()
			return redirect('../')
		else:
			return redirect('../' + server_id + '/')		
	# Updateformular anzeigen
	else:
		oss = OS.objects.all()
		funktionen = Funktion.objects.all()
		return render(request, 'scom/update_server.html', {		
			"server": server,
			"oss": oss,
			"funktionen": funktionen,
		})


# Neuen Operator erfassen
def add_operator(request):
	operator = request.POST['operator']
	# entspricht Login
	if len(operator) != 4:
		messages.add_message(request, messages.INFO, 'Operator Name muss 4 zeichen lang sein')
		return redirect('../../')

	Operator(name=operator).save()
	return redirect('../../')


# Helperfunktion fuer update_server und add_server
def get_server_data(request):
	# Daten aus POST request holen
	name = request.POST['name']
	ip = request.POST['ip']
	funktion = Funktion.objects.get(name=request.POST['funktion'])
	os = OS.objects.get(name=request.POST['os'])
	is_virtual = False

	if 'is_virtual' in request.POST:
		is_virtual = True

	# Input Checks
	if len(name) == 0 or len(ip) == 0:
		messages.add_message(request, messages.INFO, 'Fuellen Sie das Formular vollstaendig aus')
		return

	# IP auf gueltigkeit pruefen
	octet = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
	ip_regex = re.compile('^' + octet + '\.' + octet + '\.' + octet + '\.' + octet + '$')
	if not ip_regex.match(ip):
		messages.add_message(request, messages.INFO, 'Keine gueltige Ip')
		return redirect('../')

	return name, ip, funktion, os, is_virtual


# Neuen server erfassen
def add_server(request):
	name, ip, funktion, os, is_virtual = get_server_data(request)
	Server(name=name, ip=ip, funktion=funktion, os=os, is_virtual=is_virtual).save()
	return redirect('../')


# Neue Source erfassen
def add_source(request):
	source = request.POST['source']
	if len(source) == 0:
		messages.add_message(request, messages.INFO, 'Geben Sie eine Source ein')
		return redirect('../../')

	Source(name=source).save()
	return redirect('../../')


# Neuen Alert erfassen
def add_alert(request):
	alert = request.POST['alert']
	if len(alert) == 0:
		messages.add_message(request, messages.INFO, 'Geben Sie einen Alert ein')
		return redirect('../../')

	Alert(name=alert).save()
	return redirect('../../')


# Vorfall erfassen
def add_vorfall(request):
	datum = date.today() # Immer aktuelles Datum
	# Daten aus POST Request holen
	operator = Operator.objects.get(name=request.POST['operator'])
	server = Server.objects.get(name=request.POST['server'])
	source = Source.objects.get(name=request.POST['source'])
	alert = Alert.objects.get(name=request.POST['alert'])
	status = Status.objects.get(name=request.POST['status'])
	aktion = request.POST['aktion']
	if len(aktion) == 0:
		messages.add_message(request, messages.INFO, 'Geben Sie eine Aktion ein')
		return redirect('../../')

	vorfall = Vorfall(datum=datum, operator=operator, server=server, source=source, alert=alert, status=status)
	vorfall.save()
	aktion = Aktion(datum=datum, operator=operator, name=aktion, vorfall=vorfall).save()

	return redirect('../../')


# Aktion erfassen
def add_aktion(request, vorfall_id):
	datum = date.today()
	vorfall = Vorfall.objects.get(id=vorfall_id)
	operator = Operator.objects.get(name=request.POST['operator'])
	status = Status.objects.get(name=request.POST['status'])
	aktion = request.POST['aktion']
	if len(aktion) == 0:
		messages.add_message(request, messages.INFO, 'Geben Sie eine Aktion ein')
		return redirect('../../')
	vorfall.status = status
	vorfall.save()
	aktion = Aktion(datum=datum, operator=operator, name=aktion, vorfall=vorfall).save()

	return redirect('../../')