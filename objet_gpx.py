# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

import sys
import os
import re
import os.path
import math
import psycopg2
import datetime
import platform
import socket
import processing
import time

import qgis.utils

from qgis import *
from qgis.core import *
from qgis.gui import *

from os.path import basename
from xml.dom import minidom 
from collections import Counter

import shapefile
import shapefile as shp
import decimal


# avoir path plugins
path_absolute = os.path.dirname(os.path.realpath(__file__))

class Class_objet(object):
	def __init__(self, mon_UI):
		self.mon_UI = mon_UI
	
	
	def showme(self, event):
		mesinfos  = """<b><FONT COLOR='#2424B7'>Bienvenue RAHOILIJAONA</FONT></b>
				<br> <FONT COLOR='#FF6600'>Développeur Informatique et Programmeur en Géomatique</FONT>
				<br> Consultant Informatique, Développeur Géomaticien
				<br> gmail: <U>henriprincetoky@gmail.com</U>
				<br> Perso : +261 34 96 788 50
				"""
		QtGui.QMessageBox.information(QWidget(),'Message', mesinfos.decode("utf-8"))
	
	def repGpxOuvrir_func(self):
		#global path_absolute
		#dialog = QtGui.QFileDialog.getExistingDirectory(None, 'Select directory')
		dialog = QtGui.QFileDialog.getExistingDirectory(QWidget(), 'Select directory')
		if dialog:
			self.mon_UI.rep_travail.setText(dialog)
			isa_file = 0
			gpx_dir = dialog
			subdirs = [x[0] for x in os.walk(gpx_dir)]
			for subdir in subdirs:
				files  = os.walk(subdir).next()[2]
				if (len(files) > 0):
					for xfile in files:
						if xfile.endswith(".gpx"):
							isa_file +=1
			if isa_file > 0:
				self.mon_UI.lbl_Events.setText(str(isa_file))
			else:
				self.mon_UI.lbl_Events.setText("0")
	
	def compteGpx_func(self):
		gpx_dir = self.mon_UI.rep_travail.toPlainText()
		if gpx_dir != '':
			
			#len_mon_dir = len(gpx_dir)
			isa_file = 0
			subdirs = [x[0] for x in os.walk(gpx_dir)]
			for subdir in subdirs:
				files  = os.walk(subdir).next()[2]
				if (len(files) > 0):
					for xfile in files:
						if xfile.endswith(".gpx"):
							isa_file +=1
			if isa_file > 0:
				self.mon_UI.lbl_Events.setText(str(isa_file))
			else:
				self.mon_UI.lbl_Events.setText("0")
	
	def RepShpSave_func(self):
		filecsv = QFileDialog.getSaveFileName(QWidget(), "Selectionner fichier de sortie (shapefile) ","", '*.shp')
		if filecsv:
			self.mon_UI.rep_shpSave.setText(filecsv)
		return
	
	def update_progress(self, progress, sa_pos, nbre_tot):
		#longueur de la bar
		barLength = 20
		status = ""
		if isinstance(progress, int):
			progress = float(progress)
		if not isinstance(progress, float):
			progress = 0
			status = "error: progress var must be float\r\n"
		if progress < 0:
			progress = 0
			status = "Halt...\r\n"
		if progress >= 1:
			progress = 1
			status = "Done...\r\n"
		block = int(round(barLength*progress))
		#text = "\rStatus: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
		text = "\rStatus : " + sa_pos + " sur " + nbre_tot + " [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
		#sys.stdout.write(text)
		#sys.stdout.flush()
		self.mon_UI.lbl_progress.setText(text)
	
	def Executer_func(self):
		gpx_dir = self.mon_UI.rep_travail.toPlainText()
		shpSave = self.mon_UI.rep_shpSave.toPlainText()
		nbre_tot = self.mon_UI.lbl_Events.text()
		val_cmt = ""
		val_elev_pt = 0
		str_val_cmt = ""
		if shpSave != '' and gpx_dir != '' and int(nbre_tot) > 0 :
			#si file exists, enleve les
			if os.path.isfile(gpx_dir):
				reply = QtGui.QMessageBox.question(QWidget(),'Confirmation',"Ce fichier existe déjà, remplacer?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
				if reply ==  QtGui.QMessageBox.Yes:
					os.remove(gpx_dir)
					os.remove(gpx_dir[:-4] + ".shx")
					os.remove(gpx_dir[:-4] + ".dbf")
			# recuperer le nom de fichier
			infos_shp = QFileInfo(shpSave)
			Nomfile = infos_shp.baseName()
			son_rang = 1

			# Definir le point
			w = shp.Writer(shp.POINT)
			w.autoBalance = 1
			w.field("ID")
			w.field("nom_gpx",'C','100')
			w.field("id_point",'C','100')
			w.field("coor_x",'F','40')
			w.field("coor_y",'F','40')
			w.field("elev",'F','40')
			w.field("temps",'C','50')
			w.field("comments",'C','200')
			w.field("sous_dos",'C','100')
			w.field("nom_rep",'C','200')
			id=0
			# traiter le fichier gpx
			len_mon_dir = len(gpx_dir)
			subdirs = [x[0] for x in os.walk(gpx_dir)]
			for subdir in subdirs:
				try:
					files  = os.walk(subdir).next()[2]
					if (len(files) > 0):
						#nom sous dossier
						sous_dos = subdir[len_mon_dir +1 :]
						sous_rep = str(sous_dos).replace("\\","_")
						for xfile in files:
							if xfile.endswith(".gpx"):
								#traitement de fichier gpx
								son_rang +=1
								path_gpx = subdir + "/" + xfile
								doc = minidom.parse(path_gpx)
								gpx = doc.getElementsByTagName("gpx")
								wpt = doc.getElementsByTagName("wpt")
								isa = doc.getElementsByTagName("wpt").length
								if isa > 0:
									#traiter nombre de wpt
									for isaplus in range(isa):
										for elem in gpx:
											wpt = elem.getElementsByTagName("wpt")[isaplus]
											coor_x = wpt.getAttribute("lon")
											coor_y = wpt.getAttribute("lat")
											try:
												elev_pt = wpt.getElementsByTagName("ele")[0].firstChild.nodeValue
												if elev_pt:
													val_elev_pt = elev_pt
												else:
													val_elev_pt = 0
											except:
												pass	
											
											nom = wpt.getElementsByTagName("name")[0].firstChild.nodeValue 
											temps = wpt.getElementsByTagName("time")[0].firstChild.nodeValue
											try:
												commentaires = wpt.getElementsByTagName("cmt")[0].firstChild.nodeValue
												if commentaires:
													val_cmt = commentaires
												else:
													val_cmt = "NO_COMMENTS"
											except:
												pass
											
											#ajouter dans shapefile
											id +=1
											"""
											vertices = []
											parts = []
											vertices.append([float(coor_x),float(coor_y)])
											parts.append(vertices)
											w.point(parts)
											"""
											a_x = decimal.Decimal(coor_x)
											a_x = round(a_x,6)
											a_y = decimal.Decimal(coor_y)
											a_y = round(a_y,6)
											w.point(a_x, a_y)
											str_val_cmt = val_cmt.encode("utf-8") #.upper()
											
											#Enregistrer
											w.record(id, str(xfile)[:-4], str(nom), a_x, a_y, float(val_elev_pt), str(temps), str_val_cmt, sous_rep, gpx_dir)
								#dresser progress
								for ij in range(100):
									time.sleep(0.01)

									#appel function
									QtGui.qApp.processEvents()
									self.update_progress(ij/100.0, str(son_rang), str(nbre_tot))
				
				except:
					pass
				
			# sauvegarder shapefile
			w.save(shpSave)	

			# charger dans qgis avec SCR laborde 29702
			if self.mon_UI.chbxCanvas.isChecked() == True:
				layer = QgsVectorLayer(shpSave, Nomfile, "ogr")
				if not layer.isValid():
					QtGui.QMessageBox.information(QWidget(),'Message',"Impossible de charger le fichier")
				else:
					layer.setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) )
					QgsMapLayerRegistry.instance().addMapLayer(layer)	
	
		else:
			if gpx_dir == '':
				QtGui.QMessageBox.information(QWidget(),'Message',"Veuillez selectionner le Repertoire pour les fichiers gpx")
			if shpSave == '':
				QtGui.QMessageBox.information(QWidget(),'Message',"Veuillez selectionner le Repertoire pour le shapefile")
	
		
	