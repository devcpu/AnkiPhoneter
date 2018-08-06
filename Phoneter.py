#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import logging
import os
import pickle
import shutil
import tempfile
import urllib2

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, askUser, getFile
from anki.hooks import addHook

import string,re
import os, tempfile
import time, random, socket, hashlib #guid

from aqt.qt import *
from aqt.utils import tooltip, askUser, getFile
from anki.hooks import addHook
from PyQt4 import QtGui, QtCore
# from puddlestuff.functions import false
import requests
from bs4 import BeautifulSoup


# Get log file
irFolder = os.path.join(mw.pm.addonFolder(), 'Phoneter')
logFile = os.path.join(irFolder, 'phoneter.log')

# if Phoneter's folder doesn't exist, create one
if not os.path.exists(irFolder):
    os.makedirs(irFolder)

# create the logFile
open(logFile, 'w').close()

# setup logger
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename = logFile, level = logging.DEBUG)
logger = logging.getLogger(__name__)


class PhoneterUI(QDialog):
    """
    Allows copying/replacing/swapping of fields to another field, in bulk.
    """
    oldtemplate = ""

    #Browser batch editing dialog
    def __init__(self, browser, nids):
        QDialog.__init__(self, parent=browser)
        self.browser = browser
        self.nids = nids
        self._setupUi()

    def _setupUi(self):
        #------------------------------------------------------
        fields = self._getFields()
        Phoneter = self
        #======================================================
        # Form Layout
        #======================================================
        Phoneter.setObjectName("Phoneter")
        Phoneter.resize(330, 195)
        Phoneter.setMinimumSize(QtCore.QSize(330, 195))
        Phoneter.setSizeGripEnabled(False)
        self.vMainLayout = QtGui.QVBoxLayout(Phoneter)
        self.vMainLayout.setObjectName("vMainLayout")
        #======================================================
        # Action/Source/Destination widget
        #======================================================
        self.widgetPrimaryCtrls = QtGui.QWidget(Phoneter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetPrimaryCtrls.sizePolicy().hasHeightForWidth())
        self.widgetPrimaryCtrls.setSizePolicy(sizePolicy)
        self.widgetPrimaryCtrls.setMaximumSize(QtCore.QSize(640, 16777215))
        self.widgetPrimaryCtrls.setObjectName("widgetPrimaryCtrls")
        self.vlWidgetSource = QtGui.QVBoxLayout(self.widgetPrimaryCtrls)
        self.vlWidgetSource.setContentsMargins(0, 0, 0, 0)
        self.vlWidgetSource.setObjectName("vlWidgetSource")
        #======================================================
        # Action Widget
        #======================================================
