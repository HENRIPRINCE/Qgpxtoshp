# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui



import sys
import os
import os, re
import os.path
import math
import datetime
import platform
import socket
import processing
import time
import getpass

import qgis.utils

#Import de QGIS
from qgis import *
from qgis.core import *
from qgis.gui import *

# chargement du fichier d'interface graphique créé 
from Ui_gpx_shp import Ui_gpx_shp

from objet_gpx import *

"""
if str(platform.uname()[0]) == 'Windows':
	if str(platform.architecture()[0]) == '32bit':
		from objet_gpx_win32 import *
	if str(platform.architecture()[0]) == '64bit':
		from objet_gpx_win64 import *

if str(platform.uname()[0]) == 'Linux':
	if str(platform.architecture()[0]) == '32bit':
		from objet_gpx_lin32 import *
	if str(platform.architecture()[0]) == '64bit':
		from objet_gpx_lin64 import *
"""


# avoir path plugins
path_absolute = os.path.dirname(os.path.realpath(__file__))

class gpx_shpDialog(QDialog):
	def __init__(self): #On récupère le dictionnaire des communes
		QDialog.__init__(self) 
		# Set up the user interface from Designer. 
		self.ui = Ui_gpx_shp ()
		self.ui.setupUi(self)
		# SIGNAL SLOT
		self.connect(self.ui.btn_RepgpxOuvrir,SIGNAL("clicked()"), self.repGpxOuvrir)
		self.connect(self.ui.btn_RepshpSave,SIGNAL("clicked()"), self.RepShpSave)
		self.connect(self.ui.btn_Executer,SIGNAL("clicked()"), self.Executer)
		self.ui.lbl_moi_web.mousePressEvent = self.showmeDialog
			
	def showmeDialog(self, event):
		cls_SQL = Class_objet(self.ui)
		cls_SQL.showme(event)
		
	def repGpxOuvrir(self):
		#QtGui.QMessageBox.information(self, 'Message',  'hita bout1')
		cls_SQL = Class_objet(self.ui)
		cls_SQL.repGpxOuvrir_func()
		#compte gpx dans le rep
		#cls_SQL.compteGpx_func()

	def RepShpSave(self):
		#QtGui.QMessageBox.information(self, 'Message',  'hita bout2')
		cls_SQL = Class_objet(self.ui)
		cls_SQL.RepShpSave_func()
	
	def Executer(self):
		#QtGui.QMessageBox.information(self,'Message',"Veuillez selectionner le Repertoire pour le shapefile")
		cls_SQL = Class_objet(self.ui)
		cls_SQL.Executer_func()
		
