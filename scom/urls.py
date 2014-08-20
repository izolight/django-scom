# -*- coding: utf-8 -*-
#####################################
#                                   #
# Url Config fuer SCOM Aktionsplan   #
#                                   #
# Author: Gabor Tanz                #
# Changed: 13.08.2014               #
#                                   #
#####################################

from django.conf.urls import patterns, include, url
from scom import views

urlpatterns = patterns('',
    # Hauptseite
    url(r'^$', views.index), 
    # Serververwaltung
    url(r'^servers/$', views.servers),
    # einzelnen Server hinzufuegen
    url(r'^servers/add/$', views.add_server), 
    # bestehenden Server Updaten
    url(r'^servers/(\d+)/$', views.update_server),
    # Server-Funktion hinzufuegen
    url(r'^funktionen/add/$', views.add_funktion),
    # Server-OS hinzufuegen
    url(r'^os/add/$', views.add_os),
    # SCOM-Operator hinzufuegen
    url(r'^operators/add/$', views.add_operator),
    # SCOM-Source hinzufuegen
    url(r'^sources/add/$', views.add_source),
    # SCOM-Alert hinzufuegen
    url(r'^alerts/add/$', views.add_alert),
    # Vorfall hinzufuegen
    url(r'^vorfall/add/$', views.add_vorfall),
    # Aktion zu Vorfall hinzufuegen
    url(r'^vorfall/(\d+)/$', views.add_aktion),
)