#         self.hlAction = QtGui.QHBoxLayout()
#         self.hlAction.setObjectName("hlAction")
#         self.lblAction = QtGui.QLabel(self.widgetPrimaryCtrls)
#         sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.lblAction.sizePolicy().hasHeightForWidth())
#         #Setup label
#         self.lblAction.setSizePolicy(sizePolicy)
#         self.lblAction.setMinimumSize(QtCore.QSize(100, 0))
#         self.lblAction.setMaximumSize(QtCore.QSize(150, 16777215))
#         self.lblAction.setBaseSize(QtCore.QSize(100, 0))
#         self.lblAction.setLayoutDirection(QtCore.Qt.LeftToRight)
#         self.lblAction.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
#         self.lblAction.setObjectName("lblAction")
#         self.hlAction.addWidget(self.lblAction)
#         #Setup combobox
#         self.cmbAction = QtGui.QComboBox(self.widgetPrimaryCtrls)
#         self.cmbAction.setEnabled(True)
#         sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Ignored)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.cmbAction.sizePolicy().hasHeightForWidth())
#         self.cmbAction.setSizePolicy(sizePolicy)
#         self.cmbAction.setMinimumSize(QtCore.QSize(150, 26))
#         self.cmbAction.setMaximumSize(QtCore.QSize(250, 16777215))
#         self.cmbAction.setBaseSize(QtCore.QSize(160, 0))
#         self.cmbAction.setObjectName("cmbAction")
#         self.cmbAction.addItem("") #0 Replace
#         self.cmbAction.addItem("") #1 After
#         self.cmbAction.addItem("") #2 Before
#         self.cmbAction.addItem("") #3 Move
#         self.cmbAction.addItem("") #4 Swap
#         self.cmbAction.addItem("") #5 Custom
#         self.hlAction.addWidget(self.cmbAction)
#         spacerItem = QtGui.QSpacerItem(175, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.hlAction.addItem(spacerItem)
#         self.vlWidgetSource.addLayout(self.hlAction)
        #======================================================
        # Source Widget
        #======================================================
        self.hlSource = QtGui.QHBoxLayout()
        self.hlSource.setObjectName("hlSource")
        self.lblSource = QtGui.QLabel(self.widgetPrimaryCtrls)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSource.sizePolicy().hasHeightForWidth())
        #Setup label
        self.lblSource.setSizePolicy(sizePolicy)
        self.lblSource.setMinimumSize(QtCore.QSize(100, 0))
        self.lblSource.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lblSource.setBaseSize(QtCore.QSize(100, 0))
        self.lblSource.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblSource.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSource.setObjectName("lblSource")
        self.hlSource.addWidget(self.lblSource)
        #Set up combobox
        self.cmbSource = QtGui.QComboBox(self.widgetPrimaryCtrls)
        self.cmbSource.setEnabled(True)
        sizePolicySD = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        sizePolicySD.setHorizontalStretch(0)
        sizePolicySD.setVerticalStretch(0)
        sizePolicySD.setHeightForWidth(self.cmbSource.sizePolicy().hasHeightForWidth())
        self.cmbSource.setSizePolicy(sizePolicySD)
        self.cmbSource.setMinimumSize(QtCore.QSize(200, 26))
        self.cmbSource.setMaximumSize(QtCore.QSize(250, 16777215))
        self.cmbSource.setBaseSize(QtCore.QSize(200, 26))
        self.cmbSource.setObjectName("cmbSource")
        #------------------------------------------------------
        self.cmbSource.addItems(fields)
        #------------------------------------------------------
        self.hlSource.addWidget(self.cmbSource)
        #Setup Insert button
        #self.btnInsert = QtGui.QPushButton(self.widgetPrimaryCtrls)
        #self.btnInsert.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.btnInsert.sizePolicy().hasHeightForWidth())
        #self.btnInsert.setSizePolicy(sizePolicy)
        #self.btnInsert.setMaximumSize(QtCore.QSize(50, 16777215)) #HELLO THERE (w, h)
        #self.btnInsert.setMinimumSize(QtCore.QSize(50, 0))
        #self.btnInsert.setFlat(False)
        #self.btnInsert.setObjectName("btnInsert")
        #self.hlSource.addWidget(self.btnInsert)

        spacerItem_cmbSource = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlSource.addItem(spacerItem_cmbSource)
        self.vlWidgetSource.addLayout(self.hlSource)
        #======================================================
        # Destination Widget
        #======================================================
        self.hlDestinaton = QtGui.QHBoxLayout()
        self.hlDestinaton.setObjectName("hlDestinaton")
        self.lblDestination = QtGui.QLabel(self.widgetPrimaryCtrls)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDestination.sizePolicy().hasHeightForWidth())
        #Setup label
        self.lblDestination.setSizePolicy(sizePolicy)
        self.lblDestination.setMinimumSize(QtCore.QSize(100, 0))
        self.lblDestination.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lblDestination.setBaseSize(QtCore.QSize(100, 0))
        self.lblDestination.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblDestination.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDestination.setObjectName("lblDestination")
        self.hlDestinaton.addWidget(self.lblDestination)
        # Set up combobox
        self.cmbDestination = QtGui.QComboBox(self.widgetPrimaryCtrls)
        self.cmbDestination.setSizePolicy(sizePolicySD)
        self.cmbDestination.setMinimumSize(QtCore.QSize(200, 0))
        self.cmbDestination.setMaximumSize(QtCore.QSize(250, 16777215))
        self.cmbDestination.setBaseSize(QtCore.QSize(200, 26))
        #self.cmbDestination.setBaseSize(QtCore.QSize(150, 26))
        self.cmbDestination.setObjectName("cmbDestination")
        #------------------------------------------------------
        self.cmbDestination.addItems(fields)
        #------------------------------------------------------
        self.hlDestinaton.addWidget(self.cmbDestination)
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum) #HELLO HERE
        self.hlDestinaton.addItem(spacerItem1)
        self.vlWidgetSource.addLayout(self.hlDestinaton)
        #------------------------------------------------------
        # END Action/Source/Destination widget:
        #------------------------------------------------------
        self.vMainLayout.addWidget(self.widgetPrimaryCtrls)
        #======================================================
        # 'Custom' Widget
        #======================================================
