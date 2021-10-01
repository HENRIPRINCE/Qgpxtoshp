# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import sys
import os
import os.path
import shapefile
import shapefile as shp
import math
import processing
#Import de QGIS
from qgis import *
from qgis.core import *
from qgis.gui import *

# chargement du fichier d'interface graphique créé 
from Ui_gridLaborde import Ui_gridLaborde

dx=0
dy=0

# avoir path plugins
path_absolute = os.path.dirname(os.path.realpath(__file__))

class gridLabordeDialog(QDialog):
	def __init__(self): #On récupère le dictionnaire des communes
		QDialog.__init__(self) 
		# Set up the user interface from Designer. 
		self.ui = Ui_gridLaborde ()
		self.ui.setupUi(self)
		

		#IMPORTANT :
		#Recupetation dans self.iface des proprietes d'acces à l'interface ! (self.iface)
		# self.iface = classe_iface_parent.iface
		# et aussi le QgsMapCanvas
		# self.canvas = self.iface.mapCanvas()
		
		# pour remplir echelle et orientation, Format
		self.ui.cbxEchelle.addItems("2500 5000 10000 12500 50000 100000" .split())
		self.ui.cbxOrientation.addItems("Portrait Paysage" .split())
		self.ui.cbxFormat.addItems("A4 A3 A2 A1" .split())		
		
		# SIGNAL SLOT
		self.connect(self.ui.chbxMarge,SIGNAL("clicked()"), self.activeMarge)
		self.connect(self.ui.chbxLayer,SIGNAL("clicked()"), self.chargerCoucheExist)
		self.connect(self.ui.btn_RepshpOuvrir,SIGNAL("clicked()"), self.repShpOuvrir)
		self.connect(self.ui.btn_RepshpSave,SIGNAL("clicked()"), self.RepShpSave)
		self.connect(self.ui.btn_Executer,SIGNAL("clicked()"), self.Executer)
		
		self.connect(self.ui.cbxLayer,SIGNAL("currentIndexChanged(int)"),self.trouver_coor)
		self.connect(self.ui.cbxEchelle,SIGNAL("currentIndexChanged(int)"),self.trouver_grille)
		self.connect(self.ui.cbxOrientation,SIGNAL("currentIndexChanged(int)"),self.trouver_grille)
		self.connect(self.ui.cbxFormat,SIGNAL("currentIndexChanged(int)"),self.trouver_grille)
		
		# rendre invisible
		
		self.ui.x_max_2.setVisible(False)
		self.ui.y_max_2.setVisible(False)
		self.ui.x_min_2.setVisible(False)
		self.ui.y_min_2.setVisible(False)
		
		
		
	def activeMarge(self):
		if self.ui.chbxMarge.isChecked() == True:
			self.ui.grb_Marge.setEnabled(True)
		else:
			self.ui.grb_Marge.setEnabled(False)
			
			
	# pour choisir le fichier dans DialogBox standard			
	def repShpOuvrir(self):
		global path_absolute
		self.ui.cbxLayer.clear()
		dialog = QtGui.QFileDialog.getOpenFileName(self, "Ouvrir Fichier Vecteur...", None,
		"Shape (*.shp)")
		if dialog:
			self.ui.cbxLayer.addItem(dialog)
			shpEtoTmp = self.ui.cbxLayer.currentText()
			#rep_shpLaborde='C:/Users/rbienvenue/.qgis2/python/plugins/gridLaborde/tmp_shp/shpLaborde.shp'
			rep_shpLaborde=os.path.join(path_absolute, 'tmp_shp/shpLaborde.shp')
			rep_shpLaborde=rep_shpLaborde.replace('\\','/')
			
			"""
			#Supprimer si déjà existé mais ils sont attaché par le programme qgis
			rep_shp_dbf=os.path.join(path_absolute, 'tmp_shp/shpLaborde.dbf')
			rep_shp_shx=os.path.join(path_absolute, 'tmp_shp/shpLaborde.shx')
			rep_shp_prj=os.path.join(path_absolute, 'tmp_shp/shpLaborde.prj')
			rep_shp_qpj=os.path.join(path_absolute, 'tmp_shp/shpLaborde.qpj')
			
			rep_shp_dbf=rep_shp_dbf.replace('\\','/')
			rep_shp_shx=rep_shp_shx.replace('\\','/')
			rep_shp_prj=rep_shp_prj.replace('\\','/')
			rep_shp_qpj=rep_shp_qpj.replace('\\','/')
			
			if os.path.exists(rep_shpLaborde)==True and os.path.exists(rep_shp_dbf)==True and os.path.exists(rep_shp_shx)==True:
				os.remove(rep_shpLaborde)
				os.remove(rep_shp_dbf)
				os.remove(rep_shp_shx)
			if os.path.exists(rep_shp_prj)==True and os.path.exists(rep_shp_qpj)==True:
				os.remove(rep_shpLaborde)
				os.remove(rep_shp_dbf)
				os.remove(rep_shp_shx)
			"""	
			
			# verifie sa projection
			layer = QgsVectorLayer(shpEtoTmp ,  'shpWGS84', "ogr")
			crs_eto=layer.crs().authid()
			nom_crs=str(crs_eto)
			# si WGS84
			# if nom_crs=='EPSG:4326':
			if crs_eto=='EPSG:4326':
				# pour afficher extent initial
				shpEto = self.ui.cbxLayer.currentText()
				sf_Init = shapefile.Reader(shpEto)
				shapes = sf_Init.shapes()
				# XMin YMin XMax Ymax
				bbox = shapes[0].bbox
				self.ui.x_min.setText(str(Minbbox[0]))
				self.ui.y_min.setText(str(Minbbox[1]))
				self.ui.x_max.setText(str(Maxbbox[0]))
				self.ui.y_max.setText(str(Maxbbox[1]))
				
				# transforme en fichier Laborde pour calculer en metric
				processing.runalg("qgis:reprojectlayer", shpEtoTmp, "epsg:29702", rep_shpLaborde)
				layer2 = QgsVectorLayer(rep_shpLaborde ,  'shpLaborde', "ogr")
				box_laborde = layer2.extent().toString()
				# crs_eto2=layer2.crs().authid()
				# XMin, YMin : XMax, Ymax
				bbox =box_laborde.split(":")
				Minbbox=bbox[0].split(",")
				Maxbbox=bbox[1].split(",")
				# pour calculer en laborde
				self.ui.x_min_2.setText(str(Minbbox[0]))
				self.ui.y_min_2.setText(str(Minbbox[1]))
				self.ui.x_max_2.setText(str(Maxbbox[0]))
				self.ui.y_max_2.setText(str(Maxbbox[1]))	
				
			else:
				shpEto = self.ui.cbxLayer.currentText()
				sf = shapefile.Reader(shpEto)
				shapes = sf.shapes()
				# XMin YMin XMax Ymax
				bbox = shapes[0].bbox 
				self.ui.x_min.setText(str(bbox[0]))
				self.ui.y_min.setText(str(bbox[1]))
				self.ui.x_max.setText(str(bbox[2]))
				self.ui.y_max.setText(str(bbox[3]))
				# pour calculer en laborde
				self.ui.x_min_2.setText(str(bbox[0]))
				self.ui.y_min_2.setText(str(bbox[1]))
				self.ui.x_max_2.setText(str(bbox[2]))
				self.ui.y_max_2.setText(str(bbox[3]))
		return		

	def RepShpSave(self):
		filecsv = QFileDialog.getSaveFileName(self, "Selectionner fichier de sortie (shapefile) ","", '*.shp')
		if filecsv:
			self.ui.rep_shpSave.setText(filecsv)
		return
	
	def chargerCoucheExist(self):
		self.ui.cbxLayer.clear()
		if self.ui.chbxLayer.isChecked() == True:
			#names = [layer.name() for layer in QgsMapLayerRegistry.instance().mapLayers().values()]
			# for layer in QgsMapLayerRegistry.instance().mapLayers().values():
			layer_list = []
			layers = QgsMapLayerRegistry.instance().mapLayers().values()
			for layer in layers:
				# pour verifier si vecteur
				# if layer.type() == QgsMapLayer.VectorLayer or QgsMapLayer.rasterLayer:
				if layer.type() == QgsMapLayer.VectorLayer:
					# layers = self.iface.activeLayer()
					# if layer > 0:
					layer_list.append(layer.name())
			self.ui.cbxLayer.addItems(layer_list)
	
	def trouver_coor(self):
		if self.ui.chbxLayer.isChecked() == True:
			global path_absolute
			# on cherche par layer en cours
			s_LayerIndex = self.ui.cbxLayer.currentIndex
			n_layer = str(self.ui.cbxLayer.currentText())
			# rep_shpLaborde=rep_shpLaborde='C:/Users/rbienvenue/.qgis2/python/plugins/gridLaborde/tmp_shp/shpLaborde.shp'
			rep_shpLaborde=os.path.join(path_absolute, 'tmp_shp/shpLaborde.shp')
			rep_shpLaborde=rep_shpLaborde.replace('\\','/')
			vl = QgsMapLayerRegistry.instance().mapLayersByName(n_layer)[0]
			# verifie sa projection
			crs_eto=vl.crs().authid()
			nom_crs=str(crs_eto)
			# si WGS84
			#if nom_crs=='EPSG:4326':
			if crs_eto=='EPSG:4326':
				# pour afficher extent initial
				box_Init = vl.extent().toString()
				# XMin, YMin : XMax, Ymax
				bbox =box_Init.split(":")
				Minbbox=bbox[0].split(",")
				Maxbbox=bbox[1].split(",")
				self.ui.x_min.setText(str(Minbbox[0]))
				self.ui.y_min.setText(str(Minbbox[1]))
				self.ui.x_max.setText(str(Maxbbox[0]))
				self.ui.y_max.setText(str(Maxbbox[1]))
				
				# transforme en fichier Laborde pour calculer en metric
				processing.runalg("qgis:reprojectlayer", vl, "epsg:29702", rep_shpLaborde)
				layer2 = QgsVectorLayer(rep_shpLaborde ,  'shpLaborde', "ogr")
				# crs_eto2=layer2.crs().authid()
				box_laborde = layer2.extent().toString()
				# XMin, YMin : XMax, Ymax
				bbox =box_laborde.split(":")
				Minbbox=bbox[0].split(",")
				Maxbbox=bbox[1].split(",")
				# pour calculer en laborde
				self.ui.x_min_2.setText(str(Minbbox[0]))
				self.ui.y_min_2.setText(str(Minbbox[1]))
				self.ui.x_max_2.setText(str(Maxbbox[0]))
				self.ui.y_max_2.setText(str(Maxbbox[1]))
				
			else:
				box = vl.extent().toString()
				# XMin, YMin : XMax, Ymax
				bbox =box.split(":")
				Minbbox=bbox[0].split(",")
				Maxbbox=bbox[1].split(",")
				self.ui.x_min.setText(str(Minbbox[0]))
				self.ui.y_min.setText(str(Minbbox[1]))
				self.ui.x_max.setText(str(Maxbbox[0]))
				self.ui.y_max.setText(str(Maxbbox[1]))
				# pour calculer en laborde
				self.ui.x_min_2.setText(str(Minbbox[0]))
				self.ui.y_min_2.setText(str(Minbbox[1]))
				self.ui.x_max_2.setText(str(Maxbbox[0]))
				self.ui.y_max_2.setText(str(Maxbbox[1]))
				
				

	def trouver_grille(self):
		"""
		1cm carte donne 50 000 cm  ou 50m ou 0.05 km sur terrain
		donc trouver par orientation et format, echelle
		"""
		global dx
		global dy
		# minx,maxx,miny,maxy = float(self.ui.x_min.toPlainText()), float(self.ui.x_max.toPlainText()),float(self.ui.y_min.toPlainText()), float(self.ui.y_max.toPlainText())
		minx,maxx,miny,maxy = float(self.ui.x_min_2.toPlainText()), float(self.ui.x_max_2.toPlainText()),float(self.ui.y_min_2.toPlainText()), float(self.ui.y_max_2.toPlainText())
		# trouver dimension grille par format et orientation
		if self.ui.cbxFormat.currentText() =='A4':
			if self.ui.cbxOrientation.currentText() =='Portrait':
				dx = 0.21 * int(self.ui.cbxEchelle.currentText())
				dy = 0.297 * int(self.ui.cbxEchelle.currentText())
			if self.ui.cbxOrientation.currentText() =='Paysage':
				dx = 0.297 * int(self.ui.cbxEchelle.currentText())
				dy = 0.21 * int(self.ui.cbxEchelle.currentText())
		elif self.ui.cbxFormat.currentText() =='A3':
			if self.ui.cbxOrientation.currentText() =='Portrait':
				dx = 0.297 * int(self.ui.cbxEchelle.currentText())
				dy = 0.42 * int(self.ui.cbxEchelle.currentText())
			if self.ui.cbxOrientation.currentText() =='Paysage':
				dx = 0.42 * int(self.ui.cbxEchelle.currentText())
				dy = 0.297 * int(self.ui.cbxEchelle.currentText())
		elif self.ui.cbxFormat.currentText() =='A2':
			if self.ui.cbxOrientation.currentText() =='Portrait':
				dx = 0.42 * int(self.ui.cbxEchelle.currentText())
				dy = 0.594 * int(self.ui.cbxEchelle.currentText())
			if self.ui.cbxOrientation.currentText() =='Paysage':
				dx = 0.594 * int(self.ui.cbxEchelle.currentText())
				dy = 0.42 * int(self.ui.cbxEchelle.currentText())
		else:
			if self.ui.cbxOrientation.currentText() =='Portrait':
				dx = 0.594 * int(self.ui.cbxEchelle.currentText())
				dy = 1.188 * int(self.ui.cbxEchelle.currentText())
			if self.ui.cbxOrientation.currentText() =='Paysage':
				dx = 10.188 * int(self.ui.cbxEchelle.currentText())
				dy = 0.594 * int(self.ui.cbxEchelle.currentText())
		
		# trouver nombre grille
		nbrx = int(math.ceil(abs(maxx - minx)/dx))
		nbry = int(math.ceil(abs(maxy - miny)/dy))
		# afficher pour informations
		totGrid=nbrx*nbry
		self.ui.lbl_Gridxy.setText(str(dx) + " x " + str(dy))
		self.ui.lbl_Nbregrid.setText("Total: " + str(totGrid) + " dont :" + str(nbrx) + " x " + str(nbry))
	
	def Executer(self):
		repEto = self.ui.rep_shpSave.toPlainText()
		if repEto != '':
			# recuperer le nom de fichier
			infos_shp = QFileInfo(repEto)
			Nomfile = infos_shp.baseName()
			#Creer grid
			# minx,maxx,miny,maxy = float(self.ui.x_min.toPlainText()), float(self.ui.x_max.toPlainText()),float(self.ui.y_min.toPlainText()), float(self.ui.y_max.toPlainText())
			minx,maxx,miny,maxy = float(self.ui.x_min_2.toPlainText()), float(self.ui.x_max_2.toPlainText()),float(self.ui.y_min_2.toPlainText()), float(self.ui.y_max_2.toPlainText())
			nx = int(math.ceil(abs(maxx - minx)/dx))
			ny = int(math.ceil(abs(maxy - miny)/dy))
			# Ajouter marge pour la dernière case si avec marge
			if self.ui.chbxMarge.isChecked() == True:
				if self.ui.xMarge.toPlainText() !='' and self.ui.yMarge.toPlainText() !='':
					if self.ui.xMarge.toPlainText().isnumeric()==True and self.ui.yMarge.toPlainText().isnumeric() ==True:
						plus_y=(int(self.ui.yMarge.toPlainText())*ny)*3
						plus_x=(int(self.ui.xMarge.toPlainText())*nx)*2
						minx,maxx,miny,maxy =minx,maxx+plus_x,miny-plus_y,maxy #+plus_y
						
			
			# Definir le polygone
			w = shp.Writer(shp.POLYGON)
			w.autoBalance = 1
			w.field("ID")
			w.field("Ech")
			w.field("Sens")
			w.field("Format")
			w.field("nom_grid")
			w.field("nom_row")
			w.field("nom_col")
			w.field("marge_row")
			w.field("marge_col")
			w.field("unite")
			id=0
			# verifier si avec marge
			if self.ui.chbxMarge.isChecked() == True:
				if self.ui.xMarge.toPlainText() =='' or self.ui.yMarge.toPlainText() =='':
					QtGui.QMessageBox.information(self,'Message',"Valeur incorrecte pour les champs")
					if self.ui.xMarge.toPlainText() =='':
						self.ui.xMarge.setFocus()
					if self.ui.yMarge.toPlainText() =='':
						self.ui.yMarge.setFocus()
					# sortie de la function
					return None
				if self.ui.xMarge.toPlainText().isnumeric()==False or self.ui.yMarge.toPlainText().isnumeric() ==False:
					QtGui.QMessageBox.information(self,'Message',"Valeur incorrecte pour les champs")
					return None
				# charger marge dans le champs
				val_xMarge =self.ui.xMarge.toPlainText()
				val_xMarge =self.ui.yMarge.toPlainText()
				val_unite='metre'
			else:
				val_xMarge =''
				val_xMarge =''
				val_unite =''
			

			
				
			# charger les shapes		
			for i in range(ny):
				for j in range(nx):
					id+=1
					vertices = []
					parts = []
					if self.ui.xMarge.toPlainText() !='' and self.ui.yMarge.toPlainText() != '':
						# x =j, y = i
						if j==0 and i==0:
							vertices.append([min(minx+dx*j,maxx),max(maxy-dy*i,miny)])
							vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*i,miny)])
							vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*(i+1),miny)])
							vertices.append([min(minx+dx*j,maxx),max(maxy-dy*(i+1),miny)])
							
						if j ==0 and i>0:
							# dymarge=2*i
							dymarge=int(self.ui.yMarge.toPlainText())*i
							vertices.append([min(minx+dx*j,maxx),max(maxy-dy*i,miny)+dymarge])
							vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*i,miny)+dymarge])
							vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*(i+1),miny)+dymarge])
							vertices.append([min(minx+dx*j,maxx),max(maxy-dy*(i+1),miny)+dymarge])
					   
						if j>0 and i==0:
							# dxmarge=2*j
							dxmarge=int(self.ui.xMarge.toPlainText())*j
							vertices.append([min(minx+dx*j,maxx)-dxmarge,max(maxy-dy*i,miny)])
							vertices.append([min(minx+dx*(j+1),maxx)-dxmarge,max(maxy-dy*i,miny)])
							vertices.append([min(minx+dx*(j+1),maxx)-dxmarge,max(maxy-dy*(i+1),miny)])
							vertices.append([min(minx+dx*j,maxx)-dxmarge,max(maxy-dy*(i+1),miny)])
						
						
						if j>0 and i>0:
							# dxmarge=2*j
							# dymarge=2*i
							dymarge=int(self.ui.yMarge.toPlainText())*i
							dxmarge=int(self.ui.xMarge.toPlainText())*j
							vertices.append([min(minx+dx*j,maxx)-dxmarge,max(maxy-dy*i,miny)+dymarge])
							vertices.append([min(minx+dx*(j+1),maxx)-dxmarge,max(maxy-dy*i,miny)+dymarge])
							vertices.append([min(minx+dx*(j+1),maxx)-dxmarge,max(maxy-dy*(i+1),miny)+dymarge])
							vertices.append([min(minx+dx*j,maxx)-dxmarge,max(maxy-dy*(i+1),miny)+dymarge])
					
					else:
						vertices.append([min(minx+dx*j,maxx),max(maxy-dy*i,miny)])
						vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*i,miny)])
						vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*(i+1),miny)])
						vertices.append([min(minx+dx*j,maxx),max(maxy-dy*(i+1),miny)])
						
					# charger shapefile
					parts.append(vertices)
					w.poly(parts)
					w.record(id, 
					str(self.ui.cbxEchelle.currentText()),
					str(self.ui.cbxOrientation.currentText()),
					str(self.ui.cbxFormat.currentText()),
					str(i) +"_" + str(j), i, j, val_xMarge, val_xMarge, val_unite)
			# sauvegarder shapefile
			w.save(repEto)
			
			# charger dans qgis avec SCR laborde 29702
			if self.ui.chbxCanvas.isChecked() == True:
				layer = QgsVectorLayer(repEto, Nomfile, "ogr")
				if not layer.isValid():
					QtGui.QMessageBox.information(self,'Message',"Impossible de charger le fichier")
				else:
					layer.setCrs( QgsCoordinateReferenceSystem(29702, QgsCoordinateReferenceSystem.EpsgCrsId) )
					QgsMapLayerRegistry.instance().addMapLayer(layer)
			# vider tous les champs
			self.ui.chbxLayer.setChecked(False)
			self.ui.cbxLayer.clear()
			self.ui.chbxMarge.setChecked(False)
			self.ui.grb_Marge.setEnabled(False)
			self.ui.xMarge.setText('')
			self.ui.yMarge.setText('')
			self.ui.x_min.setText('')
			self.ui.y_min.setText('')
			self.ui.x_max.setText('')
			self.ui.y_max.setText('')
			# pour calculer en laborde
			self.ui.x_min_2.setText('')
			self.ui.y_min_2.setText('')
			self.ui.x_max_2.setText('')
			self.ui.y_max_2.setText('')
			self.ui.rep_shpSave.setText('')
			
		else:
			QtGui.QMessageBox.information(self,'Message',"Veuillez selectionner le Repertoire pour le shapefile")
		
