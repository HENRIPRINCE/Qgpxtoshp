# -*- coding: utf-8 -*-

from PyQt4.QtSql import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

import sys
import os
import os, re
import os.path
import math
import psycopg2
import datetime
import platform
import socket
import processing
import qgis.utils

from qgis import *
from qgis.core import *
from qgis.gui import *
from Ui_gpx_shp import Ui_gpx_shp
from objet_tools import *


path_absolute = os.path.dirname(os.path.realpath(__file__))


class gpx_shpDialog(QDialog):
	def __init__(self):
		# On récupère le dictionnaire des communes
		QDialog.__init__(self)
		# Set up the user interface from Designer.
		self.ui = Ui_gpx_shp()
		self.ui.setupUi(self)
		
		#treeView
		self.model = QStandardItemModel()
		self.model.setHorizontalHeaderLabels([self.tr("DATA_SERVER")])
		self.ui.tV_table.setContextMenuPolicy(Qt.CustomContextMenu)
		self.ui.tV_table.customContextMenuRequested.connect(self.openMenu)
		self.ui.tV_table.clicked.connect(self.on_treeView_clicked)

		# SIGNAL SLOT
		self.connect(self.ui.btn_Cnx, SIGNAL("clicked()"), self.loginuser)
		self.connect(self.ui.r_spatial, SIGNAL("clicked()"), self.radio1_clicked)
		self.connect(self.ui.r_nonspatial, SIGNAL("clicked()"), self.radio2_clicked)
		self.ui.liste_base.currentItemChanged.connect(self.chargertable)
		self.connect(self.ui.btn_Ajout, SIGNAL("clicked()"), self.ajouter)
		self.connect(self.ui.btn_Annule_Select, SIGNAL("clicked()"), self.annule_tous)

		self.ui.son_statut.setVisible(False)
		self.ui.base_encours.setVisible(False)
		self.ui.btn_Ajout.setDisabled(True)
		self.ui.btn_Annule_Select.setDisabled(True)
		
		rep_epidemio=os.path.join(path_absolute, 'tmp_dos/epidemio.png')
		rep_IPM=os.path.join(path_absolute, 'tmp_dos/IPM.png')
		self.ui.label_epidemio.setPixmap(QtGui.QPixmap(rep_epidemio))
		self.ui.label_ipm.setPixmap(QtGui.QPixmap(rep_IPM))
		

	def openMenu(self, position):
		indexes = self.ui.tV_table.selectedIndexes()
		if len(indexes) > 0:

			level = 0
			index = indexes[0]
			while index.parent().isValid():
				index = index.parent()
				level += 1
		
		menu = QMenu()
		if level == 0:
			menu.addAction(self.tr("Edit person"))
		elif level == 1:
			menu.addAction(self.tr("Edit DATA_SERVER/container"))
		elif level == 2:
			menu.addAction(self.tr("Edit DATA_SERVER"))

		menu.exec_(self.ui.tV_table.viewport().mapToGlobal(position))
	
	
	def on_treeView_clicked(self):
		"""
		index = self.ui.tV_table.selectedIndexes()[0]
		fileName = index.model().itemFromIndex(index).text()
		isanZaza=0
		Zanany = index.model().itemFromIndex(index).rowCount()
		for isa in range (0, Zanany):
			isanZaza +=1
		
		if isanZaza == 0:
			QtGui.QMessageBox.information(self, 'Message',  fileName)
		else:
			QtGui.QMessageBox.information(self, 'Message',  'reniny')	
		"""
		cls_SQL = Class_objet(self.ui)
		cls_SQL.on_treeView_clicked_fonc()
	
	def loginuser(self):
		txt_login = self.ui.son_login.toPlainText()
		txt_mdp = self.ui.son_mdp.text()
		if txt_login != '' and txt_mdp != '':
			cls_SQL = Class_objet(self.ui)
			cls_SQL.login_ici()
		else:
			QtGui.QMessageBox.information(self, 'Message', "Veuillez identifier votre login et mot de passe")
			

	def radio1_clicked(self):
		cls_radio1 = Class_objet(self.ui)
		cls_radio1.click_radio1()
		#vider
				
	def radio2_clicked(self):
		cls_radio2 = Class_objet(self.ui)
		cls_radio2.click_radio2()
		#vider
		
	def chargertable(self):
		cls_chargertable = Class_objet(self.ui)
		cls_chargertable.chargertable_fonc()
		

	def ajouter(self):
		isanZananySeleky=0
		#for index in self.ui.tV_table.selectedIndexes():
		for index in self.ui.tV_table.selectionModel().selectedIndexes():
			isanZaza=0
			Zanany = index.model().itemFromIndex(index).rowCount()
			for isa in range (0, Zanany):
				isanZaza +=1
				
			if isanZaza == 0:
				isanZananySeleky +=1
				fileName = index.model().itemFromIndex(index).text()
				#QtGui.QMessageBox.information(self, 'isan zaza :', fileName)
				#appel function
				cls_ajouter = Class_objet(self.ui)
				cls_ajouter.ajouter_fonc(fileName)
		
		"""
		#QtGui.QMessageBox.information(self, 'isan zaza :', str(isanZananySeleky))
		if isanZananySeleky > 0:
			cls_ajouter = Class_objet(self.ui)
			cls_ajouter.ajouter_fonc()
		"""
	
	def annule_tous(self):
		"""
		if self.ui.liste_table.count()>0:
			self.ui.liste_table.clearSelection()
		"""
		self.ui.tV_table.clearSelection()
		
		
	

	