#         self.groupTemplate = QtGui.QGroupBox(Phoneter)
#         self.groupTemplate.setObjectName("groupTemplate")
#         self.vlGroupTemplate = QtGui.QVBoxLayout(self.groupTemplate)
#         self.vlGroupTemplate.setObjectName("vlGroupTemplate")
#         self.txtCustom = QtGui.QPlainTextEdit(self.groupTemplate)
#         self.txtCustom.setEnabled(True)
#         sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.txtCustom.sizePolicy().hasHeightForWidth())
#         self.txtCustom.setSizePolicy(sizePolicy)
#         self.txtCustom.setMinimumSize(QtCore.QSize(0, 45))
#         self.txtCustom.setSizeIncrement(QtCore.QSize(0, 0))
#         self.txtCustom.setBaseSize(QtCore.QSize(0, 50))
#         self.txtCustom.setFrameShape(QtGui.QFrame.StyledPanel)
#         self.txtCustom.setFrameShadow(QtGui.QFrame.Plain)
#         self.txtCustom.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
#         self.txtCustom.setPlainText("")
#         self.txtCustom.setObjectName("txtCustom")
#         self.vlGroupTemplate.addWidget(self.txtCustom)
#         self.vMainLayout.addWidget(self.groupTemplate)
        #======================================================
        # Main Buttons Widget
        #======================================================
        self.widgetMainButtons = QtGui.QWidget(Phoneter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetMainButtons.sizePolicy().hasHeightForWidth())
        self.widgetMainButtons.setSizePolicy(sizePolicy)
        self.widgetMainButtons.setMinimumSize(QtCore.QSize(250, 0))
        self.widgetMainButtons.setMaximumSize(QtCore.QSize(0, 60))
        self.widgetMainButtons.setObjectName("widgetMainButtons")
        self.vlWidgetMainButtons = QtGui.QVBoxLayout(self.widgetMainButtons)
        self.vlWidgetMainButtons.setContentsMargins(0, 0, 0, 0)
        self.vlWidgetMainButtons.setObjectName("vlWidgetMainButtons")
        self.hlMainButtons = QtGui.QHBoxLayout()
        self.hlMainButtons.setObjectName("hlMainButtons")

        # Cancel Button setup
        self.btnCancel = QtGui.QPushButton(self.widgetMainButtons)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCancel.sizePolicy().hasHeightForWidth())
        self.btnCancel.setSizePolicy(sizePolicy)
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 32))
        self.btnCancel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btnCancel.setObjectName("btnCancel")
        self.hlMainButtons.addWidget(self.btnCancel)

        # OK Button setup
        self.btnOK = QtGui.QPushButton(self.widgetMainButtons)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOK.sizePolicy().hasHeightForWidth())
        self.btnOK.setSizePolicy(sizePolicy)
        self.btnOK.setMinimumSize(QtCore.QSize(0, 32))
        self.btnOK.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btnOK.setObjectName("btnOK")
        self.hlMainButtons.addWidget(self.btnOK)

        # Add OK and Cancel Buttons to parent group/widget
        self.vlWidgetMainButtons.addLayout(self.hlMainButtons)
        self.vMainLayout.addWidget(self.widgetMainButtons)
        #------------------------------------------------------
        self.retranslateUi()
        #------------------------------------------------------
        QtCore.QMetaObject.connectSlotsByName(Phoneter)
        #======================================================
        # Setup/Process form
        #======================================================
#        self.cmbAction.currentIndexChanged.connect(self.onActionIndexChange)
        self.cmbSource.currentIndexChanged.connect(self.onSourceIndexChange)
        self.cmbDestination.currentIndexChanged.connect(self.onDestinationIndexChange)
#        self.btnInsert.clicked.connect(self.onInsert)
        #------------------------------------------------------
#        self.onCustom()
        #self.processTemplate("<br>")
        #------------------------------------------------------
        if self.cmbDestination.count() > 1:
            self.cmbDestination.setCurrentIndex(1)
        #------------------------------------------------------
        #btnOK.clicked.connect(lambda state, x="saysomething": self.onConfirm)
        #btnOK.clicked.connect(lambda state, x="replace": self.onConfirm)
        self.btnOK.clicked.connect(self.onConfirm)
        self.btnCancel.clicked.connect(self.close)
        #------------------------------------------------------

    def _getFields(self):
        nid = self.nids[0]
        mw = self.browser.mw
        model = mw.col.getNote(nid).model()
        fields = mw.col.models.fieldNames(model)
        return fields

    def retranslateUi(self):
        Phoneter = self
        Phoneter.setWindowTitle(QtGui.QApplication.translate("Phoneter", "Phoneter", None, QtGui.QApplication.UnicodeUTF8))
