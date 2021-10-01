# -*- coding: utf-8 -*-

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QProgressBar
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
#import resources
import sys
import os
import os.path
import urllib2
import ConfigParser
import platform

try:
    import resources
except ImportError:
    import resources_rc

# Import the code for the dialog
from gpx_shp_dialog import gpx_shpDialog

class gpx_shp:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
		# pour metadata
		config = ConfigParser.ConfigParser()
		config.read(os.path.join(os.path.dirname(__file__),'metadata.txt'))
		name = config.get('general', 'name')
		description = config.get('general', 'description')
		version = str(config.get('general', 'version'))
		next_version = str(config.get('general', 'next_version'))

		# Save reference to the QGIS interface
		self.iface = iface
		# initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		# initialize locale
		locale = QSettings().value('locale/userLocale')[0:2]
		locale_path = os.path.join(self.plugin_dir, 'i18n', 'gpx_shp_{}.qm'.format(locale))
		if os.path.exists(locale_path):
			self.translator = QTranslator()
			self.translator.load(locale_path)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)

		# Create the dialog (after translation) and keep reference
		self.dlg = gpx_shpDialog()

		# Declare instance attributes
		self.actions = []
		self.menu = self.tr(u'&gpx_shp')
		# TODO: We are going to let the user set this up in a future iteration
		self.toolbar = self.iface.addToolBar(u'gpx_shp')
		self.toolbar.setObjectName(u'gpx_shp')
		
		try:
			version_next = 'http://172.16.0.230/ipm_sig/qgis_plugins/version_dos/gpx_shp_v'+ next_version +'.png'
			ret = urllib2.urlopen(version_next)
			if ret.code == 200:
				#print "Exists!"
				#Satuts Bar
				#iface.mainWindow().statusBar().showMessage( u"Misy Io fichier Io" )
				#Message Bar
				iface.messageBar().pushInfo( u'gpx_shp', u' La version : ' +  next_version + ' est disponible')
		except:
			#print "tsymis io!"
			#Satuts Bar
			#iface.mainWindow().statusBar().showMessage( u"Tsy misy io fichier io" )
			#Message Bar
			#iface.messageBar().pushInfo( u'gpx_shp', u' La prochaine version : ' +  next_version + ' sera disponible')
			pass
	
    
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('gpx_shp', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            #self.iface.addPluginToVectorMenu
			self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/gpx_shp/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GPX to SHAPEFILE'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
			#self.iface.removePluginVectorMenu
            self.iface.removePluginMenu(
                self.tr(u'&gpx_shp'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