#        self.lblAction.setText(QtGui.QApplication.translate("Phoneter", "Action:", None, QtGui.QApplication.UnicodeUTF8))
#        self.cmbAction.setItemText(0, QtGui.QApplication.translate("Phoneter", "Replace", None, QtGui.QApplication.UnicodeUTF8))
#        self.cmbAction.setItemText(1, QtGui.QApplication.translate("Phoneter", "Copy After", None, QtGui.QApplication.UnicodeUTF8))
#        self.cmbAction.setItemText(2, QtGui.QApplication.translate("Phoneter", "Copy Before", None, QtGui.QApplication.UnicodeUTF8))
#        self.cmbAction.setItemText(3, QtGui.QApplication.translate("Phoneter", "Move", None, QtGui.QApplication.UnicodeUTF8))
#        self.cmbAction.setItemText(4, QtGui.QApplication.translate("Phoneter", "Swap", None, QtGui.QApplication.UnicodeUTF8))
#        self.cmbAction.setItemText(5, QtGui.QApplication.translate("Phoneter", "Custom", None, QtGui.QApplication.UnicodeUTF8))
#        self.btnInsert.setText(QtGui.QApplication.translate("Phoneter", ">>", None, QtGui.QApplication.UnicodeUTF8))
#        self.groupTemplate.setTitle(QtGui.QApplication.translate("Phoneter", "Template:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("Phoneter", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("Phoneter", "OK", None, QtGui.QApplication.UnicodeUTF8))

#        idx = self.cmbAction.currentIndex()
#
#         if idx == 0:   # If Replace
#             self.lblSource.setText(QtGui.QApplication.translate("Phoneter", "Source Field:", None, QtGui.QApplication.UnicodeUTF8))
#             self.lblDestination.setText(QtGui.QApplication.translate("Phoneter", "Replace:", None, QtGui.QApplication.UnicodeUTF8))
#         elif idx == 1: # Copy After
#             self.lblSource.setText(QtGui.QApplication.translate("Phoneter", "Copy Field:", None, QtGui.QApplication.UnicodeUTF8))
#             self.lblDestination.setText(QtGui.QApplication.translate("Phoneter", "After:", None, QtGui.QApplication.UnicodeUTF8))
#         elif idx == 2: # Copy Before
#             self.lblSource.setText(QtGui.QApplication.translate("Phoneter", "Copy Field:", None, QtGui.QApplication.UnicodeUTF8))
#             self.lblDestination.setText(QtGui.QApplication.translate("Phoneter", "Before:", None, QtGui.QApplication.UnicodeUTF8))
#         elif idx == 3: # Move
#             self.lblSource.setText(QtGui.QApplication.translate("Phoneter", "Move Field:", None, QtGui.QApplication.UnicodeUTF8))
#             self.lblDestination.setText(QtGui.QApplication.translate("Phoneter", "To:", None, QtGui.QApplication.UnicodeUTF8))
#         elif idx == 4: # Swap
#             self.lblSource.setText(QtGui.QApplication.translate("Phoneter", "Swap Field:", None, QtGui.QApplication.UnicodeUTF8))
#             self.lblDestination.setText(QtGui.QApplication.translate("Phoneter", "With:", None, QtGui.QApplication.UnicodeUTF8))
#         elif idx == 5: # Custom
#             self.lblSource.setText(QtGui.QApplication.translate("Phoneter", "Insert:", None, QtGui.QApplication.UnicodeUTF8))
#             self.lblDestination.setText(QtGui.QApplication.translate("Phoneter", "Destination:", None, QtGui.QApplication.UnicodeUTF8))
        #------------------------------------------------------


    def onSourceIndexChange(self,idx):
        pass

    def onDestinationIndexChange(self,idx):
        pass

#     def onActionIndexChange(self,idx):
#         
#     def processTemplate(self,spacer):
#         idx = self.cmbAction.currentIndex()
#         fldSource =  self.cmbSource.currentText()
#         fld2 = self.cmbDestination.currentText() #itemText(idx), currentText, currentIndex
#         if idx != 5:
#             #current_template = self.txtCustom.toPlainText()
#         new_template = self.getTemplate(fldSource, fld2, spacer)
#         self.txtCustom.setPlainText( new_template )
#             
#     def getTemplate(self,fldSource, fld2, spacer):
#           if idx == 1: #Copy After
#               return "{{" + fld2 + "}}" + spacer + "{{" + fldSource + "}}"
#           elif idx == 2: #Copy Before
#               return "{{" + fldSource + "}}" + spacer + "{{" + fld2 + "}}"
#           else: #Default is Replace (0), Move (3), Swap (4), Custom (5)
#               return "{{" + fldSource + "}}"
            
            

    def onInsert(self):
        cursor = self.txtCustom.textCursor()
        cursor.insertText("{{" + self.cmbSource.currentText() +  "}}")

    def onConfirm(self):
        browser = self.browser
        nids = self.nids
#        idx = self.cmbAction.currentIndex()
        fld1 = self.cmbSource.currentText()
        fld2 = self.cmbDestination.currentText()

#         if idx == 0:   # If Replace
#             q = (u"The contents of the field '{1}' will be replaced. The field '{0}' will replace it in {2} selected note(s).<br><br>Is this okay?").format(fld1, fld2, len(nids))
#         elif idx == 1: # Copy After
#             q = (u"The contents of the field '{1}' will change. The field '{0}' will be appended to it in {2} selected note(s).<br><br>Is this okay?").format(fld1, fld2, len(nids))
#         elif idx == 2: # Copy Before
#             q = (u"The contents of the field '{1}' will change. The field '{0}' will be prepended to it in {2} selected note(s).<br><br>Is this okay?").format(fld1, fld2, len(nids))
#         elif idx == 3: # Move
#             q = (u"The contents of the field '{0}' will move to field '{1}'. This will replace out field '{1}' but also empty out field '{0}' in {2} selected note(s).<br><br>Is this okay?").format(fld1, fld2, len(nids))
#         elif idx == 4: # Swap
#             if fld1 == fld2:
#                 QMessageBox.warning(self, "Swap Error", (u"You must select two different fields in order to swap them. You selected '{0}' in both boxes.").format(fld1))
#                 return
#             q = (u"The contents of the fields '{0}' and '{1}' will be swapped. The contents of '{0}' will become '{1}' and '{1}' will become '{0}', in {2} selected note(s).<br><br>Is this okay?").format(fld1, fld2, len(nids))
#         elif idx == 5: # Custom
#             q = (u"The contents of the field '{1}' will be replaced with the processed contents of the custom template in {2} selected note(s).<br><br>Is this okay?").format(fld1, fld2, len(nids))
        #if idx between 0 and 4
#         if 0 <= idx <= 5:
#             if not askUser(q, parent=self):
#                 return
# 
#         template = self.txtCustom.toPlainText()
        flds = self._getFields()
        process(browser, nids, flds, fld1, fld2)
        self.close()

def process(browser, nids, flds, fld1, fld2):
    mw = browser.mw
    mw.checkpoint("Phoneter")
    mw.progress.start()
    browser.model.beginReset()
    cnt = 0
    
    #pattern = re.compile('^[(.+)(,\sAm\s.+])')
    
    for nid in nids:
        note = mw.col.getNote(nid)
        #if 0 not in (self.a, self.b) :
        if (fld1 in note) and (fld2 in note):
            logger.debug(fld1)
            reqwordlst = note[fld1].split()
            logger.debug(reqwordlst)
            phon = ''
            for w in reqwordlst:
                logger.debug(w)
                w.replace(',', '')
                logger.debug(w)
                if (w == 'to'):
                    continue
                p = getPhonetic(w)
                logger.debug(p)
                px = re.sub(r'^\[(.+)(,\sAm\s.+\])', r'[\1]', p)
                logger.debug(px)
                phon += px + ', '
                
            x = len(phon)
            note[fld2] = phon[0:x-2]
            cnt += 1
            note.flush()

    browser.model.endReset()
    mw.requireReset()
    mw.progress.finish()
    mw.reset()
    #self.cleanup()
    tooltip("Processed {0} notes.".format(cnt), parent=browser)
    

def getPhonetic(requested_word):
    page = requests.get("https://en.pons.com/translate?q=" + requested_word + "&l=deen&in=en&lf=de")
    soup = BeautifulSoup(page.content, 'html.parser')
    phonetics = soup.find_all('span', class_='phonetics')
    
    if len(phonetics) > 0:
        return phonetics[0].get_text()
    else:
        return "[]"


def onAdvPhoneter(browser):
    nids = browser.selectedNotes()
    if not nids:
        tooltip("No cards selected.")
        return
    
    dialog = PhoneterUI(browser, nids)
    dialog.exec_()
    
    
def setupMenu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Phoneter')
#    a.setShortcut(QKeySequence("Ctrl+Alt+C"))
    browser.connect(a, SIGNAL("triggered()"), lambda b=browser: onAdvPhoneter(b))

addHook("browser.setupMenus", setupMenu)
