#################################################################################################
# File name: Drawing IB Topo from ibnetdiscovery_v1.0
# Description: it helps to create IB topology. In details, my script converts ibnetdiscovery file to ".gv" file, and MS Visio imports ".gv" file and draws IB Topology.
# Author: Brian, HyungKwang Choi
# Software: Python 3.8+, PYQT v5
# Revision:
# v0  :    -       Initial Draft by from Brian
# v1  : 6/10/2023  created GUI version and added several useful features ex) drawing End hosts, detecting Invalid LID, and mis-cabling and so on.
#################################################################################################


######################### Debugging statement for quick reference ##############
###### export Dictionary 
"""gvname = fPath + fnameBase + "_ibnet.txt"
     # open file for writing, "w" is writing
    w = csv.writer(open(gvname, "w"))

    # loop over dictionary keys and values
    for key, val in ibNet.items():
        w.writerow([key, val])"""
        
##### exporting List 

"""with open("boxRankLists", 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(boxRankLists)"""

########################Conversion QT GUI to python##############################
#C:\Python39\Scripts>pyuic5.exe -x "C:\E\기술\Creating Document\Tarzan\Tarzan coding\sub_window.ui" -o "C:\E\기술\Creating Document\Tarzan\Tarzan coding\sub_window.py"


import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
           
        
class SubWindow(QtWidgets.QWidget):
        
    def __init__(self):

        super(SubWindow, self).__init__()
         
        self.all_values = {0:"unchecked", 1:"8", 2:"0", 3:"", 4:"1" ,5:"1" ,6:"1" , 7:"circle", 8:"0.04" ,9:"0.08" ,10:"0", 11:"solid", 12:"black", 13:"green", 14:"rectangle", 15:"0.04" ,16:"0.08" ,17:"0" , 18:"solid", 19:"black", 20:"white" ,21:"rectangle", 22:"0.04" ,23:"0.08" ,24:"0" ,25:"solid", 26:"black", 27:"white" ,28:"rectangle", 29:"0.04" ,30:"0.08" ,31:"0",   32:"solid", 33:"black", 34:"white", 35:"green", 36:"blue", 37:"black", 38:"Calibri" , 39:"1" , 40:"solid" }
     
        #0: Radio Button of "By default" 
        #1 : Node Rank Space    : lineEdit_10
        #2 :  Node space        : lineEdit_11
        #3 : Caption
        #4 : Host <--> L1 Switch Line width
        #5 : L1 Switch <--> L2 Switch Line width
        #6 : L3 Switch <--> L3 Switch Line width   
        #7 : Host Shape
        #8 : Host  font size
        #9 : Host  width
        #10 : Host  Heigh     
        #11 : Host Style
        #12 : Host font color
        #13 : Host Fill Color
        #14 : Switch1 Shape
        #15 : L1 switch font size
        #16:  L1 switch width
        #17 : L1 switch Heigh     
        #18:  Switch1 Style
        #19 : Switch1 Font Color
        #20 : Switch1 Fill Color
        #21 : Switch2 Shape
        #22 : L2 switch font size
        #23 : L2 switch width
        #24:  L2 switch Heigh    
        #25 : Switch2 Style
        #26 : Switch2 Font Color
        #27 : Switch2 Fill Color
        #28 : Switch3 Shape
        #29 : L3 switch Font size
        #30 : L3 switch width
        #31 : L3 switch Heigh     
        #32 : Switch3 Style     
        #33 : Switch3 Font color
        #34:  Switch3 Fill Color
        #35 : Line Codr between Host <-> SW1
        #36 : Line Codr   SW1 <-> SW2
        #37 : Line Codr   SW2 <-> SW3
        #38 : Node "Font Name" (comboBox_57)   
        #39 : # Caption Font Size (lineEdit_13)
        #40 : # Caption style (comboBox_58)      

    def setupUi(self, dd):
    
        dd.setObjectName("dd")
        dd.resize(917, 667)
        self.centralwidget = QtWidgets.QWidget(dd)
        self.centralwidget.setObjectName("centralwidget")

        self.temp =  dd
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)          
            
        
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(30, 20, 861, 621))
        self.groupBox_6.setStyleSheet("background-color: rgb(239, 239, 239);")
        self.groupBox_6.setObjectName("groupBox_6")                
        
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_7.setGeometry(QtCore.QRect(50, 100, 781, 450))
        self.groupBox_7.setStyleSheet("background-color: rgb(239, 239, 239);")
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_7.setEnabled(False)
        
        self.groupBox.setGeometry(QtCore.QRect(17, 10, 331, 91))
        self.groupBox.raise_() 
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Global option")
   
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 120, 731, 320))
        self.groupBox_5.setObjectName("groupBox_5")
        self.groupBox_5.setTitle("Drawing options")        
        self.groupBox_5.raise_()
               
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_2.setGeometry(QtCore.QRect(207, 92, 101, 221))
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")   
        self.groupBox_2.setTitle("L1 switch")        
        self.groupBox_2.raise_()      
              
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_3.setGeometry(QtCore.QRect(417, 92, 101, 221))
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setTitle("L2 switch")
        self.groupBox_3.raise_()      
                
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_4.setGeometry(QtCore.QRect(617, 92, 101, 221))
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setTitle("L3 switch")      
        self.groupBox_4.raise_()         

        self.label_31 = QtWidgets.QLabel(self.groupBox)
        self.label_31.setGeometry(QtCore.QRect(10, 20, 91, 20))
        self.label_31.setObjectName("label_31")
        self.label_31.setText("Node Rank Space")
        self.label_31.raise_() 
        
        self.label_28 = QtWidgets.QLabel(self.groupBox)
        self.label_28.setGeometry(QtCore.QRect(10, 39, 61, 20))
        self.label_28.setObjectName("label_28")
        self.label_28.setText("Node space")
        self.label_28.raise_()

        self.label_29 = QtWidgets.QLabel(self.groupBox)
        self.label_29.setGeometry(QtCore.QRect(170, 66, 131, 21))
        self.label_29.setObjectName("label_29")
        self.label_29.setText("Caption Font Size")          
        self.label_29.raise_()
                   
        self.lineEdit_11 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_11.setGeometry(QtCore.QRect(100, 42, 31, 16))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_11.setText("0")                
        self.lineEdit_11.raise_()   
        
        self.lineEdit_10 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_10.setGeometry(QtCore.QRect(100, 20, 31, 16))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_10.setText("8")
        self.lineEdit_10.raise_()
        
        self.lineEdit_13 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_13.setGeometry(QtCore.QRect(265, 69, 31, 16))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.lineEdit_13.setText("1")    
 
        
        self.lineEdit_12 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_12.setText("Caption (Null)")              
        self.lineEdit_12.setGeometry(QtCore.QRect(170, 17, 115, 20))
        self.lineEdit_12.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_12.raise_()
                                  
        self.comboBox_57 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_57.setGeometry(QtCore.QRect(10, 63, 110, 20))
        self.comboBox_57.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_57.setEditable(False)
        self.comboBox_57.setObjectName("comboBox_57")
        self.comboBox_57.raise_()
        
        self.comboBox_58 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_58.setGeometry(QtCore.QRect(170, 43, 115, 20))
        self.comboBox_58.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_58.setEditable(False)
        self.comboBox_58.setObjectName("comboBox_58")


        self.label_37 = QtWidgets.QLabel(self.groupBox_5)
        self.label_37.setGeometry(QtCore.QRect(518, 17, 61, 20))
        self.label_37.setObjectName("label_37")
        self.label_37.setText("Line Width")
        self.label_37.raise_()

        self.lineEdit1_4 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit1_4.setGeometry(QtCore.QRect(12, 51, 101, 31))
        self.lineEdit1_4.setFont(font)
        self.lineEdit1_4.setObjectName("lineEdit1_4")
        self.lineEdit1_4.setText("            Host")
        self.lineEdit1_4.raise_()
        
        self.lineEdit1_3 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit1_3.setGeometry(QtCore.QRect(207, 51, 101, 31))
        self.lineEdit1_3.setFont(font)
        self.lineEdit1_3.setObjectName("lineEdit1_3")               
        self.lineEdit1_3.setText("        L1 switch")
        self.lineEdit1_3.raise_()
                     
        self.lineEdit1_2 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit1_2.setGeometry(QtCore.QRect(417, 53, 101, 31))
        self.lineEdit1_2.setFont(font)
        self.lineEdit1_2.setObjectName("lineEdit1_2")
        self.lineEdit1_2.setText("        L2 switch")
        self.lineEdit1_2.raise_()   
        
        self.lineEdit1 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit1.setGeometry(QtCore.QRect(617, 51, 101, 31))
        self.lineEdit1.setFont(font)
        self.lineEdit1.setObjectName("lineEdit1")
        self.lineEdit1.setText("        L3 switch")
        self.lineEdit1.raise_()
                        
        self.comboBox_40 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_40.setGeometry(QtCore.QRect(523, 42, 81, 21))
        self.comboBox_40.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_40.setEditable(False)
        self.comboBox_40.setObjectName("comboBox_40")
        self.comboBox_40.raise_()  
        
        self.lineEdit_60 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_60.setGeometry(QtCore.QRect(59, 50, 31, 16))
        self.lineEdit_60.setObjectName("lineEdit_60")
        self.lineEdit_60.setText("0.04")         
        self.lineEdit_60.raise_()        
                
        self.comboBox_53 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_53.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.comboBox_53.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_53.setEditable(False)
        self.comboBox_53.setObjectName("comboBox_53")
        self.comboBox_53.raise_()

        self.comboBox_54 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_54.setGeometry(QtCore.QRect(10, 110, 81, 21))
        self.comboBox_54.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_54.setEditable(False)
        self.comboBox_54.setObjectName("comboBox_54")
        self.comboBox_54.raise_()
        
        self.comboBox_55 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_55.setGeometry(QtCore.QRect(10, 136, 81, 21))
        self.comboBox_55.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_55.setEditable(False)
        self.comboBox_55.setObjectName("comboBox_55")
        self.comboBox_55.raise_()
        
        self.comboBox_56 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_56.setGeometry(QtCore.QRect(10, 160, 81, 21))
        self.comboBox_56.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_56.setEditable(False)
        self.comboBox_56.setObjectName("comboBox_56")
        self.comboBox_56.raise_()
               
        self.label_36 = QtWidgets.QLabel(self.groupBox_5)
        self.label_36.setGeometry(QtCore.QRect(114, 19, 61, 20))
        self.label_36.setObjectName("label_36")
        self.label_36.setText("Line Width")     
        self.label_36.raise_()              
       
        self.label_38 = QtWidgets.QLabel(self.groupBox_5)
        self.label_38.setGeometry(QtCore.QRect(318, 18, 61, 20))
        self.label_38.setObjectName("label_38")
        self.label_38.setText("Line Width")
        self.label_38.raise_()
                
        self.comboBox_38 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_38.setGeometry(QtCore.QRect(118, 42, 81, 21))
        self.comboBox_38.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_38.setEditable(False)
        self.comboBox_38.setObjectName("comboBox_38")
        self.comboBox_38.raise_() 

        self.comboBox_39 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_39.setGeometry(QtCore.QRect(319, 42, 81, 21))
        self.comboBox_39.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_39.setEditable(False)
        self.comboBox_39.setObjectName("comboBox_39")
        self.comboBox_39.raise_() 

        self.lineEdit_22 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_22.setGeometry(QtCore.QRect(170, 21, 27, 16))
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.lineEdit_22.setText("1")        
        self.lineEdit_22.raise_()
                                   
        self.lineEdit_20 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_20.setGeometry(QtCore.QRect(574, 19, 27, 16))
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.lineEdit_20.setText("1")
        self.lineEdit_20.raise_()
        
        self.lineEdit_21 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_21.setGeometry(QtCore.QRect(374, 19, 27, 16))
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.lineEdit_21.setText("1")      
        self.lineEdit_21.raise_()
                
        self.groupBox_1 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_1.setGeometry(QtCore.QRect(12, 89, 101, 221))
        self.groupBox_1.setTitle("Host")
        self.groupBox_1.raise_()      
        self.groupBox_1.setFont(font)
        self.groupBox_1.setObjectName("groupBox_1")
        
        self.label_10 = QtWidgets.QLabel(self.groupBox_1)
        self.label_10.setGeometry(QtCore.QRect(10, 50, 51, 16))
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_10.setText("font size")
        self.label_10.raise_()
                
        self.lineEdit_30 = QtWidgets.QLineEdit(self.groupBox_1)
        self.lineEdit_30.setGeometry(QtCore.QRect(59, 51, 31, 16))
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.lineEdit_30.setText("0.04")        
        self.lineEdit_30.raise_()      
        
        self.comboBox_41 = QtWidgets.QComboBox(self.groupBox_1)
        self.comboBox_41.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.comboBox_41.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_41.setEditable(False)
        self.comboBox_41.setObjectName("comboBox_41")
        self.comboBox_41.raise_()   

        self.comboBox_42 = QtWidgets.QComboBox(self.groupBox_1)
        self.comboBox_42.setGeometry(QtCore.QRect(10, 110, 81, 21))
        self.comboBox_42.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_42.setEditable(False)
        self.comboBox_42.setObjectName("comboBox_42")
        self.comboBox_42.raise_()   
        
        self.comboBox_43 = QtWidgets.QComboBox(self.groupBox_1)
        self.comboBox_43.setGeometry(QtCore.QRect(10, 136, 81, 21))
        self.comboBox_43.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_43.setEditable(False)
        self.comboBox_43.setObjectName("comboBox_43")
        self.comboBox_43.raise_()   
        
        self.comboBox_44 = QtWidgets.QComboBox(self.groupBox_1)
        self.comboBox_44.setGeometry(QtCore.QRect(10, 162, 81, 21))
        self.comboBox_44.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_44.setEditable(False)
        self.comboBox_44.setObjectName("comboBox_44")
        self.comboBox_44.raise_()
           
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(10, 49, 51, 16))
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_14.setText("font size")        
        self.label_14.raise_()
                
        self.lineEdit_50 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_50.setGeometry(QtCore.QRect(59, 51, 31, 16))
        self.lineEdit_50.setObjectName("lineEdit_50")
        self.lineEdit_50.setText("0.04")        
        self.lineEdit_50.raise_()
  
        self.comboBox_49 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_49.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.comboBox_49.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_49.setEditable(False)
        self.comboBox_49.setObjectName("comboBox_49")
        self.comboBox_49.raise_()   
        
        self.comboBox_50 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_50.setGeometry(QtCore.QRect(10, 109, 81, 21))
        self.comboBox_50.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_50.setEditable(False)
        self.comboBox_50.setObjectName("comboBox_50")
        self.comboBox_50.raise_()   

        self.comboBox_51 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_51.setGeometry(QtCore.QRect(10, 135, 81, 21))
        self.comboBox_51.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_51.setEditable(False)
        self.comboBox_51.setObjectName("comboBox_51")
        self.comboBox_51.raise_()   
        
        self.comboBox_52 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_52.setGeometry(QtCore.QRect(10, 160, 81, 21))
        self.comboBox_52.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_52.setEditable(False)
        self.comboBox_52.setObjectName("comboBox_52")
        self.comboBox_52.raise_()   
        
        self.label_33 = QtWidgets.QLabel(self.groupBox_5)
        self.label_33.setGeometry(QtCore.QRect(114, 62, 92, 10))
        self.label_33.setObjectName("label_33")
        self.label_33.setText("--------------------------")
        
        self.label_34 = QtWidgets.QLabel(self.groupBox_5)
        self.label_34.setGeometry(QtCore.QRect(308, 62, 108, 10))
        self.label_34.setObjectName("label_34")
        self.label_34.setText("-----------------------------")
          
        self.label_35 = QtWidgets.QLabel(self.groupBox_5)
        self.label_35.setGeometry(QtCore.QRect(518, 62, 98, 10))
        self.label_35.setObjectName("label_35")
        self.label_35.setText("--------------------------")
                     
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(10, 49, 51, 16))
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_12.raise_()
        self.label_12.setText("font size")            
        
        self.lineEdit_40 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_40.setGeometry(QtCore.QRect(59, 51, 31, 16))
        self.lineEdit_40.setObjectName("lineEdit_40")
        self.lineEdit_40.raise_()
        self.lineEdit_40.setText("0.04")     
                        
        self.comboBox_45 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_45.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.comboBox_45.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_45.setEditable(False)
        self.comboBox_45.setObjectName("comboBox_45")
        self.comboBox_45.raise_()   
        
        self.comboBox_46 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_46.setGeometry(QtCore.QRect(10, 108, 81, 21))
        self.comboBox_46.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_46.setEditable(False)
        self.comboBox_46.setObjectName("comboBox_46")
        self.comboBox_46.raise_()   
                
        self.comboBox_47 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_47.setGeometry(QtCore.QRect(10, 134, 81, 21))
        self.comboBox_47.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_47.setEditable(False)
        self.comboBox_47.setObjectName("comboBox_47")
        self.comboBox_47.raise_()   
        
        self.comboBox_48 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_48.setGeometry(QtCore.QRect(10, 160, 81, 21))
        self.comboBox_48.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_48.setEditable(False)
        self.comboBox_48.setObjectName("comboBox_48")
        self.comboBox_48.raise_()   
           
        dd.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(dd)
        self.statusbar.setObjectName("statusbar")
        dd.setStatusBar(self.statusbar)
        dd.setWindowTitle("Drawing options for End hosts & Switches")
        
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_2.setGeometry(QtCore.QRect(40, 70, 91, 17))
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setObjectName("radioButton_3")
        self.radioButton_2.setText("Customerized")
                
        self.radioButton_1 = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_1.setGeometry(QtCore.QRect(40, 30, 91, 17))
        self.radioButton_1.setChecked(True)
        self.radioButton_1.setObjectName("radioButton_4")
        self.radioButton_1.setText("By Default")    
        
        self.label_18 = QtWidgets.QLabel(self.groupBox_1)
        self.label_18.setGeometry(QtCore.QRect(10, 69, 51, 16))
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_18.setText("Width")  
        self.label_18.raise_()

        self.label_19 = QtWidgets.QLabel(self.groupBox_1)
        self.label_19.setGeometry(QtCore.QRect(10, 90, 51, 16))
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_19.setText("Height")    
        self.label_19.raise_()

        self.label_24 = QtWidgets.QLabel(self.groupBox_4)
        self.label_24.setGeometry(QtCore.QRect(10, 69, 51, 16))
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.label_24.setText("Width")
        self.label_24.raise_()
                        
        self.label_25 = QtWidgets.QLabel(self.groupBox_4)
        self.label_25.setGeometry(QtCore.QRect(10, 90, 51, 16))
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.label_25.setText("Height")
        self.label_25.raise_()
               
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(10, 49, 48, 16))
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_16.setText("font size")        
        self.label_16.raise_()
        
        self.label_22 = QtWidgets.QLabel(self.groupBox_3)
        self.label_22.setGeometry(QtCore.QRect(10, 69, 51, 16))
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_22.setText("Width")
        self.label_22.raise_()
                        
        self.label_23 = QtWidgets.QLabel(self.groupBox_3)
        self.label_23.setGeometry(QtCore.QRect(10, 90, 51, 16))
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_23.setText("Height")
        self.label_23.raise_()
        
        self.label_20 = QtWidgets.QLabel(self.groupBox_2)
        self.label_20.setGeometry(QtCore.QRect(11, 68, 51, 16))
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_20.setText("Width")
        self.label_20.raise_()
                        
        self.label_21 = QtWidgets.QLabel(self.groupBox_2)
        self.label_21.setGeometry(QtCore.QRect(11, 89, 51, 16))
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_21.setText("Height")
        self.label_21.raise_()

        self.lineEdit_61 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_61.setGeometry(QtCore.QRect(59, 70, 31, 16))
        self.lineEdit_61.setObjectName("lineEdit_61")
        self.lineEdit_61.setText("0.08")        
        self.lineEdit_61.raise_()
        
        self.lineEdit_62 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_62.setGeometry(QtCore.QRect(59, 91, 31, 16))
        self.lineEdit_62.setObjectName("lineEdit_62")
        self.lineEdit_62.setText("0")
        self.lineEdit_62.raise_()
                        
        self.lineEdit_31 = QtWidgets.QLineEdit(self.groupBox_1)
        self.lineEdit_31.setGeometry(QtCore.QRect(59, 70, 31, 16))
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.lineEdit_31.setText("0.08")
        self.lineEdit_31.raise_()               
        
        self.lineEdit_32 = QtWidgets.QLineEdit(self.groupBox_1)
        self.lineEdit_32.setGeometry(QtCore.QRect(59, 91, 31, 16))
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.lineEdit_32.setText("0")   

        self.lineEdit_32.raise_()
        self.lineEdit_52 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_52.setGeometry(QtCore.QRect(59, 91, 31, 16))
        self.lineEdit_52.setObjectName("lineEdit_52")
        self.lineEdit_52.setText("0")
        self.lineEdit_52.raise_()
                        
        self.lineEdit_51 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_51.setGeometry(QtCore.QRect(59, 70, 31, 16))
        self.lineEdit_51.setObjectName("lineEdit_51")
        self.lineEdit_51.setText("0.08")        
        self.lineEdit_51.raise_()

        self.lineEdit_41 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_41.setGeometry(QtCore.QRect(58, 69, 31, 16))
        self.lineEdit_41.setObjectName("lineEdit_41")
        self.lineEdit_41.setText("0.08")
        self.lineEdit_41.raise_()
                        
        self.lineEdit_42 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_42.setGeometry(QtCore.QRect(57, 90, 31, 16))
        self.lineEdit_42.setObjectName("lineEdit_42")
        self.lineEdit_42.setText("0")
        self.lineEdit_42.raise_()

        font = QtGui.QFont()
        font.setPointSize(15)
 
        self.pushButton2_1 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton2_1.setText("Click to SAVE") 
        self.pushButton2_1.setGeometry(QtCore.QRect(50, 570, 781, 41))
        self.pushButton2_1.setObjectName("pushButton2_1")
        self.pushButton2_1.setFont(font)        
        self.pushButton2_1.raise_()
        self.pushButton2_1.setStyleSheet("background-color: rgba(98, 211, 162, 255)")

        self.radioButton_2.raise_()
        self.radioButton_1.raise_()
        self.groupBox_7.raise_()
        
        QtCore.QMetaObject.connectSlotsByName(dd)

        self.shape_dict = {0: 'Shape', 1: "rectangle", 2: 'box', 3: 'circle', 4:'point', 5:'triangle', 6: 'diamond', 7: 'star'}
        
        for k, v in self.shape_dict.items() :  
            self.comboBox_41.addItem(v)
            self.comboBox_45.addItem(v)
            self.comboBox_49.addItem(v)
            self.comboBox_53.addItem(v)
   
        self.device_style_dict = {0: 'Device style', 1: 'solid', 2: 'dashed', 3:'dotted', 4:'invisible', 5: 'bold', 6: 'filled', 7:'striped', 8:'wedged'}
           
        for k, v in self.device_style_dict.items() : 
            self.comboBox_42.addItem(v)
            self.comboBox_46.addItem(v)
            self.comboBox_50.addItem(v)
            self.comboBox_54.addItem(v)
        
        self.font_color_dict = {0: 'Font Color', 1: 'black', 2: 'orange', 3:'green', 4:'blue', 5: 'purple', 6: 'yellow', 7: 'indigo', 8: 'pink', 9: 'gray', 10: 'cyan'}

        for k, v in self.font_color_dict.items() :
            self.comboBox_43.addItem(v)
            self.comboBox_47.addItem(v)
            self.comboBox_51.addItem(v)
            self.comboBox_55.addItem(v)
            
        self.fill_color_dict = {0: 'Fill Color', 1: 'none', 2: 'black', 3: 'orange', 4:'green', 5:'blue', 6: 'purple', 7: 'yellow', 8: 'indigo', 9: 'pink', 10: 'gray', 11: 'cyan'}
         
        for k, v in self.fill_color_dict.items() :
            self.comboBox_44.addItem(v)
            self.comboBox_48.addItem(v)
            self.comboBox_52.addItem(v)
            self.comboBox_56.addItem(v)
                
        self.line_color_dict = {0: 'Line Color', 1: 'black', 2: 'orange', 3:'green', 4:'blue', 5: 'purple', 6: 'yellow', 7: 'indigo', 8: 'pink', 9: 'gray', 10: 'cyan'}
     
        for k, v in self.line_color_dict.items() :
            self.comboBox_38.addItem(v)
            self.comboBox_39.addItem(v)
            self.comboBox_40.addItem(v)
            
        self.Node_font_name_dict = {0: 'Node Font Name', 1: 'Lucida Console', 2: 'Calibri', 3:'Franklin Gothic Book', 4:'Courier New'}
        
        for k, v in self.Node_font_name_dict.items() :
            self.comboBox_57.addItem(v)
            
            
        self.Caption_font_style_dict = {0: 'Caption Style', 1: 'solid', 2: 'dashed', 3:'dotted', 4:'invisible', 5: 'bold', 6: 'filled', 7:'striped', 8:'wedged'}
        
        for k, v in self.Caption_font_style_dict.items() :
            self.comboBox_58.addItem(v)        
                          
        self.radioButton_2.toggled.connect(self.toggleGroupBox)     
        self.pushButton2_1.clicked.connect(self.openOtherForm)
       

    def toggleGroupBox(self):

        if self.radioButton_2.isChecked():
            self.groupBox_7.setEnabled(True)      
              
        else:
            self.groupBox_7.setEnabled(False)
            
    def openOtherForm(self):
        
        self.all_values[1] = str(self.lineEdit_10.text())   # node Rank Space
        self.all_values[2] = str(self.lineEdit_11.text())   # node  Space
        self.all_values[39] = str(self.lineEdit_13.text())  # Caption Font Size
                         
        self.all_values[4] = str(self.lineEdit_20.text())  #Host <--> L1 Switch Line width
        self.all_values[5] = str(self.lineEdit_21.text())  #L1 Switch <--> L2 Switch Line width
        self.all_values[6] = str(self.lineEdit_22.text())  #L3 Switch <--> L3 Switch Line width              

        self.all_values[8] = str(self.lineEdit_30.text())  #Host switch font size
        self.all_values[9] = str(self.lineEdit_31.text())  #Host switch width
        self.all_values[10] = str(self.lineEdit_32.text())  #Host switch Heigh             
          
        self.all_values[15] = str(self.lineEdit_40.text())  #L1 switch font size
        self.all_values[16] = str(self.lineEdit_41.text())  #L1 switch width
        self.all_values[17] = str(self.lineEdit_42.text())  #L1 switch Heigh           
    
        self.all_values[22] = str(self.lineEdit_50.text())  #L2 switch font size
        self.all_values[23] = str(self.lineEdit_51.text())  #L2 switch width
        self.all_values[24] = str(self.lineEdit_52.text())  #L2 switch Heigh           
            
        self.all_values[29] = str(self.lineEdit_60.text())  #L3 switch font size
        self.all_values[30] = str(self.lineEdit_61.text())  #L3 switch width
        self.all_values[31] = str(self.lineEdit_62.text())  #L3 switch Heigh        

        ###########  Line Color           
        if self.comboBox_38.currentText() != "Line Color" :       
            self.all_values[35] =   self.comboBox_38.currentText()          
        if self.comboBox_39.currentText() != "Line Color" : 
            self.all_values[36] =   self.comboBox_39.currentText()               
        if self.comboBox_40.currentText() != "Line Color" : 
            self.all_values[37] =   self.comboBox_40.currentText()   
             
        ############   Host 
        if self.comboBox_41.currentText() != "Shape" :       
            self.all_values[7] =   self.comboBox_41.currentText()          
        if self.comboBox_42.currentText() != "Device style" : 
            self.all_values[11] =   self.comboBox_42.currentText()        
        if self.comboBox_43.currentText() != "Font Color" : 
            self.all_values[12] =   self.comboBox_43.currentText()   
        if self.comboBox_44.currentText() != "Fill Color" : 
            self.all_values[13] =   self.comboBox_44.currentText()   
            
        ############   L1 switch 
        if self.comboBox_45.currentText() != "Shape" :       
            self.all_values[14] =   self.comboBox_45.currentText()          
        if self.comboBox_46.currentText() != "Device style" : 
            self.all_values[18] =   self.comboBox_46.currentText()   
        if self.comboBox_47.currentText() != "Font Color" : 
            self.all_values[19] =   self.comboBox_47.currentText()   
        if self.comboBox_48.currentText() != "Fill Color" : 
            self.all_values[20] =   self.comboBox_48.currentText()                 
        
        ############   L2 switch     
        if self.comboBox_49.currentText() != "Shape" :       
            self.all_values[21] =   self.comboBox_49.currentText()         
        if self.comboBox_50.currentText() != "Device style" : 
            self.all_values[25] =   self.comboBox_50.currentText()   
        if self.comboBox_51.currentText() != "Font Color" : 
            self.all_values[26] =   self.comboBox_51.currentText()   
        if self.comboBox_52.currentText() != "Fill Color" : 
            self.all_values[27] =   self.comboBox_52.currentText()           
                       
        ############   L3 switch                                  
        if self.comboBox_53.currentText() != "Shape" :       
            self.all_values[28] =   self.comboBox_53.currentText()          
        if self.comboBox_54.currentText() != "Device style" : 
            self.all_values[32] =   self.comboBox_54.currentText()   
        if self.comboBox_55.currentText() != "Font Color" : 
            self.all_values[33] =   self.comboBox_55.currentText()   
        if self.comboBox_56.currentText() != "Fill Color" : 
            self.all_values[34] =   self.comboBox_56.currentText()           
                     
        ############   Node Font Name              
        if self.comboBox_57.currentText() != "Node Font Name" : 
            self.all_values[38] =   self.comboBox_57.currentText()   
                   
        ############   Caption Font Name              
        if self.comboBox_58.currentText() != "Caption Style" : 
            self.all_values[40] =   self.comboBox_58.currentText()                        
        if self.radioButton_2.isChecked():    
            self.all_values[0] = "checked"  #노드 Rank Space
            
        ############   Caption             
        self.all_values[3] = self.lineEdit_12.text() # caption        
        if  self.lineEdit_12.text() == "Caption (Null)" :              
            self.all_values[3] = ""       
            
        try:
            self.all_values[1] = self.lineEdit_10.text()   #node Rank Space
            self.all_values[2] = self.lineEdit_11.text()   #node  Space
            self.all_values[39] = self.lineEdit_13.text()  #Caption Font Size
                        
            self.all_values[4] = self.lineEdit_20.text()  #Host <--> L1 Switch Line width
            self.all_values[5] = self.lineEdit_21.text()  #L1 Switch <--> L2 Switch Line width
            self.all_values[6] = self.lineEdit_22.text()  #L3 Switch <--> L3 Switch Line width              

            self.all_values[8] = self.lineEdit_30.text()  #Host switch font size
            self.all_values[9] = self.lineEdit_31.text()  #Host switch width
            self.all_values[10] = self.lineEdit_32.text()  #Host switch Heigh                      
            
            self.all_values[15] = self.lineEdit_40.text()  #L1 switch font size
            self.all_values[16] = self.lineEdit_41.text()  #L1 switch width
            self.all_values[17] = self.lineEdit_42.text()  #L1 switch Heigh           
    
            self.all_values[22] = self.lineEdit_50.text()  #L2 switch font size
            self.all_values[23] = self.lineEdit_51.text()  #L2 switch width
            self.all_values[24] = self.lineEdit_52.text()  #L2 switch Heigh           
            
            self.all_values[29] = self.lineEdit_60.text()  #L3 switch font size
            self.all_values[30] = self.lineEdit_61.text()  #L3 switch width
            self.all_values[31] = self.lineEdit_62.text()  #L3 switch Heigh        
   
            self.temp.close()                    
            
        except:
            self.error_messages =  "Pleae check if you put weird value"
            self._new_window_pop_up(self.error_messages)

            self.all_values = {0:"unchecked", 1:"8", 2:"0", 3:"", 4:"1" ,5:"1" ,6:"1" , 7:"circle", 8:"0.04" ,9:"0.08" ,10:"0", 11:"solid", 12:"black", 13:"green", 14:"rectangle", 15:"0.04" ,16:"0.08" ,17:"0" , 18:"solid", 19:"black", 20:"white" ,21:"rectangle", 22:"0.04" ,23:"0.08" ,24:"0" ,25:"solid", 26:"black", 27:"white" ,28:"rectangle", 29:"0.04" ,30:"0.08" ,31:"0",   32:"solid", 33:"black", 34:"white", 35:"green", 36:"blue", 37:"black", 38:"Calibri" , 39:"1" , 40:"solid" }
            pass
             
    def _new_window_pop_up(self,template):
     
        self.pop_up_window = QtWidgets.QMainWindow()                                    
        self.pop_up_window.setWindowTitle('error_messages')

        self.pop_up_window.move(self.geometry().x() + self.geometry().width() + 30,         
                 self.geometry().y() - 30)
        
        text_display = QtWidgets.QTextBrowser(self.pop_up_window)      
        text_display.setStyleSheet('font: 10pt "Fixedsys"; background-color: rgb(0, 0, 0); color: rgb(0, 255, 72);')  

        self.pop_up_window.setGeometry(600,150,320,90)
        text_display.setGeometry(10,10,300,70)    
        text_display.setText(template)

        self.pop_up_window.show()

        
# -*- coding: ansi -*-
#                           IBNETDISCOVER PARSER (TARZAN)
#
# 
# NOTE: this source code is not open source and is not for use outside of Nvidia.  It may contain
# information that is confidential to Nvidia.
#
# This code processes an ibnetdiscover output file and derives some higher-level information 
# that is otherwise labor-intensive to figure out, including:
# - IB fabric topology diagram (Visio) via GraphVizio
# - Switch-level views of connections to other IB entities
# - Director-level views of connections to other IB entities
# - Detection of common fabric issues such as sub-optimal cabling 
#
# An ibnetdiscover output file begins with a few lines of information about the run, followed
# by a blank line. The rest of the report consists of node descriptions, each of which ends
# with a blank line.
# NOTE:  this code assumes there are no extraneous text lines (e.g. CLI commands) at the
# beginning or end of the input file.  It also assumes the file is complete.
#
# This is my first Python program and contains a mixture of coding styles due to learning
# the language on the fly.  Much improvement in efficiency, elegance, and Pythonicness is possible.  
# OK here we go.
#
# device IDs to incorporate:
# bd36: 32-port IS-IV switch?  Goldman Sachs
# 5a62: 4036E
# 5a65: HCA  Goldman Sachs
# 673c: HCA 2-port  "MT25408 ConnectX Mellanox Technologies" Goldman Sachs & GM
# c738:  32-port Switch-X?  Blade? GM; there is a 36-port version at Shell
# b924:  24-port switch "MT47396 Infiniscale-III Mellanox" at GE
# 5a42:  24-port 2012/2004 "ISR2012/ISR2004 Voltaire sRB-20210G-2LOW" at GE
# 5a40: 24-port ISR2004 "Voltaire sFB-2004" at GE
# 634a: 2-port HCA "MT47396 Infiniscale-III Mellanox Technologies" at GE
#
ouiDict = {"2c9" : "Mellanox", "258b" : "Mellanox", "e41d2d" : "Mellanox", "f45214" : "Mellanox",
    "15b3" : "Mellanox", "8f1": "Voltaire/Mellanox", "88dd79" : "Voltaire/Mellanox", 
    "5ad" : "TopSpin", "1867" : "TopSpin", "66a" : "SilverStorm/QLogic", "1175" : "PathScale",
    "1077" : "QLogic/Intel", "1fc1" : "QLogic/Intel", "5ad" : "Cisco", "1708" : "HP", "5076" : "IBM"}
mellanoxDevice = {
    "5a44" : "MT23108 InfiniHost HCA", 
    "5e8c" : "MT24204 InfiniHost III Lx HCA",
    "6274" : "MT25204 InfiniHost III Lx HCA", 
    "6282" : "MT25208 InfiniHost III Ex HCA",
    "5274" : "MT21108 InfiniBridge",
    "634a" : "MT2548 ConnectX VPI HCA, PCIe 2.0 2.5GT/s, IB DDR 10GbE",
    "6732" : "MT26418 ConnectX VPI  HCA, PCIe 2.0 5GT/s, IB DDR 10GbE",
    "2c9:1003" : "MT27500 ConnextX-3 VPI HCA, IB FDR",
    "2c9:1007" : "FDR HCA",    # Saw this one at U of Chicago
    "2c9:1011" : "MT27600 Connect-IB HCA, IB FDR",
    "2c9:1013" : "MT27700 ConnectX-4 VPI HCA, IB EDR",
    "2c9:1017" : "MT27800 ConnectX-5 VPI HCA, IB EDR", 
    "2c9:1019" : "MT28800 ConnectX-5 Ex VPI HCA, IB EDR",
    "2c9:101b" : "MT28908 ConnectX-6 VPI HCA, IB HDR", 
    "2c9:673c" : "MT26428 ConnectX VPI HCA, PCIe 2.0 5GT/s IB QDR 10GbE",
    "6278" : "MT25208 InfiniHost III Ex HCA (Tavor compatibility mode)",
    "c738" : "SX60xx Switch",
    "2c9:c739" : "SX60xx Gateway"}
qlogicDevice = {"7220" : "IBA7220 InfiniBand HCA", "d" : "IBA6110 InfiniBand HCA",
    "10" : "IBA6120 InfiniBand HCA", "7322" : "IBA7322 QDR InfiniBand HCA"}
topspinDevice = {"5a44" : "MT23108 InfiniHost HCA", "6282" : "MT25208 InfiniHost III Ex",
    "5e8c" : "MT24204 InfiniHost III Lx HCA", "6274" : "MT25204 InfiniHost III Lx HCA",
    "6278" : "MT25208 InfiniHost III Ex (Tavor compatibility mode)"}
silverstormDevice = {}
voltaireDevice = {"6278" : "MT25208 InfiniHost III Ex HCA (Tavor compatibility mode)",
    "5a30" : "ISR 9024D DDR Switch", 
    "5a31" : "ISR 9024D-M DDR Switch",
    "5a2e" : "ISR 9024S SDR Switch",
    "5a5a" : "GD 4036 QDR Switch",
    "5a38" : "sLB-2024 DDR Leaf Board for ISR 20xx Switch",
    "5a37" : "sFB-2012 DDR Fabric Board for ISR 2012 Switch",
    "5a40" : "sFB-2004 DDR Fabric Board for ISR 2004 Switch",
    "5a42" : "sRB-20210G DDR Leaf/Gateway Board for ISR 20xx Switch",
    "5a5b" : "sLB-4018 QDR Leaf Board for GD 4x00 Switch",
    "5a5c" : "sFB-4700 QDR Fabric Board for GD 4700 Switch",
    "5a62" : "Mellanox/Voltaire GD 4036E Switch/Gateway"}
pathscaleDevice = {}
ciscoDevice = {"b924" : "SFS700D DDR Switch"}
hpDevice = {}
ibmDevice = {}
sunDevice = {}
oracleDevice = {}
spineDeviceIDs = frozenset (["5a37", "5a40", "5a5c", "5a5d"])    # Not complete set- need MLNX, ISR9096, 
leafDeviceIDs = frozenset (["5a38", "5a42", "5a5b"])    # Not a complete set - need MLNX, ISR9096, 
directorDeviceIDs = spineDeviceIDs | leafDeviceIDs    # The union of the two sets
qlogicSpineNames = frozenset (["S111A", "S111B", "S113A", "S113B", "S115A", "S115B", \
    "S117A", "S117B", "S209A", "S209B", "S211A", "S211B", "S213A", "S213B", "S215A", "S215B", \
    "S217A", "S217B"])    # Qlogic uses the Node Description to indicate Director Spines (and Leafs)
mlnxSpineNames = frozenset (["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", \
    "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20"])   # MLNX DDR, QDR, EDR, HDR
ibGenToLaneSpeed = {"SDR":2.5,"DDR":5,"QDR":10,"FDR10":10,"FDR":14,"EDR":25,"HDR":50,"NDR":100,"???":2.5," ":2.5}
deviceIDsofMappedDirectors = {}    # Will be filled in by buildDirectorMaps routine
noPeer = " "

import re
from time import ctime
from collections import namedtuple
from tkinter import filedialog
from tkinter import *
from shutil import copyfile
import unicodedata
import xlsxwriter

#####################################################################################
#### Data Structures 
#####################################################################################

Link = namedtuple ("Link", "peerType peerNodeGUID portGUID fromPortNum toPortNum peerLID \
    linkWidthXRate linkDesc")
# peerType: "S" if other end of this link is a Switch, "H" if its an HCA
# peerNodeGUID:  Node GUID of the device on the other end of this link
# portGUID:  If either end of this link is an HCA, this is the HCAs Port GUID
# fromPortNum:  Port number on the local device that this link is attached to
# toPortNum:  Port number on the device attached to the other end of this link
# peerLID: Base LID in decimal of peer Port (character string)
# linkWidthXRate:  Link width and rate, e.g. "4xFDR"
# linkDesc:  Text, LID, LMC, etc. from the end of the input line
defaultLink = Link (peerType = " ", peerNodeGUID = noPeer, portGUID = " ", fromPortNum = "0",
    toPortNum = "0", peerLID = " ", linkWidthXRate = " ", linkDesc = " ")
currentLink=defaultLink

Node = namedtuple ("Node", "nodeType vendorID deviceID sysimgGUID nodeGUID nodeGUID2 \
    nodeDesc nodePortCount nodePortList nodeDirectorGUID nodePortZeroLID nodeModel \
    nodeIBGen nodeLayout nodeSlotName nodeSwitchLinks nodeHCALinks nodeSpecialHCAs \
    nodeHasVPorts nodeVPortLists nodeNeighborhood nodeSwGroup nodeRail")
# nodeType:  "S" for a Switch, "H" for an HCA
# vendorID:  Vendor OUI for this device 
# deviceID:   Vendor-assigned device typeOUI
# sysimgGUID:   System Image GUID for this device
# nodeGUID:  Node GUID
# nodeGUID2:  Second GUID reported by ibnetdiscover for a Switch Port GUID of Switch port 0?   
# nodeDesc:   Rest of text reported by ibnetdiscover for a node
# nodePortCount:   Number of ports on this device (character string)
# nodePortList:  List of Port structures, including one for Port 0 (which is not used)
# nodeDirectorGUID: pseudo-GUID of Director containing this node (" " otherwise)
# nodePortZeroLID: LID for Port 0 if node is a Switch (character string)
# nodeIBGen: string describing the node IB technology (e.g. "FDR")
# nodeModel: string describing the Switch (e.g. "SX60xx")
# nodeLayout: string describing how the ports are physically arranged
# nodeSlotName: if node is a Leaf or Spine, a string naming its slot, e.g. "L17", "S3" (else " ")
# nodeSwitchLinks: number of links to Switches from this node (string)
# nodeHCALinks: number of links to HCAs from this node (string) ("0" if node is an HCA)
# nodeSpecialHCAs:  number of virtual HCAs active (e.g. SHARP, Gateway)(string)
# nodeHasVPorts:  whether this node (HCA) has virtual ports (vPorts) (boolean)
# nodeVPortLists:  if node has vPorts, a list of n lists where n = node port count
# nodeNeighborhood:  for a leaf (L1) switch, the (arbitrary) # of the low latency neighborhood it belongs to
# nodeSwGroup: for a Switch, will contain the analyzeBoxGraph-assigned boxRank starting with "1" (string)
# nodeRail:  for an HCA that is part of a DGX 'rail', the rail ID (string)
defaultNode = Node (nodeType = " ", vendorID = " ", deviceID = " ", sysimgGUID = " ",nodeGUID = " ",
    nodeGUID2 = " ", nodeDesc = " ", nodePortCount = " ", nodePortList = " ", nodeDirectorGUID = " ",
    nodePortZeroLID = " ", nodeIBGen = " ", nodeModel = " ", nodeLayout = " ", nodeSlotName = " ",
    nodeSwitchLinks = "0", nodeHCALinks = "0", nodeSpecialHCAs = "0", nodeHasVPorts = False,
    nodeVPortLists = " ", nodeNeighborhood = " ", nodeSwGroup = " ", nodeRail = " ")
currentNode = defaultNode

Port = namedtuple ("Port", "portType portConnected portLink")
# portType:  "IB" for InfiniBand, "EN" for Ethernet, " " for none (e.g. if port is on an absent Leaf board)
# portConnected:  "Y" if theres a working link connected to this port, "N" if not
# portLink:  a Link structure describing the link connected to this Port (if any)
defaultPort = Port (portType = "IB", portConnected = "N", portLink = " ")
currentPort = defaultPort

Director = namedtuple ("Director", "directorVendorID directorSpineDeviceID directorSpineGUIDList \
    directorLeafGUIDList directorNodeGUID directorMaxPorts directorSpeed directorModel \
    directorLayout directorLeafExtPorts directorPeerList directorDesc")
# directorVendorID:  Vendor OUI for this Director
# directorSpineDeviceID:  Device OUI of this Directors Spine modules
# directorSpineGUIDList:  List of Node GUIDs for the Directors Spine boards (incl. unused entry 0)
# directorLeafGUIDList:  List of Node GUIDs for the Directors Leaf boards (incl. unused entry 0)
# directorNodeGUID:  pseudo Node GUID
# directorMaxPorts:  Number of external ports in a fully populated Director (character string)
# directorLeafExtPorts:  Number of external ports per Leaf board (character string) 
# directorSpeed:  string describing the Director IB technology (e.g. "FDR")
# directorModel:  string describing the Director (e.g. "CS7500")
# directorLayout:  string describing how the ports& leaf boards are physically arranged
# directorPeerList:  List of Peer structures for all possible ports, including an unused entry zero
# directorDesc:  portion of Node Description from one Spine ASIC-- user-assigned chassis name
defaultDirector = Director (directorVendorID = " ", directorSpineDeviceID = " ", 
    directorSpineGUIDList = " ", directorLeafGUIDList = " ",     directorNodeGUID = " ",
    directorLeafExtPorts = " ", directorMaxPorts = " ", directorSpeed = " ", directorModel = " ",
    directorLayout = " ", directorPeerList = " ", directorDesc = " ")
currentDirector = defaultDirector

Peer = namedtuple ("Peer", "peerNodeType peerNodeGUID peerLID peerLinkType peerPortNum")
# peerNodeType:   "S" or "H" for switch or HCA 
# peerNodeGUID:  Node GUID of peer node
# peerLID:  LID of peer node
# peerLinkType:  e.g. "4XQDR" or "1XSDR"
# peerPortNum:  port number on peer, between 1 and the max port count (char string)
defaultPeer = Peer (peerNodeType = " ", peerNodeGUID = noPeer, peerLID = " ", peerLinkType = " ",
    peerPortNum = " ")

directorMap = namedtuple ("directorMap", "dirModel dirSpeed portsPerASIC numOfLeafASICs \
    numOfSpineASICs dirMaxPorts dirLayout dirLeafExtPorts spinePortToLeafList leafPortToSpineList")
# dirName:  Director type (char string)
# dirSpeed:  string describing product speed, e.g. "EDR"
# portsPerASIC:  number P of ports on an ASIC (char string)
# numOfLeafASICs:  number L of Leaf ASICs in a fully populated chassis (char string)  
# numOfSpineASICs:  number S of Spine ASICs in afully populated chassis (char string)
# dirMaxPorts: number of external ports if fully populated (char string)
# dirLayout: string describing how the Leaf module ports are arranged
# dirLeafExtPorts:  n# of external ports per Leaf module (char string)
# spinePortToLeafList: L entries in order of Leaf ASIC names, e.g. starting with "L01/U1".
#   e.g. if the entry in spinePortToLeafList is ['L01/U1','1','3'] it means that
#   *each* Spine ASIC in the Director has two ports, 1 and 3, connected to the 
#   Leaf ASIC named "L01/U1". 
# leafPortToSpineList: S entries in order of Spine ASIC names, e.g. starting with "S01/U1".
#   e.g. if the entry in leafPortToSpineList is ['S01/U1','23','24'] it means that
#   *each* Leaf ASIC in the Director has two ports, 23 and 24, connected to the 
#   Spine ASIC named "S01/U1". 
defaultDirectorMap = directorMap (dirModel = " ", dirSpeed = " ", portsPerASIC = "0", 
    numOfSpineASICs = "0", numOfLeafASICs = "0", dirMaxPorts = " ", dirLayout = " ", 
    dirLeafExtPorts = " ", spinePortToLeafList = [], leafPortToSpineList = [])

asicAttributes = namedtuple ("asicAttributes", "model desc ibGen")
asicTable = {
    "2c9:1003" : asicAttributes (model="ConnectX-3", desc="MT27500 ConnextX-3 VPI HCA, IB FDR", ibGen="FDR"),
    "2c9:1011" : asicAttributes (model="Connect-IB", desc="MT27600 Connect-IB HCA, IB FDR", ibGen="FDR"),
    "2c9:1013" : asicAttributes (model="ConnectX-4", desc="MT27700 ConnectX-4 VPI HCA, IB EDR", ibGen="EDR"),
    "2c9:1017" : asicAttributes (model="ConnectX-5", desc="MT27800 ConnectX-5 VPI HCA, IB EDR", ibGen="EDR"),
    "2c9:1019" : asicAttributes (model="ConnectX-5 Ex", desc="MT28800 ConnectX-5 Ex VPI HCA, IB EDR", ibGen="EDR"),
    "2c9:101b" : asicAttributes (model="ConnectX-6", desc="MT28908 ConnectX-6 VPI HCA, IB HDR", ibGen="HDR"), 
    "2c9:673c" : asicAttributes (model="ConnectX", desc="MT26428 ConnectX VPI HCA, PCIe 2.0 5GT/s IB QDR 10GbE", ibGen="QDR"),
    "2c9:c739" : asicAttributes (model="SX60xx Gateway", desc="SX60xx Gateway virtual HCA", ibGen="FDR")}

#### end of Data Structures ####

#### warnSection ####
def warnSection (sectionTitle):
    global wf    # The 'warnings' .rtf file
    global warnSectionTitle
    warnSectionTitle = sectionTitle
#### end of warnSection ####

#### warn ####
def warn (warnText):
    global wf    # The 'warnings' .rtf file
    global warnSectionTitle
    global warn_return2
    
    if len (warnSectionTitle) > 1:
    #    wf.write (" " + rtfEOL)
    #    wf.write (warnSectionTitle + rtfEOL)
    #    wf.write (" " + rtfEOL)      
        warn_return2.append(warnSectionTitle)  
        warnSectionTitle = " "
    #wf.write ("   " + warnText + rtfEOL)           
    #wf.write (" " + rtfEOL)
    warn_return2.append(warnText)  
        
#### end of warn ####

#####################################################################################
#### Begin routines to parse the ibnetdiscover file and build data structures to represent the fabric.
#####################################################################################

#### getHeading ####

def getHeading():    # Get, save, and partially parse the opening lines of the ibnetdiscover file
    global f    # The ibnetdiscover file
    global l    # The current line from the ibnetdiscover file
    global genTimeAndDate    # Time that ibnetdiscover file was run
    global hdrx

    
    genTimeAndDate = "????"
    hdrx = []
    l = f.readline()
    done = False
    while len (l) > 0 and not done:    # In case the file was cut&pasted, e.g. from a PUTTY session
        if l [0] == "#":    # If start of heading section 
            done = True
        else:
            hdrx.append ("JUNK AT BEGINNING OF IBNETDISCOVER FILE: " + l)
            l = f.readline ()
    done = False
    while len (l) > 0 and not done:
        #print ("//// Input line: ", l [:-1])    #### DEBUG ####
        if not (len(l) == 1 or l[0] == "#"):    # Must be the start of actual content
            done = True
        else:
            if l [0] == "#": 
                if "Timestamp:" in l:    # New heading format with creation time in UTC +0000
                    getTimeAndDate = (l.split ("Timestamp:", 1))[1].strip() 
                if "generated on" in l:     # Older heading format
                    # We don't know the creation time zone so can't convert to UTC
                    genTimeAndDate = (l.split ("generated on", 1))[1].strip()
            hdrx.append (l) 
            l = f.readline ()


#### end of getHeading ####

#### getLink ####

# Reads and processes one link description from an ibnetdiscover report.
# Assumes the text line has already been read, and reads a new line just as it finishes.
# Note: ibnetdiscover has a little-used option, "--Full", which appends additional data (from
# the Port Info attribute?) to each link description.  Currently this data is *ignored*.
# Need to rewrite this routine to use Regular Expressions someday.
def getLink():    # Get a connection from my port to another Node's port
    global l    # The current line from the ibnetdiscover file 
    global currentNode
    global currentLink
    global defaultLink
    global sawVPorts
    #print (l)       
    currentLink = defaultLink
    linkDesc = l.partition("#")
    lineLeft = linkDesc[0]
    linkDesc = linkDesc[2].rstrip ('\n')    # This part contains the Node Desc, LID, link speed &width
    j = lineLeft.find("(")     # Extract a Port GUID if there is one (it can appear in one of two locations)
    k = lineLeft.find(")")
    pglen = k - j -1                                                                     # GUID16
    if (pglen in (13, 14, 15, 16)):    # Allow Port GUID to be 13 to 16 hex characters    # GUID16
        linkPortGUID = lineLeft[(j + 1) : k]
        #print ("LINKPORTGUID ", linkPortGUID, " NODE GUID ", currentNode.nodeGUID) 
    else:    # No Port GUID, i.e. this is a switch-to-switch link
        linkPortGUID = " "
    j = lineLeft.find("[")    # Extract the from port number
    k = lineLeft.find("]")
    if ((k - j) in (2,3)):    # Port number should only be 1 or 2 characters
        linkFromPort = lineLeft[(j + 1) : k]
    j = lineLeft.rfind("[")    # Extract the to port number
    k = lineLeft.rfind("]")
    if ((k - j) in (2,3)):    # Port number should only be 1 or 2 characters
        linkToPort = lineLeft[(j + 1) : k]
    j = lineLeft.find("\"")    # Extract the to port Node GUID preceded by H- or S- indicating node type
    k = lineLeft.rfind("\"")
    if ((k - j) == 19):    # Assume the length is always 19 characters for now (incl. trailing quote) # GUID16
        linkNodeGUID = lineLeft[(j + 1) : k]
    linkPeerNodeType = linkNodeGUID[0]
    linkNodeGUID = linkNodeGUID[2 : 18]  # Takes 16 chars of GUID                     # GUID16
    # Now get the LID
    lid = " "
    j = linkDesc.rfind ("lid")    # Will return the index of the "l" in "lid"
    if j > -1:    # We found "lid"
        k = j + 4    # Skip over "lid" plus a blank to the first LID digit
        lid =""
        while linkDesc [k] in "0123456789":
            lid = lid + linkDesc [k]
            k = k + 1
    # Now get the link width and rate.  Since ibnetdiscover may report "?????" if it can't determine
    # what the link is doing, we need to allow for that.  k will be pointing at the blank after the LID num
    wxr = " "
    j = linkDesc.rfind ("x", k+2, len (linkDesc))    # Look for the "x" in "4xFDR" e.g.
    if j > -1:    # We found an x near the end of the Link Description (as opposed to "?????")
        #wxr = linkDesc [j - 1:].rstrip()    # Get the width, plus "x", plus rate, minus trailing white space/newlines
        wxr = linkDesc [j - 1:j + 4]   # Get the width, plus "x", plus rate acronym (e.g. "FDR")
        #print ('>>>> WXR = "' + wxr + '"')    #### DEBUG ####
    # Now pack the data into the Link structure
    currentLink = currentLink._replace(peerType = linkPeerNodeType)
    currentLink = currentLink._replace(peerNodeGUID = linkNodeGUID)
    currentLink = currentLink._replace(fromPortNum = linkFromPort)
    currentLink = currentLink._replace(toPortNum = linkToPort)
    currentLink = currentLink._replace(linkDesc = linkDesc)
    currentLink = currentLink._replace(portGUID = linkPortGUID)
    currentLink = currentLink._replace (peerLID = lid)
    currentLink = currentLink._replace (linkWidthXRate = wxr)
    j = int(linkFromPort)
    k = currentNode.nodePortList[j]    # Get the Port structure for the from port
    k = k._replace (portConnected = "Y")    # Update it
    k = k._replace (portLink = currentLink)
    currentNode.nodePortList[j] = k    # Put it back
    # A bit more housekeeping:
    if linkPeerNodeType == "S":    # Is the peer Node a Switch?
        n = int (currentNode.nodeSwitchLinks)
        currentNode = currentNode._replace (nodeSwitchLinks = str (n + 1))
    else:    # Peer is an HCA
        np = int (currentNode.nodePortCount)    # Get the number of ports I have
        if (not (j%2 == 0) and (np == j)):    # If peer HCA connects to my highest port & that port # is odd
            currentNode = currentNode._replace (nodeSpecialHCAs = "1")    # 'special' HCA, e.g. SHARP
        else:
            n = int (currentNode.nodeHCALinks)
            currentNode = currentNode._replace (nodeHCALinks = str (n + 1))
    ibNet [currentNode.nodeGUID] = currentNode  
    l = f.readline()
    if l [0:6] == "vPorts":    # We treat the Virtual ports as an extension of the physical Link description
        #print ("VPORT: " + l)
        if not (currentNode.nodeHasVPorts):    # Well it does now
            currentNode = currentNode._replace (nodeHasVPorts = True)    # And initialize its vPortLists (1 per port):
            listOfLists = [[] for i in range (int(currentNode.nodePortCount))]
            currentNode = currentNode._replace (nodeVPortLists = listOfLists) 
        vp = int (l.split()[2])    # Line text should be "vPorts TopIndex <n>" so get <n> as an integer
        l = f.readline ()    # Skip the "vPorts TopIndex" line
        vpl = []    # We'll build a list of the vPort text lines
        while vp > 0:    # This loop collects the lines describing each virtual port
            #print ("VPORT:" + l [:-1])    #### DEBUG ####
            vpl = vpl + [l [:-1]]    # Add it to the sub-list, without the newline
            l = f.readline ()
            vp = vp - 1
        i = int (linkFromPort) - 1    # VPortLists [0] corresponds to Node Port 1
        listOfLists = currentNode.nodeVPortLists
        listOfLists [i] = vpl
        currentNode = currentNode._replace (nodeVPortLists = listOfLists)
        ibNet [currentNode.nodeGUID] = currentNode

#### end of getLink ####

#### getNode ####

# Reads and processes the ibnetdiscover description of a node and its links to other nodes.
# Assumes that the first line of the node description has already been read, and reads past the
# blank line(s) that end the section.
def getNode():    
    global f    # The ibnetdiscover file
    global l    # The current line from the ibnetdiscover file 
    global currentNode
    global ibNet
    currentNode = defaultNode

    parts = l.partition ("=")    # Get vendor ID (OUI)
    j = len(parts[2]) - 1    # Last character should be a line feed
    currentNode = currentNode._replace (vendorID = parts [2][2:j])
    l = f.readline()    # Get device ID line
    parts = l.partition ("=")
    j = len(parts[2]) - 1
    currentNode = currentNode._replace (deviceID = parts [2][2:j])
    l = f.readline()    # Get System Image GUID line
    parts = l.partition ("=")
    j = len(parts[2]) - 1    # Last character should be a line feed
    currentNode = currentNode._replace (sysimgGUID = parts [2][2:j])
    l = f.readline()    # Get Node GUID line
    parts = l.partition ("=")
    currentNode = currentNode._replace (nodeGUID = parts [2][2:18])    # Assume full 16 characters # GUID16
    if (l[0:6] == "switch"):
        currentNode = currentNode._replace (nodeType = "S")
        parts = parts[2].partition ("(")    # Get the second switch GUID (whatever it means)
        currentNode = currentNode._replace (nodeGUID2 = parts[2][0:16])                            # GUID16
    else:
        currentNode = currentNode._replace (nodeType = "H")
    l = f.readline()    # Get the Node GUID, port count, etc.
    parts = l.partition ("#")    # Get the node description, LID, LMC
    ndesc = parts [2]
    currentNode = currentNode._replace (nodeDesc = ndesc)
    parts = parts [0].partition ("\"")    #  Find the start of the Node GUID string
    currentNode = currentNode._replace (nodeGUID = parts[2][2:18])    # Take the last 16 characters # GUID16
    j = parts[0][-2]
    if (parts[0][-3] in "0123456789"):    # Port count is 2 digits
        j = parts[0][-3:-1]
    currentNode = currentNode._replace (nodePortCount = j)
    pl = []    # Prepare to build a default PortList
    for i in range (int(j) + 1):    #  Includes Port 0-- it wont be used but makes entry [N] = port N
        pl.append (defaultPort)
    currentNode = currentNode._replace (nodePortList = pl)
    # If this node is a Switch, extract the Port 0 LID from the node description line
 
   
    if currentNode.nodeType == 'S':  
        j = ndesc.rfind ("lid")    # Will return the index of the "l" in "lid"
        if j > -1:
            k = j + 4    # Skip over "lid" plus a blank to the first LID digit
            lid =""
            while ndesc [k] in "0123456789":
                lid = lid + ndesc [k]
                k = k + 1
            currentNode = currentNode._replace (nodePortZeroLID = lid)    
    
    # Now the completed Node structure goes into the ibNet dictionary, indexed by its Node GUID
    ibNet [currentNode.nodeGUID] = currentNode
 
    
    l = f.readline()    # Read first link description
    while len(l) > 1:
        getLink()
    while len (l) == 1:    # Skip blank lines which only contain a newline (\n) until we
        l = f.readline()    # Get the first line of the next node section or end of file

#### end of GetNode ####

#### processIBNetDiscover ####
#  Assumes the input file is already open but no lines have been read.

def processIBNetDiscover ():
    global f    # The ibnetdiscover file (already open)
    global l    # The current line from the ibnetdiscover file
    #print ("  Parsing heading...")
    getHeading ()    # Get and save the opening lines of an ibnetdiscover report
   # print ("  Parsing main text...")
    while (len(l)>0):
        getNode ()    # Build the ibNet dictionary of Nodes

#### end of processIBNetDiscover ####

#### getLinkStruct ####
# This routine returns a Link structure given a Node GUID (string) and a port number (integer).
# If there is no link present on the port, the defaultLink structure is returned.  The caller
# can use a blank (" ") peerType field (e.g.) to determine if there's not actually a Link.
# NOTE:  This is a newer routine and could be retrofitted into other areas of the code that
# deal with Links, to make them easier to read and maintain.
def getLinkStruct (nodeGUID, portNum):
    global defaultLink
    linkStruct = defaultLink
    nodeStruct = ibNet [nodeGUID]
    ports = int (nodeStruct.nodePortCount)
    if not (portNum > ports):
        portStruct = nodeStruct.nodePortList [portNum]
        if portStruct.portType == "IB":
            if not (portStruct.portLink == " "):
                linkStruct = portStruct.portLink
    return linkStruct
#### end of getLinkStruct ####

#### peerExists #### 
# Helper routine for finding peers (neighbors) of a given Node.
# nodeGUID is the GUID of the known node, and nodePortNum is the integer
# value of a port on that node.  
# Parameters peerGUID and peerLink *must* be lists with at least one entry.
# Returns False if there is no peer node; otherwise it returns True and 
# supplies the GUID of the peer Node and the Link structure representing
# the connection to that peer.  
#
def peerExists (nodeGUID, nodePortNum, peerGUID, peerLink):
    global ibNet
    #print (nodeGUID, nodePortNum, peerGUID, peerLink)
    peerLink [0] = getLinkStruct (nodeGUID, nodePortNum)
    #print("peerLink: ", peerLink)
    peerGUID [0] = peerLink[0].peerNodeGUID
    #print("peerGUID: ", peerGUID)
    return (not(peerGUID [0] == " "))

#### end of peerExists ####

#### checkLinkSpeeds ####
# Look at every Link in ibNet, and determine if it's not running at full speed.  This depends
# on the Node capabilities at each end of the Link.  We generate Warnings for each instance.
# We build a dictionary called portSpeed that contains every port of every link.  It's indexed by
# a string of the form "<guid>:<port>" where <guid> is the node GUID and <port> is the
# node port connected to a given link.
# Two entries exist per link, so the GUID:port from either end of the link can be used as a key.
# Each portSpeed entry is a 3-tuple: [<wxr1>, <link good>, <wxr2>] where <wxr1> is a string denoting
# the actual link width & speed (e.g. "4xHDR"), <link good> is a Boolean indicating the link has optimal
# width & rate, and <wxr2> is the optimal link width & rate.
# We also build a dictionary called linkSpeedIssuesByWXR, which only contains links that
# are running narrower or slower than expected.  It is indexed by a string "<wxr>", the actual
# width & rate (e.g. "1xSDR").  Each entry has the form <guid1>:<p1>-<guid2>:<p2>.
def checkLinkSpeeds ():
    global ibNet
    global wf
    global portSpeed    
    global linkSpeedIssuesByWXR    ####
    global sawWXR
    peerNodeGUID = [noPeer]    # For use by the peerExists routine
    peerLink = [" "]    # For use by the peerExists routine
    #portSpeed = {}    # Can't do this here-- must be done in main prog
    linkSpeedIssuesByWXR = {}
    #sawHDR = False
    sawWXR = {}    # Dictionary of (optimal) link speeds we encounter
    for i, key in enumerate (ibNet):
        #print ("checkLinkSpeeds KEY: ", key)
        if ibNet[key].nodeType == "S":    # We base our checking on Switch ASICs and their neighbors
            switchIBGen = ibNet[key].nodeIBGen    # E.g. "EDR" or "HDR"
            if switchIBGen == " ":    #### DEBUG ####
                print ("EMPTY IB GEN ON: ", key)    #### DEBUG ####
            switchLaneSpeed = ibGenToLaneSpeed[switchIBGen]    # Get max lane speed in Gbits/sec, e.g. 50 for HDR
            ports = int (ibNet[key].nodePortCount)
            for p in range (1, ports + 1):
                #print ("PORT :", p)     
                if peerExists (key, p, peerNodeGUID, peerLink):    # Look at the Link on port p and the Peer Node on the other end
                    linkWXR = peerLink[0].linkWidthXRate    # Get the link width & apparent IB generation, e.g. "4xHDR"
                    linkLaneSpeed = 1.0    # Initially assume it runs at an improbably low rate
                    if len(linkWXR) == 5:
                        if linkWXR[2:5] in ibGenToLaneSpeed:
                            linkLaneSpeed = ibGenToLaneSpeed[linkWXR[2:5]]    # We do know its lane speed
                    peerIBGen = ibNet[peerNodeGUID[0]].nodeIBGen    # Get the peer node's max speed
                    if peerIBGen == " ":    #### DEBUG ####
                        print ("EMPTY PEER IB GEN: ", peerNodeGUID[0])    #### DEBUG ####
                    peerLaneSpeed = ibGenToLaneSpeed[peerIBGen]    # Get the peer's max lane speed in Gbits/sec
                    slowerIBGen = switchIBGen    # Maybe...
                    smallerLaneSpeed = switchLaneSpeed    # This is the fastest possible lane speed (maybe)
                    if peerLaneSpeed < switchLaneSpeed:    # The Peer node is slower
                        slowerIBGen = peerIBGen
                        smallerLaneSpeed = peerLaneSpeed
                    #print("XXXXXXX slowerIBGen: ", slowerIBGen)
                    linkPoor = (linkWXR.split("x")[0] != "4") or (linkLaneSpeed < smallerLaneSpeed)    # True if Link isn't as fast/wide as possible
                    if linkPoor and False:    ####
                        print ("XXXXXX LINK POOR  Link:", linkWXR, " Switch:", key, switchIBGen, " Peer:", peerNodeGUID[0], peerIBGen)    ####
                    #if linkWXR[2:5] == "HDR":
                        #sawHDR = True
                    width = "4x"
                    # ibnetdiscover doesn't contain enough info to always know if HDR100 is top speed
                    if linkWXR == "2xHDR":    # Do some extra sleuthing to see if HDR100 is legit
                        bPorts = int(ibNet[peerNodeGUID[0]].nodePortCount)    # Get number of ports on peer Node 
                        linkPoor = (40 in [ports, bPorts]) or (41 in [ports, bPorts])    # If one or both Nodes is a non-split HDR ASIC
                        if not linkPoor:    # 2X width is probably legit
                            width = "2x"
                    pp = peerLink[0].toPortNum    # The peer Node's port number (string)
                    akey = key + ":" + str(p)    # A key into portSpeed based on my GUID & port #
                    bkey = peerNodeGUID[0] + ":" + pp    # A key based on the peer GUID & port #        
                    if not (akey in portSpeed):    # If we haven't already seen this link (e.g. by looking from the other end of it)
                        portSpeed [akey] = [linkWXR, not linkPoor, width + slowerIBGen]    # Each dict entry is a 3-tuple
                        portSpeed [bkey] = [linkWXR, not linkPoor, width + slowerIBGen]    # Put 2 entries so either node can be the index
                        sawWXR [width + slowerIBGen] = True                      
                    if linkPoor:    # Build a dictionary of problem links, grouped by the offending link width & rate
                        while not (linkWXR in linkSpeedIssuesByWXR):  linkSpeedIssuesByWXR [linkWXR] = []
                        link = akey + "-" + bkey    # A string representing the link
                        linkSpeedIssuesByWXR [linkWXR] = linkSpeedIssuesByWXR [linkWXR] + [link]    # Build list of bad links having this WXR
    warnSection ("#################### Check All Links for Sub-Optimal Speed #################### ")
    if len (linkSpeedIssuesByWXR) > 0 and ("4xHDR" in sawWXR):    # Don't confuse customers who don't yet have HDR
        warn ("(Note: ibnetdiscover doesn't contain enough data to determine if 2xHDR is a valid link speed in every case)")
    guidAndPortSeen = {}
    for j, WXR in enumerate (linkSpeedIssuesByWXR):
        wxr = WXR
        if len(WXR) < 5:
            wxr = "?"
        list = linkSpeedIssuesByWXR [WXR]
        warn ("Links Connected At " + wxr + ":")
        for i in range (0, len (list)):
            x = list[i]    # Get the next entry from the list, its form is <guid1>:<p1>-<guid2>:<p2>
            ap = x.split("-")[0]    # Get the 1st GUID and its port number
            a = ap.split(":")[0]    # Get the 1st GUID
            bp = x.split("-")[1]    # Get the 2nd GUID and its port number
            b = bp.split(":")[0]    # Get the 2nd GUID
            if not ((ap in guidAndPortSeen) or (bp in guidAndPortSeen)):    # Don't complain twice about the same link
                sa = ibNet[a].nodeType + " " + a + " " + ibNet[a].nodeDesc[:-1].rsplit('"', 1)[0] + '" [' + ap.split(":")[1] + "]"    
                sb = ibNet[b].nodeType + " " + b + " " + ibNet[b].nodeDesc[:-1].rsplit('"', 1)[0] + '" [' + bp.split(":")[1] + "]"    
                if sa[0] == "H":    # Always put HCAs first, to make it easier to spot them
                    warn ("   " + sa + " <- " + wxr + "-> " + sb)
                else:
                    warn ("   " + sb + " <- " + wxr + "-> " + sa)    # If the 2nd Node is an HCA, it will be shown first
                guidAndPortSeen [ap] = " "    # Create an entry - entry value isn't used
                guidAndPortSeen [bp] = " "    # Ditto
#### end of checkLinkSpeeds ####

#### addDirsToPortSpeed ####
# After the Directors (if any) have been discovered, this routine extends the
# portSpeed dictionary to include entries accessed by keys of the form
# "<dir GUID>:<port>".  Each new portSpeed entry is just a copy of the
# entry for the corresponding Leaf ASIC and its port number.
# E.g. for HDR Director D3 port 800, the new key is "D3:800" and its value
# is a copy of the entry for key "<D3 leaf L20/U2's guid>:40".
# Note that which leaf ASIC port #s are the external ones should really be
# a Director structure attribute (set by setDirectorAttributes?).
def addDirsToPortSpeed ():
    global portSpeed
    global allDirectors
    for i, dguid in enumerate (allDirectors):
        #print ("DIRECTOR: ", dguid)
        dir = allDirectors [dguid]
        dports = int (dir.directorMaxPorts)    # Needed?
        extports = 18
        if dir.directorSpeed in ["HDR"]:
            extports = 20
        elif dir.directorSpeed in ["SDR", "DDR"]:
            extports = 12
        #print ("EXTPORTS: ", extports)
        spID = dir.directorSpineDeviceID
        if spID in ["7320", "bd36", "c738", "cb20"]:    # If QLGC or MLNX
            b = 0    # Leaf ASIC external port #s begin at 1
        else:
            b = extports    # Leaf ASIC ext ports are the high half of the port #s
        dirport = 1
        leafguidlist = dir.directorLeafGUIDList
        #print ("leafguidlist: ", len (leafguidlist), " ", leafguidlist)
        for l in range (1, len(leafguidlist)):
            leafguid = leafguidlist[l]
            #print ("leafguidlist[", l, "]: ", leafguid)
            if leafguid != " ":
                for leafp in range (1, extports + 1):   
                    pskey = leafguid + ":" + str (b + leafp)
                    pskey2 = dguid + ":" + str (dirport)
                    if pskey in portSpeed:
                        #print ("Existing key: ", pskey, "  New dir key: ", pskey2)
                        portSpeed [pskey2] = portSpeed [pskey]
                        #print ("portSpeed[", pskey2, "]", portSpeed[pskey2])
                    #else:
                        #print ("Key not found in portSpeed: ", pskey)
                    dirport = dirport + 1
            else:
                dirport = dirport + extports    # Skip Dir ports resulting from empty Leaf slot
#### end of addDirsToPortSpeed ####

#####################################################################################
#### Begin routines to derive inter-switch link (ISL) meta-information from the ibNet data.
#####################################################################################

# Needs to be called before any post-processing is done on ibNet, e.g. Director discovery.
#
# Looks at every Switch node in ibNet, and builds a data structure, islDict,
# representing all the inter-Switch links (ISLs) in ibNet for later analysis.
# In this context, "Switch" means "switch ASIC".
#
# islDict is a dictionary indexed by Node GUID strings.  There is an entry 
# for each Switch (ASIC) from ibNet.  Each entry A in turn is a sub-dictionary
# indexed by Node GUIDs and represents the Switches adjacent to Switch A.
#
# Each of these 'neighbor' sub-dictionary entries N contains a list of port
# numbers on Switch A that connect to a neighboring Switch N.  
# The port list is in ascending order and each port number is an integer (not
# a string).  So, each sub-dictionary entry represents one or more parallec 
# links connecting Switch A to an adjacent Switch N, as viewed from Switch A.
#
# Also look for HCAs that are referenced but never defined, and generate dummy
# HCAs so analysis can proceed.
#
# Note: it would be nice (consistent) to make the port numbers strings instead
# of integers... Also, it would be good to use the peerExists routine.
#
def buildISLDictionary ():
    global islDict
    global ibNet
    global missingHCAs    ####
    global wf
    #
    missingHCAs = []    # In case we find HCAs that are referenced but never defined
    for i, guid in enumerate (ibNet):
        node  = ibNet [guid]    # Get Node structure for this Node
        if node.nodeType == "S":   # If this Node is a Switch
            #print("Build ISLs for Switch ", guid)
            peerGUIDDict = {}    # Start a new sub-dictionary for this Switch   
            pc = int (node.nodePortCount)    # Get number of Switch ports
            for p in range (1, pc+1):    # Loop through all ports ignoring Port 0
                port = node.nodePortList [p]    # Get Port structure for this port
                if port.portType == "IB" and port.portConnected == "Y":
                    link = port.portLink    # Get Link structure for this port
                    if link.peerType == "S":    # We only care about links to other Switches
                        peerGUID = link.peerNodeGUID
                        #print ("   Peer: ",peerGUID)
                        if not (peerGUID in peerGUIDDict):
                            peerGUIDDict [peerGUID] = []    # Create dict entry with empty port list
                        l = peerGUIDDict [peerGUID]
                        l = l + [p]    # Add current port # to list associated with this peer Switch
                        peerGUIDDict [peerGUID] = l.copy()   # Update dictionary entry
                    else:    # Peer is an HCA; do some consistency checking.  We will build 'fakes' for missing HCAs
                        peerGUID = link.peerNodeGUID
                        if not (peerGUID in ibNet):    # HCA was referenced but never defined in ibnetdiscover
                            hcaNode = defaultNode    # Build a dummy HCA node containing the least possible info
                            hcaNode = hcaNode._replace (nodeType = "H")
                            hcaNode = hcaNode._replace (nodeGUID = peerGUID)
                            hcaNode = hcaNode._replace (nodeDesc= "Dummy generated by Tarzan")
                            hcaNode = hcaNode._replace (nodePortCount = "1")    # Later we can deal with 2 ports if needed
                            missingHCAs.append (hcaNode)                
            islDict [guid] = peerGUIDDict.copy()    # Enter Switch in islDict with its sub-dict
    if len(missingHCAs) != 0:
        warnSection ("############## Found HCAs that were referenced but never defined (e.g. due to a truncated ibnetdiscover file)")
        warn ("Dummy HCA nodes have been generated so analysis can proceed (" + str(len(missingHCAs)) + "):")
        #print ("#### ERROR:  Some HCAs were referenced but never defined in the ibnetdiscover. ####")
        #print ("#### ibnetdiscover file was truncated or corrupted.  missingHCAs list contains HCA info.  ####")
        for i in range(len(missingHCAs)):    # We couldn't add ibNet entries while above loop was running
            hcaNode = missingHCAs[i]
            ibNet [hcaNode.nodeGUID] = hcaNode
            warn ("HCA " + hcaNode.nodeGUID)    # Could later expand this to include Switch GUID & port #
        #print ("#### Dummy HCA nodes have been generated so that analysis can proceed.  ####")

#### end of buildISLDictionary ####

#####################################################################################
#### Begin routines to for assigning colors to nodes.  Used for the .RTF files.
#####################################################################################

#### assignNodeColors ####
def assignNodeColors ():
    global nodeColors
    nodeColors = {noPeer:1, "!":3}    # Unknown GUIDs are Black; empty Ports due to no Leaf Modules are Dark Gray 
    clr = 4     # First 3 colors are reserved (black, white, dark gray)
    #clr = 32    #### DEBUG - TRY HIGHER NUMBERED COLORS ####
    for i, key in enumerate (ibNet):    # Loop through all ASICs in ibNet
        node = ibNet [key]
        if node.nodeType == "S":
            nodeColors [key] = clr
            clr = clr + 1
            if clr > len(nodeRTFStrings)-1:
                clr = 4
        else:
            nodeColors [key] = 2    # Non-switches get colored white
    for i, key in enumerate (allDirectors):    # Loop through all Directors
        nodeColors [key] = clr
        clr = clr + 1
        if clr > len(nodeRTFStrings)-1:
            clr = 4 

#### end of assignNodeColors ####

#####################################################################################
#### Begin helper routines for the newer DIrector detection algorithm, which is table-based.
#####################################################################################

#### addDirectorMap ####
# Helper routine to add a directorMap entry to directorMaps.
# The input string is a compact form of the data that will go into a new
# directorMap structure.

def addDirectorMap (s):
    global directorMaps
    # Handle header here
    newMap = defaultDirectorMap
    a = s.split("!")    # Parse string into sections: header, spine to leaf, leaf to spine
    if not(len(a) == 3):
        print ("addDirectorMap input has wrong # of sections: ", a)
    hdr = a[0].split(",")    # Extract the header fields
    if not(len(hdr) == 8):
        print ("addDirectorMap header has wrong # of fields: ", hdr)
    # Unpack header fields into new Map
    directorModel = hdr [0]
    newMap = newMap._replace (dirModel = directorModel)
    newMap = newMap._replace (dirSpeed = hdr[1])
    newMap = newMap._replace (portsPerASIC = hdr[2])
    newMap = newMap._replace (numOfLeafASICs = hdr[3])
    newMap = newMap._replace (numOfSpineASICs = hdr[4])
    newMap = newMap._replace (dirMaxPorts = hdr[5])
    newMap = newMap._replace (dirLayout = hdr[6])
    newMap = newMap._replace (dirLeafExtPorts = hdr[7])
    #
    asicList = [[],[],[]]
    #print ("asicList ", asicList)
    for j in range (1, 3):    # Process 2 'port to ASIC' input lists
        portToASIC = a[j].split (";")
 
        asics = len (portToASIC)
        if not (asics == int (hdr [j + 2])):
            print ("Wrong number of ASIC entries ", portToASIC)
        for i in range (1, asics + 1):
            asic = portToASIC [i - 1].split (",")
        #    print ("asic ", asic)
            asicList [j] = asicList [j] + [asic]
    newMap = newMap._replace (spinePortToLeafList = asicList [1])
    newMap = newMap._replace (leafPortToSpineList = asicList [2])
    # Create a new entry in the directorMaps dictionary
    directorMaps [directorModel] = newMap

#### end of addDirectorMap ####

#### buildDirectorMaps ####

def buildDirectorMaps ():
    global directorMaps
    global deviceIDsofMappedDirectors
    directorMaps = {}
    deviceIDsofMappedDirectors = {"cb20","cf08", "d2f0"}    # EDR: SwitchIB-1, SwitchIB-2; HDR: Quantum
# CS7520.  Layout and Ext Port count are temporary  ######## FIX ME: PUT IN CORRECT VALUES ####
    s = "CS7520,EDR,37,12,6,216,9x2,18!" \
        "L01/U1,1,13,25;L01/U2,2,14,26;L02/U1,3,15,27;L02/U2,4,16,28;L03/U1,5,17,29;L03/U2,6,18,30;" \
        "L04/U1,7,19,31;L04/U2,8,20,32;L05/U1,9,21,33;L05/U2,10,22,34;L06/U1,11,23,35;L06/U2,12,24,36!" \
        "S01/U1,24,30,36;S02/U1,23,29,35;S03/U1,22,28,34;S04/U1,21,27,33;S05/U1,20,26,32;S06/U1,19,25,31"
    addDirectorMap (s)
# CS7510.  Layout and Ext Port count are temporary  ######## FIX ME: PUT IN CORRECT VALUES ####
    s = "CS7510,EDR,37,18,9,324,9x2,18!" \
        "L01/U1,1,3;L01/U2,2,4;L02/U1,5,7;L02/U2,6,8;L03/U1,9,11;L03/U2,10,12;" \
        "L04/U1,13,15;L04/U2,14,16;L05/U1,17,19;L05/U2,18,20;L06/U1,21,23;L06/U2,22,24;" \
        "L07/U1,25,27;L07/U2,26,28;L08/U1,29,31;L08/U2,30,32;L09/U1,33,35;L09/U2,34,36!" \
        "S01/U1,23,24;S02/U1,21,22;S03/U1,19,20;S04/U1,29,30;S05/U1,27,28;S06/U1,25,26;" \
        "S07/U1,35,36;S08/U1,33,34;S09/U1,31,32"
    addDirectorMap (s)
# CS7500.  Layout and Ext Port count are temporary  ######## FIX ME: PUT IN CORRECT VALUES ####
    s = "CS7500,EDR,37,36,18,648,9x2,18!" \
        "L01/U1,1;L01/U2,2;L02/U1,3;L02/U2,4;L03/U1,5;L03/U2,6;L04/U1,7;L04/U2,8;L05/U1,9;" \
        "L05/U2,10;L06/U1,11;L06/U2,12;L07/U1,13;L07/U2,14;L08/U1,15;L08/U2,16;L09/U1,17;L09/U2,18;" \
        "L10/U1,19;L10/U2,20;L11/U1,21;L11/U2,22;L12/U1,23;L12/U2,24;L13/U1,25;L13/U2,26;L14/U1,27;" \
        "L14/U2,28;L15/U1,29;L15/U2,30;L16/U1,31;L16/U2,32;L17/U1,33;L17/U2,34;L18/U1,35;L18/U2,36!" \
        "S01/U1,24;S02/U1,23;S03/U1,22;S04/U1,21;S05/U1,20;S06/U1,19;S07/U1,30;S08/U1,29;S09/U1,28;" \
        "S10/U1,27;S11/U1,26;S12/U1,25;S13/U1,36;S14/U1,35;S15/U1,34;S16/U1,33;S17/U1,32;S18/U1,31"
    addDirectorMap (s)
# CS8500.  Layout and Ext Port count are temporary  ######## FIX ME: PUT IN CORRECT VALUES ####
# All Spine-Leaf connections are HDR; Leaf ASIC external ports can be any mix of HDR and HDR100.  
#### NEED TO ENSURE WE CAN HANDLE SPLIT LEAFS DURING DIRECTOR DISCOVERY  ####
    s = "MCS8500,HDR,41,40,20,800,10x2,20!" \
        "L01/U1,1;L01/U2,21;L02/U1,2;L02/U2,22;L03/U1,3;L03/U2,23;L04/U1,4;L04/U2,24;L05/U1,5;" \
        "L05/U2,25;L06/U1,6;L06/U2,26;L07/U1,7;L07/U2,27;L08/U1,8;L08/U2,28;L09/U1,9;L09/U2,29;" \
        "L10/U1,10;L10/U2,30;L11/U1,11;L11/U2,31;L12/U1,12;L12/U2,32;L13/U1,13;L13/U2,33;L14/U1,14;" \
        "L14/U2,34;L15/U1,15;L15/U2,35;L16/U1,16;L16/U2,36;L17/U1,17;L17/U2,37;L18/U1,18;L18/U2,38;" \
        "L19/U1,19;L19U2,39;L20/U1,20;L20/U2,40!"\
        "S01/U1,21;S02/U1,22;S03/U1,23;S04/U1,24;S05/U1,25;S06/U1,26;S07/U1,27;S08/U1,28;S09/U1,29;" \
        "S10/U1,30;S11/U1,31;S12/U1,32;S13/U1,33;S14/U1,34;S15/U1,35;S16/U1,36;S17/U1,37;S18/U1,38;"\
        "S19/U1,39;S20/U1,40"
    addDirectorMap (s)
#### end of buildDirectorMaps ####

#####################################################################################
#### Begin routines to assist Director detection.
#####################################################################################

#### countLeafsAndSpines ####
def countLeafsAndSpines():
    global ibNet
    leafDevices = {}
    spineDevices = {}
    for i, key in enumerate (ibNet):    # Loop through all of the ASICs in ibNet
        currentNode = ibNet [key]
        id = currentNode.deviceID
        if id in leafDeviceIDs:    # Is the device ID a known leaf ID?
            if id not in leafDevices:
                leafDevices [id] = 1    # First time weve seen this leaf ID
            else:
                leafDevices [id] = leafDevices [id] + 1    # Else count this one
        elif id in spineDeviceIDs:    # NEED TO REWRITE THIS TO USE isSpine()
            if id not in spineDevices:
                spineDevices [id] = 1    # First time weve seen this spine ID
            else:
                spineDevices [id] = spineDevices [id] + 1
    for i, key in enumerate (leafDevices):
        print ("leaf device ID ", key, " occurs ", leafDevices [key], " times")
    for i, key in enumerate (spineDevices):
        print ("spine device ID ", key, " occurs ", spineDevices [key], " times")
#### end of countLeafsAndSpines ####

#### isSpine ####
# Parameter is the Node structure of a Switch ASIC.  This routine looks at the Device ID, Node
# Description, and other clues to determine whether the ASIC is in the spine of a Director.
def isSpine ( node ):
    global spineGUIDs    # Allows user to explicitly tell us which GUIDs are Spines
    devID = node.deviceID
    itsASpine = False
    if devID in spineDeviceIDs:
        itsASpine = True
    
    elif node.nodeGUID in spineGUIDs:
        itsASpine = True
        
    elif devID == "7320":    # If this is a Qlogic QDR switch node
        desc = node.nodeDesc
        parts = desc.rpartition ("\"")    # Find the trailing quote in the Node Description
        if len(parts[0]) > 4:    # Make sure remaining Node Description is long enough 
            if parts[0][-5:] in qlogicSpineNames:    # E.g. "S111A"
                itsASpine = True
    elif devID in ["bd36", "c738", "cb20", "cf08", "d2f0"]:    # If it's a MLNX QDR, FDR, EDR, HDR switch node
        desc = node.nodeDesc    # For MLNX Directors, we also need to inspectt the Node Description
        #print("node desc=",desc)
        parts = desc.rpartition ("\"")    # Find the trailing quote in the Node Description (rewrite to use regex?)
        #print(parts[0])
        parts = parts [0].rpartition ("/")    # Find slash "/" preceding trailing quote (spine descs end in "/U1")
        #print(parts[0])
        if len(parts[0]) > 2:    # Make sure remaining Node Description is long enough
            #print(parts[0][-3:])
            if parts[0][-3:] in mlnxSpineNames:    # E.g. if it's "S11" 
                itsASpine = True
    return (itsASpine)
#### end of isSpine ####

#### setDirNameAndSysImgGUID ####
# This routine looks at a Director's ASICs and extracts its user-assigned name.  It also gets the
# System Image GUID.  Because a Director contains many ASICs, it's possible that the
# user-assigned name and/or the System Image GUID won't be consistent due to user error,
# software error, factory error, module replacement, etc. so we generate warnings for these.
# Assumes currentDirector points to the Director data structure.  
# Call this routine after the more basic Director attributes have been set, e.g. the model.
def setDirNameAndSysImgGUID ():
    global currentDirector
    global ibNet
    global wf 
    dir = currentDirector    # Shorter name, for convenience
    # Set a flag if it's MLNX FDR, EDR, HDR  (should probably also add VOLT)
    lookForName = dir.directorSpineDeviceID in ["c738", "cb20", "cf08", "d2f0"]
    #print ("directorSpineDeviceID: ", dir.directorSpineDeviceID)    
    dName = {}    # Create a dictionary of user-defined names we see (should only be 1)
    siGUID = {}    # Create a dictionary of System Image GUIDs we see (should only be 1)
    gList = dir.directorSpineGUIDList + dir.directorLeafGUIDList    # All ASIC slots
    #print ("gList: ", gList)    
    while " " in gList: gList.remove(" ")    # Omit empty slots, plus the unused entry that begins each GUID list
    #print ("new gList: ", gList)         
    for i in range (0, len(gList)):    # Look at every non-empty ASIC slot, Spines and then Leafs
        node = ibNet [gList [i]]    # Use GUID to get Node structure
        sig = node.sysimgGUID
        #print ("i: ", i, " gList[i]: ", gList[i], " sys img GUID: ", sig, " dName: ", dName)    
        while not (sig in siGUID):  siGUID [sig] = 0
        siGUID [sig] = siGUID [sig] + 1    # Count how many times we see this Sys Img GUID
        if lookForName:
            desc = node.nodeDesc    #    Get Node Description of this ASIC
            n = "<none>"
            m = re.search (";[-a-zA-Z0-9 ]*:", desc)    # Look for string delimited by ";" and ":"; allow "-" and " "
            if m:       
                n = desc[m.start()+1:m.end()-1]    # Get the text minus the delimiters
            else:
                mm = re.search(r'"(.*?)"', desc)    # Look for quoted string-- ? makes * operator lazy/non-greedy
                if mm:
                    n = desc[mm.start():mm.end()]    # Get the text + quotes (in case string is empty)
            #print ("Director ASIC: ", node.nodeGUID, " Director Name = ", n)       
            while not (n in dName):  dName [n] = 0
            dName [n] = dName [n] + 1    # Count how many times we see this (supposed) name
    # Now see what we found
    warnSection ("#################### Check Director ASIC Names and System Image GUIDs #################### ")
    #print ("siGUID: ", siGUID)    
    sgl = sorted ([[k,v] for [v,k] in siGUID.items()], reverse=True)    # Convert to list of 2-tuples sorted by count (descending)
    #print ("sgl: ", sgl)
    dirSysImgGUID = sgl[0][1]    # Pick the most popular sys img GUID seen (2-tuples are [value, key])
    if len(siGUID) > 1:    # We saw multiple System Image GUIDs (!)
        warn ("ASICs in Director "+ dir.directorNodeGUID +" have multiple System Image GUIDs: " + ", ".join(list(siGUID)))
    #currentDirector = currentDirector._replace (directorSysImgGUID = dirSysImgGUID)    ##### IMPLEMENT ATTRIBUTE ####
    if lookForName:
        nl = sorted ([[k,v] for [v,k] in dName.items()], reverse=True)    # Convert to list of 2-tuples sorted by count (descending)
        #print ("nl: ", nl)
        dirName = nl [0][1]    # Pick the most popular name seen (2-tuples are [value, key])
        if dirName == "<none> ":    # We never recognized a name
            warn ("ASICs in Director "+ dir.directorNodeGUID + " have no recognizable names")
        elif len (dName) > 1:    # We found multiple names (!)
            warn ("ASICs in Director "+ dir.directorNodeGUID + " have multiple names: " + ", ".join(list(dName)))            
        currentDirector = currentDirector._replace (directorDesc = dirName) 

#### end of setDirNameAndSysImgGUID ####

#### setDirectorAttributes ####
def setDirectorAttributes ():
    global currentDirector
    global ibNet
    global wf
    sID = currentDirector.directorSpineDeviceID
    vID = currentDirector.directorVendorID
    lbp = currentDirector.directorLeafExtPorts
    ports = currentDirector.directorMaxPorts               
    #
    if sID == "5a5c":    # Voltaire GD4700
        model = "GD4700"
        speed = "QDR"
        layout = "18x1"    # Leaf Board has 1 row of 18 ports
    elif sID == "5a5d":    # Voltaire GD4700 with double-density Fabric boards
        model = "GD4700 Hyper"
        speed = "QDR"
        layout = "18x1"    # Leaf Board has 1 row of 18 ports
    elif sID == "5a37":    # Voltaire ISR2012
        model = "ISR2012"
        speed = "DDR"
        layout = "12x2"    # Leaf Board has 2 rows of 12 ports (2 ASICs)
    elif sID == "c738":    # SwitchX-based Director
        speed = "FDR"    # What about the FDR10 version?
        layout = "9x2"    # Leaf Board has two rows of 9 ports
        if ports == "108":
            model = "SX6506"
        elif ports == "216":
            model = "SX6512"
        elif ports == "324":
            model = "SX6518"
        else:
            model = "SX6536"
    elif sID == "cb20":    # SwitchIB-based Director
        speed = "EDR"
        layout = "9x2"    #### FIX ME-- EDR Leaf Boards actually have dual ASICs  ##############
        if ports == "216":
            model = "CS7520"
        elif ports == "324":
            model = "CS7510"
        else:
            model = "CS7500"
    elif sID == "d2f0":    # Quantum-based Director
        speed = "HDR"
        layout = "10x2"    # Analogous to HDR - 2 ASICs per Leaf module -- but 10x ports per half row
        if ports == 800:
            model = "CS8500"
        else:
            model = "CS85xx"
    elif sID ==  "ffff":    # InfiniScale IV-based director - CHANGE TO CORRECT SPINE ID###########
        speed = "QDR"
        layout = "9x2"    # Leaf Board has two rows of 9 ports 
        if ports == "108":
            model = "IS5100"
        elif ports == "216":
            model = "IS5200"
        elif ports == "324":
            model = "IS5300"
        else:
            model = "IS5600"
    elif sID == "7320":    #Qlogic QDR Director
        speed = "QDR"
        layout = "9x2"    # Leaf Board has 2 rows of 9 ports
        model = "12800-xxx"
        if ports == "72":
            model = "12800-040"
        elif ports == "216":
            model = "12800-120"
        elif ports == "324":
            model = "12800-180"
        elif ports == "648":
            model = "12800-360"
    else:
        model = "Unknown (" + sID +")"
        speed = " "
        if lbp == "12":
            layout = "12x2"
        else:
            layout = "18x1"    # Assume18 ports per leaf board
    currentDirector = currentDirector._replace (directorModel = model)
    currentDirector = currentDirector._replace (directorSpeed = speed) 
    currentDirector = currentDirector._replace (directorLayout = layout)
    # Now set the IBGen attribute for every ASIC in this Director
    print ("SET ATTRIBUTES FOR :", currentDirector.directorNodeGUID)    #### DEBUG ####
    guidlist = currentDirector.directorSpineGUIDList + currentDirector.directorLeafGUIDList
    while " " in guidlist: guidlist.remove (" ")    # Squeeze out entries representing empty slots
    print ("GUIDLIST: ", guidlist)    #### DEBUG ####
    for i in range (0, len(guidlist)):
        g = guidlist[i]
        ##asicnode = ibNet [guidlist[i]]
        ibNet [g] = ibNet [g]._replace (nodeIBGen = speed)
        #print ("GUID: ", i, g, ibNet[g].nodeIBGen)    #### DEBUG ####

#### end of setDirectorAttributes ####

#####################################################################################
#### Begin routines to detect ASICs that belong to the same Director chassis, and build a Director structure.
#####################################################################################

#### processDirector ####
# Assumes currentNode points to a Spine (Switch) module found in ibNet.
# Discovers the associated Spine and Leaf modules, then builds a pseudo-ASIC that
# looks like a Switch ASIC with a large number of ports that represents the Director if it were
# fully populated with Leafs and Spines.  
#
def processDirector():
    global currentNode
    global currentDirector
    global allDirectors
    seedDevID = currentNode.deviceID    # Remember device ID of Seed spine Switch
    #print ("========================")
    #print ("Seed Spine: ", currentNode.nodeGUID)
    currentDirector = defaultDirector    # Initialize a data structure to represent this new Director
    currentDirector = currentDirector._replace (directorSpineDeviceID = currentNode.deviceID)
# Create a pseudo Node GUID for this Director
    i = len (allDirectors) + 1
    dGUID = "D" + str (i)  
    currentDirector = currentDirector._replace (directorNodeGUID = dGUID)
#
    currentNode = currentNode._replace (nodeDirectorGUID = dGUID)    # Link seed Spine to Dir
    sp = int (currentNode.nodePortCount)    # Get the number of ports of the Directors ASICs
    ep = int (sp / 2)    # Number of external ports per Leaf board
    currentDirector = currentDirector._replace (directorLeafExtPorts = str (ep))    # Ext ports per
    # Leaf board (except for QLogics 2:1 leaf module) 
    currentDirector = currentDirector._replace (directorVendorID = currentNode.vendorID)
    leafGUIDList = [" "] * (sp + 1)    # Start list for Node GUIDs of the Spines neighbors + unused entry 0
    portList = currentNode.nodePortList
    # Examine what is connected to each IB port of this Spine ASIC.  Normally there will only be open ports
    # (indicating non-installed Leaf boards) or Leaf Boards-- no HCAs and no other Spines. 
    # However, a Spine ASIC on a Voltaire GD4700 with double-density (Hyperscale) Fabric Boards can also
    # be connected to other Spines (e.g. two 4700s back-to-back), external Switches, or even HCAs (unlikely).
    # The Hyperscale ASIC device ID is '5a5d' and the leaf board ASIC is '5a5b'.
    j = 0
    for i in range (1, sp + 1):    # Look at everything connected to this Spine should all be Leaf boards
        currentPort = portList [i]    # Look at the seed Spines next Port
        if currentPort.portType == "IB" and currentPort.portConnected == "Y":
            currentLink = currentPort.portLink    # Get the info for this Ports link
            peerGUID = currentLink.peerNodeGUID    # Assume its a Leaf board; really should verify
            #print ("leaf: ", peerGUID)    
            peerNode = ibNet [peerGUID]    # Get Node structure for peer Node
            if (not (seedDevID=="5a5d")) or (peerNode.deviceID=="5a5b"):    #Skip if Hyperscale Spine but peer <> 4700 Leaf
                leafGUIDList [i] = peerGUID   # Put it in our list, associated w. Spine port it connects to
                leafNode = ibNet [peerGUID]
                ibNet [peerGUID] = leafNode._replace (nodeDirectorGUID = dGUID)    # Link LB to this Director
                lastLeafNode = leafNode    # Remember the last Leaf board we saw
    #print ("leafGUIDList: ", leafGUIDList)
    #
    # Now we have a list (which may contain duplicates) of the Node GUIDs of all Leaf boards installed
    # in this Director (unless all of the internal links from the seed Spine to an installed Leaf are broken).
    # Now we use one of the discovered Leaf boards to find the rest of the installed Spines.
    spineGUIDList = [" "] * (sp + 1)    # Start list for Node GUIDs of the Leafs neighbors+ unused entry 0
    portList = lastLeafNode.nodePortList    # Arbitrarily use the last Leaf Board we saw
    for i in range (1, sp + 1):    # Look at everything connected to this Leaf board
        currentPort = portList [i]    # Look at the seed Leafs next Port
        if currentPort.portType == "IB" and currentPort.portConnected == "Y":
            currentLink = currentPort.portLink    # Get the info for this Ports link
            peerGUID = currentLink.peerNodeGUID    # Not all Leaf neighbors must be Spines
            if isSpine (ibNet [peerGUID]):
                #print ("spine: ", peerGUID)
                spineGUIDList [i] = peerGUID   # Put it in our list, associated with the Leaf port it connects to
                spineNode = ibNet [peerGUID]
                ibNet [peerGUID] = spineNode._replace (nodeDirectorGUID = dGUID) # Link Spine to Dir
    #print ("spineGUIDList = ", spineGUIDList)
    #
    # Now we also have a list of the Node GUIDs of all Spine boards installed in this Director.  Next we
    # figure out this Directors internal topology so we know its max number of Spines, Leafs, and
    # external ports when fully populated.  We assume its non-blocking, although this isnt always true,
    # e.g. for the Voltaire GD4200, or for the QLogic directors that support a 2:1 leaf board.
    # We also assume a very regular internal connection scheme, where port number N on every Spine
    # connects to the same Leaf board.  We further assume that Spines 1 to N are connected in 
    # sequence to Leaf boards ports 1 to N, and that Leaf Boards 1 to M are connected in sequence to
    # Spine board ports 1 to M.
    linksPerLeaf = leafGUIDList.count (leafNode.nodeGUID)    # How often 1 Leaf brd links to 1 Spine
    print ("links per leaf: ", linksPerLeaf)
    mp = int ((sp * sp) / 2)    # The max ports in the largest 1:1 Director buildable with this switch ASIC
    #print ("mp ", mp)
    dp = int (mp / linksPerLeaf)    # Compute the maximum port count for this *particular* director model
    maxSpines = int (dp / sp)    # Max number of Spine slots in this Director
    maxLeafs = int (maxSpines * 2)    # Max number of Leaf slots in this Director
    if seedDevID == '5a5d':    # It's a Hyperscale GD4700 (assume all spine boards are double-density)
        dp = 324
        maxSpines = 9
        maxLeafs = 18
    #print ("dp ", dp)
    #print (maxSpines, maxLeafs)
    #
    #  Both the leafList & spineList should now have the same properties:  walking down the list from
    # index 1, there should be tuples of length linksPerLeaf in which all entries have the same value.  
    # This value will either be blank (corresponding to a depopulated module) or the Node GUID 
    # of a module.  If there are broken internal links, there may even be blanks within a non-blank tuple.  
    # Our objective now is to compact each tuple to length 1- either a blank or a Node GUID-
    # so that each list essentially maps Node GUIDs to module slots in this Director.
    # NOTE: it would be easy to check for cases where linksPerLeaf > 1 and the actual number of
    # links found is less than this due to malfunctioning internal links.
    i = 1
    k = 1
    while i < sp +1:   # Compact Leaf GUID & Spine GUID lists (Spine list will become the shorter list)
        j = i + linksPerLeaf    # Index of the end of the next tuple in both lists
        print (i, j)
        t = leafGUIDList [i: j]    # Get the next Leaf board tuple
        #print ("leaf tuple: ", t)
        leafGUIDList [k] = max (t)    # Will pick a non-blank entry (hope all non-blank entries are the same)
        t = spineGUIDList [i : j]    # Get the next Spine board tuple
        #print ("spine tuple: ", t, " k: ", k, " max(t) = ", max(t))
        spineGUIDList [k] = max (t)
        k = k + 1
        i = j    
    leafGUIDList = leafGUIDList [0 : maxLeafs + 1]    # Truncate to 1 entry per Leaf (plus entry 0)
    j = 1
    # Some Directors are internally wired with the lower-number Leaf ports connected to the Spines.  Others
    # are wrired with the higher-numbered Leaf ports connected to the Spines.  Still other schemes are
    # possible but we don't yet deal with them here.
    fep = ep + 1    # First external port number
    if seedDevID in ["7320", "bd36", "c738", "cb20"]:    # If QLGC or MLNX Director, take 2nd half of Spine GUID list
        j = j + maxSpines    # These directors are wired differently than VOLT
        fep = 1
    spineGUIDList = [" "] + spineGUIDList [j : j + maxSpines]    # Truncate to 1 entry per Spine (+ entry 0)
    # print ("leafGUIDList:", leafGUIDList)
    print ("spineGUIDList: ", spineGUIDList)
    # Continue filling in the Director object.
    currentDirector = currentDirector._replace (directorMaxPorts = str (dp))
    currentDirector = currentDirector._replace (directorLeafGUIDList = leafGUIDList)
    currentDirector = currentDirector._replace (directorSpineGUIDList = spineGUIDList)
    #
    # Set the slot names for the Spine nodes.    Slot numbers begin at 1.
    for i in range (1, len(spineGUIDList)):
        if not (spineGUIDList [i] == " "):    # If there's a node in this slot
            currentSpine = ibNet [spineGUIDList [i]]    # Get its Node structure
            currentSpine = currentSpine._replace (nodeSlotName = "S" + str (i))    # Slot name
            ibNet [spineGUIDList [i]] = currentSpine    # Update the Node entry
    # Now build a list of all the peer nodes this Director could have if fully populated, then go through
    # the list of installed Leaf boards and record the peer node connected to each Port (if any)
    peerList = [defaultPeer] * (dp + 1)    # Build empty list of all poss. ports (peers) + unused entry 0
    i = 1    # Index into peerList where we will store the Node GUID of the next peer node
    for j in range(1, len (leafGUIDList)):    # Loop through all Leaf board slots
        # print ("leaf slot ", j, " is ", leafGUIDList [j])
        if leafGUIDList [j] == " ":    # If blank, this is a Leaf board slot with no Leaf board installed
            i = i + ep    # All corresponding port/peer entries for the absent Leaf board = default
        else:
            currentLeaf = ibNet [leafGUIDList [j]]   # Get the Node structure for this Leaf ASIC
            currentLeaf = currentLeaf._replace (nodeSlotName = "L" + str (j))    # Build its slot name
            ibNet [leafGUIDList [j]] = currentLeaf    # Update Node entry
            portList2 = currentLeaf.nodePortList
            for k in range (fep, fep + ep):    # Loop through the external ports on this Leaf ASIC
                currentPeer = defaultPeer
                currentPort = portList2 [k]    # Get the Port structure
                if currentPort.portType == "IB" and currentPort.portConnected == "Y":
                    currentLink = currentPort.portLink    # Get the Link structure
                    # Should fill in *all* of the Peer structure fields here, but for now
                    currentPeer = currentPeer._replace (peerNodeGUID = currentLink.peerNodeGUID)
                    currentPeer = currentPeer._replace (peerNodeType = currentLink.peerType)
                    currentPeer = currentPeer._replace (peerPortNum = currentLink.toPortNum)
                    currentPeer = currentPeer._replace (peerLID = currentLink.peerLID)
                    currentPeer = currentPeer._replace (peerLinkType = currentLink.linkWidthXRate)
                    peerList [i] = currentPeer    # Update the Peer list entry for this external port
                    # print ("peer [", i, "]: ", currentPeer) 
                i = i + 1
    currentDirector = currentDirector._replace (directorPeerList = peerList)
    setDirectorAttributes()
    setDirNameAndSysImgGUID()
    #
    allDirectors [dGUID] = currentDirector    # Put it in the dictionary of Directors

#### end of processDirector ####

#### getDirectorMap ####
# The Node structure parameter has already been identified as a Spine ASIC belonging to a Director
# switch product that has a matching directorMap structure.  Here we figure out exactly which
# directorMap that is.
# Note: it might be better to have the isSpine function set a global variable to the DIrector product
# model since it needs to do most of the work anyway.  It would obviate the need for this routine.
def getDirectorMap (nodeStruct):
    global directorMaps
    # Look at the node's Node Description attribute.


    nd = nodeStruct.nodeDesc
    dMap = " "
    for i, key in enumerate (directorMaps):   # Iterate through the dictionary of maps
        if key in nd:    # This check allows the Director model name to be anywhere in the Desc
        #    print ("getDirectorMap found this Key: ", key, " #######")    ########### TESTING ##########
            dMap = directorMaps [key]         
        elif not(nd.find(":"+key+"/S")==-1):    # The dictionary key is the Director product model (char string)
        #    print ("getDirectorMap found this Key: ", key, " #######")    ########### TESTING ##########
            dMap = directorMaps [key]  
    
    return (dMap)

#### end of getDirectorMap ####

#### processDirector2 ####  
#
# This code was superceded by processDirector3, and omitted in August 2022.
#
#### end of processDirector2 ####

#### processDirector3 ####  
# Even newer approach to finding the components of a Director switch, that is more
# robust in the presence of missing midplane links.
# Assumes currentNode points to a Spine (Switch) node found in ibNet.
# dMap is the directorMap entry deduced by the caller by examining the Spine node.
# Finds all the associated Spine and Leaf modules, then builds a pseudo- ASIC that
# looks like a giant single Switch ASIC with a large number of ports.  
# E.g. a 324-port Director resembles a Switch ASIC with 324 ports.
#
def processDirector3 (dMap):
    global ibNet
    global currentNode
    global currentDirector
    global allDirectors
    peerNodeGUID = [noPeer]    # For use by the peerExists routine
    peerLink = [" "]    # For use by the peerExists routine
    seedSpineGUID = currentNode.nodeGUID
    #print ("HOHOHOHOHOHOHOHOHOHOHOHO")
    #print ("Seed Spine: ", currentNode.nodeGUID)
    #print ("dMap: ", dMap)
    currentDirector = defaultDirector    # Initialize a data structure to represent this new Director
    # Fill in some Director attributes based on the Spine ASIC and the Director Map
    currentDirector = currentDirector._replace (directorSpineDeviceID = currentNode.deviceID)
    currentDirector = currentDirector._replace (directorVendorID = currentNode.vendorID)
    currentDirector = currentDirector._replace (directorSpeed = dMap.dirSpeed)
    currentDirector = currentDirector._replace (directorModel = dMap.dirModel)
    currentDirector = currentDirector._replace (directorMaxPorts = dMap.dirMaxPorts)
    currentDirector = currentDirector._replace (directorLayout = dMap.dirLayout)
    currentDirector = currentDirector._replace (directorLeafExtPorts = dMap.dirLeafExtPorts)
    # Create a pseudo Node GUID for this Director
    i = len (allDirectors) + 1
    dGUID = "D" + str (i)  
    currentDirector = currentDirector._replace (directorNodeGUID = dGUID)
    # We know one of the Spine GUIDs (the Seed).  From that we can find all of the 
    # Leaf ASIC Nodes, using the spinePortToLeafList in the Directory Map, and build
    # a leafGUIDList.  A blank (" ") entry in the list means no Leaf ASIC is in that slot.
    # To deal with the possibility that the seed Spine's links are broken to one or more Leafs, we
    # iterate:  find Leafs from Spines, then use the Leafs to find more Spines (if any), until no more
    # Spine or Leaf ASICs are found.
    # Initialize some more stuff
    spinePortToLeafList = [" "] + dMap.spinePortToLeafList    # Add entry 0 so we can index by slot #
    leafPortToSpineList = [" "] + dMap.leafPortToSpineList    # Add entry 0 so we can index by slot #
    nss = int (dMap.numOfSpineASICs)    # Number of Spine ASIC slots in this Director model
    nls = int (dMap.numOfLeafASICs)    # Number of Leaf ASIC slots in this Director model
    spineGUIDList = [" "] * (nss + 1)    # Start a list for Spine ASIC GUIDs (plus an unused entry 0)
    leafGUIDList = [" "] * (nls + 1)    # Start a list for Leaf ASIC GUIDs (plus an unused entry 0)
    newSpineGUIDs = [seedSpineGUID]
    # The iteration loop starts here ###########################
    while len(newSpineGUIDs) > 0:
        #print ("newSpineGUIDs=", newSpineGUIDs)    #
        spineGUID = newSpineGUIDs.pop(0)    # Remove first entry from Spine list FIFO
        #print (dGUID, " looking for leafs of spine ", spineGUID)    #
        newLeafGUIDs = []
        # We have a Spine GUID.  Find all the Leafs it connects to.
        for i in range (1, nls+1):    # Get next entry in spinePortToLeafList, corresponding to Leaf slot i
            spinePortToLeafEntry = spinePortToLeafList [i]    # Each entry is a list: [Slot Name, port, port, port...]
            leafSlotName = spinePortToLeafEntry [0]
            m = len (spinePortToLeafEntry) - 1    # Number of links from a Spine ASIC to this Leaf slot
            #print ("m: ", m, " i: ", i)    #
            for k in range (1, m + 1):    
                p = int (spinePortToLeafEntry [k])    # Get next Spine port # connecting to Leaf slot i
                if peerExists (spineGUID, p, peerNodeGUID, peerLink):
                    peerGUID = peerNodeGUID [0]
                    if leafGUIDList [i] == " ":   
                        #print ("From spine ", spineGUID, "port ", p, " found leaf ", peerGUID)    #
                        newLeafGUIDs = newLeafGUIDs + [peerGUID]   # Append to list of newly found Leaf ASICs                
                        leafGUIDList [i] = peerGUID    # Put the Node GUID in the Leaf list slot; entry 0 is unused
                        ibNet [peerGUID] = ibNet [peerGUID]._replace (nodeDirectorGUID = dGUID)
                        #print (";;;;;;;;;; ", peerGUID, " ", dGUID)    #
                        ibNet [peerGUID] = ibNet [peerGUID]._replace (nodeSlotName = leafSlotName)
                        ibNet [peerGUID] = ibNet [peerGUID]._replace (nodeIBGen = dMap.dirSpeed)
        # Now use each Leaf to find Spines we haven't already seen.  Note that the Seed Spine will be re-discovered.
        while len(newLeafGUIDs) > 0:
            leafGUID = newLeafGUIDs.pop (0)    # Remove first entry from Leaf list FIFO
            # We have a Leaf ASIC GUID.    Find all the Spine ASICs it connects to
            for i in range (1, nss+1):    # Get next entry in leafPortToSpineList, corresponding to Spine slot i
                leafPortToSpineEntry = leafPortToSpineList [i]    # Each entry is a list: [Slot Name, port, port, port...]
                spineSlotName = leafPortToSpineEntry [0]
                m = len (leafPortToSpineEntry) - 1   # Get # of ports linking to Spine slot i
                #print ("m: ", m, " i: ", i) 
                for k in range (1, m + 1):    
                    p = int (leafPortToSpineEntry [k])    # Get next Leaf port # connecting to Spine slot i
                    if peerExists (leafGUID, p, peerNodeGUID, peerLink):
                        peerGUID = peerNodeGUID [0]
                        if spineGUIDList [i] == " ":    # If we haven't seen this Spine ASIC before
                            #print ("From leaf ", leafGUID, "port ", p, " found spine ", peerGUID)    #
                            if peerGUID != seedSpineGUID:    # This will save a bit of redundant re-discovery
                                newSpineGUIDs = newSpineGUIDs + [peerGUID]    # Append to list of newly found Spines
                            spineGUIDList [i] = peerGUID    # Put the Node GUID in the Spine list slot; entry 0 is unused
                            ibNet [peerGUID] = ibNet [peerGUID]._replace (nodeDirectorGUID = dGUID)
                            ibNet [peerGUID] = ibNet [peerGUID]._replace (nodeSlotName = spineSlotName)
                            ibNet [peerGUID] = ibNet [peerGUID]._replace (nodeIBGen = dMap.dirSpeed)  
    # This next stuff goes after the end of the loop 
    #print(dGUID, " spineGUIDList = ", spineGUIDList)    #
    #print(dGUID, " leafGUIDList = ", leafGUIDList)    #
    currentDirector = currentDirector._replace (directorSpineGUIDList = spineGUIDList)
    currentDirector = currentDirector._replace (directorLeafGUIDList = leafGUIDList)   
    # Now loop through all of the Leafs, and for each port on a Leaf ASIC that has an active link
    # to a peer node, create a Peer structure.  The resulting list of Peer structures becomes the
    # peerList attribute of the Director structure.
    nlp = int (dMap.dirLeafExtPorts)    # Number of external ports on a Leaf ASIC
    peerList = [defaultPeer]    # Entry zero in the list (unused)
    for i in range (1, nls + 1):    # For each Leaf slot:
        nextExtPorts = [defaultPeer] * nlp    # Initialize a chunk of places to put Peer structures 
        leafGUID = leafGUIDList [i]
        if leafGUID != " ":    # There's a Leaf ASIC in this position
            for p in range (1, nlp + 1):    # We assume ext ports are numbered from 1 to nlp
                if peerExists (leafGUID, p, peerNodeGUID, peerLink):
                    peerGUID = peerNodeGUID [0]
                    pLink = peerLink [0]
                    currentPeer = defaultPeer
                    # Should fill in *all* of the Peer structure fields here, but for now
                    currentPeer = currentPeer._replace (peerNodeGUID = peerGUID)
                    currentPeer = currentPeer._replace (peerNodeType = pLink.peerType)
                    currentPeer = currentPeer._replace (peerPortNum = pLink.toPortNum)
                    currentPeer = currentPeer._replace (peerLID = pLink.peerLID)
                    currentPeer = currentPeer._replace (peerLinkType = pLink.linkWidthXRate)
                    nextExtPorts [p - 1] = currentPeer    # The chunk indices start at 0
        peerList = peerList + nextExtPorts    # Append this chunk to the peerList
    currentDirector = currentDirector._replace (directorPeerList = peerList)    
    # Finish up.  No need to call setDirectorAttributes since dMap contains the relevant info.
    setDirNameAndSysImgGUID()
    allDirectors [dGUID] = currentDirector    # Put it in the dictionary of Directors


#### end of processDirector3 ####

#### getDirectors ####
# Original algorithm for finding Directors.
# Walks through ibNet and calls processDirector for each Spine Switch it finds.  processDirector
# will use each Spine switch as the basis for collecting the other Spine switches and Leaf switches
# into a Director data structure. During this process, processDirector will set each of a Directors
# switch Nodes nodeDirectorGUID attribute to point to the Director data structure.
def getDirectors():
    global ibNet
    global allDirectors
    global currentNode
    global currentDirector
    allDirectors = {}
    guids = list (ibNet.keys())    # Make a list of all the Node GUIDs in ibNet, instead of a dictionary
    for i in range (len (guids)):
        ng = guids [i]    # Get next Node GUID from list
        currentNode = defaultNode if ng == " " else ibNet [ng]
        #if not ng == " ":
            #currentNode = ibNet [ng]

                                    
        if currentNode.nodeType == "S":    # We only care about Switch nodes
            if isSpine(currentNode):    # processDirector takes a Spine as input
                if currentNode.nodeDirectorGUID == " ":    # processDirector hasnt seen this one yet
                    if currentNode.deviceID in deviceIDsofMappedDirectors:    #  Use processDirector3 for this Director
                    #    print("Node ", ng, " IS IN MAPPED IDs")    ################################## TESTING ##
                        dMap = getDirectorMap (currentNode)    # Figure out which directorMap structure applies
                        processDirector3 (dMap)    # Use the newer mechanism to assemble this Director
                    else:
                        processDirector()    # Collect all info about this Director & build a data structure
            

#### end of getDirectors ####

#####################################################################################
#### Begin routines to generate .RTF report files.
#####################################################################################

#### putCentered ####
# Someday rewrite to take more advantage of string methods...
def putCentered ( string, width ):
    s = string
    w = len (s)
    rw = width - w
    if rw < 0:    # String is too long for the width so take the rightmost characters preceded by "!"
        s = "!" + s [-(width - 1):]
    elif rw > 0:    # String needs padding with blanks to fit the width
        w2 = int (rw  / 2)
        s = (" " * w2) + s + (" " * (rw - w2))
    return (s)

#### end of putCentered ####

#### putIbnetdiscoverNameAndDate ####
def putIbnetdiscoverNameAndDate ():
    global fnameBase
    global genTimeAndDate
    s = "'" + fnameBase + "' dated " + genTimeAndDate
    return (s)
#### end of putIbnetdiscoverNameAndDate ####

#### putPeerTypeAndLinkType ####
# Version for Director ports, as opposed to Switch ports.
# NOTE: this routine doesnt YET allow for the possibility that the peer is also a Director.
def putPeerTypeAndLinkType ( director, extPortNum, width, highlightnum ):
    linkAbbrev = " "
    pnt = " "
    linkOK = True
    p = director.directorPeerList [extPortNum]    # Get Peer structure for selected port
    pg = p.peerNodeGUID    # Get Node GUID of node on other end of link
    if not (pg == " "):
        myRate = director.directorSpeed    # Get string describing Dir. IB speed e.g. "QDR"
        linkWidthXRate = p.peerLinkType    # Link speed reported by ibnetdiscover e.g. "4xQDR"
        linkWidthXRate = linkWidthXRate + "  "    # Pad in case its value is " " (default)
        linkRate = linkWidthXRate [2:]    # Omit the leading width, e.g. "1x" or "4x"
        linkAbbrev = linkWidthXRate [0:3]    # Get the first 3 chars, e.g. "4xQ" (or "   " if default)
        peerRate = ibNet[p.peerNodeGUID].nodeIBGen    # E.g. "FDR"
        pnt = p.peerNodeType
        # The following logic doesnt NOT allow one end of link to be slower technology FIX ME
        if not (linkWidthXRate == " "):    # If we know the link width and speed
            if not (linkWidthXRate [0:2] == "4x"):    # If link width is known but isnt 4x
                linkOK= False
            elif not (myRate == " "):    # If link speed is known and mine is too
                linkOK = not (myRate == linkRate)
            elif not (peerRate == " "):    # If link speed is known and peers is too
                linkOK = not (peerRate == linkRate)
            else:    # Link status is good but we dont know the speed on either end
                linkOK = True    
    s = pnt + ":" + linkAbbrev    # This is the text well output, with ":" in place of " "
    txt = putCentered (s, width)    # Centered text with blank fill
    parts = txt.partition (":")    # Split it at the ":"; well replace the ":" with a blank
    s = nodeRTFStrings[highlightnum][0] + " " + parts [0] + " "    # The portion with the Peer type
    if linkOK:    # If nothing is known to be wrong with the link width or speed
        s = s + parts [2] + nodeRTFStrings[highlightnum][1]   # First 3 chars, e.g. "4xQ", and turn off highlight/pattern
    elif highlightnum == rtfColorIndex["White"]:    # If link is wonky and normal background is White
        s = s + nodeRTFStrings[2][1]    # Turn off current (White) highlight/pattern
        s = s + nodeRTFStrings[rtfColorIndex["Yellow"]][0] + " " + parts [2]
        s = s + nodeRTFStrings[rtfColorIndex["Yellow"]][1]   # Highlight link issue via Yellow background
    else:    # Link is wonky and normal background isn't White
        s = s + nodeRTFStrings[highlightnum][1]    # Turn off current highlight/pattern
        s = s + nodeRTFStrings[rtfColorIndex["White"]][0] + " " + parts [2]
        s = s + nodeRTFStrings[rtfColorIndex["White"]][1]    # Highlight link issue via a White background
    return (s)

#### end of putPeerTypeAndLinkType ####

#### putSwPeerTypeAndLinkType ####
# Version for Switch ports, as opposed to Director ports.
def putSwPeerTypeAndLinkType ( switchNode, portNum, width, highlightnum ):
    global ibNet
    global resolveDirectors
    global currentPeerGUIDs
    global currentLinkWidths
    global portSpeed
    g = switchNode.nodeGUID
    type = " "
    linkAbbrev = " "
    linkOK = True
    p = switchNode.nodePortList [portNum]    # Get peer Port structure
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink    # Get Link structure
        type = l.peerType    # Get node type of peer, e.g. "H" or "S"
        pg = l.peerNodeGUID    # Get Node GUID of peer entity
        psKey = g + ":" + str(portNum)    # Key into portSpeed dictionary
        if psKey in portSpeed:
            linkWidthXRate = portSpeed[psKey][0]    # 1st 2-tuple part is the link width & rate, e.g. "4xEDR"
            linkWidth = linkWidthXRate [0:2]    # Isolate the width, e.g. "4x"
            #linkRate = linkWidthXRate [2:]    # Isolate the rate, e.g. "HDR"
            linkAbbrev = linkWidthXRate [0:3]    # Truncate for display, e.g. "4xE"
            linkOK = portSpeed[psKey][1]    # 2nd 2-tuple part tells us if the link speed is optimal
        peerNode = ibNet [pg]
        currentPeerGUIDs [portNum] = pg    # Part of the HDR split port display mechanism...
        dg = peerNode.nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            type = "D"
            currentPeerGUIDs [portNum] = dg    # Show Director GUID as the peer
        currentLinkWidths [portNum] = linkWidth    # Part of the HDR split port display mechanism.
    s = type + ":" + linkAbbrev    # This is the text well output, with ":" in place of " "
    txt = putCentered (s, width)    # Centered text with blank fill
    parts = txt.partition (":")    # Split it at the ":"; well replace the ":" with a blank
    s = nodeRTFStrings[highlightnum][0] + " " + parts [0] + " "    # The portion with the Peer type
    if linkOK:    # If link width and speed are optimal
        s = s + parts [2] + nodeRTFStrings[highlightnum][1]   # First 3 chars, e.g. "4xQ", and turn off highlight/pattern
    elif highlightnum == rtfColorIndex["White"]:    # If link is wonky and normal background is White
        s = s + nodeRTFStrings[2][1]    # Turn off current (White) highlight/pattern
        s = s + nodeRTFStrings[rtfColorIndex["Yellow"]][0] + " " + parts [2]
        s = s + nodeRTFStrings[rtfColorIndex["Yellow"]][1]   # Highlight link issue via Yellow background
    else:    # Link is wonky and normal background isn't White
        s = s + nodeRTFStrings[highlightnum][1]    # Turn off current highlight/pattern
        s = s + nodeRTFStrings[rtfColorIndex["White"]][0] + " " + parts [2]
        s = s + nodeRTFStrings[rtfColorIndex["White"]][1]    # Highlight link issue via a White background
    return (s)

#### end of putSwPeerTypeAndLinkType ####

#### putPeerNodeGUID #### 
def putPeerNodeGUID ( director, extPortNum, width , highlightnum):
    p = director.directorPeerList [extPortNum]
    s = p.peerNodeGUID [-width:]
    return (nodeRTFStrings[highlightnum][0] + " " + putCentered (s, width) + nodeRTFStrings[highlightnum][1])

#### end of putPeerNodeGUID ####

#### putSwPeerNodeGUID ####
def putSwPeerNodeGUID ( switchNode, portNum, width , highlightnum):
    global resolveDirectors
    g = " " * width
    p = switchNode.nodePortList [portNum]    # Get the Port structure for the specified port
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink
        g = l.peerNodeGUID
        dg = ibNet[g].nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            g = dg
    s = g [-width:]
    return (nodeRTFStrings[highlightnum][0] + " " + putCentered (s, width) + nodeRTFStrings[highlightnum][1])

#### end of putSwPeerNodeGUID ####

#### putPeerLID ####
def putPeerLID ( director, extPortNum, width, highlightnum ):
    p = director.directorPeerList [extPortNum]
    s = p.peerLID
    return (nodeRTFStrings[highlightnum][0] + " " + putCentered (s, width) + nodeRTFStrings[highlightnum][1])

#### end of putPeerLID ####

#### putSwPeerLID ####
def putSwPeerLID ( switchNode, portNum, width, highlightnum ):
    global resolveDirectors
    p = switchNode.nodePortList [portNum]    # Get the Port structure for the specified port
    s = " "
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink
        s = l.peerLID
        pg = l.peerNodeGUID
        dg = ibNet[pg].nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            #print ("PEER IS A DIRECTOR LEAF: ", pg, ibNet[pg].nodeSlotName)
            slotName = ibNet [pg].nodeSlotName.replace("/", "")    # Remove "/" to shorten, e.g. L01/U2->L01U2
            if (not (slotName == " ")) and (len(slotName) <= width):
                s = slotName
    return (nodeRTFStrings[highlightnum][0] + " " + putCentered (s, width) + nodeRTFStrings[highlightnum][1])	
#### end of putSwPeerLID ####

#### putPeerPort ####
def putPeerPort ( director, extPortNum, width, highlightnum ):
    p = director.directorPeerList [extPortNum]
    s = p.peerPortNum
    if not (s == " "):
        s = "p" + s    # For now; later need to convert to "leaf/port format
    return (nodeRTFStrings[highlightnum][0] + " " + putCentered (s, width) + nodeRTFStrings[highlightnum][1])

#### end of putPeerPort ####

#### putSwPeerPort ####
def putSwPeerPort ( switchNode, portNum, width, highlightnum ):
    global resolveDirectors
    p = switchNode.nodePortList [portNum]    # Get the Port structure for the specified port
    s = " "
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink
        s = l.toPortNum    # Port number on peer (character string)
        g = l.peerNodeGUID
        dg = ibNet[g].nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            dir = allDirectors [dg]
            xp = int (dir.directorLeafExtPorts)    # Get # of external ports per Dir. Leaf Board
            pn = int (s)
            if pn > xp:    # Translate Leaf Board ASIC port # to external port #
                s = str (pn - xp)
    if not (s == " "):
        s = "p" + s    # For now; LATER NEED to convert to "leaf/port" format
    return (nodeRTFStrings[highlightnum][0] + " " + putCentered (s, width) + nodeRTFStrings[highlightnum][1])

#### end of putSwPeerPort ####

#### putLeafBoardGUID ####
def putLeafBoardGUID (director, leafBoardNum, width):
    guid = director.directorLeafGUIDList [leafBoardNum]
    if guid == " ":
        guid = "-" * (width - 2)
    s = guid [-(width - 2):]
    return (putCentered (s, width))   

#### end of putLeafBoardGUID ####

#### putLeafBoardLID ####
def putLeafBoardLID ( director, leafBoardNum, width ):
    guid = director.directorLeafGUIDList [leafBoardNum]
    if guid == " ":    # No Leaf Board in this slot
        s = " "
    else:
        node = ibNet [guid]
        s = node.nodePortZeroLID
    return (putCentered (s, width))

#### end of putLeafBoardLID ####

#### putSpineBoardGUIDv1 ####
def putSpineBoardGUIDv1 ( director, spineBoardNum, width ):
    guid = director.directorSpineGUIDList [spineBoardNum]
    if guid == " ":    # No Spine Board in this slot
        guid = "-" * (width - 2)
    s = guid [-(width - 2):]
    return (putCentered (s, width))   

#### end of putSpineBoardGUIDv1 ####

#### putSpineBoardGUIDv2 #### UNDER CONSTRUCTION #####
# Added a check for an HDR Spine that somehow has gotten its ports split, and
# if there are too few midplane links.
# STILL need to verify that all links are the right speed and width. ########
def putSpineBoardGUIDv2 ( director, spineBoardNum, width ):
    global rtfColorIndex
    prefix = ""
    suffix = ""  
    highlightnum = 0    
    guid = director.directorSpineGUIDList [spineBoardNum]
    if guid == " ":    # No Spine Board in this slot
        guid = "-" * (width - 2)
    else:
        if ibNet [guid].nodeSpecialHCAs != "0":
            suffix = "#"    # A virtual HCA is enabled (e.g. SHARP); flag the GUID with a #
        leafList = director.directorLeafGUIDList
        leafSlots = len (leafList) - 1
        installedLeafs = leafSlots - leafList.count (" ") + 1
        pc = int (ibNet [guid].nodePortCount)    # Get number of Spine ASIC ports
        pp = int (pc/2)*2    # Get rid of the odd (virtual) port if there is one
        r = int ((installedLeafs / leafSlots) * pp)    # Compute how many midplane links this Spine ASIC should have
        links = int(ibNet[guid].nodeSwitchLinks)
        if links != r:    # Missing links on the midplane
            highlightnum = rtfColorIndex ["Red"]
            if not noWarn:
                warn ("Spine " + ibNet[guid].nodeSlotName + " " + guid + " is missing " + str (r - links) + " midplane link(s).")
        elif director.directorSpineDeviceID == "d2f0":    # Is Spine an HDR ASIC?
            if pc != 41:    # E.g. if Spine ports somehow got split/splittable
                highlightnum = rtfColorIndex ["Yellow"]
                if not noWarn:
                    warn ("HDR Spine " + ibNet[guid].nodeSlotName + " " + guid + " is in 'split port' mode.")
        if highlightnum > 0: 
            prefix = nodeRTFStrings[highlightnum][0]
            suffix = nodeRTFStrings[highlightnum][1] + suffix
    s = guid [-(width - 2):]    # Take the last N digits of the GUID
    return (prefix + putCentered (s, width) + suffix)   

#### end of putSpineBoardGUIDv2 ####

#### putSpineBoardGUID ####
# Added a check for an HDR Spine that somehow has gotten its ports split, or
# if there are too few midplane links, or if there are degraded links.
def putSpineBoardGUID ( director, spineBoardNum, width, noWarn):
    global rtfColorIndex
    peerGUID = [" "]    # For use by peerNodeExists
    peerLinkStruct = [" "]    # For use by peerNodeExists
    prefix = ""
    suffix = ""  
    highlightnum = 0    
    guid = director.directorSpineGUIDList [spineBoardNum]
    if guid == " ":    # No Spine Board in this slot
        guid = "-" * (width - 2)
    else:
        spineWXR = "4x" + director.directorSpeed    # E.g. if IBGen is "HDR", result is "4XHDR"
        if ibNet [guid].nodeSpecialHCAs != "0":
            suffix = "#"    # A virtual HCA is enabled (e.g. SHARP); flag the GUID with a #
        leafList = director.directorLeafGUIDList
        leafSlots = len (leafList) - 1    # Don't count entry 0
        installedLeafs = leafSlots - leafList.count (" ") + 1
        pc = int (ibNet [guid].nodePortCount)    # Get number of Spine ASIC ports
        pp = int (pc/2)*2    # Deduct the odd (virtual) port if there is one
        r = int ((installedLeafs / leafSlots) * pp)    # Compute # of midplane links this Spine ASIC should have
        linksSeen = 0
        badLinks = 0
        for p in range (1, pp + 1):    # Loop through all of this Spine's external ports
            if peerExists (guid, p, peerGUID, peerLinkStruct):
                linksSeen = linksSeen + 1
                if peerLinkStruct[0].linkWidthXRate != spineWXR:    # Link width or rate < Spine ASIC's capability
                    print ("BAD LINK: ", peerLinkStruct[0].linkWidthXRate, " ", spineWXR)    ###### DEBUG #####
                    badLinks = badLinks + 1
        if ((r != linksSeen) or (badLinks > 0)) and not (noWarn):
            highlightnum = rtfColorIndex ["Red"]
            if (badLinks > 0):
                warn ("Spine " + ibNet[guid].nodeSlotName + " " + guid + " has " + str(badLinks) + " sub-optimal links.")
            else:
                warn ("Spine " + ibNet[guid].nodeSlotName + " " + guid + " is missing " + str (r - linksSeen) + " midplane link(s).")
        elif director.directorSpineDeviceID == "d2f0":    # Is Spine an HDR ASIC?
            if pc != 41:    # E.g. if Spine ports somehow got split/splittable
                highlightnum = rtfColorIndex ["Yellow"]
                if not (noWarn):
                    warn ("HDR Spine " + ibNet[guid].nodeSlotName + " " + guid + " is in 'split port' mode.")
        if highlightnum > 0: 
            prefix = nodeRTFStrings[highlightnum][0]
            suffix = nodeRTFStrings[highlightnum][1] + suffix
    s = guid [-(width - 2):]    # Take the last N digits of the GUID
    return (prefix + putCentered (s, width) + suffix)   

#### end of putSpineBoardGUID ####

#### putSpineBoardLID ####
def putSpineBoardLID ( director, spineBoardNum, width ):
    guid = director.directorSpineGUIDList [spineBoardNum]
    if guid == " ":    # No SPine Board in this slot
        s = " "
    else:
        node = ibNet [guid]
        s = node.nodePortZeroLID
    return (putCentered (s, width))

#### end of putSpineBoardLID ####

#### getNodeColor ####
# For Director ports.   extPortNum is an integer, starting at 1.
def getNodeColor ( director, extPortNum ):
    p = director.directorPeerList [extPortNum]
    g = p.peerNodeGUID
    if g == " ":    # If there's no Peer connected to the port
        leafSlot = int((extPortNum - 1) / int(director.directorLeafExtPorts)) + 1    # Compute Leaf slot # (0 is unused)
        if director.directorLeafGUIDList [leafSlot] ==" ":    # If no Leaf module is installed in this slot
            g = "!"    # Choose a color indicating a missing Leaf module
    return (nodeColors [g])

#### end of getNodeColor ####

#### getSwNodeColor ####
def getSwNodeColor ( switchNode, portNum ):
    global resolveDirectors
    global defaultPortColor
    g = defaultPortColor [portNum]
    p = switchNode.nodePortList [portNum]    # Get the Port structure for the specified Port
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink
        g = l.peerNodeGUID    # Get the GUID of the device connected to the port
        dg = ibNet [g].nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            g = dg
    return (nodeColors [g])

#### end of getSwNodeColor ####

#### showDirectorSummary ####
def showDirectorSummary (noWarn):
# If noWarn then don't generate entries in the Warnings .rtf file.
# Assumes currentDirector is the Director structure to be displayed.
    global ff
    global wf
    global currentDirector
    #
    dg = currentDirector.directorNodeGUID
    dn = currentDirector.directorDesc
    if not (noWarn):
        warnSection ("#################### Analyzing Director " + dn + " (" + dg + ") #################### ")
    s = dg + "  Name: " + dn + "    Vendor: "
    vID = currentDirector.directorVendorID
    vName = ouiDict.get (vID, " ")
    s = s + vName + " (" + vID + ")  " 
    s = s + currentDirector.directorModel + " ("
    s = s + currentDirector.directorSpeed + ")"
    ff.write (s + rtfEOL)
    #
    s = "Max ports: " + currentDirector.directorMaxPorts + " "
    nls = len(currentDirector.directorLeafGUIDList) - 1    # Leaf ASIC slots
    nss = len(currentDirector.directorSpineGUIDList) - 1    # No. of Spine ASIC slots
    els = currentDirector.directorLeafGUIDList.count (" ") - 1    # Empty Leaf ASIC slots
    ess = currentDirector.directorSpineGUIDList.count (" ") - 1    # Empty Spine ASIC slots
    s = s + "    Spine ASICs: " + str (nss - ess) + " of " + str (nss) + " "
    s = s + "    Leaf ASICs: " + str (nls - els) + " of " + str (nls) + " "    # Later add # of connections to Switches & HCAs
    ff.write (s + rtfEOL)
    #
    w = 8
    # Display a list of the Spine ASIC GUIDs and LIDs
    sn = 1
    #print("nss=", nss)
    s = "Spine ASICs + LIDs:  "
    while not (sn > nss):
        for i in range (6):
            if not (sn > nss):
                #print("sn=",sn)
                s = s + putSpineBoardGUID (currentDirector, sn, w, noWarn)
                s = s + putSpineBoardLID (currentDirector, sn, w-2) + ","
            sn = sn + 1
        if sn > nss: 
            j = len (s)
            s = s [: j - 2]    # Cut off comma at end of this line
        ff.write (s + rtfEOL)
        s = "                     "
    # Display a list of the Leaf ASIC GUIDs and LIDs
    ln = 1
    s = "Leaf ASICs + LIDs:   "
    while not (ln > nls):
        for i in range (6):
            if not (ln > nls):
                s = s + putLeafBoardGUID (currentDirector, ln, w)
                s = s + putLeafBoardLID (currentDirector, ln, w-2) + ","
            ln = ln + 1
        if ln > nls: 
            j = len (s)
            s = s [: j - 2]    # Cut off comma at end of this line
        ff.write (s + rtfEOL)
        s = "                     "
    ff.write ("     (# = SHARP enabled; yellow = Spine ports are splittable; red = missing/degraded midplane links)" + rtfEOL)

#### end of showDirectorSummary ####

#### showDirector12x2 ####

# Assumes currentDirector is the Director structure to be displayed.
# Creates a text file that portrays the front panel of a Director built from 24-port ASICs with Leaf
# Boards that have two rows of 12 connectors (e.g. the ISR 20xx).
def showDirector12x2 ():
    global currentDirector
    global ff
    dir = currentDirector
    leafList = dir.directorLeafGUIDList
    leafBoards  = int (len (leafList) / 2)
    #
    pb = 12    # Ports per row
    portMap = [0] * ((leafBoards * 24) + 1)    # Allocate an array to map Port numbers
    i = 1
    for j in range (leafBoards):
        for k in range (pb):
            portMap [i + k] = i + k
            portMap [i + k + pb] = i + k + pb
        i = i + pb + pb
    #
    w = 6
    v = "\\u9474?"    # Box Drawings Light Vertical
    hlin = "\\u8212?"    # Em Dash
    s = " " * (w + 1)
    for i in range (pb):
        s = s + putCentered (str(i + pb + 1), w + 1)    # Print out a line of port numbers for reference
    ff.write (s + rtfEOL)
    # 
    j = 1
    for b in range (1, len (leafList)):
        if b % 2 == 1:    # If b is odd
            s = (" " * (w + 1)) + ("=" * (pb * w)) + ("=" * (pb-1))    # Draw a "=" line at the top of port row
        else:
            s = " L" + str (int ((b/2)))
            s = putCentered (s, w) + v
            s = s + (hlin * (pb * w)) + (hlin * (pb-1)) + v    # Draw a "-" line at the top of port row
        ff.write (s + rtfEOL) 
        s = (" " * w) + v    
        for i in range (pb):
            p = portMap [j + i]
            s = s + putPeerTypeAndLinkType (dir, p, w, getNodeColor (dir, p)) + v
        ff.write (s + rtfEOL)
        s = putLeafBoardGUID (dir, b, w) + v    # Node GUID for this leaf Board
        for i in range (pb):
            p = portMap [j + i]
            s = s + putPeerNodeGUID (dir, p, w, getNodeColor (dir, p)) + v
        ff.write (s + rtfEOL)
        s = putLeafBoardLID (dir, b, w) + v    # Port 0 LID of this Leaf Board
        for i in range (pb):
            p = portMap [j + i]
            s = s + putPeerLID (dir, p, w, getNodeColor (dir, p)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (pb):
            p = portMap [j + i]
            s = s + putPeerPort (dir, p, w, getNodeColor (dir, p)) + v
        ff.write (s + rtfEOL)
        j = j + pb
    s = (" " * (w + 1)) + ("=" * (pb * w)) + ("=" * (pb-1))    # Put a line of "=" at the bottom
    ff.write (s + rtfEOL)
    s = " " * (w + 1)
    for i in range (pb):
        s = s + putCentered (str(i + 1), w + 1)    # Print out a line of port numbers for reference
    ff.write (s + rtfEOL)

#### end of showDirector12x2 ####

#### showDirector18x1 ####

# Assumes currentDirector is the Director structure to be displayed.
# Creates a text file that portrays the front panel of a Director built from 36-port ASICs with Leaf
# Boards that have one row of 18 connectors (e.g. the GD 4700).
def showDirector18x1 ():
    global currentDirector
    global ff
    global rtfColors
    dir = currentDirector
    #
    pb = 18    # Ports per row
    w = 5
    v = "\\u9474?"    # Box Drawings Light Vertical
    hlin = "\\u8212?"    # Em Dash
    p = 1
    majorLine = (" " * (w+1)) + (hlin * (pb * w)) + (hlin * (pb - 1))    # Build a line for the top of a Leaf Bd
    s = (" " * w) 
    for i in range (pb):
        s = s + putCentered (str(i + 1), w + 1)    # Print a line of port numbers for reference
    ff.write (s + rtfEOL)
    #
    leafList = dir.directorLeafGUIDList 
    for b in range (1, len (leafList)):
        ff.write (majorLine + rtfEOL)    # Draw a line at the top of the Leaf Board 
        s = " L" + str (b)
        s = putCentered (s, w) + v
        for i in range (pb):
            s = s + putPeerTypeAndLinkType (dir, p + i, w, getNodeColor (dir, p + i)) + v
        ff.write (s + rtfEOL)
        s = putLeafBoardGUID (dir, b, w) + v    # Node GUID for this leaf Board
        for i in range (pb):
            s = s + putPeerNodeGUID (dir, p + i, w, getNodeColor (dir, p + i)) + v
        ff.write (s + rtfEOL)
        s = putLeafBoardLID (dir, b, w) + v    # Port 0 LID of this Leaf Board
        for i in range (pb):
            s = s + putPeerLID (dir, p + i, w, getNodeColor (dir, p + i)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (pb):
            s = s + putPeerPort (dir, p + i, w, getNodeColor (dir, p + i)) + v
        ff.write (s + rtfEOL)
        p = p + pb
    #
    ff.write (majorLine + rtfEOL)    # Draw a line at the bottom of the last row 
    s = "   "
    for i in range (pb):
        s = s + putCentered (str(i + 1), w + 1)    # Print out a line of port numbers for reference
    ff.write (s + rtfEOL)

#### end of showDirector18x1 ####

#### showDirector9x2 ####

# Assumes currentDirector is the Director structure to be displayed.
# Creates a text file that portrays the front panel of a Director built from 36-port ASICs with Leaf
# Boards that have 2 rows of 9 connectors and 2 Leaf Boards are side by side (e.g. the SX6536).
def showDirector9x2 ():
    global currentDirector
    global ff
    global rtfColors
    #
   # print("SHOWDIRECTOR9x2")
    dir = currentDirector
    pb = 18
    w = 5
    v = "\\u9474?"    # Box Drawings Light Vertical
    hlin = "\\u8212?"    # Em Dash
    p = 1
    majorLine = ("=" * (int(pb/2) * (w+1)))    # Build a line for the top of the port row
    majorLine = majorLine [:-1]
    majorLine = (" " * (w + 1)) + majorLine + "  " + majorLine
    minorLine = (hlin * (int(pb/2) * (w+1)))    # Build a line for the middle of the Leaf Boards
    minorLine = v + minorLine [:-1] + v
    minorLine = (" " * w) + minorLine + minorLine
    s = (" " * w) 
    for i in range (1, pb, 2):
        s = s + putCentered (str(i), w + 1)    # Print out a line of port numbers for reference
    s = s[:-1] +"  "
    for i in range (1, pb, 2):
        s = s + putCentered (str(i), w + 1)    # Now continue for the right-hand Leaf Boards
    ff.write (s + rtfEOL)
    leafList = dir.directorLeafGUIDList
    #print("leafList = ", leafList, " $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #
    for b in range (1, len (leafList), 2):
        #
        ff.write (majorLine + rtfEOL)    # Draw a line at the top of the port row
        s = (" " * w) + v
        for i in range (0, pb, 2):
            #print("b = ", b, ", leafList[b] = ", leafList[b], ", p+i = ", p+i, "   @@@@@@@@@@@")
            s = s + putPeerTypeAndLinkType (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerTypeAndLinkType (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        #
        ff.write (minorLine + rtfEOL)    # Draw a line at the top of the port row 
        s = (" " * w) + v
        for i in range (0, pb, 2):
            s = s + putPeerTypeAndLinkType (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerTypeAndLinkType (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        s = (" " * w) + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        p = p + pb + pb
    ff.write (majorLine + rtfEOL)    # Draw a line at the bottom of the last port row
    s = (" " * w) 
    for i in range (2, pb + 1, 2):
        s = s + putCentered (str(i), w + 1)    # Print out a line of port numbers for reference
    s = s[:-1] +"  "
    for i in range (2, pb + 1, 2):
        s = s + putCentered (str(i), w + 1)    # Now continue for the right-hand Leaf Boards
    ff.write (s + rtfEOL)

#### end of showDirector9x2 ####

#### showDirector10x2 ####

# Assumes currentDirector is the Director structure to be displayed.
# Creates a text file that portrays the front panel of a Director built from 40-port ASICs with Leaf
# Boards that have 2 rows of 10 connectors and 2 Leaf Boards are side by side (e.g. the CS8500)--
# whether the two ASICs are separate modules or packaged as one module.
def showDirector10x2 ():
    global currentDirector
    global ff
    global rtfColors
    #
    #print("SHOWDIRECTOR10x2")
    dir = currentDirector
    pb = 20
    w = 5
    #v = "\\u9474?"    # Box Drawings Light Vertical #### CAUSES ISSUES IN THIS REPORT ####
    v = "|"
    #hlin = "\\u8212?"    # Em Dash    #### CAUSES ISSUES IN THIS REPORT ####
    hlin = "-"
    p = 1
    majorLine = ("=" * (int(pb/2) * (w+1)))    # Build a line for the top of the port row
    majorLine = majorLine [:-1]
    majorLine = (" " * (1)) + majorLine + "  " + majorLine
    minorLine = (hlin * (int(pb/2) * (w+1)))    # Build a line for the middle of the Leaf Boards
    minorLine = v + minorLine [:-1] + v
    minorLine = (" " * 0) + minorLine + minorLine
    s = (" " * 1) 
    for i in range (1, pb, 2):
        s = s + putCentered (str(i), w + 1)    # Print a line of port numbers for reference
    s = s[:-1] +"  "
    for i in range (1, pb, 2):
        s = s + putCentered (str(i), w + 1)    # Now continue for the right-hand Leaf Boards
    ff.write (s + rtfEOL)
    leafList = dir.directorLeafGUIDList
    #print("leafList = ", leafList, " $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #
    for b in range (1, len (leafList), 2):
        #
        ff.write (majorLine + rtfEOL)    # Draw a line at the top of the port row
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            #print("b = ", b, ", leafList[b] = ", leafList[b], ", p+i = ", p+i, "   @@@@@@@@@@@@@@@@")
            s = s + putPeerTypeAndLinkType (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerTypeAndLinkType (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + i, w, getNodeColor (dir, p + i)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + pb + i, w, getNodeColor (dir, p + pb + i)) + v
        ff.write (s + rtfEOL)
        #
        ff.write (minorLine + rtfEOL)    # Draw a line at the top of the port row 
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            s = s + putPeerTypeAndLinkType (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerTypeAndLinkType (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerNodeGUID (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerLID (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        s = (" " * 0) + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + i + 1, w, getNodeColor (dir, p + i + 1)) + v
        s = s [0:len(s)-1] + v + v
        for i in range (0, pb, 2):
            s = s + putPeerPort (dir, p + pb + i + 1, w, getNodeColor (dir, p + pb + i + 1)) + v
        ff.write (s + rtfEOL)
        p = p + pb + pb
    ff.write (majorLine + rtfEOL)    # Draw a line at the bottom of the last port row
    s = (" " * 0) 
    for i in range (2, pb + 1, 2):
        s = s + putCentered (str(i), w + 1)    # Print out a line of port numbers for reference
    s = s[:-1] +"  "
    for i in range (2, pb + 1, 2):
        s = s + putCentered (str(i), w + 1)    # Now continue for the right-hand Leaf Boards
    ff.write (s + rtfEOL)

#### end of showDirector10x2 ####

#### setSwitchAttributes ####
# Assumes currentNode is the Switch in question
def setSwitchAttributes ():
    global currentNode
    global ibNet
    nodeGUID = currentNode.nodeGUID
    #print ("SET SWITCH ATTRIBUTES: ", nodeGUID)    
    devID = currentNode.deviceID
    model = "Unknown (" + devID + ")"
    gen = " "
    if devID == "b924":    # Mellanox DDR 24-port ASIC
        gen = "DDR"
        model = "Mellanox ASIC"
        if currentNode.vendorID == "66a":    # SilverStorm
            model = "9xx0 Director Module"
    elif devID == "5a30":    # Voltaire 9024D
        model = "ISR9024D"
        gen = "QDR"
    elif devID == "5a31":    # Voltaire 9024D-M
        model = "ISR9024D-M"
        gen = "QDR"
    elif devID == "5a2e":    # Voltaire 9024S
        model = "ISR9024S"
        gen = "SDR"
    elif devID == "5a5b":    # Voltaire sLB-4018
        model = "sLB-4018"
        gen = "QDR"
    elif devID == "5a5c":    # Voltaire sFB-4700
        model = "sFB-4700"
        gen = "QDR"
    elif devID == "5a5d":    # Voltaire sFB-4700 Hyperscale
        model = "sFB-4700 Hyper"
        gen = "QDR"
    elif devID == "bd36":    # Mellanox IS50xx    # 
        model = "IS50xx"
        gen = "QDR"
    elif devID == "c738":    # Mellanox SX60xx
        model = "SX60xx"
        gen = "FDR"
    elif devID == "5a5a":    # Voltaire 4036
        model = "GD4036"
        gen = "QDR"
    elif devID == "7320":    # QLogic 12300
        model = "12300"
        gen = "QDR"
    elif devID == "cf08":    # Mellanox SB77x0 - SwitchIB2 
        model = "SB77x0-2"
        gen = "EDR"
    elif devID == "cb20":    # Mellanox SB77x0
        model = "SB77x0"
        gen = "EDR"
        if re.search('MSB7780/U1"', currentNode.nodeDesc):    # If it's an IB Router
            model = "Router"    # Mellanox SB7780
            if not (nodeGUID [-1] == "0"):   # It's a virtual Router if last GUID digit isn't "0"
                model = "vRouter"
    elif devID == "d2f0":   # Mellanox Quantum HDR
        model = "QM87x0"
        gen = "HDR"
    else:
        ports = int (currentNode.nodePortCount)    # Use port count to detect NDR until devID is knkown
        if ports in [64, 65, 66, 128, 129, 130]:    #################### TEMPORARY ################
            model = "QM97x0"
            gen = "NDR"   
    if (gen == " ") and False:    ####    
        print ("NODE HAS EMPTY IB GEN: ", nodeGUID)    ####
    currentNode = currentNode._replace (nodeIBGen = gen)
    currentNode = currentNode._replace (nodeModel = model)
    ibNet [nodeGUID] = currentNode
    #print ("UPDATED NODE IB GEN: ", nodeGUID, ibNet[nodeGUID].nodeIBGen)   

#### end of setSwitchAttributes ####

#### setAllSwitchAttributes ####
# Loops through all of the Switches that arent part of a Director, and sets some additional
# Node attributes that arent found in an ibnetdiscover output.
def setAllSwitchAttributes ():
    global currentNode
    global ibNet
    for j, key in enumerate (ibNet):
        currentNode = ibNet [key]
        if currentNode.nodeType == "S":    # We only care about Switches
            dg = currentNode.nodeDirectorGUID 
            if dg == " ":    # If this Switch isnt part of a Director chassis
                setSwitchAttributes ()

#### end of setAllSwitchAttributes ####

#### showSwitchSummary ####
# Assumes currentNode is the Switch in question.
def showSwitchSummary (showSwitchColor):
    global currentNode
    global ff
    s = "GUID: " + currentNode.nodeGUID
    s = s + "   LID: " + currentNode.nodePortZeroLID
    vID = currentNode.vendorID
    vName = ouiDict.get (vID, " ")
    s = s + "   Vendor: " + vName + " (" + vID + ")"
    s = s + "   " + currentNode.nodeModel
    s = s + "  " + currentNode.nodeIBGen
    s = s + "   Ports: " + currentNode.nodePortCount
    ff.write (s + rtfEOL)
    s = "Description: " + currentNode.nodeDesc
    if showSwitchColor:
        nc = nodeColors [currentNode.nodeGUID]
        s = s + "  " + nodeRTFStrings[nc][0] + "      " +nodeRTFStrings[nc][1]
        s = s + " \\cf4 " + str(nc) + "\\cf0"    #### DEBUG ####
    ff.write (s + rtfEOL)

#### end of showSwitchSummary ####

#### analyzeSwitch ####

# Assumes currentNode is the switch Node structure to be analyzed.
# For each set of links from this Switch to an adjacent Switch, get a list of
# port numbers on this switch.   
def analyzeSwitch ():
    global currentNode
    global ff
    #
    # peerGUIDDict is a dictionary of GUIDs of Switches adjacent to me.  Each dictionary
    # entry is a list of my ports (as integers, in ascending order) that link to 
    # that Switch.
    myGUID = currentNode.nodeGUID
    #print("Current Node = ",myGUID)
    peerGUIDDict = islDict [myGUID].copy()    #
    #print(peerGUIDDict)
    #
    # Look through peerGUIDDict and see if there are multiple ISLs to an adjacent Switch that
    # don't connect to continguous ports on my switch.
    for i, peerGUID in enumerate(peerGUIDDict):     
        l = peerGUIDDict [peerGUID]
        s = "Links to " + peerGUID + ": " + str (l)
        #print(l)
        n = len (l)
        if n > 1:    # If multiple links from me to this peer Switch
            a = l[0]   # Lowest of my port numbers
            b = l[n-1]    # Highest of my port numbers
            #print (n, a, b)
            if not ((a + n - 1) == b):    # If non-contiguous ports
                #print ("From ", myGUID, " ", s, " Ports are not contiguous")
                s = s + "\\cf17" + "  Ports are not contiguous" + "\\cf"    # Need nicer way to specify font color
                ff.write (s + rtfEOL)
    s = " "
    ff.write (s + rtfEOL)

#### end of analyzeSwitch ####

#### analyzeSwitch2 ####

# Assumes currentNode is the switch Node structure to be analyzed.
def analyzeSwitch2 ():
    global currentNode
    global ff
    peerNodeGUID = [noPeer]    # For use by the peerExists routine
    peerLink = [" "]    # For use by the peerExists routine
    g = currentNode.nodeGUID
    np = int(currentNode.nodePortCount)    # Includes extra 'special' port if present
    for p in range (1, np + 1):    # Ports are numbered from 1 to np
        if peerExists (g, p, peerNodeGUID, peerLink):
            pg = peerNodeGUID [0]
            if ibNet[pg].nodeType == "H":
                pDesc = ibNet[pg].nodeDesc
                s = "p"+str(p)+": "+pg+" "+pDesc
                ff.write (s + rtfEOL)

#### end of analyzeSwitch2 ####

#### putPortNumbers ####
#  N fields of width 'width', separated by one sepChar.  Total length (N*width) + (N-1).
def putPortNumbers (portList, width, sepChar, fillChar):
    s = "" 
    for i in range (0, len(portList)):
        s = s + sepChar [(i+1)%2] + putCentered (str(portList [i]), width)    # Build a line of port numbers
    return (s.replace (" ", fillChar)[1:])
#### end of putPortNumbers ####

#### showSwitchRow ####
def showSwitchRow (portList, vbar):
    global currentNode
    global ff
    global rtfColorSet
    global defaultPortColor
    global currentLinkWidths
    global currentPeerGUIDs
    node = currentNode
    #print (portList)
    pb = len (portList)
    w = 5
    v = "\\u9474?"    # Box Drawings Light Vertical
    leadIn = " " + v
    s = leadIn
    for i in range (0, pb):
        port = portList [i]
        s = s + putSwPeerTypeAndLinkType (node, port, w, getSwNodeColor (node, port)) + vbar [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (0, pb):
        port = portList [i]
        s = s + putSwPeerNodeGUID (node, port, w, getSwNodeColor (node, port)) + vbar [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (0, pb):
        port = portList [i]
        s = s + putSwPeerLID (node, port, w, getSwNodeColor (node, port)) + vbar [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (0, pb):
        port = portList [i]
        s = s + putSwPeerPort (node, port, w, getSwNodeColor (node, port)) + vbar [i % 2]
    ff.write (s + rtfEOL)

#### end showSwitchRow ####

#### showSplitSwitch ####
# Creates RTF text that portrays the front panel of a Switch with 80 physical ports,
# e.g. an HDR ToR in 'splittable' mode. 
# Assumes currentNode is the switch Node structure to be displayed.
# Non-split (4x) ports only appear on odd-numbered ports, and the subsequent even-
# numbered port will always be empty.  Instead of showing this 2nd port as being
# empty/disconnected-- to indicate that it's really a part of the 4x port-- we show it as 
# having the same color but without text.  The currentPeerGUIDs list, which is indexed
# by port number, helps retrieve the colors of the previous port row.

def showSplitSwitch ():
    global currentNode
    global ff
    global rtfColors
    global currentLinkWidths
    global currentPeerGUIDs
    global defaultPortColor
    #
    node = currentNode    # Shorter name
    #print ("SWITCH ", node.nodeGUID)
    isNDR = node.nodeIBGen == "NDR"
    if isNDR:
        ff.write ("\\fs9"+rtfEOL)    # Reduce font size so the display fits between the margins
    #
    for i in range (1, len (defaultPortColor)):
        defaultPortColor [i] = noPeer
        currentLinkWidths [i] = " "
        currentPeerGUIDs [i] = noPeer
    ps = int (node.nodePortCount)    # Get total IB ports, including virtual ports e.g. SHARPv3
    pb = int (ps / 4)    # Number of IB ports displayed per row
    ps = pb * 4    # Omit "n+1st" port (e.g. for SHARP) if present
    w = 5
    v = "\\u9474?"    # Box Drawings Light Vertical
    v = "|"
    leadIn = " " + v
    vs = [":", v] if isNDR else [v, v]
    #macron=unicodedata.lookup ("MACRON")   # Avoid explicit use of some chars disliked by Python on Mac OS
    macron = chr (0xAF)    # Avoid explicit use of certain characters disliked by Python on Mac OS
    if isNDR:
        portL = list (range (1, pb, 2))    # Physical port #s - 1 connector per 2 IB ports
        t = putPortNumbers (portL, w + w + 1, [" "," "], " ")
    else:
        portL = list (range (1, pb * 2, 2))    # Physical port #s
        t = putPortNumbers (portL, w, [" "," "], " ")
    ff.write ("   \\cf4" + t + "\\cf0" +rtfEOL)
    # Row 1
    portL = list (range (1, ps, 4))    # IB port numbers  
    t = putPortNumbers (portL, w, vs, macron)
    ff.write (" " + v + t + v + rtfEOL)    
    showSwitchRow (portL, vs)
    for i in range (0, pb):
        pnum = portL[i]
        if currentLinkWidths [pnum] == "4x":    # For each 4x link on this row, carry its port color to port n+1
            defaultPortColor [pnum+1] = currentPeerGUIDs [pnum]
            #print("Change defaultPortColor [",pnum+1,"] to ",currentPeerGUIDs[pnum])
    # Row 2
    portL = list (range (2, ps, 4))    # IB port numbers 
    t = putPortNumbers (portL, w, vs, macron)
    ff.write (" " + v + t + v + rtfEOL)    
    showSwitchRow (portL, vs)
    # Row 3
    portL = list (range (3, ps, 4))    # IB port numbers
    t = putPortNumbers (portL, w, vs, macron)
    ff.write (" " + v + t + v + rtfEOL)    
    showSwitchRow (portL, vs)
    for i in range (0, pb):
        pnum = portL[i]
        if currentLinkWidths [pnum] == "4x":    # For each 4x link on this row, carry its port color to port n+1
            defaultPortColor [pnum+1] = currentPeerGUIDs [pnum]
            #print("Change defaultPortColor [",pnum+1,"] to ",currentPeerGUIDs[pnum])
    # Row 4
    portL = list (range (4, ps + 1, 4))    # IB port numbers
    t = putPortNumbers (portL, w, vs, macron)
    ff.write (" " + v + t + v + rtfEOL)    
    showSwitchRow (portL, vs)
    # Draw a line at the bottom of the switch and put physical connector #s ========
    if isNDR:
        portL = list (range (2, pb + 1, 2))    # Physical port #s - 1 connector per 2 IB ports
        t = putPortNumbers (portL, w + w + 1, [" "," "], macron)
    else:
        portL = list (range (2, (pb * 2) + 1, 2))    # Physical port #s
        t = putPortNumbers (portL, w, [" "," "], macron)
    ff.write ("  \\cf4" + t + "\\cf0" + rtfEOL)
    #analyzeSwitch ()    # Do some additional analysis of this Switch
    #analyzeSwitch2 ()    # List the HCAs connected to this Switch
    if isNDR:    # Restore the font size
        ff.write ("\\fs15" + rtfEOL)
    s = " "
    ff.write (s + rtfEOL)

#### end of showSplitSwitch ####

#### showSwitch ####

# Assumes currentNode is the switch Node structure to be displayed.
# Creates RTF text that portrays the front panel of a Switch, assuming *two* rows of ports.
# For NDR I chose to 'go wide', using 2 rows of logical ports, 32 ports per row, and a
# smaller font, to maximize the number of switches per output page. 
# Note:  someday rewrite this to use showSwitchRow.
def showSwitch ():
    global currentNode
    global ff
    global rtfColors
    global defaultPortColor
    #  
    fc = rtfColorIndex ["Gray 50%"]    # Font color
    node = currentNode
    ps = int (node.nodePortCount)    # IB ports per Switch, includes virtual ones e.g. for SHARP
    isNDR = currentNode.nodeIBGen == "NDR"
    if isNDR:
        ff.write ("\\fs9"+rtfEOL)    # Reduce font size so the display fits between the margins
    #
    for i in range (1, len (defaultPortColor)):
        defaultPortColor [i] = noPeer
    #print(currentNode.nodeGUID, " ooo---------> ", defaultPortColor)
    pb = int (ps / 2)    # IB ports per row.  
    ps = pb + pb    # Ignore "n+1st" port (e.g. for SHARP) if present    
    w = 5
    v = "\\u9474?"    # Box Drawings Light Vertical
    hlin = "\\u8212?"    # Em Dash
    leadIn = " " + v
    vs = [v, ":"] if isNDR else [v, v]
    portMap = [0] * (ps + 1)    # portMap [0] is unused
    vName = ouiDict.get (node.vendorID, " ")    # Get Vendor name, or " " if unknown
    if vName == "Mellanox":
        if isNDR:    # NDR's OSFP connectors create a different layout of logical ports
            for j in range (1, pb+1, 2):    # Build an array that maps port position to port number
                portMap [j] = (j * 2) - 1    # Top port row is 1, 2, 5, 6, ...
                portMap [j + 1] = portMap [j] + 1
                portMap [j + pb] = (j * 2) + 1    # Bottom row is 2nd half of array:  3, 4, 7, 8, ...
                portMap [j + pb + 1] = portMap [j + pb] + 1
        else:
            for j in range (1, pb+1):    # Build an array that maps port position to port number
                portMap [j] = (j * 2) - 1    # Top port row is 1, 3, 5,... n-1
                portMap [j + pb] = portMap [j] + 1    # Bottom row is 2nd half of array: 2, 4, 6,... n
    else:
        for j in range (1, pb+1):    # Works for Voltaire, SilverStorm; need to check other vendors
            portMap [j] = j + pb    # Top row is 19, 20, 21, , 36
            portMap [j + pb] = j    # Bottom row is 1, 2, 3, , n/2
    majorLine = "  " + ("=" * (pb * w)) + ("=" * (pb - 1))    # Build a line for the top/bottom
    minorLine = "  " + (hlin * (pb * w)) + (hlin * (pb - 1)) + v    # A line for the middle of the switch
    s = " "
    if isNDR:
        s = "  \\cf" + str(fc)
        for i in range (1, pb+1, 2):    # NDR has 2 IB ports per physical port (connector)
            s = s + putCentered (str (i), (2 * w) + 2)
        s = s + "\\cf0"
    else: 
        for i in range (1, pb+1):
            s = s + putCentered (str (portMap [i]), w + 1)
    ff.write (s + rtfEOL)    # Print out a line of connector numbers for reference
    #
    ff.write (majorLine + rtfEOL)    # Draw a line at the top of the switch ==========
    if isNDR:
        s = leadIn
        for i in range (1, pb+1):
            s = s + putCentered (str (portMap [i]), w) + vs [i % 2]
        ff.write (s + rtfEOL)    # Print out a line of IB port numbers
    s = leadIn
    for i in range (1, pb+1):
        port = portMap [i]
        s = s + putSwPeerTypeAndLinkType (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (1, pb+1):
        port = portMap [i]
        s = s + putSwPeerNodeGUID (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (1, pb+1):
        port = portMap [i]
        s = s + putSwPeerLID (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (1, pb+1):
        port = portMap [i]
        s = s + putSwPeerPort (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    ff.write (minorLine + rtfEOL)    # Draw a line in the middle of the Leaf Board --------
    if isNDR:
        s = leadIn
        for i in range (1, pb+1):
            s = s + putCentered (str (portMap [i+pb]), w) + vs [i % 2]
        ff.write (s + rtfEOL)    # Print out a line of IB port numbers
    s = leadIn
    for i in range (pb+1, ps+1):
        port = portMap [i]
        s = s + putSwPeerTypeAndLinkType (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (pb+1, ps+1):
        port = portMap [i]
        s = s + putSwPeerNodeGUID (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (pb+1, ps+1):
        port = portMap [i]
        s = s + putSwPeerLID (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    s = leadIn
    for i in range (pb+1, ps+1):
        port = portMap [i]
        s = s + putSwPeerPort (node, port, w, getSwNodeColor (node, port)) + vs [i % 2]
    ff.write (s + rtfEOL)
    #
    ff.write (majorLine + rtfEOL)    # Draw a line at the bottom of the switch ========
    s = " "
    if isNDR:
        s = "  \\cf" + str(fc)
        for i in range (2, pb+1, 2):    # NDR has 2 IB ports per physical port (connector)
            s = s + putCentered (str (i), (2 * w) + 2)
        s = s + "\\cf0"
    else:
        for i in range (1, pb+1):
            s = s + putCentered (str(portMap[i+pb]), w + 1)
    ff.write (s + rtfEOL)    # Print a line of connector numbers for reference
    #analyzeSwitch ()    # Do some additional analysis of this Switch
    #analyzeSwitch2 ()    # List the HCAs connected to this Switch
    if isNDR:    # Restore the font size
        ff.write ("\\fs15" + rtfEOL)
    s = " "
    ff.write (s + rtfEOL)

#### end of showSwitch ####

#### RTF Colors ####
# RGB color strings for use in RTF color tables.
# NOTE:  MS Word is very bad at rendering RTF colors-- at least those 
# specified by decimal RGB triplets.  It seems to map all RTF colors to
# about a dozen colors.  So-- wrong colors as well as duplicate ones.  :-(
rtfBlack = "\\red0\\green0\\blue0;"
rtfWhite = "\\red255\\green255\\blue255;"
rtfDarkSlateGray = "\\red47\\green79\\blue79;"    # Slightly prettier than Black
rtfDarkGray = "\\red169\\green169\\blue169;" 
rtfRed = "\\red255\\green0\\blue0;"
rtfMediumBlue = "\\red123\\green104\\blue238;"
rtfGray30 = "\\red179\\green179\\blue179;"
# The following dictionary excludes Black and White.
rtfColorSet = {
    "Yellow" :       "\\red255\\green255\\blue0;",    # aka Vibrant Yellow
    "Light Yellow1" : "\\red255\\green255\\blue204;",
    "Bright Green" : "\\red0\\green255\\blue0;",
    "Turquoise" :    "\\red0\\green255\\blue255;",
    "Pink" :         "\\red255\\green0\\blue255;",
#  "Light Pink": "\\red255\\green182\\blue193);",    # MS Word thinks this is the same as Pink
    "Blue" :         rtfMediumBlue,
    "Red" :          rtfRed,    # aka Vibrant Red
#  "Dark Blue" :    "\\red0\\green0\\blue128;",    # Too dark
    "Teal" :         "\\red0\\green128\\blue128;",
    "Green" :        "\\red0\\green128\\blue0;",
    "Spring Green" : "\\red0\\green255\\blue127;",
    "Violet" :       "\\red128\\green0\\blue128;",
    "Wheat" :       "\\red245\\green222\\blue179;",
#  "Dark Red" :     "\\red128\\green0\\blue0;",
    "Dark Yellow" :  "\\red128\\green128\\blue0;",
    "Gray 50%" :     "\\red128\\green128\\blue128;",
#  "Gray 40%":      "\\red154\\green154\\blue154;",    # MS Word thinks this the same as Gray 50%
    "Gray 30%":      rtfGray30,
#  "Gray 25%" :     "\\red192\\green192\\blue192;",
    "Light Gray" :     "\\red204\\green204\\blue204;",
#  "Gray 20%":      "\\red205\\green205\\blue205;",    # MS Word thinks this is the same as Gray 30%
#  "Gray 10%":      "\\red230\\green230\\blue230;",    # MS Word displays this as white :-(
#  "Medium Gray" :    "\\red165\\green165\\blue165;",
    "Vibrant Orange" : "\\red255\\green192\\blue0;",
    "Vibrant Green" :  "\\red0\\green176\\blue80;",
    "Vibrant Blue" :   "\\red0\\green77\\blue187;",
    "Vibrant Purple" : "\\red155\\green0\\blue211;",
    "Pastel Red" :     "\\red221\\green132\\blue132;",
    "Pastel Orange" :  "\\red243\\green164\\blue71;",
    "Pastel Yellow" :  "\\red223\\green206\\blue4;",   
    "Pastel Green" :   "\\red119\\green221\\blue119;",    
    "Pastel Blue" :    "\\red174\\green198\\blue207;",
#  "Pastel Purple" :  "\\red179\\green158\\blue181;"    # MS Word thinks this is a gray
    }

# These patterns describe RTF patterns and colors that will be used for Switch ports.
# The buildNodeRTFStrings routine will convert them to actual RTF syntax and 
# store them in the nodeRTFStrings table.  The basic colors available are determined
# by the rtfColorSet dictionary.
# Each pattern consists of two parts separated by a colon.  To give an RTF text string
# a background color or pattern, it is prefixed by the 1st part and suffixed by the 2nd.
nodePatterns = [
    "\\highlight'Yellow':\\highlight0",
    "\\highlight'Light Yellow1':\\highlight0",
    "\\highlight'Bright Green':\\highlight0",
    "\\highlight'Turquoise':\\highlight0",
    "\\highlight'Pink':\\highlight0",
    "\\highlight'Blue':\\highlight0",
    "\\highlight'Red':\\highlight0",
    "\\highlight'Teal':\\highlight0",
    "\\highlight'Green':\\highlight0",
    "\\highlight'Spring Green':\\highlight0",
    "\\highlight'Violet':\\highlight0",
    "\\highlight'Wheat':\\highlight0",
    "\\highlight'Dark Yellow':\\highlight0",
    "\\highlight'Gray 50%':\\highlight0",
    "\\highlight'Gray 30%':\\highlight0",
    "\\highlight'Vibrant Orange':\\highlight0",
    "\\highlight'Vibrant Green':\\highlight0",
    "\\highlight'Vibrant Blue':\\highlight0",
    "\\highlight'Vibrant Purple':\\highlight0",
    "\\highlight'Pastel Red':\\highlight0",
    "\\highlight'Pastel Orange':\\highlight0",
    "\\highlight'Pastel Yellow':\\highlight0",
    "\\highlight'Pastel Green':\\highlight0",
    "\\highlight'Pastel Blue':\\highlight0",
    "\\chcfpat'Red'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Red'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Red'\\chcbpat'Yellow'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Red'\\chcbpat'Yellow'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Blue'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Blue'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Teal'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Teal'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Yellow'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Yellow'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Green'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Green'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Vibrant Purple'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Vibrant Purple'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Gray 50%'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Gray 50%'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Turquoise'\\chcbpat'White'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Turquoise'\\chcbpat'White'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Yellow'\\chcbpat'Blue'\\chbgdkfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
    "\\chcfpat'Yellow'\\chcbpat'Blue'\\chbgfdiag:\\chcfpat0\\chcbpat0\\chshdng1",
     ]

#### buildNodeRTFStrings ####
# This routine converts entries from nodePatterns into entries in nodeRTFStrings.
# nodePatterns is a list of strings, each of which describes RTF commands to
# set highlighting or a pattern for a section of text, and then turn the highlight or
# pattern off again.
# Each nodePattern string consists of two substrings, separated by a ":".  The first
# substring is RTF command(s) to enable a highlight/pattern; the second is
# RTF command(s) to disable that highlight/pattern.  The substrings are referred
# to here as prefix and suffix.
# Each nodePattern can refer to one or more colors from the RTF Color Table, which
# is declared at the beginning of an RTF file.  RTF refers to colors using numeric
# indices into the Color Table, instead of using color names, and these indices can change
# as RTF colors are added or deleted.  To mask any shuffling of color indices, we
# use the rtfColorIndex dictionary, which maps color names to Color Table indices and
# is built when the Color Table is built.
# This routine inspects each nodePattern for color names delimited by single quotes,
# replaces each color name with its corresponding Color Table index (via rtfColorIndex),
# splits the resulting string at the ":" into prefix and suffix, creates a 2-element list, and
# appends the 2-tuple to the nodeRTFStrings list.
# Example:  the NodePattern "\highlight'Gray':\highlight0" would become the 2-tuple
#    ["\highlight21", "\highlight0"] assuming that Gray has a Color Table index of 21.
def buildNodeRTFStrings ():
    global nodePatterns
    global rtfColorIndex
    global nodeRTFStrings
    nodeRTFStrings = [[" ", " "]]    # Entry zero, which is not used
    # We put 'special' node colors/patterns at the positions 1 through 4:  
    #   black, white, dark gray, gray 30%
    # These map to positions in the RTF Color Table.
    # Someday, replace these with symbolic names instead of relying on well-known
    # indices into nodeRTFStrings and the RTF Color Table.
    nodeRTFStrings.append (["\\highlight1", "\\highlight0"])
    nodeRTFStrings.append (["\\highlight2", "\\highlight0"])
    nodeRTFStrings.append (["\\highlight3", "\\highlight0"])
    nodeRTFStrings.append (["\\highlight4", "\\highlight0"])
    # Now handle the nodePatterns:
    for j in range (len(nodePatterns)):
        p = nodePatterns [j]
        #print ("PATTERN:  ", p)
        m = re.search ("'[a-zA-Z0-9% ]*'", p)    # Look for a color name delimited by single quotes
        while m:    # Loop until we've translated all color names to Color Table indices
            s = m.start()
            e = m.end()
            colorName = p[s+1:e-1]
            #print (colorName)
            index = rtfColorIndex [colorName]
            #print (index)
            p = p[0:s] + str (index) + p[e:]    # Replace the color name with its index
            #print("new p = ", p)
            m = re.search ("'[a-zA-Z0-9% ]*'", p)    # Look for another color name
        prefix = p.split (":")[0]
        suffix = p.split (":")[1]
        nodeRTFStrings.append ([prefix, suffix])
#### end of buildNodeRTFStrings ####

#### putRTFColorTbl ####
def putRTFColorTbl (colorDict):
    global rtfColors
    global rtfColorIndex
    s = "{\\colortbl;" + rtfBlack + rtfWhite + rtfDarkGray + rtfGray30   # Put these at colortbl positions 1, 2, 3, 4.
    # Black, white, and dark gray are 'reserved' colors for Switch/Director ports.  The other special colors help
    # make certain reports prettier but can also be used as port colors.
    rtfColorIndex = {"Black": 1, "White": 2, "Dark Gray": 3, "Gray 30%": 4}
    rtfColors = len(rtfColorIndex)
    for i, key in enumerate(colorDict):
        rtfColors = rtfColors + 1
        s = s + colorDict [key]    # Append this RGB color string to the color table in the next position
        rtfColorIndex [key] = rtfColors    # So we can look up the colortbl index (position) of a color by name
    s = s + "}"
    #print ("rtfColors: ", rtfColors)
    return (s)
#### end of putRTFColorTbl ####

#### rtfTest ####
def rtfTest ():
    global fPath
    global rtfColorIndex
    global nodeRTFStrings
    rname = fPath + "rtftest.rtf"
    rtf = open (rname, "w")
    rtf.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Courier;}}\n")    # RTF file header
    rtf.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    for i, key in enumerate (rtfColorIndex):
        rtf.write ("\\highlight" + str(rtfColorIndex [key]) + " COLOR " + str(rtfColorIndex [key]) + " " + key +"\\highlight0\\line\n")
    rtf.write ("----------------  \\line\n")
    for i in range(1, len(nodeRTFStrings)):    # Skip entry 0
        s = nodeRTFStrings[i][0] + " nodeRTFString [" + str(i) + "] " + nodeRTFStrings[i][1]
        rtf.write (s + "\\line\n")
    rtf.write ("}")
    rtf.close ()
#### end of rtfTest ####

#### showLegend ####
# Print a legend for the director or switch layouts
def showLegend (type):
    global ff
    ff.write ("                                       " + type + " LAYOUTS (CONNECTOR SIDE)" + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write ("PORT LEGEND:" + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write (" =====" + rtfEOL)
    ff.write ("|" + "T WXR" + "|     T = peer type: (S)witch, (H)CA, (D)irector; WXR = link (W)idth X (R)ate" + rtfEOL)
    ff.write ("|GGGGG|     Least significant hex digits of peer Node GUID, or Director ID" + rtfEOL)
    ff.write ("| LLL |     Peer LID (decimal)" + rtfEOL)
    ff.write ("| PPP |     Peer port number" + rtfEOL)
    ff.write (" =====" + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write ("Port color for inter-Switch links is the color arbitrarily assigned to that peer Switch or" + rtfEOL)
    ff.write ("Director (white for HCAs, black for no connection)" + rtfEOL)

#### end of ShowLegend ####


#### showAllDirectors ####
def showAllDirectors ():
    global fPath
    global fnameBase
    global allDirectors
    global currentDirector
    global ff
    ffname = fPath + fnameBase + "_directors.rtf"
    ff = open (ffname, "w")    # Overwrite the file if it already exists
    # Create introductory stuff for .rtf file
    ff.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
    ff.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    ff.write ("\\fs15" + "\n")    # Font size
    ff.write ("\\margl576")    # Margins
    ff.write ("\\margr576")
    ff.write ("\\margt576")
    ff.write ("\\margb576" + "\n")
    #
    ff.write (putIbnetdiscoverNameAndDate () + rtfEOL)
    ff.write (rtfEOL)
    showLegend ("DIRECTOR")
    ff.write ("\\page" + "\n")
    #
    for j, key in enumerate (allDirectors):
        currentDirector = allDirectors [key]
        showDirectorSummary (False)
        layout = currentDirector.directorLayout
      
        if layout == "18x1":    #
            showDirector18x1 ()
        elif layout == "12x2":
            showDirector12x2 ()
        elif layout == "9x2":
            showDirector9x2 ()
        elif layout == "10x2":
            showDirector10x2 ()
        ff.write ("\\page" + "\n")
    ff.write ("}\n")
    ff.close()

#### end of showAllDirectors ####

#### showAllSwitches ####
# Assumes analyzeBoxGraph has already been called, in order to set Nodes' nodeSwGroup attribute.
def showAllSwitches ():
    global fPath
    global fnameBase
    global ibNet
    global currentNode
    global ff
    swNameList = []
    ffname = fPath + fnameBase + "_switches.rtf"
    ff = open (ffname, "w")    # Overwrite the file if it already exists
    ff.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
    ff.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    ff.write ("\\fs15" + "\n")    # Font size
    ff.write ("\\margl576")    # Margins
    ff.write ("\\margr576")
    ff.write ("\\margt576")
    ff.write ("\\margb576" + "\n")
    ff.write (putIbnetdiscoverNameAndDate () + rtfEOL)
    ff.write (rtfEOL)
    showLegend ("SWITCH")
    ff.write (" " + rtfEOL)
    ff.write (" " + rtfEOL)
    #   
    switchList = []
    for j, guid in enumerate (ibNet):
        currentNode = ibNet[guid]
        if currentNode.nodeType == "S" and currentNode.nodeDirectorGUID == " ":    #Switch & not part of Director
            # Build a sort key to determine the ordering of Switches in report
            sn = currentNode.nodeDesc.split('"')[1].replace("MF0;","").ljust(20)    # Extract Switch name & omit MLNX "MF0;" prefix if present
            key = (currentNode.nodeSwGroup).zfill (3) + ":" + sn + "=" + guid
            switchList.append (key)
    slst = sorted (switchList)
    #for i in range (0, len(slst)):

    for j in range (len(slst)):
        guid = slst[j].rsplit("=")[1]    # Extract Switch Node GUID from end of list entry
        currentNode = ibNet [guid]
        sn = currentNode.nodeDesc[2:].rsplit('"')[0].replace('MF0;', '')    # Get Switch name, unquoted, remove MLNX 'MF0;' prefix if present
        swNameList.append (sn + "  GUID: " + currentNode.nodeGUID)
        showSwitchSummary (True)
        if (currentNode.nodeIBGen == "HDR") and (int(currentNode.nodePortCount) > 41):
            showSplitSwitch ()    # Split HDR switch
        elif (currentNode.nodeIBGen == "NDR") and (int(currentNode.nodePortCount) > 65):
            showSplitSwitch ()    # Split NDR switch
        else:
            showSwitch ()
    ff.write (" " + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write ("Switch Names  (" + str(len(swNameList)) + ")" + rtfEOL)
    ff.write ("============" + rtfEOL)
    lst = sorted (swNameList)
    for i in range (len(lst)):
        ff.write (lst [i] + rtfEOL)
    ff.write ("}\n")
    ff.close()
#### end of showAllSwitches ####

#####################################################################################
#### Begin routines to deal with HCAs.  In the past, we sort of ignored them.
#####################################################################################

#### setHCAAttributes ####
# Assume currentNode points to the HCA's Node structure.
# Set the HCA Node's IB generation (e.g. "HDR") and model (e.g. ConnectX-6".
def setHCAAttributes ():
    global currentNode
    global asicTable
    peerNodeGUID = [noPeer]    # For use by the peerExists routine
    peerLink = [" "]    # For use by the peerExists routine
    guid = currentNode.nodeGUID
    key = currentNode.vendorID + ":" + currentNode.deviceID
    if key in asicTable:
        currentNode = currentNode._replace (nodeIBGen = asicTable [key].ibGen)
        currentNode = currentNode._replace (nodeModel = asicTable [key].model)
    else:    # We don't know what it can do; get its current link speed(s)
        #print ("NOT FOUND ", key)
        gen = "SDR"    # Slowest possible IB generation
        ls = 4 * ibGenToLaneSpeed ["SDR"]    # Get the aggregate (4X) speed in Gbits/sec
        ports = int (currentNode.nodePortCount)
        for p in range (1, ports+1):
            if peerExists (guid, p, peerNodeGUID, peerLink):
                wxr = peerLink[0].linkWidthXRate   # Get the Link width and speed, e.g. "4xHDR"
                gen2 = wxr.split("x")[1]    # Get the IB generation string
                # NOTE: 2xHDR is a legitimate max speed (HDR100), e.g. a split port.  Could/should we detect that?
                ls2 = 4 * ibGenToLaneSpeed [gen2]    # Get the aggregate 4X speed in Gbits/sec
                if ls2 > ls:
                    gen = gen2    # Keep the fastest speed we've seen 
        currentNode = currentNode._replace (nodeIBGen = gen)
    ibNet [guid] = currentNode
#### end of setHCAAttributes ####

#### setAllHCAAttributes ###
def setAllHCAAttributes ():
    global ibNet
    global currentNode
    for i, key in enumerate (ibNet):
        if ibNet [key].nodeType == "H":
            currentNode = ibNet [key]
            setHCAAttributes ()
#### end of setAllHCAAttributes ####

#####################################################################################
#### Begin routines to generate warnings about the topology.  NOTE - no longer used.
#####################################################################################

#### analyzeISLs ####
# This routine analyzes the islDict dictionary, reporting inter-switch link bundles that start
# or end on non-contiguous ports.  It also generates an input file for OpenSM that will
# cause the IB routing engine to scan the ports in a more optimum sequence.
def analyzeISLs ():
    global fPath
    global fnameBase
    global islDict
    global ibNet
    global wf   # 'W' is for 'warning'  :-)
    # Open an RTF-formatted file in which to post the warnings.
    wfname = fPath + fnameBase + "_warnings.rtf"
    wf = open (wfname, "w")    # Overwrite the file if it already exists
    wf.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
    wf.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    wf.write ("\\fs15" + "\n")    # Font size
    wf.write ("\\margl576")    # Margins
    wf.write ("\\margr576")
    wf.write ("\\margt576")
    wf.write ("\\margb576" + "\n")
    #
    wf.write (rtfEOL)
    ff.write (putIbnetdiscoverNameAndDate () + rtfEOL)
    ff.write (rtfEOL)
    s = "NON-CONTIGUOUS INTER-SWITCH LINK PORTS:"
    badGUIDs = []    # Start a list of GUIDs that have ISL bundles with non-contiguous ports
    #   
    guids = list (islDict.keys())    # Make a list of all islDict switch Node GUIDs, instead of a dictionary
    guids = sorted (guids)    # Sort the switch GUIDs in ascending order 
    for j in range (len(guids)):
        nodeGUID = guids[j]
        peerGUIDDict = islDict [nodeGUID]
        issues = 0
        for i, peerGUID in enumerate (peerGUIDDict):
            l = peerGUIDDict [peerGUID]    # Sorted list of port #s connecting node to this peer
            n = len (l)
            if n > 1:    # If there are multiple links to this peer Switch
                a = l[0]    # Lowest port number on node (not peer) side
                b = l[n-1]    # Highest port number on node
                if not ((a+n-1)==b):    # Ports are not contiguous
                    wf.write (s + rtfEOL)
                    issues = issues + 1
                    s = "On " + nodeGUID + " links to " + peerGUID + " from ports "+ str(l).strip('[]')
        if not (issues == 0):
           badGUIDs = badGUIDs + [nodeGUID]
    wf.write (s + rtfEOL)
    if len(badGUIDs) == 0:
        wf.write (" " + rtfEOL)
        wf.write ("   NONE" + rtfEOL)
    else:
        # Create text lines for a port_search_ordering_file that can be used by OpenSM.
        wf.write ("---------------------" + rtfEOL)
        wf.write ("The following lines of text can be given to OpenSM to change the order that Switch ports" + rtfEOL)
        wf.write ("are scanned by the IB routing engine.  This will temporarily compensate for the use of " + rtfEOL)
        wf.write ("non-contiguous ports and should improve routing efficiency.  Usage with OpenSM is:" + rtfEOL)
        wf.write ("     -O, --port_search_ordering_file <path to file containing the text lines below>" + rtfEOL)
        wf.write ("---------------------" + rtfEOL)
        for j in range (len(badGUIDs)):    # Generate a set of text lines for a port_search_ordering_file
            nodeGUID = badGUIDs[j]
            peerGUIDDict = islDict [nodeGUID]
            portListDict = {}
            # Build a set (not a list) of all port #s on this switch, excluding 0.
            p = int (ibNet[nodeGUID].nodePortCount)
            portSet = set ()
            for i in range (p):
                portSet.add(i+1)
            s = "0x"+ nodeGUID + " "
            for i, peerGUID in enumerate (peerGUIDDict):
                l = peerGUIDDict [peerGUID]    # Sorted list of port #s connecting current node to this peer
                portListDict [l[0]] = l    # Create a dictionary of port lists, indexed by lowest port # in each list
                #print ("portListDict[", l[0], "] = ", portListDict[l[0]])
            lists = list (portListDict.keys())    # Convert dictionary to list
            lists = sorted (lists)
            #print ("lists: ",lists)
            # Note that some port lists may represent contiguous ports.  It only takes one non-contiguous port
            # list to cause a given Switch to deserve a line in the port_search_ordering_file.
            for k in range (len(lists)):    # Go through the port lists, in order of the first port in each list
                n = lists[k]    # n is a port number that starts one of the port lists
                l = portListDict [n]    # Get the corresponding port list
                s2 = str (l).strip('[]')    # Convert the port list to a string separated by commas
                # Now look at any 'gap' ports, in between ports in the port list.  If there are only a couple of
                # them and they are all open ports (no link connected), we'll assume they might represent
                # missing/broken cables.
                foundNonEmptyGap = False
                gapList = []
                m = l[len(l)-1]    # Get last port # in list
                while n < m:
                    if not (n in l):    # Port n isn't in this port list
                        linkStruct = getLinkStruct (nodeGUID, n)    # Get the Link structure for port n
                        #print("n=",n," currentLink=",currentLink)
                        if linkStruct.peerType == " ":    # If this port isn't connected to anyone
                            gapList = gapList + [n]
                        else:
                            foundNonEmptyGap = True    # There's a cable but it doesn't go to the right peer 
                    n = n + 1
                # If we found the right number of non-connected gap ports, append them to the original
                # port list.  The list is no longer in ascending order in this case.  Later, if someone
                # plugs a cable in the gap, it will be scanned by OpenSM immediately after the (presumably 
                # still-connected) ports and thus be discovered as a (logically) contiguous port.
                if not (foundNonEmptyGap) and (len (gapList) == 1):    # Only allow one gap for now
                    #print("gap ports: ", gapList)
                    l = l + gapList
                    s3 = str (gapList).strip('[]')    # Convert the gap port list to a comma-separated string  
                    s2 = s2 + " \i " + s3 + "\i0 "    # Append the selected gap port string, in italics
                s = s + s2 + " "
                # Remove all ports in list l from the portSet
                portSet = portSet - set(l)
            #print("remaining ports: ",portSet)
            # Append the remaining ports in the portSet to strings, in ascending order.  This will ensure
            # that newly added cables will be scanned although it doesn't ensure they'll be scanned optimally.
            l = sorted (list(portSet))
            s2 = "\i " + str (l).strip('[]') + "\i0"    # Convert remaining port set to a string separated by commas
            s = s + s2
            s = s.replace(",","")    # Now omit all commas
            wf.write (s + rtfEOL)
    wf.write ("}\n")
    wf.close()

#### end of analyzeISLs ####

#####################################################################################
#### Begin routines to create a _graphviz (.GV) file representing a graph of the topology.
#####################################################################################

#### getBoxGraph ####
# We now want to change to a physical view of the IB fabric and deal with switch enclosures (boxes) 
# instead of ASICs.  This routine gathers all of the boxes-- the Directors plus all of the switch 
# ASICs that aren't part of a Director.  Each box in the boxGraph dictionary is given an empty
# dictionary that will later be used to represent all of a box's neighboring boxes.
def getBoxGraph ():
    global ibNet
    global boxGraph
    boxGraph = {}
    for i, key in enumerate (ibNet):    # For every ASIC weve discovered
        currentNode = ibNet [key]    # Key = Node GUID
        dirGUID = currentNode.nodeDirectorGUID    # Pseudo-GUID of the associated Director, if any
        if (currentNode.nodeType =="S") and (dirGUID == " "):    # If a Switch that's not part of a Director
            boxGraph [key] = {}    # Add this Switch node & give it an empty dictionary of neighbors
            #print (key)
    for i, key in enumerate (allDirectors):    # For every Director we've discovered
        boxGraph [key] = {}    # Add the Director & give it an empty dictionary of neighbors
        #print (key)
#### end of getBoxGraph ####

#### connectBoxGraph ####
# Assumes getBoxGraph has been called, to build the boxGraph dictionary.
# Finds all of the links between the boxes in the boxGraph dictionary.  A count is kept of links
# between a given box pair.  We also count the total number of inter-box links and the number of 
# HCAs connected to each box.
# Each inter-box link will be represented twice, once from each end, due to the way that
# ibnetdiscover builds its report.  Duplicate inter-box links will be removed later.
def connectBoxGraph (): 
    global boxGraph
    global boxGraph2    # New-- add to description above
    global boxISLs
    global boxHCAs
    global boxesWithHCAs
    global maxISLs
    global boxesWithMaxISLs
    global ibNet
    global allDirectors
    boxGraph2 = {}
    boxHCAs = {}
    boxISLs = {}
    boxesWithHCAs = []
    boxesWithMaxISLs = []
    maxISLs = 0    # Keep track of the most inter-switch links we see on any box
    for i, key in enumerate (boxGraph):    # key is either a Node GUID or a Director pseudo-GUID
        #print("KEY ", key)    
        isls = 0    # Counts the total inter-box links from this box to other boxes
        hcas = 0    # Counts the total HCAs connected to this box
        nd = {}    # Start building a dictionary of this box's neighbors
        nd2 = {}    
        if key in ibNet:    # We have a Node GUID; this box is a single ASIC
            currentNode = ibNet [key]    
            k = int(currentNode.nodePortCount)    # Get the number of ports for this Switch
            for j in range (1, k + 1):    # Skip the entry for Port 0
                p = currentNode.nodePortList [j]    # Get Port structure
                if (p.portType == "IB" and p.portConnected == "Y"):    # Check for an IB connection
                    #print(j, " ", p) 
                    lnk = p.portLink    # Now look at the Link properties
                    if (lnk.peerType == "S") and (lnk.peerNodeGUID != key):    # If a Switch & not a loopback, add it to the neighbor dict
                        isls = isls + 1
                        key2 = lnk.peerNodeGUID
                        neighborNode = ibNet [key2]
                        dGUID = neighborNode.nodeDirectorGUID
                        if dGUID != " ":    # If this neigbor is part of a Director
                            key2 = dGUID
                        if key2 in nd:    #  Keep a count of the number of links to the same neighbor
                            nd[key2] = nd[key2] + 1    # Another Link has already been seen between these boxes
                            #print("dup: ", key, " ", key2, " ", nd[key2])
                            nd2[key2] = nd2[key2] + [str (j)]    
                        else:
                            #print("new ", key, " ", key2)    
                            nd[key2] = 1    # This is the first Link weve seen between these two boxes
                            nd2[key2] = [str (j)]
                    elif lnk.peerType == "H":    # If neighbor is an HCA
                        hcas = hcas + 1
        else:    # We have a Director pseudo-GUID
            dir = allDirectors [key]
            k = int (dir.directorMaxPorts)    # Get the # of possible ports
            peers = dir.directorPeerList
            for j in range (1, k + 1):    # Skip the entry for port 0
                peer = peers [j]
                if peer.peerNodeType == "S":    # This neighbor is a Switch (or part of a Director)
                    key2 = peer.peerNodeGUID
                    neighborNode = ibNet [key2]
                    dGUID = neighborNode.nodeDirectorGUID
                    if dGUID != " ":    # If this neigbor is part of a Director
                        #print ("CONNECTBOXGRAPH: ", key2, " ", dGUID)    #
                        key2 = dGUID
                    if key != key2:    # If not a loopback to current Director
                        isls = isls + 1
                        if key2 in nd:    #  Keep a count of the number of links to the same neighbor
                            nd[key2] = nd[key2] + 1    # Another Link has already been seen between these boxes
                            #print("dup: ", key, " ", key2, " ", nd[key2])
                            nd2[key2] = nd2[key2] + [str(j)]
                        else:
                            #print("new ", key, " ", key2)
                            nd[key2] = 1    # This is the first Link weve seen between these two boxes
                            nd2[key2] = [str(j)]
                elif peer.peerNodeType == "H":
                    hcas = hcas + 1
        boxGraph [key] = nd    # Associate the neighbor directory with the box
        boxGraph2 [key] = nd2
        #print ("nd = ", nd)
        boxHCAs [key] = hcas
        if hcas > 0:
            if not (key in boxesWithHCAs):
                boxesWithHCAs = boxesWithHCAs + [key]
        boxISLs [key] = isls
        if isls > maxISLs:    # This box has the most inter-switch links we've seen
            maxISLs = isls
            boxesWithMaxISLs = [key]
        elif isls == maxISLs:
            boxesWithMaxISLs = boxesWithMaxISLs + [key]
    #print ("ZZZZZZZ boxGraph (still has duplicate links): ", boxGraph)        
#### end of connectBoxGraph ####

#### buildBoxFingerprints ####
# Call this *after* connectBoxGraph but *before* RemoveDuplicateLinks.
# NOTE: some of the resulting data structures may end up not being used.  Need to ditch those...
def buildBoxFingerprints ():
    global boxHCAs
    global boxFingerprints
    global boxNeighbors
    global boxClade
    global boxesWithSameNeighbors
    global boxesWithSameFingerprints
    global cladesWithSameNeighbors
    boxFingerprints = {}
    boxNeighbors = {}
    boxClade = {}
    boxesWithSameNeighbors = {}
    boxesWithSameFingerprints = {}
    cladesWithSameNeighbors = {}
    bgl = sorted (list (boxGraph.keys()))    # Make a list from boxGraph.  Sorting it helps all derived lists to be sorted. 
    for i in range (len(bgl)):    # For each Node GUID or Director GUID in boxGraph
        key = bgl [i]
        if key in ibNet:
            node = ibNet [key]
            c = node.nodeModel + "/" + node.nodePortCount
        else:
            dir = allDirectors [key]
            c = dir.directorModel + "/" + dir.directorMaxPorts
        c = c + "/" + str(boxISLs[key]) + "/" + str(boxHCAs[key])    # c now has <model>/<max ports>/<# of ISLs>/<# of HCAs>
        boxClade [key] = c
        sn = "{"    # Start building a different string listing only the box's neighbors
        nd = boxGraph [key]    # Get the dictionary of this box's neighbors
        nl = sorted (list (nd.keys()))    # Convert to a sorted list of neighbor GUIDs
        for j in range(len(nl)):    # Get each of the neighbor NodeGUIDs (and the # of links to it)
            ng = nl [j]    # Get neighbor GUID
            #sn = sn + ng+ ":" + str (nd [ng]) + ","    # Add the neighbor GUID and the # of links to it
            sn = sn + ng + ","    # Add the neighbor GUID but not the # of links to it
        sn = sn + "}"
        s = c + sn    # Append the neighbor GUID list to the Switch info
        boxFingerprints [key] = s
        boxNeighbors [key] = sn
        # Use the neighbor string as a key into a dictionary.  Each dict entry lists boxes with those neighbors
        if sn in boxesWithSameNeighbors:
            boxesWithSameNeighbors [sn] = boxesWithSameNeighbors [sn] + [key]
            cladesWithSameNeighbors [sn] = cladesWithSameNeighbors [sn] + [c]
        else:
            boxesWithSameNeighbors [sn] = [key]
            cladesWithSameNeighbors [sn] = [c]
        # Use the fingerprint string as a key into a dictionary.  Each dict entry lists boxes with those fingerprints
        if s in boxesWithSameFingerprints:
            boxesWithSameFingerprints [s] = boxesWithSameFingerprints [s] + [key]
        else:
            boxesWithSameFingerprints [s] = [key]
    #print ("FFFFFFF boxesWithSameFingerprints", boxesWithSameFingerprints)
#### end of buildBoxFingerprints ####

#### removeDuplicateLinks ####
# Prepare the boxGraph dictionary to draw a diagram of the connections between its nodes.
# Assumes connectBoxGraph has been run, which finds all the inter-node connections but each
# link is represented twice once for each end of the connection.
# For each node N in boxGraph, it looks through Ns neighbor dictionary and for each neighbor J
# it removes the entry for node N in Js neighbor dictionary (it removes itself as the neighbors neighbor)..
#  As a result, a link is now represented only once in boxGraph.
def removeDuplicateLinks ():
    global boxGraph
    #print ("BOXGRAPH: ", boxGraph)    #
    for i, key in enumerate (boxGraph):   # For each Node GUID or Director GUID in boxGraph
        nd = boxGraph [key]    # Get the dictionary of neighbors
        for j, key2 in enumerate (nd):    # Get each of the neighbor Node GUIDs
            nd2 = boxGraph [key2]   # Get the neighbors dictionary of neighbors
            if key in nd2:   # As expected, my neighbor lists me as *his* neighbor
                #print ("Removed a link")
                del nd2 [key]    # Take me off his list
            else:
                print ("yikes! no matching neighbor for", key, " in ", key2)
#### end of removeDuplicateLinks ####

#### countLinks ####
# Counts how many links exist between all of the switches in the boxGraph dictionary.  These are
# logical links (neighbor relationships) not cables.
def countLinks ():
    global boxGraph
    j = 0
    for i, key in enumerate (boxGraph):   # For each Node GUID or Director GUID in boxGraph
        nd = boxGraph [key]    # Get the dictionary of neighbors
        j = j + len (nd)    # Add the number of neighbor entries to the total
    #print ("Links: ", j)
#### end of countLinks ####

#### addBoxAndItsPeersToThisRank ####
# Helper routine for analyzeBoxGraph.
# Assume thisRank list is initialized by the caller.
def addBoxAndItsPeersToThisRank (key):
    global thisRank
    global boxesLeft
    global boxNeighbors
    global boxesWithSameNeighbors
    myNeighbors = boxNeighbors [key]    # Get a string listing all boxes I'm connected to
    # In a Clos or fat tree, boxes are connected north-south but not east-west.
    myPeers = boxesWithSameNeighbors [myNeighbors]    # Get a list of boxes whose neighbors are my neighbors
    for j in range (len(myPeers)):    # Add myself and my peers to thisRank list
        guid = myPeers [j]
        thisRank = thisRank + [guid]    # Add GUID (or Director pseudo-GUID)
        del boxesLeft [guid]    # Remove it from 'to analyze' list    
#### end of addBoxAndItsPeersToThisRank ####

#### matchMultiplePatterns ####
# This routine applies a list of regular expressions against a single string, and returns the list index
# of the first match.  It returns -1 if there are no matches.
# There's probably a clever way to build a single regular expression that combines all of the list
# entries, e.g. using "|", and thus do a single re.match operation, but brute force is used here.
def matchMultiplePatterns (candidate, patternList):
    matched = -1
    l = len (patternList)
    i = 0
    while i < l:
        if bool (re.match (patternList[i], candidate)):
            matched = i
            i = l
        i = i + 1
    return (matched)
#### end of matchMultiplePatterns ####

#### analyzeBoxGraph ####
# This routine attempts to find the roots and leafs of the topology in boxGraph,  It assumes 
# removeDuplicateLinks has NOT been called (should call it *after* calling AnalyzBoxGraph).
# The results are intended for use by generateGraphViz:  a set of "max rank" boxes (L1 leafs) 
# and a set of "min rank" boxes (roots), and possibly other ranks in between. 
# An algorithm that works pretty well: pick all boxes that have HCAs attached as L1 leafs 
# and then move up the tree layer by layer.  Possible refinements include ignoring Gateways
# if their only HCA is the internal one, and picking as roots those boxes whose inter-box link
# count is within X% of the max.
def analyzeBoxGraph ():
    global thisRank ####
    global nextRank ####
    global boxesLeft ####
    global boxGraph
    global boxHCAs
    global boxRankLists
    global boxesWithSameNeighbors
    global algorithm
    global switchL1NamePatterns
    global ibNet
    boxRankLists = []
    algorithm = 1
    if algorithm == 0:
        print ("algorithm 0")
        print ("IMPLEMENT ME")
    else:    #### DON'T call removeDuplicateLinks BEFORE this or it WON'T WORK !!!!!!####
        #print ("algorithm 1")
        thisRank = []    # Initially this list represents the L1 leaf boxes (will be "max rank" in .gv terms)
        boxRankLists = []
        boxRank = 1    # Ranks start from L1
        boxesLeft = boxGraph.copy()    # We will remove boxes as we process them
        # Currently we treat any box with HCAs as an L1 Switch.  At some point we could skip boxes that
        # only have a virtual HCA, e.g. Gateways, or Switches with a SHARP Aggregation Node enabled.
        #for i, key in enumerate (boxGraph):
            #if key in boxesLeft:    # If this box hasn't already been seen & removed:
                #if boxHCAs [key] > 0:    # This box is connected to HCAs
                    #thisRank = thisRank + [key]    # Add to ...
        for i, key in enumerate (boxGraph):
            if not (key in thisRank):    # Skip it if we've already handled it
                nl = boxNeighbors [key]    # Get the list of this box's neighbors (GUIDs), as a key into bWSN dict
                boxList = boxesWithSameNeighbors [nl]    # Get a list of GUIDs of boxes that share the neighbors
                foundL1s = False
                for k in range (len(boxList)):    # Iterate through these similiar boxes & see if they should be L1 switches
                    guid = boxList [k]
                    if guid in allDirectors:    # If box is a Director
                        desc = allDirectors [guid].directorDesc
                        specialHCAs = 0
                    else:    # Box is a Switch
                        desc = ibNet[guid].nodeDesc[2:].rsplit('"')[0].replace('MF0;', '')    # Get Switch name, strip double quotes, omit MLNX 'MF0' prefix if present
                        specialHCAs = int(ibNet[guid].nodeSpecialHCAs)
                    nameMatch = matchMultiplePatterns (desc, switchL1NamePatterns) >= 0    # See if idesc matches the GUI-provided name matching template(s)
                    if nameMatch:    #### DEBUG ####
                        print ("L1 MATCH: ", desc, " ", guid)    #### DEBUG ####
                    if (boxHCAs [guid] > specialHCAs) or nameMatch:    # If this box has HCAs or its name matches a template we deem it an L1
                        foundL1s = True
                if foundL1s:
                    thisRank = thisRank + boxList    # Add the whole list to the L1 leaf box list, even if some have no HCAs 
        #boxRankLists.append (thisRank)
        #### Someday should also inspect the L1s for groups that aren't connected to one another...
        # Now we move up the tree, layer by layer, until we run out of boxes.
        while len(boxesLeft) > 0:    
            #print (len(boxesLeft))
            #print (len(thisRank), ":", thisRank)
            for i in range (0, len (thisRank)):    # Loop through our list & omit from the boxesLeft dictionary
                key = thisRank [i]
                if key in boxesLeft:
                    del boxesLeft[key]
            nextRank = []
            for i in range (0, len(thisRank)):
                key = thisRank [i]
                if key in ibNet:
                    ibNet[key]=ibNet[key]._replace (nodeSwGroup = str(boxRank))    # Use this opportunity to set Switch Node's group attribute
                    #print ("YES!!!! ", key)  
                nd = boxGraph [key]    # Get dictionary of box's neighbors
                for j, key2 in enumerate (nd):
                    if key2 in boxesLeft:
                        if not (key2 in nextRank):
                            #print("found ", key2)    #
                            nextRank = nextRank + [key2]
                #del boxesLeft[key]
            # Now we have a list (nextRank) of all the neighbors of the previous rank (thisRank).
            # IB switch tiers typically contain boxes that connect upward and downward but not
            # within the tier itself.  We will inspect thisRank and try to find the group(s) of
            # boxes that are not connected to one another, and generate a separate rank for            
            # each so they will be visually separated when drawn.
            tempRank = thisRank[:]    # Make a copy of the list
            while len(tempRank)>0:
                key = tempRank [0]
                nd = boxGraph [key].copy()
                #print ("initial nd ", nd)
                group = [key]
                for i in range (1, len(tempRank)):
                    key2 = tempRank [i]
                    #print ("len(tempRank ", len(tempRank), " key2 ", key2)
                    if not (key2 in nd):
                        nd2 = boxGraph[key2]
                        #print ("nd2 ", nd2)
                        nd.update(nd2)
                        #print ("new nd ", nd)
                        group = group + [key2]
                #print("group ", group)
                for i in range (0, len(group)):
                    key2 = group [i]
                    tempRank.remove(key2)
                boxRankLists.append(group)
                boxRank = boxRank + 1
            thisRank = nextRank
            #print("xxxx ", thisRank)
#### end of analyzeBoxGraph ####

#linkColor = [ \
#   "red", "black", "blue", "green", "purple", "orange", "darkgreen", "aqua", "cyan", "magenta", \
#   "lightgray", "yellowgreen", "navajowhite", "lightblue", "darkgray", "deeppink"];
# Paul Tol's 21-color "Palette 1": 
#linkColor = [ \
#   '"#77aadd"', '"#77cccc"', \
#   '"#88ccaa"', '"#dddd77"', '"#ddaa77"', '"#dd7788"', '"#cc99bb"', '"#4477aa"', '"#44aaaa"', '"#44aa77"', \
#   '"#aaaa44"', '"#aa7744"', '"#aa4455"', '"#aa4488"', '"#114477"', '"#117777"', '"#117744"', '"#777711"', \
#   '"#774411"', '"#771122"', '"#771155"'];
#
# This table Will be indexed by the number of parallel links between two nodes. Uses Paul Tol's 9-color 
# continuous rainbow palette for the common numbers of parallel links: 2, 3, 4, 6, 8, 9, 12, 16, 18; 
# black is used for a single link.  Uses other colors to indicate oddball link counts.
linkColorOld = [ \
    "red", "black", '"#781c81"', '"#3f4ea1"', '"#4683c1"', "navajowhite", '"#57a3ad"', "lightyellow", '"#6db388"', \
    '"#b1be4e"', "yellow", "yellow", '"#dfa53a"', "darkyellow", "darkyellow", "lightgray", '"#e7742f"', "gray", \
    '"#d92120"', "darkgray", "darkgray", "darkgray", "darkgray", "darkgray", "darkgray", "darkgray", "darkgray", \
    "darkgray", "darkgray", "darkgray", "darkgray"]; 
# Link color scheme for trunk width, based on resistor color codes 
# (entry 0 is used when cable count exceeds color table length):
linkColor = [ \
    "darkgray", "brown", "red", "orange", "yellow", "green", "blue", "violet", "lightgray", "navajowhite", \
    "black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "lightgray", "navajowhite", \
    "black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "lightgray", "navajowhite"];
# Link color scheme based on optimal speed
linkColorDict = { \
    "4xSDR" : "Red", "4xDDR" : "Brown", "4xQDR" : "Yellow", "4xFDR10" : "Green", "4xFDR" : "Orange", \
    "4xEDR" : "Blue", "2xHDR" : "Lightgray", "4xHDR" : "Black", "4xNDR" : "Violet"};

#### testLinkColors ####
def testLinkColors ():
    global fPath
    global LinkColor
    gvname = fPath + "linkcolortest.gv"
    gv = open (gvname, "w")    # Overwrite if it already exists
    # Create a .gv file and set some introductory attributes
    gv.write ("graph linkcolortest {\n")
    gv.write ('splines = "false";\n')
    gv.write ('node [shape = "rectangle", fontsize = 4, width=0.1, fixedsize=true];\n')
    gv.write ('ranksep = "1 equally";\n')    # Request 1 inches between ranks
    for i in range (0, len(linkColor)-1):
        a = "a" + str(i) 
        b = "b" + str(i)
        gv.write (a + ' [label="."]\n')
        gv.write (b + ' [label="."]\n') 
        gv.write (a + "--" + b + " [color=" + linkColor[i] + ", label=" + linkColor[i]+ ", penwidth=50];\n")
        gv.write ("{rank=same " + a + " " + b + "};\n")  
    gv.write ("}\n")
    gv.close ()
#### end of testLinkColors ####

#### getBoxSwitchName ####
# The swguid parameter is the GUID of the Switch to be processed, or
# the pseudo-GUID of a Director.
# If the flag parameter is True, this routine returns TWO values:
# - The Graphvizfont size (as a string) to use for the Switch text box
# - A Switch name string ending with a newline code; it may contain 
#   additional newlines to split it into multiple lines.
# If the flag parameter is False, the Graphviz font size will equal
# the defaultfontsize parameter and the Switch name string will be empty.
# The defaultfontsize parameter is a string representing a Graphiz 
# font size.  
# Note that formatting box text with GraphVizio is very very inflexible; 
# it only implements a small subset of what GraphViz can do.  We try
# to achieve similar box widths for different font sizes; the box
# heights are allowed to vary somewhat. 
def getBoxSwitchName (flag, swguid, defaultfontsize):
    global ibNet
    global allDirectors
    fs = defaultfontsize
    s = ""
    if flag:    # Should we insert the Switch name?
        if swguid in allDirectors:
            sname = allDirectors [swguid].directorDesc    # User-assigned name
            nlength = len (sname)
            if nlength <13:    
                fs = "20"    # Graphviz font size
                lines = 1
                chars = 12    # Chars per line
            elif nlength < 29:
                fs = "12"
                lines = 2
                chars = 14
            elif nlength < 55:
                fs = "10"
                lines = 3
                chars = 18
            else:
                fs = "8"
                lines = 4
                chars = 26 
        else:
            swdesc = ibNet [swguid].nodeDesc    # Get the entire Node Desc string
            sname = swdesc.rsplit ('"', 1)[0]    # Start extracting the user-assigned Switch name
            sname = sname[2:].replace ('MF0;', "")    # Continue removing unwanted goop from Node Desc
            nlength = len (sname)
            if nlength < 11:
                fs = "8"    # Graphviz font size
                lines = 1
                chars = 10    # Chars per line
            elif nlength < 29:
                fs = "5"
                lines = 2
                chars = 14
            elif nlength < 55:
                fs = "4"
                lines = 3
                chars = 18
            else:
                fs = "3"
                lines = 4
                chars = 26    # Chars per line
        #print (len(sname), sname)
        s2 = sname + " " * (lines * chars)    # Pad the heck out of it
        for l in range (0, lines):
            s = s + s2 [l * chars : (l + 1) * chars] + "\\n"
    return (fs, s)
#### end of getBoxSwitchName ####

#### shortID ####
def shortID (id):
    if len (id) < 7:
        return (id)    # Already short enough (e.g. a Director peudo-GUID)
    else:    # It is presumably a long GUID string
        return (id [-6:])
#### end of shortID ####

#### putBoxDesc ####
def putBoxDesc (key, outlineColor, fontColor, fillColor):
    global ibNet
    global allDirectors
    global boxHCAs
    global boxISLs
    global putSwitchNamesInBoxes
    #print ("putBoxDesc: ", key, " ", outlineColor, " ", fontColor)    ###########
    s = '"' + key + '" [color = ' + outlineColor + ', fontcolor = ' + fontColor + ', fillcolor = ' + fillColor
    if key in allDirectors:
        ports = allDirectors[key].directorMaxPorts    # A string
        #fontSize = '"60"'
        fontSize = '"20"'    #### DEBUG / TESTING ####
        model = allDirectors[key].directorModel
        #swn = ""    # In the future, maybe set this to the Director name
        fontSize, swn = getBoxSwitchName (putSwitchNamesInBoxes, key, fontSize)
    else:
        ports = ibNet[key].nodePortCount    # A string
        #fontSize = '"24"'
        fontSize = "8"    #### DEBUG / TESTING ####
        model = ibNet[key].nodeModel
        fontSize, swn = getBoxSwitchName (putSwitchNamesInBoxes, key, fontSize)
    s = s + ', fontsize = ' + fontSize + ', label = "' + swn + shortID (key) + '\\n'  
    #s = s + shortID (key) + '\\n'    #### EXPERIMENTAL ####  Putting multiple GUIDs per box
    s = s + model + '\\n'
    # The next text line in the box has the form ppp:sss+hhh.  We like having the box be
    # auto-resized so that Directors are bigger than leaf Switches, but we don't want
    # auto-resizing otherwise, e.g. some Director boxes being bigger than others.
    s3 = ports + ':' + str (boxISLs[key]) + '+' + str (boxHCAs[key])
    pl = len (ports)    # Number of digits in port count
    w = (pl * 3) + 2    # Max width of the 3rd text line, for a given # of digits in the port count
    s = s + s3.center (w) + '"]'    # Pad s3 with blanks if necessary
    return (s)
#### end of putBoxDesc ####

#### putStackedBox ####
# Applies only to L1 Switches, not Directors or Switches in other tiers.
def putStackedBox (guid, outlineColor, fontColor, stackedL1s):
    global ibNet
    global boxHCAs
    global boxISLs
    fillColor = "white"
    #s = putBoxDesc (guid, outlineColor, fontColor, fillColor)
    s = '"' + guid + '" [color = ' + outlineColor + ', fontcolor = ' + fontColor + ', fillcolor = ' + fillColor
    ports = ibNet [guid].nodePortCount    # A string
    fontSize = '"24"'
    fontSize = "8"    #### DEBUG / TESTING ####
    model = ibNet [guid].nodeModel
    s = s + ', fontsize = ' + fontSize + ', label = "' + shortID (guid) + '\\n'  
    s = s + model + '\\n'
    # The third text line in the box has the form ppp:sss+hhh.
    s3 = ports + ':' + str (boxISLs [guid]) + '+' + str (boxHCAs [guid])
    pl = len (ports)    # Number of digits in port count
    w = (pl * 3) + 2    # Max width of the 3rd text line, for a given # of digits in the port count
    s = s + s3.center (w) + '\\n'   # Pad s3 with blanks if necessary
    sL1s = str (stackedL1s)
    y = 10 - len (sL1s) - 2    # 4th line will be padded to 10 chars
    s = s + "." + (y * " ") + "x" + sL1s + '"]'    # 
    return (s)
#### end of putStackedBox ####

#### putBox ####
# Note:  Could move more of the box-drawing piece from putBoxDesc into this routine.
def putBox (key, outlineColor, fontColor):
    global ibNet
    global allDirectors
    global boxHCAs
    global boxISLs
    fillColor = "white"
    if key in ibNet:    # Special case for IB Router boxes
        if ibNet [key].nodeModel == "vRouter":   # Virtual IB Router
            fillColor = "ivory"
    s = putBoxDesc (key, outlineColor, fontColor, fillColor)
    return (s)
#### end of putBox ####

#### getTrunkAttributes ####
# On Visio output, a line between Boxes may represent a 'trunk' of N physical links.
# This routine provides additional data about the trunk, as a 3-tuple list:
# - trunkGood: True if each link runs at its optimal width & speed (links might not all be the same)
# - trunkBestWXR:  the width & rate of the fastest link(s) in the trunk (e.g. 2XHDR")
# - number of links in the trunk (decimal)
def getTrunkAttributes (guid1, guid2):
    global portSpeed
    trunkBestWXR = "1xSDR"
    trunkBestWidth = 1
    trunkBestRate = 1
    trunkGood = True
    nd2 = boxGraph2 [guid1]
    islPortList = nd2 [guid2]
    isls = len (islPortList)
    for i in range (0, isls):
        port1 = islPortList[i]    # (string)
        tuple = portSpeed [guid1 + ":" + port1]
        #islActualWXR = tuple [0]    # We don't need this for our purposes
        islGood = tuple [1]
        islBestWXR = tuple [2]    # 
        trunkGood = trunkGood and islGood
        islBestWidth = int (islBestWXR[0])    # E.g. 4 for "4x"
        islBestRate = ibGenToLaneSpeed [islBestWXR[2:]]
        if (islBestWidth * islBestRate) > (trunkBestWidth * trunkBestRate):
            trunkBestWidth = islBestWidth
            trunkBestRate = islBestRate 
            trunkBestWXR = islBestWXR
    return ([trunkGood, trunkBestWXR, isls]) 
#### end of getTrunkAttributes ####

#### generateGraphViz ####  
# Assumes removeDuplicateLinks has already been called, to cut the number of graph edges in half.
# This routine generates a .gv file that can be used to vizualize the IB topology using either GraphViz
# or a Visio add-in called GraphVizio.  At this time, GraphVizio is more restrictive than GraphViz so we
# restrict ourselves to features common to both as of GraphViz v2.38.0 and GraphVizio v1.1.6
# (from bitbucket.org/cowhamr, slightly improved from Maurice Calvert's version).
# Known limitations of GraphVizio include: graphs must have names; no HTML labels (!); cannot use
# headport or tailport.
# The general structure of a .gv file is:
# - Some setup stuff, defaults, etc.
# - Define a set of boxes, each with a name (in this case a GUID usually), outline shape, and text
# - Define 'ranks' which are lists of box names that should be drawn on the same level
# - Define the lines to be drawn between pairs of boxes
#  Note:  GraphViz has a concept of box ranking where boxes in 'high' ranks are drawn 'below' boxes
# in 'lower' ranks.  (I think this can be inverted).  As it is, this is exactly the opposite of how this 
# Python program creates ranks of boxes, in which rank 0 is meant to be leaf Switches that will be
# drawn at the bottom (max rank) of the Visio page.  Confusing.
# Note:  GraphVizio likes to re-size boxes; I haven't found the right attributes to stop this 100%.
# It helps to use a fixed-pitch font and keep the longest string length consistent among all boxes.
def generateGraphViz ():
    global fPath
    global fnameBase
    global boxGraph
    global gv
    global minRankBoxes    ####
    global maxRankBoxes    ####
    global sameRankBoxes    ####
    global BoxHCAs
    global BoxISLs
    global boxRankLists
    global linkColor
    global dontDrawBox
    global boxClade
    global boxNeighbors 
    global cladeList    ####
    global gvL1BoxesToStack
    global genTimeAndDate
    global showCableCount
    global lineScheme
    global sawWXR
    dontDrawBox = {}
    # Create a .gv file and set some introductory attributes
    gvname = fPath + fnameBase + "_graphviz.gv"
    gv = open (gvname, "w")    # Overwrite if it already exists
    gv.write ("graph ibnetdiscover {\n")
    gv.write ('splines = "line";\n')    # Straight lines between boxes
    #gv.write ('forcelabels = "true";\n')    ###### EXPERIMENTAL ######
    gv.write ('node [shape = "rectangle", fontsize=24, fontname="Lucida Console"];\n')    # Default gv box
    gv.write ('ranksep = "8 equally";\n')    # Request 8 inches between ranks
    gv.write ('nodesep = "0";\n')    # Tighten up the spacing within each row of boxes
    # Create a gv node that will serve as the graph caption
    s = '"caption" [style = invis, fontcolor = black, fontsize = 24, label = "' + "'" + fnameBase + "'\\n"
    s = s + 'Generated\\n' + genTimeAndDate + '\\n'
    s = s + 'Analyzed\\n' + ctime()
    if (gvL1BoxesToStack > 1):
        s = s +'\\nSOME L1 SWITCHES MIGHT NOT BE SHOWN'
    s = s + '"]\n'
    gv.write (s)
    # Create gv nodes that will be drawn as the graph legend
    s = '"legend1" [color = green, fontcolor = green, fontsize = 20, fontname = "Lucida Console", ' 
    s = s + 'label = "gggggg\\nmmmmm\\npp:sss+hhh"]\n'
    gv.write (s)
    s = '"legend2" [style = invis, fontcolor = green, fontsize = 20, fontname = "Lucida Console", '
    s = s + 'label = "BOX LEGEND\\nLast digits of Switch GUID\\nSwitch Model\\nTotal ports: Links to Switches +\\nLinks to HCAs"]\n'
    gv.write (s)
    l3 = ''
    if lineScheme == 1:
        # NOTE: this only handles the default line color scheme-- NEED TO ADD the other scheme(s) ###
        s = '"legend3" [style = invis, fontcolor = black, fontsize = 20, fontname = "Lucida Console", '
        s = s + 'label = "LINE STYLE:\\nWidth: # of Links'
        for i, key in enumerate (sawWXR):
            s = s + '\\n' + linkColorDict.get (key, "Brown") + ': ' + key  
        s = s + '\\nDashed: Slow Link(s)'
        gv.write (s + '"]\n')
        l3 = ' "legend3"'
    # Boxes with the highest gv rank will be drawn at the bottom of the diagram; we hope they are Level 1 (L1) Switches       
    
      
    s = '{rank = max "legend1" "legend2"' + l3    # Begin the string that lists 'max rank' boxes; it includes the legend boxes
    maxRankBoxes = boxRankLists [0]    # The L1 Switches are always in list 0 in the list of rank lists
    cladeList = {}    #
    #print("MAXRANKBOXES ------ ", maxRankBoxes)
    for i in range (len(maxRankBoxes)):    #
        guid = maxRankBoxes [i]
        clade = boxClade [guid] + boxNeighbors [guid]    # The combined strings are the dictionary key
        if not (clade in cladeList):
            cladeList [clade] = [guid]
        else:
            cladeList [clade] = cladeList [clade] + [guid]
    #print("cladeList  ", cladeList)
    for i, key in enumerate (cladeList):
        boxList = cladeList [key]    # Get the list of boxes having the same key
        nb = len(boxList);    # Total # of boxes
        k = 0
        while k < nb:
            ns = min (gvL1BoxesToStack, nb - k);     # Compute # of boxes in this stack
            guid1 = boxList [k]
            s = s + ' "' + guid1 + '"' ;   # Add the 1st box name to the max rank list
            sgl = ""    # List of Short IDs for boxes in this stack
            for m in range(ns):
                guid = boxList[k]
                sgl = sgl + shortID (guid) + "\\n"
                dontDrawBox [guid] = "X"    # Just need to create a dictionary entry DO WE NEED THIS?
                k = k + 1;
            sgl = sgl [:-2]    # Trim off final newline
            fc = "green"    # Font color for .gv box
            if ns > 1:
                print ("STACK:  ", sgl)
            # remove the 1st dontDrawBox entry added for this box stack
            del dontDrawBox [guid1]
            #### TEMPORARILY DONT SHOW THE FULL LIST OF GUIDs in the STACK
            if ns> 1: 
                fc = "purple"
                gv.write (putStackedBox (guid1, "green", fc, ns) + '\n')    # Generate a .gv text line defining a box representing N L1 switches
            else:
                gv.write (putBox (guid1, "green", fc,) + '\n')    # Generate a .gv text line defining each Switch box in rank=max 
    gv.write (s + "}\n")    # Now output the set of Switch box names at rank = max, plus legend
    # Boxes with the lowest .gv rank will be drawn at the top of diagram; we hope they are Spine switches
    s = '{rank = min "caption"'
    if len (boxRankLists) > 1:    # Don't do anything more if it's a degenerate topology (only one rank)
        minRankBoxes = boxRankLists [len (boxRankLists) - 1]    # Get the last list in the list of rank lists
        for i in range (0, len (minRankBoxes)):
            key = minRankBoxes [i]
            s = s + ' "' + key + '"'
            gv.write (putBox (key, "blue", "blue") + '\n')    # Generate a gv text line defining each Switch box in rank=min
    gv.write (s + ' }\n')    # Now output the set of Switch box names at rank=min, plus caption
    # The remaining ranks of boxes (if any) are each grouped as "rank = same"
    if len(boxRankLists) > 2:    # Are there intermediate ranks?
        for r in range (1, len (boxRankLists) - 1):
            s = "{rank = same"
            sameRankBoxes = boxRankLists [r]    # Get the next list of boxes that have been ranked together
            for i in range (0, len (sameRankBoxes)):
                key = sameRankBoxes [i]
                s = s + ' "' + key + '"'
                gv.write (putBox (key, "black", "black") + '\n')
            gv.write (s + "}\n")    
    # Now describe the links (edges) between all boxes.  Each line represents a number of parallel cables.
    # We vary each line's attributes based on how many parallel cables it represents.
    links = 0

           
    for i, key in enumerate (boxGraph):   # For each Node GUID or Director GUID in boxGraph
        nd = boxGraph [key]    # Get the dictionary of neighbors             
        for j, key2 in enumerate (nd):    # Get each of the neighbor GUIDs
                    s = '"' + key + '" -- "' + key2 + '" ['
                    cables = nd [key2]    # Get number of cables to this neighbor
                    tuple = getTrunkAttributes (key, key2)
                    if not tuple[0]:    # If trunk contains at least one sub-optimal link
                        s = s + "style=dashed,"
                    if lineScheme == 1:
                        s = s + "penwidth=" + str(cables) + ","
                        ################## DEBUG ########
                        s2 = linkColorDict.get (tuple[1], "darkgray")
                        #print("TUPLE: ", tuple)
                        s = s + "color=" + s2 + ","
                    else:    # lineScheme = 2
                        w = int((cables - 1) / 10)
                        s = s + "penwidth=" + str(2*(w + 1)) + ","
                        s = s + "color=" + linkColor [cables - (w*10)] + ","
                    if cables >= showCableCount:
                        s = s + 'labelfloat=false, label="' + str (cables) + '",'
                    s = s[:-1] + "]"    # Trim trailing comma and close line (edge) attribute brackets
       
                    #if cables >= len (linkColor):
                    #cables = 0    # Use entry 0 of link color table
                    #color = linkColor [cables]
                    #s = s + "color = " + color + "]"
                    links = links + 1
                    dropIt = not ((links % 1) == 0) or (key in dontDrawBox) or (key2 in dontDrawBox)
                    if not dropIt:   # If this link isn't to be dropped            
                        gv.write (s + ";\n")
 
    gv.write ("}\n")
    gv.close ()
    return gvname
 
#### end of generateGraphViz ####

###########################################################################################################################################################
########################## This is to check invalid LID number ############################################################################################

def check_Invalid_lid () : 

    global warn_return   #This is to warn Invalid unicat LID number
    global warn_return1  #This is to warn Mcast LID number
    global fnameBase
    global fPath
    global fExt
                
    fname = fPath + fnameBase + "." + fExt    # Assemble the strings returned by doGUI     
    f = open(fname,'rt', encoding='UTF8')
    temp_f = f.readlines()
 
        
    for i in temp_f :
        hi = i.split(" ")
        hi = [x for x in hi if x != '']
        
        for d, key in enumerate (hi):
            if key == 'lid':
        
                if  'DR' in hi[d+1] or 'lmc' in hi[d+1]  :
                    warn_return.append(i)
                    continue
                      

           
                if hi[d+1].isdigit() :            
                    temp_int = int(hi[d+1])
                                    
                    if (temp_int < 1)  or (temp_int >= 65535) : 
                        warn_return.append(i)

                                            
                    if  (temp_int > 49151) and (temp_int < 65535) :
                        warn_return1.append(i)
              
                else : 
                    warn_return.append(i)
######################################### End of the function #############################################################################################


#####################################################################################
#### Begin routines to generate a report summarizing fabric HCAs by name, and where they attach.
#####################################################################################

#### makeHCADescsUnique ####
def makeHCADescsUnique ():
    global ibNet
    global uniqueHCANodeDescs
    global nonUniqueHCANodeDescs
    global ff
    #
    uniqueHCANodeDescs = {}
    nonUniqueHCANodeDescs = {}
    dict = {}   
    guids = list (ibNet.keys())    # Make a list of all ibNet Node GUIDs, instead of a dictionary
    guids = sorted (guids)    # Sort the GUIDs in ascending order  ### NEEDED?
    for j in range (len(guids)):
        guid = guids [j]
        if not guid == " ":
            node = ibNet [guid]
            if node.nodeType == "H":    # Is node an HCA?
                #print ('HCA: ", guid)
                d = (node.nodeDesc.rstrip(' "\n')).lstrip(' "')    # Strip off leading & trailing junk
                #print ("!!!!!!!!!!!!!!!! HCA: ", guid, "  ", d)
                if not (d in dict):
                    dict [d] = []
                l = dict [d]
                dict [d] = l + [guid]
    descs = list (dict.keys())
    for j in range (len(descs)):
        d = descs [j]
        l = dict [d]    # Get list of GUIDs associated with this Node Description
        if len (l) == 1:    # If there was only one HCA with this Node Desc
            uniqueHCANodeDescs [l[0]] = d
        else:    # We have multiple HCAs with the same Node Description
            nonUniqueHCANodeDescs [d] = l
            for k in range(len(l)):
                ud = "HCA " + l[k][-6:] + "."    # Trailing "." keeps synthetic Node Desc from ending in a digit
                #print("@@@@@@@ ", ud, "  ", d)
                uniqueHCANodeDescs [l[k]] = ud
#### makeHCADescsUnique ####

#### massageHCANodeDescs ####
# Assume makeHCADescsUnique has already been called.
def massageHCANodeDescs ():
    global uniqueHCANodeDescs
    global massagedHCANodeDescs
    massagedHCANodeDescs = {}
    dict = {}
    guids = list (uniqueHCANodeDescs.keys())    # Make a list of all ibNet Node GUIDs, instead of a dictionary
    guids = sorted (guids)    # Sort the GUIDs in ascending order  ### NEEDED?
    for j in range (len(guids)):
        guid = guids [j]
        d = uniqueHCANodeDescs [guid]
        m = re.search ('(.*)( HCA-\d+\Z| mlx\d+_\d+\Z)', d)    # See if Desc ends in HCA-<n> or mlx<n>_<n>
        if m:
            d2 = m.group(1)    # Truncate the HCA or mlx part
        else:
            d2 = d
        if not (d2 in dict):
            dict [d2] = []
        l = dict [d2]
        dict [d2] = l + [guid]
    descs = list (dict.keys())
    for j in range (len(descs)):
        td = descs [j]
        l = dict [td]    # Get list of GUIDs associated with this truncated Node Description
        if len (l) == 1:    # If there was only one HCA with this truncated Node Desc
             massagedHCANodeDescs [l[0]] = td
             #print ("*****T '" + td + "'  '" + uniqueHCANodeDescs [l[0]] + "'")
        else:    
            for k in range(len(l)):
                d = uniqueHCANodeDescs [l[k]]    # Get original non-truncated Node Desc
                #print ("****** '" + d + "'")
                massagedHCANodeDescs [l[k]] = d

#### end of massageHCANodeDescs ####

#### getCoalescedHCANames ####
#### FIX THIS TEXT #### some users make use of the ability to put 'HCA-1', 'HCA-2', 'HCA-3' within the
# HCA node description as part of the HCA name, where the text prior to 'HCA-n' is
# not unique.  E.g. a storage node with 4 HCAs named 'st1 HCA-1', 'st1 HCA-2', ..
# 'st1 HCA 4'.  This routine currently strips off the 'HCA-n' and deals awkwardly with
# the resulting duplicate HCA names ('st1' in this example).  Not sure how to cope with
# this-- GUI option, clever detection of nodes with multiple HCAs, or...  The System
# Image GUID could help solve this, but is rarely used for HCAs in the field.
#
# Note: currently this routine also displays the virtual HCAs within Gateways.  The names
# of these HCAs are derived from the switch Node Description.  There are a couple of
# ways to detect these HCAs, e.g. in order to suppress them or flag them as virtual.
def getCoalescedHCANames (hcaGUIDList):
    global ibNet
    global massagedHCANodeDescs
    #
    dict = {} 
    hcaCoalescedNames = []    # Initialize the list
    for j in range (len(hcaGUIDList)):
        hcaGUID = hcaGUIDList [j]
        d = massagedHCANodeDescs [hcaGUID]
        # Now see if the user-supplied HCA name ends in a numeric string 
        m = re.search ('\d+\Z', d)
        suff = ''
        pref = d
        if m:    # If we have a match
            suff = d[m.start():m.end()]
            pref = d[0:m.start()]
        if not (pref in dict):
            dict [pref] = []
        l = dict [pref]
        if not (len(suff) == 0):
            #print (suff)
            l.append (suff)
            dict [pref] = l 
    n = sorted (list (dict.keys()))
    # We should change 'n' to something more meaningful, e.g. 'prefixes'
    #print ("##############", n)    
    for j in range (len(n)):    # Loop through the prefixes
        # For each prefix we found, build a string of the form
        #    <prefix> [ <suffix>, <suffix>, ... <suffix> ] ( <number of suffixes> )
        # These strings are useful but don't compress a sequential string of suffixes, e.g. 
        #  suffixes '1', '2', and '3' aren't represented as '1-3'.  Also, the string for a prefix with
        # only one suffix will have the form <prefix> [ <suffix> ] (1), which is verbose.
        pref = n [j]    # Get the next HCA name prefix in the list
        s = pref
        l = sorted (dict [pref], key = int)    # Get the list of suffixes for this prefix
        for i in range (len(l)):    # Build a list of suffixes for this prefix
            s = s + l [i] + ","
        s = s + "]"
        s = s + " (" + str (len (l)) + ")"    # Add the count of prefixes
        # The version of s we just generated is only used for debugging.
        #print (s)    
        #print ("/////////////////////////////////")    
        # Now generate a string for the same prefix, but try to make it more readable.
        s = pref
        if len(l) == 1:
            s = s + l[0]    # Only one suffix, so don't bother showing a list
        elif len(l) > 1:
            s = s + "["
            l.append ("0")    # Add a stopper-- zero can never be any but 1st in a sort
            i = 0
            while i < (len(l)-1):    # Loop through suffixes & try to compress sequential values
                s2 = l[i]
                v = int(s2)+1
                k = i
                #print (i, " ", k, " ", v, " ", l[k], " s=", s)    
                while int (l[k+1]) == (v):    
                    v = v + 1
                    k = k + 1    
                if k > i:
                    s2 = s2 + "-" + l[k]
                i = k + 1
                s = s + s2 + ","    
            s = s[:-1] + "] (" + str (len(l)-1) + ")"
        #print (s) 
        hcaCoalescedNames.append (s)
    return (hcaCoalescedNames)                   
#### end of getCoalescedHCANames ####

#### showHCANames ####
def showHCANames (hcaGUIDList, leadin, fontColor):
    global ff
    hcaCoalescedNames = getCoalescedHCANames (hcaGUIDList)
    for i in range (0, len (hcaCoalescedNames)):
        ff.write ("\\cf" + str(fontColor) + leadin + hcaCoalescedNames [i] + "\\cf0" + rtfEOL)        
#### end of showHCANames ####                    

#### showHCANames OLD #### REMOVE ME?  ####
#### FIX THIS TEXT #### some users make use of the ability to put 'HCA-1', 'HCA-2', 'HCA-3' within the
# HCA node description as part of the HCA name, where the text prior to 'HCA-n' is
# not unique.  E.g. a storage node with 4 HCAs named 'st1 HCA-1', 'st1 HCA-2', ..
# 'st1 HCA 4'.  This routine currently strips off the 'HCA-n' and deals awkwardly with
# the resulting duplicate HCA names ('st1' in this example).  Not sure how to cope with
# this-- GUI option, clever detection of nodes with multiple HCAs, or...  The System
# Image GUID could help solve this, but is rarely used for HCAs in the field.
#
# Note: currently this routine also displays the virtual HCAs within Gateways.  The names
# of these HCAs are derived from the switch Node Description.  There are a couple of
# ways to detect these HCAs, e.g. in order to suppress them or flag them as virtual.
def showHCANamesOLD (hcaGUIDList, leadin, fontColor):
    global ibNet
    global massagedHCANodeDescs
    global ff
    #
    dict = {}   
    for j in range (len(hcaGUIDList)):
        hcaGUID = hcaGUIDList [j]
        d = massagedHCANodeDescs [hcaGUID]
        # Now see if the user-supplied HCA name ends in a numeric string 
        m = re.search ('\d+\Z', d)
        suff = ''
        pref = d
        if m:    # If we have a match
            suff = d[m.start():m.end()]
            pref = d[0:m.start()]
        if not (pref in dict):
            dict [pref] = []
        l = dict [pref]
        if not (len(suff) == 0):
            #print (suff)
            l.append (suff)
            dict [pref] = l 
    n = sorted (list (dict.keys()))
    # We should change 'n' to something more meaningful, e.g. 'prefixes'
    #print ("##############", n)    
    for j in range (len(n)):    # Loop through the prefixes
        # For each prefix we found, build a string of the form
        #    <prefix> [ <suffix>, <suffix>, ... <suffix> ] ( <number of suffixes> )
        # These strings are useful but don't compress a sequential string of suffixes, e.g. 
        #  suffixes '1', '2', and '3' aren't represented as '1-3'.  Also, the string for a prefix with
        # only one suffix will have the form <prefix> [ <suffix> ] (1), which is verbose.
        pref = n [j]    # Get the next HCA name prefix in the list
        s = pref
        l = sorted (dict [pref], key = int)    # Get the list of suffixes for this prefix
        for i in range (len(l)):    # Build a list of suffixes for this prefix
            s = s + l [i] + ","
        s = s + "]"
        s = s + " (" + str (len (l)) + ")"    # Add the count of prefixes
        # The version of s we just generated is only used for debugging.
        #print (s)    
        #print ("/////////////////////////////////")    
        # Now generate a string for the same prefix, but try to make it more readable.
        s = pref
        if len(l) == 1:
            s = s + l[0]    # Only one suffix, so don't bother showing a list
        elif len(l) > 1:
            s = s + "["
            l.append ("0")    # Add a stopper-- zero can never be any but 1st in a sort
            i = 0
            while i < (len(l)-1):    # Loop through suffixes & try to compress sequential values
                s2 = l[i]
                v = int(s2)+1
                k = i
                #print (i, " ", k, " ", v, " ", l[k], " s=", s)    
                while int (l[k+1]) == (v):    
                    v = v + 1
                    k = k + 1    
                if k > i:
                    s2 = s2 + "-" + l[k]
                i = k + 1
                s = s + s2 + ","    
            s = s[:-1] + "] (" + str (len(l)-1) + ")"
        #print (s) 
        ff.write ("\\cf" + str(fontColor) + leadin + s + "\\cf0" + rtfEOL)                   

#### end of showHCANames OLD ####

#### getHCAsByBox ####
# Builds three dictionaries: allHCAs, hcasBySwitch, and hcasByDirector.
# The latter two will include Switches/Directors that have no HCAs.
# It also builds a dictionary of the types of HCAs found, and counts the
# number of HCAs that have virtual ports (vPorts).  Data, bring us more data!!!
def getHCAsByBox ():
    global ibNet
    global ff
    global hcasBySwitch
    global hcasByDirector
    global allHCAs
    global hcaTypes
    global hcasWithVPorts
    hcasBySwitch = {}
    hcasByDirector = {}
    allHCAs = {}
    hcaTypes = {}
    hcasWithVPorts = 0
    guids = list (ibNet.keys())    # Make a list of all ibNet Node GUIDs, instead of a dictionary
    guids = sorted (guids)    # Sort the GUIDs in ascending order  ### NEEDED?
    for j in range (len(guids)):
        guid = guids [j]
        if not guid == " ":
            node = ibNet [guid]
            if node.nodeType == "S":    # Is node a Switch?  We find HCAs via their peer Boxes
                #print ("Switch: ", guid)
                hcaList = []
                ports = int (node.nodePortCount)
                # This loop should be rewitten to use the peerExists routine: ####
                for p in range (1, ports+1):
                    port = node.nodePortList [p]    # Get Port structure for this port
                    #print ("Port: ", p)
                    if port.portType == "IB" and port.portConnected == "Y":
                        link = port.portLink    # Get Link structure for this port
                        if link.peerType == "H":    # Is it an HCA?
                            #print ("Peer GUID: ", link.peerNodeGUID)
                            hg = link.peerNodeGUID
                            allHCAs [hg] = " "
                            hcaList.append (hg)
                            h = ibNet [hg]    # Get Node structore for this HCA
                            hkey = h.vendorID + ":" + h.deviceID    # Build a string from node Vendor & Device IDs
                            while not (hkey in hcaTypes):  hcaTypes [hkey] = 0
                            hcaTypes [hkey] = hcaTypes [hkey] + 1    # Count how many times we've seen this HCA type
                            if ibNet [hg].nodeHasVPorts:
                                hcasWithVPorts = hcasWithVPorts + 1
                hcasBySwitch [guid] = hcaList    # Make dictionary entry for Switch no matter what, with list of its HCAs
                dg = node.nodeDirectorGUID  
                if dg != " ":    # If this Switch is part of a Director
                    #print(">>>>>>>> dg = ",dg)
                    #print("hcaList: ", hcaList)
                    if not (dg in hcasByDirector):
                        hcasByDirector [dg] = hcaList
                        #print(hcasByDirector)
                    else:
                        l = hcasByDirector [dg]
                        hcasByDirector [dg] = l + hcaList    # Can't use l.append here
#### end of getHCAsByBox ####

#### doHCAReport ####
# Note: some users make use of the ability to put 'HCA-1', 'HCA-2', 'HCA-3' within the
# HCA node description as part of the HCA name, where the text prior to 'HCA-n' is
# not unique.  E.g. a storage nde with 4 HCAs named 'st1 HCA-1', 'st1 HCA-2', ..
# 'st1 HCA 4'.  This routine currently strips off the 'HCA-n' and deals awkwardly with
# the resulting duplicate HCA names ('st1' in this example).  Not sure how to cope with
# this-- GUI option, clever detection of nodes with multiple HCAs...  The System
# Image GUID could help solve this, but is rarely (ever?) used for HCAs in the field.
# Note: currently this routine also displays the virtual HCAs within Gateways.  The names
# of these HCAs are derived from the switch Node Description.  There are a couple of
# ways to detect these HCAs, e.g. in order to suppress them or flag them as virtual.
def doHCAReport ():
    global fPath
    global fnameBase
    global ibNet
    global currentNode
    global currentDirector
    global nonUniqueHCANodeDescs
    global ff
    global rtfColorIndex
    global hcasWithVPorts
    fc = rtfColorIndex ["Blue"]    # Font color for HCA lists
    ffname = fPath + fnameBase + "_HCAs.rtf"
    ff = open (ffname, "w")    # Overwrite the file if it already exists
    ff.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
    ff.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    ff.write ("\\fs15" + "\n")    # Font size
    ff.write ("\\margl576")    # Margins
    ff.write ("\\margr576")
    ff.write ("\\margt576")
    ff.write ("\\margb576" + "\n")
    ff.write (putIbnetdiscoverNameAndDate () + rtfEOL)
    ff.write (rtfEOL)
    #
    makeHCADescsUnique ()    # Ensure every HCA has a unique Node Desc; synthesize one if needed
    massageHCANodeDescs ()    # Where possible, strip off "HCA-n" and "mlxn_n" at end of Descs
    #
    ff.write ("                                          HOST ADAPTERS (HCAs)" + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write (rtfEOL)
    getHCAsByBox()    # Also sets hcasWithVPorts
    if hcasWithVPorts > 0:
        ff.write ("Note: " + str (hcasWithVPorts) + " HCAs have virtual ports (vPorts) enabled.  See the '_vports.rtf' report for details." + rtfEOL)
        ff.write (rtfEOL)
    ff.write ('Note: if multiple HCAs have identical Node Descriptions, their names are replaced by "HCA gggggg.", ' + rtfEOL)
    ff.write ('      where gggggg = the least significant hex digits of the HCA Node GUID' + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write (" " + rtfEOL)
    #  Display HCA Node Description conflicts (if any)
    if len(nonUniqueHCANodeDescs) > 0:
        ff.write ("HCAs with Non-Unique Names" + rtfEOL)
        ff.write ("==========================" + rtfEOL)
        n = 0
        hcaGUIDList = list (nonUniqueHCANodeDescs.keys())
        for j in range (len(hcaGUIDList)):
            d = hcaGUIDList [j]
            ff.write ("\\cf" + str(fc) + "HCA Node Description:  '" + d + "'\\cf0" + rtfEOL) 
            l = nonUniqueHCANodeDescs [d]    # Get the list of GUIDs that have description 'd'
            for k in range (len(l)):
                ff.write ("   \\cf" + str(fc) + "HCA Node GUID:  '" + l[k] + "'\\cf0" + rtfEOL) 
                n = n + 1
        ff.write ("\\cf" + str(fc) + "TOTAL HCAs:  " + str(n) + "\\cf0" + rtfEOL)            
        ff.write (" " + rtfEOL)
        ff.write (" " + rtfEOL)
    #
    #getHCAsByBox()    # Original place where we called it
    ff.write (" " + rtfEOL)
    ff.write ("Number of HCAs by Vendor:Device ID" + rtfEOL)
    ff.write ("==================================" + rtfEOL)
    ff.write (" " + rtfEOL)
    for i, key in enumerate (hcaTypes):
        hDesc = " "
        if key.split(":")[0] in ouiDict:    # (We might know the vendor ID but not the device ID)
            hDesc = ouiDict [key.split(":")[0]]
        if key in asicTable:
            hDesc = asicTable [key].desc
        ff.write ("\\cf" + str(fc) + str(hcaTypes [key]).rjust(5) + " " + key + " " + hDesc + "\\cf0" + rtfEOL )#
    #
    ff.write (" " + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write ("HCA Summary" + rtfEOL)
    ff.write ("===========" + rtfEOL)
    ff.write (" " + rtfEOL)
    #
    hcaGUIDList = list (allHCAs.keys())
    showHCANames (hcaGUIDList, "    ", fc)
    ff.write ("\\cf" + str(fc) + "TOTAL HCAs:  " + str(len(hcaGUIDList)) + "\\cf0" + rtfEOL)   
    #
    ff.write (" " + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write ("HCAs by Switch" + rtfEOL)
    ff.write ("==============" + rtfEOL)
    ff.write (" " + rtfEOL)
    #
    switchGUIDs = list (hcasBySwitch.keys())    # Get the list of all Switch GUIDs in ibNet
    for j in range (0, len(switchGUIDs)):
        switchGUID = switchGUIDs [j]
        #ff.write ("Switch " + switchGUID + rtfEOL)
        currentNode = ibNet [switchGUID]
        if currentNode.nodeDirectorGUID == " ":    # If this Switch isn't part of a Director
            showSwitchSummary (False)
            ff.write (" " + rtfEOL)
            hcaGUIDList = hcasBySwitch [switchGUID]
            showHCANames (hcaGUIDList, "     ", fc)
            ff.write ("\\cf" + str(fc) + "TOTAL HCAs:  " + str(len(hcaGUIDList)) + "\\cf0" + rtfEOL)
            ff.write (" " + rtfEOL)    
    #
    if len(allDirectors) > 0:    # If the fabric includes Directors
        ff.write (" " + rtfEOL)
        ff.write ("HCAs by Director" + rtfEOL)
        ff.write ("================" + rtfEOL)
        ff.write (" " + rtfEOL)
    #
    dirGUIDs = sorted (list (hcasByDirector.keys()))    # Get a list of Director pseudo-GUIDs
    for j in range (0, len(dirGUIDs)):
        dirGUID = dirGUIDs [j]
        #ff.write ("Director " + dirGUID + rtfEOL)
        currentDirector = allDirectors [dirGUID]
        showDirectorSummary (True)    # But don't generate Warnings (it's already been done)
        ff.write (" " + rtfEOL)
        lgl = currentDirector.directorLeafGUIDList
        n = 0
        for i in range (1, len (lgl)):
            lg = lgl [i]
            if lg != " ":
                sn = ibNet [lg].nodeSlotName
                ff.write ("  Leaf " + sn + " " + lg + rtfEOL)
                hcaGUIDList = hcasBySwitch [lg]
                showHCANames (hcaGUIDList, "     ", fc)
                n = n + len (hcaGUIDList)
        ff.write ("\\cf" + str(fc) + "TOTAL HCAs:  " + str(n) + "\\cf0" + rtfEOL)
        #hcaGUIDList = hcasByDirector [dirGUID]    # Show all of the Director HCAs in one list
        #showHCANames (hcaGUIDList, "     ", fc)
        #ff.write ("\\cf" + str(fc) + "TOTAL HCAs:  " + str(len(hcaGUIDList)) + "\\cf0" + rtfEOL)
        ff.write (" " + rtfEOL)
    #             
    ff.write ("}\n")
    ff.close()
#### end of doHCAReport ####

#####################################################################################
#### Begin routines to generate a report analyzing 'low latency neighborhoods' on Directors.
#####################################################################################

#### getLinkCount ####
# Helper routine for doNeighborHoodReport.
def getLinkCount (linkDict, leafASICGUID, switchGUID):
    key= leafASICGUID + "-" + switchGUID
    return (linkDict.get (key, 0))    # Return 0 if there's no dict entry
#### end of getLinkCount ####

#### doNeighborhoodReport ####
# The hcasBySwitch dictionary must be set up before calling this routine.  It's set by getHCAsByBox, which is
# called by doHCAReport.
# Generate an .rtf file that shows how Switches connected to Director Leafs are grouped.  Best practice
# for latency-sensitive taffic is to minimize switch hops by building large Switch 'neighborhoods' that can talk
# among themselves without traversing Director Spines.  Even smaller neighborhoods are preferable to 
# random cabling, which can result in inconsistent path latencies and cause unintended blocking.
# By definition, a ToR/L1 switch can belong to at most one neighborhood.
# Eventually this could be extended to 2-tier Clos fabrics?
def doNeighborhoodReport ():
    global fPath
    global fnameBase
    global ibNet
    global allDirectors
    global ff
    global rtfColorIndex
    global nodeRTFStrings
    global hcasBySwitch
    global hoods    ####  Made global for easier debug
    global leafSets    ####
    global links    ####
    global leafList    ####
    global spineList    ####
    global sLines    ####
    fc = rtfColorIndex ["Blue"]    # Font color
    ffname = fPath + fnameBase + "_neighborhoods.rtf"
    ff = open (ffname, "w")    # Overwrite the file if it already exists
    ff.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
    ff.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    ff.write ("\\fs15" + "\n")    # Font size
    ff.write ("\\margl576")    # Margins
    ff.write ("\\margr576")
    ff.write ("\\margt576")
    ff.write ("\\margb576" + "\n")
    #
    hnum = rtfColorIndex ["Yellow"]
    pYellow = nodeRTFStrings[hnum][0] + "\\ "
    sYellow = nodeRTFStrings[hnum][1]  + "\\ "
    #print (nodeRTFStrings[hnum])
    ff.write (putIbnetdiscoverNameAndDate () + rtfEOL)
    ff.write (rtfEOL)    
    ff.write ("                                                 " + "\\cf" + str(fc) + "NEIGHBORHOOD ANALYSIS" + "\\cf0" + rtfEOL) 
    ff.write (" " + rtfEOL)
    ff.write ('This report shows "low-latency neighborhoods" formed by Top of Rack Switches connected to Directors.  A Neighborhood is ' + rtfEOL)
    ff.write ("a set of Switches that can communicate through Director Leafs without the traffic ever going through Director Spines." + rtfEOL)
    ff.write ("So, inter-Switch latency within a Neighborhood is 3 hops: a Leaf ASIC and 2 Switches." + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write ("This analysis excludes Top of Rack Switches that appear to be L1/leaf/edge Switches but have zero HCAs connected." + rtfEOL)
    ff.write (" " + rtfEOL)
    #
    # Do some Neighborhood analysis on ASICs instead of (graph) Boxes.  It doesn't
    # require turning off detection of Directors.
    # First, we go through all the Directors and get their Leaf ASIC GUIDs.  These form the upper tier
    # of Neighborhood analysis.  We also get their Spine ASIC GUIDs so we can exclude them
    # from consideration as 'lower tier' Switches.  (Could also achieve this by ignoring the internal
    # ports of the Leaf ASICs.) 
    leafList = []
    spineList = []
    for i, key in enumerate (allDirectors):
        leafList = leafList + allDirectors [key].directorLeafGUIDList
        spineList = spineList + allDirectors [key].directorSpineGUIDList
    while " " in leafList: leafList.remove (" ")    # Omit entries for empty Leaf ASIC slots
    while " " in spineList: spineList.remove (" ")    # Omit entries for empty Spine ASIC slots
    #print ("All Leafs: ", leafList)
    #print ("All Spines: ", spineList)
    #
    # Now, for each Director Leaf ASIC, find all of its non-Spine Switch peers that connect to HCAs.  
    peerNodeGUID = [noPeer]    # For use by the peerExists routine
    peerLink = [" "]    # For use by the peerExists routine
    switch = {}
    links = {}
    trapGUIDs = []    # Provide a list of GUIDs to monitor (DEBUG)
    for i in range (0, len(leafList)):
        lg = leafList [i]
        np = int (ibNet [lg].nodePortCount)
        for p in range (1, np + 1): 
            if peerExists (lg, p, peerNodeGUID, peerLink):
                pg = peerNodeGUID [0]
                if pg in trapGUIDs:
                    print("@@@ Found ", pg, " connected to ", lg, " port ", p)    
                if (ibNet [pg].nodeType == "S") and not (pg in spineList) and (ibNet[pg].nodeHCALinks != "0"):   
                    if not (pg in switch):    # First time we've seen this Leaf-attached Switch
                        switch [pg] = []
                        if pg in trapGUIDs:
                            print ("@@@@ First encounter of ", pg, " at ", lg," port ", p)
                    lst = switch [pg]
                    switch [pg] = lst + [lg]
                    if pg in trapGUIDs:
                        print("@@@@ switch[", pg, "]: ", switch[pg])
                    linkKey = lg + "-" + pg    # Here, the canonical form is Leaf GUID first
                    if not (linkKey in links):
                        links [linkKey] = 0
                    links [linkKey] = links [linkKey] + 1    # Count # of cables we find between this Leaf & this Switch
    #print ("Switch Dictionary: ", switch)
    #print ("Entries in Switch Dictionary: ",len(switch))
    # Next, go through the Switch list, convert each Switch's list of leaf GUIDs to a key, and
    # build a dictionary of Neighborhoods with the key and its list of Switch GUIDs:
    hoods = {}    # A dictionary of lists of switch GUIDs, indexed by strings of concatented Leaf GUIDS
    leafSets = {}    # A dictionary of sets of Leaf GUIDs, indexed by the same keys as in hoods
    for i, key in enumerate (switch):
        lst = sorted (switch [key])    # Get & sort the list of Leaf GUIDs connected to me
        key2 = ','.join(lst)    # Convert into a single string with GUIDs separated by commas 
        #print (i, " ", key2)
        if not (key2 in hoods):
            hoods [key2] = [] 
        lst2 = hoods [key2]
        hoods [key2] = lst2 + [key]
        leafSets [key2] = set(lst)    # Also build a set from the Leaf GUIDs
    #print ("HOODS: ", len(hoods), hoods) 
    #print ("LEAF SETS: ", len(leafSets), leafSets)  
    # Now consolidate neighborhoods, in the case where the Leaf GUIDs of one are a subset
    # of the Leaf GUIDs of another-- e.g. if a Switch is missing all of its uplinks to a Leaf ASIC
    ff.write ("NEIGHBORHOOD RELATIONSHIPS " + rtfEOL)
    ff.write (" " + rtfEOL)
    ff.write (" If a Switch is missing an uplink to a Leaf ASIC, this can create a smaller Neighborhood for the Switch because it" + rtfEOL)
    ff.write (" has fewer paths through Leafs to other Switches.  In this case the smaller Neighborhood can be thought of as a slightly" + rtfEOL)
    ff.write (" degraded subset of a larger Neighborhood.  However, there are other configurations where Neighborhood n may appear to be" + rtfEOL)
    ff.write (" a subset of Neighborhood m." + rtfEOL)
    ff.write (" " + rtfEOL)
    dList = []
    for i, key in enumerate (leafSets):
        for j, key2 in enumerate (leafSets):
            if (key != key2) and (leafSets [key] < leafSets [key2]):    # Test for a strict subset relationship
                ff.write (" Neighborhood " + str(i+1) + " is a subset of Neighborhood " + str(j+1) +rtfEOL)
                ff.write ("   Difference: Leaf ASIC(s) " + str (leafSets [key2] - leafSets [key]) + rtfEOL)
                if len (leafSets [key2]) - len (leafSets [key]) < 2:    # If the difference is 1 Leaf ASIC
                    ff.write ("   Combining Neighborhoods " + str (i + 1) + " and " + str (j + 1) + rtfEOL) 
                    hoods [key2] = hoods [key2] + hoods [key]    # Consolidate them
                    dList = dList + [key]    # Keep a list of keys of dictionary entries we no longer need
    if len (dList) > 0:
        ff.write ("Neighborhoods have been renumbered after combining subsets." + rtfEOL)
    for k in dList:    # Do dictionary maintenance while we're not enumerating on them
        del hoods [k]    
        del leafSets [k]    
    #
    hlin = "\\u8212?"    # Em Dash
    lrc = "\\u9496?"     # Box Drawings Light Up and Left 
    vlin = "\\u9474?"    # Box Drawings Light Vertical
    vpart = "  " + vlin
    ff.write (" " + rtfEOL)
    for z, key in enumerate (leafSets):    # Each leaf set is a Neighborhood
        n = z + 1    # Neighborhood numbering begins at 1
        warnSection ("#################### Analyze Neighborhood " + str (n))
        ff.write ("NEIGHBORHOOD " + str(n) + ":" + rtfEOL)
        # Create the text for the Switches in this Neighborhood now, even though they'll be displayed later.  This
        # helps us build the correct Links matrix even though we'll sort both the Leaf lines and the Switch lines.
        slst = hoods [key]
        sHCAList = []
        sLines = []
        for sg in slst:    # For every Switch GUID in the Neighborhood:
            nd = ibNet[sg].nodeDesc.rsplit ('"', 1)[0]    # Get main part of Node Description
            s1 = nd.replace ("MF0;", "") + '"'    # Omit "MF0;" if present; it is not user-supplied
            sLines = sLines + [s1.ljust (39)[:39] + " " + sg] 
            ibNet [sg] = ibNet [sg]._replace (nodeNeighborhood = str (n))    # Record its Neighborhood #
            #print ("Switch ", sg, " is in neighborhood ", n)    
            sHCAList = sHCAList + hcasBySwitch[sg]   # Also build a list of all HCA GUIDs in neighborhood
        #print ("HCA List: ", sHCAList)    
        sLines = sorted (sLines)     # Sort them by Node Desc and GUID
        #print ("SORTED SLINES", sLines)                     
        # Now create the text for the Leaf ASICs 
        llst = list(leafSets [key])    # Get list of Leaf ASIC GUIDs in this Neighborhood
        linkCountList = []
        for lg in llst:    # Get median value of all leaf-to-Switch link counts in this Neighborhood, so we can flag anomalies
            for sg in slst:
                lc = getLinkCount (links, lg, sg)
                if lc > 0:    # A link count of zero is excluded, we know it is an anomaly 
                    linkCountList.append (lc)
        linkCountList = sorted (linkCountList)
        indexOfMedian = int (len (linkCountList) / 2)    
        medianLinkCount = linkCountList [indexOfMedian]    # We now prefer median versus max; it allows for the case of extra cables
        print ("medianLinkCount = ", medianLinkCount, " in Neighborhood ", n)  
        #print ("llst: ", llst)    
        lHCAList = []
        lLines = []
        isNDR = False
        for lg in llst:    # For each Leaf ASIC GUID
            #print ("lg: ", lg)    
            isNDR = isNDR or ibNet [lg].nodeIBGen  == "NDR"
            nd = ibNet[lg].nodeDesc.rsplit ('"', 1)[0]
            nd = nd.replace ("MF0;", "") + '"'
            d = ibNet[lg].nodeDirectorGUID
            d = d[0] + d[1:].rjust (2, "0")    # E.g. convert "D1" to "D01" for proper sorting
            s1 = d + nd.ljust (35)[:35] + ' ' + lg
            #print ("S1: ", s1)    
            s = " "
            for sLine in sLines:
                sg = sLine.rsplit(" ", 1)[1]    # Get the corresponding Switch GUID from the sorted Switch text
                lc = getLinkCount (links, lg, sg)
                s2 = str (lc).rjust (3)
                if lc < medianLinkCount:    # If this set of links is smaller
                    warn ("Missing cable(s) from Leaf ASIC " + lg + " to Switch " + sg + ".")
                    s2 = pYellow + s2 + sYellow
                elif lc > medianLinkCount:
                    warn ("Extra cable(s) from Leaf ASIC " + lg + " to Switch " + sg + ".")
                    s2 = pYellow + s2 + sYellow    # Should make this a different color someday
                s = s + s2
            lLines = lLines + [s1 + s]
            lHCAList = lHCAList + hcasBySwitch [lg]    # Also build a list of HCA GUIDs attached to Leaf ASICs
        lLines = sorted (lLines)    # Sort the Leaf lines by Dir name + Node Desc + GUID
        #print ("SORTED LLINES: ", lLines)    
        #isNDR = True    ################## TESTING ##############################
        if isNDR:
            ff.write ("\\fs12"+rtfEOL)    # Reduce font size so the display fits between the margins
        ff.write (" LEAF ASICS (" + str(len(llst)) + "):" + rtfEOL)        
        for lLine in lLines:
            ff.write ("  " + lLine + rtfEOL)
        # Now display the Switch entries
        ff.write ("SWITCHES (" + str(len(slst)) + "):" + rtfEOL)
        nsw = len (sLines)
        for i in range (0, nsw):
            ff.write (" " + sLines[i] + "   " + (hlin * 3 * i) + lrc + (vpart * (nsw - i - 1)) + rtfEOL)
        ff.write (" HCAs (" + str (len(sHCAList)) + "):" + rtfEOL)
        showHCANames (sHCAList, "    ", rtfColorIndex ["Black"])
        if len (lHCAList) > 0:
            ff.write (" HCAs attached to Leaf ASICs (" + str (len(lHCAList)) + "):" + rtfEOL)
            showHCANames (lHCAList, "    ", rtfColorIndex ["Blue"])
        ff.write (rtfEOL)
        if isNDR:
            ff.write ("\\fs15"+rtfEOL)    # Restore font size
    #  
    ff.write ("}\n")    # Gotta finish the .RTF file properly           
    ff.close()
#### end of doNeighborhoodReport ####

#####################################################################################
#### Begin routines to generate a report about the virtual ports (vPorts) that were seen.
#####################################################################################

#### doVPortsReport ####
# Note: it's not clear (yet) whether ibnetdiscover reports all of an HCA's vPorts in a
# single list, even if it has 2 ports and both ports have vPorts-- or whether the vPort list is associated
# with a single HCA port.  The code currently handles either case,
# Note: Should we sort the HCA list, e.g. by Node Description? ####
def doVPortsReport ():
    global fPath
    global fnameBase
    global ibNet
    global ff
    global rtfColorIndex
    global nodeRTFStrings
    global hcasWithVPorts
    fc = "\\cf" + str (rtfColorIndex ["Blue"])    # RTF font color string
    ffname = fPath + fnameBase + "_vports.rtf"
    ff = open (ffname, "w")    # Overwrite the file if it already exists
    ff.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
    ff.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    ff.write ("\\fs15" + "\n")    # Font size
    ff.write ("\\margl576")    # Margins
    ff.write ("\\margr576")
    ff.write ("\\margt576")
    ff.write ("\\margb576" + "\n")
    ff.write (putIbnetdiscoverNameAndDate () + rtfEOL)
    ff.write (rtfEOL)
    #
    hnum = rtfColorIndex ["Yellow"]
    pYellow = nodeRTFStrings[hnum][0] + "\\ "
    sYellow = nodeRTFStrings[hnum][1]  + "\\ "
    #print (nodeRTFStrings[hnum])    
    ff.write ("                                           " + fc + "HCAs WITH VIRTUAL PORTS (vPorts)" + "\\cf0" + rtfEOL)
    ff.write (rtfEOL)
    ff.write (rtfEOL) 
    ff.write ("Total HCAs with vPorts: " + str (hcasWithVPorts) + rtfEOL)
    ff.write (rtfEOL)
    ff.write (rtfEOL)
    for i, hg in enumerate (ibNet):
        if ibNet [hg].nodeHasVPorts:    # (We assume it's an HCA)
            ff.write (ibNet [hg].nodeDesc + " " + ibNet [hg].nodeModel + " GUID: " + hg + rtfEOL)
            ports = int (ibNet [hg].nodePortCount)    # Get number of HCA ports            
            listOfLists = ibNet [hg].nodeVPortLists    # A list per port; list [0] corresponds to HCA Port 1
            #print ("List of lists: ", listOfLists)
            for p in range (0, ports):
                portS = ibNet [hg].nodePortList [p + 1]    # Get the Port structure for port p+1
                if portS.portConnected == "Y":
                    lynk = portS.portLink    # Get the Link structure for port p+1
                    s = "   Port " + str (p + 1) + " (GUID " + lynk.portGUID + ") <- " + lynk.linkWidthXRate   
                    s = s + " -> S " + lynk.peerNodeGUID + ibNet [lynk.peerNodeGUID].nodeDesc
                    ff.write (s + rtfEOL)
                    vPortList = listOfLists [p]    # (Sublist 0 corresponds to Port 1)
                    #print ("vPortList:", vPortList)
                    vp = len (vPortList)
                    j = 0
                    while j < vp:
                        ff.write ("     " + fc + vPortList [j] + "\\cf0" + rtfEOL)
                        j = j + 1
                else:
                    ff.write ("   Port " + str (p + 1) + " not connected" + rtfEOL)
            ff.write (rtfEOL)
    #  
    ff.write ("}\n")    # Finish the .RTF file properly           
    ff.close()

#### end of doVPortsReport ####


#### showDirHoodsMx2 ####
# m is 1/2 the number of Leaf ASIC external ports (there are 2 rows per module).
# E.g. m = 9 for EDR Directors and m = 10 for HDR.
def showDirHoodsMx2 (m):
    global ibNet
    global currentDirector
    global ff
    global rtfColorIndex
    global nodeRTFStrings
    dgray = nodeRTFStrings [rtfColorIndex ["Dark Gray"]]
    vlin = "\\u9474?"    # Box Drawings Light Vertical
    hlin = "\\u8212?"    # Em Dash
    dir = currentDirector    # For convenience
    ff.write ("\\fs18 Director " + dir.directorNodeGUID + "   " + dir.directorDesc + "     " + dir.directorModel + "\\fs15" + rtfEOL)
    lep = m * 2    # Total # of Leaf ASIC external ports
    lgl = dir.directorLeafGUIDList
    #print ("Leafs: ", lgl)
    lgs = len (lgl)
    lyne = "       " + (lep * 4 * hlin) + (2 * hlin) + rtfEOL
    for i in range (1, lgs, 2):
        ff.write (lyne)
        lg1 = lgl [i]
        s1 = m * (vlin + dgray[0] + "    " + dgray[1]) + vlin    # Default if no Leaf ASIC is installed
        s2 = s1
        s3 = s1
        s4 = s1
        g1 = "      "
        sn1 = "      "
        if lg1 != " ":
            #print ("Leaf 1: ", lg)
            g1 = lg1
            sn1 = ibNet[lg1].nodeSlotName
            s1 = putSWRowHoods (lg1, 1, lep, 2)
            s2 = putSWRowHoods (lg1, 2, lep, 2)
        lg2 =lgl [i + 1]
        g2 = "      "
        sn2 = "      "
        if lg2 != " ":
            #print ("Leaf 2: ", lg)
            g2 = lg2
            sn2 = ibNet[lg2].nodeSlotName
            s3 = putSWRowHoods (lg2, 1, lep, 2)
            s4 = putSWRowHoods (lg2, 2, lep, 2) 
        ff.write (g1[-6:] + " " + s1 + s3 + " " + g2[-6:] + rtfEOL)
        ff.write (sn1.rjust (6) + " " + s2 + s4 + " " + sn2.ljust (6) + rtfEOL)
    ff.write (lyne) 
    ff.write (rtfEOL)          
#### end of showDirHoodsMx2 ####

#### showDirHoods ####
def showDirHoods ():
    global allDirectors
    global currentDirector
    global ff
    global fpath
    global fnameBase
    global rtfColorIndex
    global nodeRTFStrings
    #fc = rtfColorIndex ["Blue"]    # Font color
    ffname = fPath + fnameBase + "_neighborhoods_graphic.rtf"
    ff = open (ffname, "w")    # Overwrite the file if it already exists
    ff.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
    ff.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
    ff.write ("\\fs15" + "\n")    # Font size
    ff.write ("\\margl576")    # Margins
    ff.write ("\\margr576")
    ff.write ("\\margt576")
    ff.write ("\\margb576" + "\n")
    ff.write (putIbnetdiscoverNameAndDate () + rtfEOL)
    ff.write (rtfEOL)
    #
    ff.write ("               DIRECTOR LEAF ASIC NEIGHBORHOOD MEMBERSHIPS  (EXPERIMENTAL)" + rtfEOL)   
    ff.write (rtfEOL)
    ff.write (rtfEOL)
    ff.write ("This report displays the mapping of low-latency 'neighborhoods' to Director Leaf ASICs.  It uses a different (arbitrary)" +rtfEOL)
    ff.write ("color coding scheme than the 'directors' report uses.  The neighborhood numbers correspond to those in the 'neighborhoods' report." + rtfEOL)
    ff.write (rtfEOL)
    ff.write ("PORT LEGEND: " + rtfEOL)
    ff.write ("     Dark gray = Leaf not installed; black = no link; 'S' = link to a Switch that is not in a neighborhood;" + rtfEOL)
    ff.write ("     'H' = link to an HCA; <n> = link to a Switch in neighborhood <n>" + rtfEOL)
    for x, key in enumerate (allDirectors):
        currentDirector = allDirectors [key]
        if currentDirector.directorLayout == "10x2":
            ff.write ("\\page" + "\n")
            showDirHoodsMx2 (10)
        elif currentDirector.directorLayout == "9x2":
            ff.write ("\\page" + "\n")
            showDirHoodsMx2 (9)
    #
    ff.write ("}\n")    # Finish the .RTF file properly           
    ff.close()
#### end of showDirHoods ####

#####################################################################################
#### Begin routines to generate a .TOPO file from an  ibnetdiscover file.
#####################################################################################

# This code was never completed and was omitted in August 2022.


#####################################################################################
#### Begin routines to generate a switches.xlsx file.
#####################################################################################

# Excel cell pattern indices, selected for use in Port coloring; complete range is 0 (no pattern) through 18:
patterns = [1,4,7,8,9,10,13,14,15,16,17,18]  # No 0, 2, 3, 5, 6, 11, 12 
solidIndex = 1
# These color tables are for deuteranopia color blindness (the most common form) by Martin Krzywinski, May 2020:
colors15 = ["#68023F", "#008169", "#EF0096", "#00DCB5", "#FFCFE2", "#003C86", "#9400E6", "#009FFA", "#FF71FD", "#7CFFFA",
    "#6A0213", "#008607", "#F60239", "#00E307", "#FFDC3D"]
colors24 = ["#003D30", "#005745", "#00735C", "#009175", "#00AF8E", "#00CBA7", "#00EBC1", "#86FFDE", "#00306F", "#00489E",
    "#005FCC", "#0079FA", "#009FFA", "#00C2F9", "#00E5F8", "#7CFFFA", "#004002", "#005A01", "#007702", "#009503",
    "#00B408", "#00D302", "#00F407", "#AFFF2A"]
# Lists that determine subsets of colorblind tables (to allow fine tuning):
selectFrom15 = [1,2,3,4,6,7,8,9,11,12,13,14]
selectFrom24 = [1,2,3,4,5,6,7,9,10,11,12,13,14,15,17,18,19,20,21,22,23]
# More (hand-selected) colors:
xtraColors = ["#F0FFF0", "#F5F5DC", "#FAEBD7", "#FFFF00", "#FFFFE0"]    # honeydew, beige, antiquewhite, yellow, lightyellow
xtraColors = xtraColors + ["#FF0000", "#FFC0CB"]    # red, pink
selectFromXtra = []
# Colors with well-known indices, e.g. to depict missing or disconnected ports:
black, white, darkSlateGray = "#000000", "#FFFFFF", "#2F4F4F"
blackIndex, whiteIndex, darkSlateGrayIndex, wellKnownColors = 0, 1, 2, 3

#### buildColors ####
def buildColors():
    global patterns
    global portColors
    # A portColors entry is a list of [cell pattern, foreground color, background color]
    portColors = [[solidIndex, white, white], [solidIndex, white, black], [solidIndex, white, darkSlateGray]] # Well known
    for p in patterns:
        for cinx in selectFrom24:
            portColors.append ([p, white, colors24 [cinx]])
    for p in patterns:
        for cinx in selectFrom15:
            portColors.append ([p, white, colors15 [cinx]])
    for p in patterns:
        for color in xtraColors:
            portColors.append ([p, white, color])
    #print (portColors)
#### end of buildColors ####

#### getNodeColorXLS ####
def getNodeColorXLS (guid):
    global nodeColors    # From Tarzan; colors begin at 1
    global portColors
    if not guid in nodeColors:  print (guid, " NOT IN nodeColors")
    cx = nodeColors.get (guid, blackIndex + 1) - 1
    #print ("cx=", cx)
    l = len (portColors)
    while cx > l: cx = cx - (l - wellKnownColors)
    return ({'pattern': portColors [cx][0], 'fg_color': portColors [cx][1], 'bg_color': portColors[cx][2]})
#### end of getNodeColorXLS ####

#### putSwitchSummaryXLS ####
# Version for .XLS reports.  Assumes currentNode is the Switch in question.
def putSwitchSummaryXLS (showSwitchColor):
    global currentNode
    global ouiDict    # From Tarzan
    s1 = "GUID: " + currentNode.nodeGUID
    s1 = s1 + "   LID: " + currentNode.nodePortZeroLID
    vID = currentNode.vendorID
    vName = ouiDict.get (vID, " ")
    s1 = s1 + "   Vendor: " + vName + " (" + vID + ")"
    s1 = s1 + "   " + currentNode.nodeModel
    s1 = s1 + "  " + currentNode.nodeIBGen
    s1 = s1 + "   Ports: " + currentNode.nodePortCount
    s2 = "Description: " + currentNode.nodeDesc
    if showSwitchColor:
        nc = nodeColors [currentNode.nodeGUID]
        s2 = s2 + "    [" + str(nc) + "]"
    return (s1, s2)
#### end of putSwitchSummaryXLS ####

#### showSHARP ####
# Assume currentNode is the Node structure for a Switch and the caller has determined an
# 'extra' Switch port (internal, for the SHARP aggregation engine) exists.
def showSHARP (row, col):
    global currentNode
    global workbook
    global worksheet
    port = int (currentNode.nodePortCount)
    fmt = {'color': 'gray', 'bold': True, 'align': 'center', 'border': 0, 'text_wrap': False, 'font_size': 12}
    tl, linkState = putSwPeerTypeAndLinkTypeXLS (currentNode, port, 5)
    s = 'Internal port ' + str (port) + '\nSHARP aggregation node:\n'
    if linkState > 0:
        fmt.update ({'color': 'black'})        
        s = s + 'Enabled'
    else:
        s = s + 'Not enabled'
    cf= workbook.add_format (fmt) 
    worksheet.write (row, col, 'SHARP', cf)
    worksheet.write_comment (row, col, s)    # Create the cell comment

#### end of showSHARP

# Modified Tarzan helper routines for displaying Switch (not Director) ports:

#### putSwPeerTypeAndLinkTypeXLS ####
# Version for .XLS Switch ports. For Switch ports, as opposed to Director ports.
def putSwPeerTypeAndLinkTypeXLS (switchNode, portNum, width):
    global ibNet
    global resolveDirectors
    global currentLinkWidths
    global portSpeed
    g = switchNode.nodeGUID
    type = " "
    linkAbbrev = " "
    linkWidth = " "
    linkState = 0    # Initially, assume no link at all
    p = switchNode.nodePortList [portNum]    # Get peer Port structure
    s = " "
    if p.portType == "IB" and p.portConnected == "Y":
        linkState = 1
        l = p.portLink    # Get Link structure
        type = l.peerType    # Get node type of peer, e.g. "H" or "S"
        pg = l.peerNodeGUID    # Get Node GUID of peer entity
        psKey = g + ":" + str(portNum)    # Key into portSpeed dictionary
        if psKey in portSpeed:
            linkWidthXRate = portSpeed[psKey][0]    # 1st 2-tuple part is the link width & rate, e.g. "4xEDR"
            linkWidth = linkWidthXRate [0:2]    # Isolate the width, e.g. "4x"
            linkAbbrev = linkWidthXRate [0:3]    # Truncate for display, e.g. "4xE"
            linkOK = portSpeed[psKey][1]    # 2nd 2-tuple part tells us if the link speed is optimal
            if linkOK: linkState = 2    # We have a link and it's running at max speed
        peerNode = ibNet [pg]
        dg = peerNode.nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors: type = "D"
        s = type + (" " * (width - 4)) + linkAbbrev    # Peer type, then first 3 chars of link, e.g. "4xQ"
    return (s, linkState)    # linkState will tell the caller if the link was down or its speed was optimal or not
#### end of putSwPeerTypeAndLinkTypeXLS ####

#### putSwPeerNodeGUIDXLS ####
# Version for .XLS reports.
def putSwPeerNodeGUIDXLS (switchNode, portNum, width):
    global resolveDirectors
    pg = " " * width
    p = switchNode.nodePortList [portNum]    # Get the Port structure for the specified port
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink
        pg = l.peerNodeGUID
        dg = ibNet[pg].nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            pg = dg
    s = pg [-width:]
    return (s, pg)
#### end of putSwPeerNodeGUIDXLS ####

#### putSwPeerLIDXLS ####
# Version for .XLS reports.
def putSwPeerLIDXLS (switchNode, portNum, width):
    global resolveDirectors
    p = switchNode.nodePortList [portNum]    # Get the Port structure for the specified port
    s = " "
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink
        s = l.peerLID
        pg = l.peerNodeGUID
        dg = ibNet[pg].nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            #print ("PEER IS A DIRECTOR LEAF: ", pg, ibNet[pg].nodeSlotName)
            slotName = ibNet [pg].nodeSlotName.replace("/", "")    # Remove "/" to shorten, e.g. L01/U2->L01U2
            if (not (slotName == " ")) and (len(slotName) <= width):
                s = slotName
    return (putCentered (s, width))	
#### end of putSwPeerLIDXLS ####

#### putSwPeerPortXLS ####
# Version for .XLS reports.
def putSwPeerPortXLS (switchNode, portNum, width):
    global resolveDirectors
    p = switchNode.nodePortList [portNum]    # Get the Port structure for the specified port
    s = " "
    if p.portType == "IB" and p.portConnected == "Y":
        l = p.portLink
        s = l.toPortNum    # Port number on peer (character string)
        g = l.peerNodeGUID
        dg = ibNet[g].nodeDirectorGUID    # See if peer Node is part of a Director
        if (not dg == " ") and resolveDirectors:    # If yes
            dir = allDirectors [dg]
            xp = int (dir.directorLeafExtPorts)    # Get # of external ports per Dir. Leaf Board
            pn = int (s)
            if pn > xp:    # Translate Leaf Board ASIC port # to external port #
                s = str (pn - xp)
    if not (s == " "):
        s = "p" + s    # For now; LATER NEED to convert to "leaf/port" format
    return (putCentered (s, width))
#### end of putSwPeerPortXLS ####

#### showSwitchRowXLS ####
# Version for XLS output.
def showSwitchRowXLS (row, col, portList, splittable, checkForSplitPorts):
    global currentNode
    global defaultPortColor
    global currentLinkWidths
    global currentPeerGUIDs
    global workbook
    global worksheet
    nodeTypes = {'H': 'HCA', 'S': 'Switch', 'D': 'Director'}
    node = currentNode    # Shorthand
    #print (portList)
    pl = len (portList)
    for i in range (0, pl):
        port = portList [i]
        s = ''
        split = False
        peerTypeAndLinkType, linkState = putSwPeerTypeAndLinkTypeXLS (node, port, 5)
        shortPeerGUID, peerGUID = putSwPeerNodeGUIDXLS (node, port, 5)
        peerLID = putSwPeerLIDXLS (node, port, 5)
        peerPort = putSwPeerPortXLS (node, port, 5)
        s = s + peerTypeAndLinkType + '\n'
        s = s + shortPeerGUID + '\n'
        s = s + peerLID + '\n'
        s = s + peerPort
        fmt = {'color': 'black', 'bold': False, 'align': 'center', 'border': 1, 'text_wrap':'True'}
        fmt.update ({'pattern': 1, 'bg_color': white, 'fg_color': white, 'font': 'Lucida Console'})
        #if (i == 5) and (linkState == 2):  linkState = 1    # Fake a slow link
        #print (i, linkState, peerGUID, getNodeColorXLS (peerGUID))
        if linkState == 0: # No link
            fmt.update ({'pattern': 1, 'bg_color': darkSlateGray, 'fg_color': 'white'})
            if checkForSplitPorts:
                if "4x" in currentLinkWidths [i]:    # If the port 'above us' was 4x
                    fmt.update (getNodeColorXLS (currentPeerGUIDs [i]))    # Make this port the same color
                    split = True
                    #fmt.update ({'top': 0})    # (Doesn't seem to work)
            currentPeerGUIDs [i] = ' '    # For split port handling
            currentLinkWidths [i] = ' '    # For split port handling
        if (linkState > 0):    # We have a link
            if peerTypeAndLinkType[0:1] != "H":
                fmt.update (getNodeColorXLS (peerGUID)) 
            currentPeerGUIDs [i] = peerGUID    # For split port handling
            currentLinkWidths [i] = peerTypeAndLinkType [-3:]    # For split port handling
            #print ("Updating:", i, currentPeerGUIDs [i], currentLinkWidths [i]) 
        if linkState == 1: fmt.update ({'diag_type': 1, 'diag_border': 5, 'diag_color': 'orange'})
        #print (i, portList [i], linkState, peerGUID, "fmt:", fmt)
        cf= workbook.add_format (fmt)
        worksheet.write (row, col + i, s, cf)    # Create the cell
        if splittable:
            s = 'Connnector ' + str (int ((port + 1) / 2)) + '\nLogical port ' + str (port) +':\n'
        else:
            s = 'Port ' + str (port) +':\n'
        if (linkState == 0):
            if split:
                s = '2nd half (2x lanes) of Port ' + str (port - 1)
            else:
                s = s + 'Peer: None\nLink: None'
        else:
            s = s + 'Peer: ' + nodeTypes.get (peerTypeAndLinkType [0:1], '??') + '\n'
            s = s + 'Peer link: ' + peerTypeAndLinkType [-3:]
            if linkState == 1: s = s + ' SLOW'
            if peerGUID in ibNet or peerGUID in allDirectors:    # If we have a peer Node
                s = s + '\nPeer GUID: ' + peerGUID + '\n'
                s = s + 'Peer LID: ' + peerLID.strip()
                if (peerLID.strip()).isdecimal():    # (Note: '1-line if' doesn't work here for some reason)
                    s = s + ' ' + hex (int (peerLID.strip()))
                s = s + '\nPeer port: ' + peerPort + '\n'
                if peerGUID in ibNet:
                    s = s + 'Peer model: ' + ibNet [peerGUID].nodeModel + '\n'
                    s = s + 'Peer desc: ' + (ibNet [peerGUID].nodeDesc.rsplit ('"', 1))[0] + '"'
        worksheet.write_comment (row, col + i, s)    # Create the cell comment          
#### end showSwitchRowXLS ####

#### showSwitch2Rows ####
def showSwitch2Rows (row, col):
    global currentNode
    global workbook
    global worksheet
    global currentLinkWidths
    global currentPeerGUIDs
    cf1 = workbook.add_format ({'color': 'black', 'bold': True, 'align': 'left', 'border': 0, 'text_wrap': False, 'font_size': 14})
    cf2 = workbook.add_format ({'bold': True, 'font_color': '#808080', 'align': 'center', 'border': 0, 'text_wrap': False})
    cf3 = workbook.add_format ({'italic': True, 'bold': True, 'font_color': 'orange', 'align': 'right', 'left': 1, 'text_wrap': False})
    s1, s2 = putSwitchSummaryXLS (True)
    worksheet.write (row, col, s1, cf1)
    worksheet.write (row + 1, col, s2, cf1)
    ibGen = currentNode.nodeIBGen
    ppr = int (int (currentNode.nodePortCount) / 2)    # Ports per row
    sp = int (currentNode.nodePortCount) % 2    # See if there's an extra (odd #) port, for SHARP    
    if sp > 0: showSHARP (row + 1, col + ppr)
    currentLinkWidths = [" "] * (ppr + sp) 
    currentPeerGUIDs = [" "] * (ppr + sp)
    x = 0
    if ibGen in ["NDR"]:
        x = 1
        worksheet.set_row (row + 2, 12)   # Row height for OSFP #s
        worksheet.write (row + 2, col - 1, 'OSFP  ', cf3)
        for c in range (0, ppr, 2):
            worksheet.write (row + 2, col + c, c + 1, cf3)
    portList = []
    for i in range (0, ppr + sp):
        portList.append ((i * 2) + 1)
    worksheet.set_row (row + 2 + x, 12)   # Row height for Port #s
    worksheet.write (row + 2 + x, col - 1, '4x Port', cf2)
    for c in range (0, len (portList)):
        worksheet.write (row + 2 + x, col + c, portList [c], cf2)
    showSwitchRowXLS (row + 3 + x, col, portList, False, False)
    portList = []
    for i in range (0, ppr):
        portList.append ((i * 2) + 2)
    showSwitchRowXLS (row + 4 + x, col, portList, False, False)
    worksheet.set_row (row + 5 + x, 12)   # Row height for Port #s
    worksheet.write (row + 5 + x, col - 1, '4x Port', cf2)
    for c in range (0, len (portList)):
        worksheet.write (row + 5 + x, col + c, portList [c], cf2)
    if x > 0:    # NDR
        worksheet.set_row (row + 7, 12)   # Row height for OSFP #s
        worksheet.write (row + 7, col - 1, 'OSFP  ', cf3)
        for c in range (0, ppr, 2):
            worksheet.write (row + 7, col + c, c + 2, cf3)
    return (9 if (x == 1) else 7)
#### end of showSwitch2Rows ####

#### showSwitch4Rows ####
def showSwitch4Rows (row, col):
    global currentNode
    global workbook
    global worksheet
    global currentLinkWidths
    global currentPeerGUIDs
    cf1 = workbook.add_format ({'color': 'black', 'bold': True, 'align': 'left', 'border': 0, 'text_wrap': False, 'font_size': 14})
    cf2 = workbook.add_format ({'bold': True, 'font_color': '#808080', 'align': 'center', 'border': 0, 'text_wrap': False})
    cf3 = workbook.add_format ({'italic': True, 'bold': True, 'font_color': 'orange', 'align': 'right', 'left': 1, 'text_wrap': False})
    cf4 = workbook.add_format ({'italic': True, 'bold': True, 'font_color': 'blue', 'align': 'center', 'border': 0, 'text_wrap': False})
    s1, s2 = putSwitchSummaryXLS (True)
    worksheet.write (row, col, s1, cf1)
    worksheet.write (row + 1, col, s2, cf1)
    ppr = int (int (currentNode.nodePortCount) / 4)    # Ports per row
    sp = int (currentNode.nodePortCount) % 2    # See if there's an extra (odd #) port, for SHARP 
    if sp > 0: showSHARP (row + 1, col + ppr)   
    currentLinkWidths = [" "] * (ppr + sp)
    currentPeerGUIDs = [" "] * (ppr + sp)
    x = 0
    if currentNode.nodeIBGen in ['NDR']:
        x = 1
        worksheet.set_row (row + 2, 12)   # Row height for OSFP #s
        worksheet.write (row + 2, col - 1, 'OSFP  ', cf3)
        for c in range (0, ppr, 2):
            worksheet.write (row + 2, col + c, c + 1, cf3)
    worksheet.set_row (row + 2 + x, 12)   # Row height for physical port #s
    worksheet.write (row + 2 + x, col - 1, '4x Port', cf2)
    for c in range (0, ppr + sp):
        worksheet.write (row + 2 + x, col + c, (c * 2) + 1, cf2)        
    worksheet.set_row (row + 3 + x, 12)   # Row height for logical port #s
    worksheet.write (row + 3 + x, col - 1, '2x Port', cf4)
    portList = []
    for i in range (0, ppr + sp):
        portList.append ((i * 4) + 1)
    for c in range (0, len (portList)):
        worksheet.write (row + 3 + x, col + c, portList [c], cf4)    # Logical port #s
    showSwitchRowXLS (row + 4 + x, col, portList, True, False)
    #print (currentLinkWidths, currentPeerGUIDs)
    portList = []
    for i in range (0, ppr):
        portList.append ((i * 4) + 2)
    showSwitchRowXLS (row + 5 + x, col, portList, True, True)
    portList = []
    for i in range (0, ppr):
        portList.append ((i * 4) + 3)
    showSwitchRowXLS (row + 6 + x, col, portList, True, False)
    #print (currentLinkWidths, currentPeerGUIDs)
    portList = []
    for i in range (0, ppr):
        portList.append ((i * 4) + 4)
    showSwitchRowXLS (row + 7 + x, col, portList, True, True)
    worksheet.set_row (row + 8 + x, 12)   # Row height    # For logical port #s
    worksheet.write (row + 8 + x, col - 1, '2x Port', cf4)
    for c in range (0, len (portList)):
        worksheet.write (row + 8 + x, col + c, portList [c], cf4)
    worksheet.set_row (row + 9 + x, 12)   # Row height for physical port #s
    worksheet.write (row + 9 + x, col - 1, '4x Port', cf2)
    for c in range (0, ppr):
        worksheet.write (row + 9 + x, col + c, (c * 2) + 2, cf2)
    if x > 0:    # NDR
        worksheet.set_row (row + 11, 12)   # Row height for OSFP #s
        worksheet.write (row + 11, col - 1, 'OSFP  ', cf3)
        for c in range (0, ppr, 2):
            worksheet.write (row + 11, col + c, c + 2, cf3) 
    return (13 if (x == 1) else 11)
#### end of showSwitch4Rows ####

#### doSwitchesXLS ####
def doSwitchesXLS ():
    global ibNet    # From Tarzan
    global currentNode
    global fPath    # From Tarzan
    global fnameBase    # From Tarzan
    global workbook
    global worksheet
    buildColors ()
    fname = fPath + fnameBase + "_switches.xlsx"
    workbook = xlsxwriter.Workbook (fname)
    #workbook.read_only_recommended ()
    worksheet = workbook.add_worksheet ('Switches')
    worksheet.hide_zero()    # Not sure what this does for us
    s = 'File: ' + putIbnetdiscoverNameAndDate ()    # From Tarzan
    cf = workbook.add_format ({'font': 'Arial', 'color': 'blue', 'bold': True, 'align': 'left', 'border': 0, 'text_wrap': False, 'font_size': 16})
    worksheet.write (0, 0, s, cf)
    row = 1
    for x, guid in enumerate (ibNet):
        currentNode = ibNet [guid]
        if currentNode.nodeType == "S" and int (currentNode.nodePortCount) in [36, 37, 40, 41, 64, 65]:
            if currentNode.nodeDirectorGUID == " ":          
                n = showSwitch2Rows (row, 1)
                row = row + n
    for x, guid in enumerate (ibNet):
        currentNode = ibNet [guid]
        if currentNode.nodeType == "S" and int (currentNode.nodePortCount) in [80, 81, 128, 129]:
            if currentNode.nodeDirectorGUID == " ":          
                n = showSwitch4Rows (row, 1)
                row = row + n
    # Try to close() the file in a loop so that if there is an exception, such as
    # if the file is open in Excel, we can ask the user to close the file, and
    # try again to overwrite it.
    while True:
        try:
            workbook.close()
        except xlsxwriter.exceptions.FileCreateError as e:
            decision = input ("Exception caught in workbook.close(): %s\n"
                         "Please close the file if it is open in Excel.\n"
                         "Try to write file again? [Y/n]: " % e)
            if decision != 'n':
                continue
        break
#### end of doSwitchesXLS ####


#####################################################################################
#### Begin routines to generate a graphical report displaying 'low latency neighborhoods' on Directors.
#####################################################################################
#### putSWRowHoods ####
# Builds & returns RTF text representing a row of Director ports, starting at startPort and.increasing the port 
# by incPort (typically 2) until endPort has been handled.
def putSWRowHoods (guid, startPort, endPort, incPort):
    global ibNet
    global rtfColorIndex
    global nodeRTFStrings
    peerNodeGUID = [noPeer]    # For use by the peerExists routine
    peerLink = [" "]    # For use by the peerExists routine
    vlin = "\\u9474?"    # Box Drawings Light Vertical
    s = vlin
    for p in  range (startPort, endPort + 1, incPort):
        #print ("p = ", p)    #### DEBUG ####
        # There are 4 possible cases for a Leaf ASIC peer:  it could be no peer (black), it could be 
        # an HCA ("H" on white), it could be a Switch not in any neighborhood ("S" on gray), or it could be
        # a Switch belonging to a neighborhood (neighborhood number on neighborhood color)
        case = 1   # The value for 'no peer' case 
        if peerExists (guid, p, peerNodeGUID, peerLink): 
            #print ("Peer GUID ", peerNodeGUID [0], " HOOD=", ibNet [peerNodeGUID [0]].nodeNeighborhood)    #### DEBUG ####
            if ibNet[peerNodeGUID[0]].nodeType == "H":
                case = 2
            else:
                case = 4
                s1 = ibNet [peerNodeGUID [0]].nodeNeighborhood
                if s1 == " ":
                    case = 3    # A Switch, but not in a neighborhood
        if case == 1:
            ci = rtfColorIndex ["Black"]
            s2 =  "   "
        elif case == 2:
            ci = rtfColorIndex ["White"]
            s2 = " H "
        elif case == 3:
            ci = rtfColorIndex ["Gray 30%"]
            s2 = " S "
        else:    # A Switch that has been assigned a neighborhood number
            nn = int (s1) - 1
            m = len (nodeRTFStrings) - 4
            ci = (nn % m) + 4
            #print ("nn=", nn, " m=", m, " ci=",ci)
            s2 = s1.center(3)
        s = s + nodeRTFStrings[ci][0] + " " + s2 + nodeRTFStrings[ci][1] + vlin
    return (s)
#### end of putSWRowHoods ####






#####################################################################################
#### Begin routines to generate a .TOPO file from an  ibnetdiscover file.
#####################################################################################

# This code was never completed and was omitted in August 2022.

#####################################################################################
#### Begin routines for other stuff.
#####################################################################################

#### dumpHCAs ####
# Quick and dirty routine to print a list of HCA node names.
# Doesn't even try to put the resulting file in the right location.
def dumpHCAs ():
    global ibNet
    f2=open("d:HCA_Names.txt", "w")    
    ccc=0
    for i, key in enumerate (ibNet):
        n = ibNet[key].nodeType
        d = ibNet[key].nodeDesc
        if n == "H":
            m = len(d) - 8
            f2.write (key + ": " + d [2:m] + "\n")
            ccc=ccc+1
   # print(ccc + " HCAs")
    f2.close()
#### end of dumpHCAs ####


############################################################################################################################################################
########################### This is to draw End host servers ###############################################################################################

def drawing_EndHosts (values_from_drawing_options):
    global fPath
    global fnameBase
    global boxGraph
    global gv
    global minRankBoxes    ####
    global maxRankBoxes    ####
    global sameRankBoxes    ####
    global BoxHCAs
    global BoxISLs
    global boxRankLists # This list has an order like [Max, Same,,,Same, MIN]. Please rfer to 'new_rank_list'. That is a reversed boxRankLists
    global linkColor
    global dontDrawBox
    global boxClade
    global boxNeighbors 
    global cladeList    ####
    global gvL1BoxesToStack
    global genTimeAndDate
    global showCableCount
    global lineScheme
    global sawWXR
    global warn_return2  #This is to warn Any errors 

    total_number_of_line = 0
            
    dontDrawBox = {}
    
    hostGuid_list_temp = []
    for_Min_hostGuid_list_temp = []
    switchGuid_list_temp = []
    new_rank_list = []  # This is a reversed boxRankLists. The list order is [min, same, same, max]
    New_boxGraph = {}  # It's the same list order above new_rank_list {min, same, same, max...}
  
    
    # Create a .gv file and set some introductory attributes
    gvname = fPath + fnameBase + "_graphviz_End_hosts.gv"
    gv = open (gvname, "w")    # Overwrite if it already exists
    gv.write ("graph ibnetdiscover {\n")
    gv.write ('splines = "line";\n')    # Straight lines between boxes      
    gv.write ('node [shape = "rectangle", fontsize='+ values_from_drawing_options[39] + ', fontname="'+ values_from_drawing_options[38] + '"];\n')    # Default gv box
    gv.write ('ranksep = "' + values_from_drawing_options[1] +' equally";\n')    # Request 4 inches between ranks
    gv.write ('nodesep = "' + str(values_from_drawing_options[2]) + '";\n')    
    # Create a gv node that will serve as the graph caption
    l3 = ''
   
    if values_from_drawing_options[3] :
        gv.write ('"caption"  [fontsize = ' + values_from_drawing_options[39] + ', fontname = "' + values_from_drawing_options[38] +  '" , style =  "' + values_from_drawing_options[40] +  '" , label = "' + values_from_drawing_options[3] + '"]\n')    
        caption =  '"caption"  [fontsize = ' + values_from_drawing_options[39] + ', fontname = "' + values_from_drawing_options[38] + '" , style  = "' + values_from_drawing_options[40]  + '" , label = "' + values_from_drawing_options[3] + '"]\n'
  

    if findDirs == True and allDirectors  :  # This function is to add "Host" in Combined Asic to director

            for i, key_temp in enumerate (boxRankLists[0]): # 지금은 max이다.

                node_temp = ibNet [key_temp]
                if node_temp.nodeType == "S":    # 
        
                    ports = int (node_temp.nodePortCount) # 37이 들어간다.
                    switchGuid_list_temp.append (key_temp)   
                    for p in range (1,ports):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다.
                        port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
            
                        
                        if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                            link_temp = port_temp.portLink    # Get Link structure for this port
                            if link_temp.peerType == "H":    # Is it an HCA?
                                hostGuid_list_temp.append (link_temp.peerNodeGUID)
                                                    
            new_rank_list.append(list(hostGuid_list_temp))  # max가 되고, 나중에 뒤집한다...
            new_rank_list.append(list(switchGuid_list_temp))
                                            
        
            
            for i in range (1, len(boxRankLists)):
                switchGuid_list_temp = []
                if boxRankLists[i] == boxRankLists[-1] :         
                    for x, key_temp in enumerate (boxRankLists[-1]):
                        
                        if key_temp in allDirectors :
                            switchGuid_list_temp.append (key_temp)   
                        else : 
                                node_temp = ibNet [key_temp]
                                if node_temp.nodeType == "S":    # 
                                    ports = int (node_temp.nodePortCount) # 37이 들어간다.    
                                    switchGuid_list_temp.append (key_temp)
                    
                                    for p in range (1,ports):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다.
                                        port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                            
                                        if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                            link_temp = port_temp.portLink    # Get Link structure for this port                 
                                            if link_temp.peerType == "H":    # Is it an HCA?
                                                for_Min_hostGuid_list_temp.append (link_temp.peerNodeGUID)
                                
                    new_rank_list.append(list(switchGuid_list_temp))                


                else :
            
                    for x, key_temp in enumerate (boxRankLists[i]):  # max바로 위에간...중간
                        node_temp = ibNet [key_temp]
                        
                        if node_temp.nodeType == "S":    # 
                            ports = int (node_temp.nodePortCount) # 37이 들어간다.    
                            switchGuid_list_temp.append (key_temp)
                            for p in range (1,ports):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다.
                                port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                    
                                if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                    link_temp = port_temp.portLink    # Get Link structure for this port
                            
                                    if link_temp.peerType == "H":    # Is it an HCA?
                                        hostGuid_list_temp.append (link_temp.peerNodeGUID)
                                        new_rank_list[0] = hostGuid_list_temp              
                    new_rank_list.append(list(switchGuid_list_temp))    
   
    else :   # This function is to add "Host" in Combined Asic to director
            for i, key_temp in enumerate (boxRankLists[0]): # This is a 'max' in graphize
            

                node_temp = ibNet [key_temp]
                if node_temp.nodeType == "S":     
        
                    ports = int (node_temp.nodePortCount) 
                    switchGuid_list_temp.append (key_temp)

                    for p in range (1,ports):  # This to exclude Agg which is the last and it starts from port1 because we don't have port0
                        port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
            
                        
                        if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                            link_temp = port_temp.portLink    # Get Link structure for this port
                            if link_temp.peerType == "H":    # Is it an HCA?
                                hostGuid_list_temp.append (link_temp.peerNodeGUID)           
            new_rank_list.append(list(hostGuid_list_temp))  
            new_rank_list.append(list(switchGuid_list_temp))

            for i in range (1, len(boxRankLists)):
                switchGuid_list_temp = []          
                if boxRankLists[i] == boxRankLists[-1] :             
                    for x, key_temp in enumerate (boxRankLists[-1]):
                        node_temp = ibNet [key_temp]
                        
                        if node_temp.nodeType == "S":    # 
                            ports = int (node_temp.nodePortCount) # 37이 들어간다.    
                            switchGuid_list_temp.append (key_temp)

                            for p in range (1,ports):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다.
                                port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                    
                                if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                    link_temp = port_temp.portLink    # Get Link structure for this port                 
                                    if link_temp.peerType == "H":    # Is it an HCA?
                                        for_Min_hostGuid_list_temp.append (link_temp.peerNodeGUID)


                    new_rank_list.append(list(switchGuid_list_temp))                

        
                    
                else :
            
                    for x, key_temp in enumerate (boxRankLists[i]):  # max바로 위에간...중간
            
                        node_temp = ibNet [key_temp]
                        
                        if node_temp.nodeType == "S":    # 
                            ports = int (node_temp.nodePortCount) # 37이 들어간다.    
                            switchGuid_list_temp.append (key_temp)
                            for p in range (1,ports):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다.
                                port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                    
                                if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                    link_temp = port_temp.portLink    # Get Link structure for this port
                            
                                    if link_temp.peerType == "H":    # Is it an HCA?
                                        hostGuid_list_temp.append (link_temp.peerNodeGUID)
                                        new_rank_list[0] = hostGuid_list_temp
                    new_rank_list.append(list(switchGuid_list_temp))    
                    
            if  for_Min_hostGuid_list_temp : 
                new_rank_list.append(list(for_Min_hostGuid_list_temp))


    
    for i in range(len(new_rank_list)):
        
        node_guid_temp = ""
        if i == 0 :
            
            s_temp = '{rank = max ' + l3    # Begin the string that lists 'max rank' boxes; it includes the legend boxes
            
            for x, key_temp in enumerate (new_rank_list[0]):
                temp_option = '[shape = ' + values_from_drawing_options[7] + ', fixedsize = true, fontsize = ' + values_from_drawing_options[8] +  ', width = ' + values_from_drawing_options[9] + ', height = ' + values_from_drawing_options[10] + ', style = ' + values_from_drawing_options[11] + ', fontcolor = ' + values_from_drawing_options[12] +  ', fillcolor = ' + values_from_drawing_options[13] + ' ]'      
                if ibNet [key_temp].nodeType == "S":                                           
                    temp_option = '[shape = ' + values_from_drawing_options[14] + ', fixedsize = true, fontsize = ' + values_from_drawing_options[15] +  ', width = ' + values_from_drawing_options[16] + ', height = ' + values_from_drawing_options[17] + ', style = ' + values_from_drawing_options[18] + ', fontcolor = ' + values_from_drawing_options[19] +  ', fillcolor = ' + values_from_drawing_options[20] + ' ]'
                
                total_number_of_line = total_number_of_line +1
                s_temp = s_temp + ' "' + key_temp + '"' 
                node_guid_temp = node_guid_temp + '"' + key_temp + '" ' + temp_option + "\n"
        
            gv.write (node_guid_temp )
            gv.write (s_temp + "}\n") 
        
            

        elif new_rank_list[i] ==  new_rank_list[-1] :
            if values_from_drawing_options[3]  :
                s_temp = '{rank = min "caption "' + l3     
                           
            s_temp = '{rank = min ' + l3    # Begin the string that lists 'max rank' boxes; it includes the legend boxes
            for x, key_temp in enumerate (new_rank_list[i]):
            
                temp_option = '[shape = ' + values_from_drawing_options[28] + ', fixedsize = true, fontsize = ' + values_from_drawing_options[29] +  ', width = ' + values_from_drawing_options[30] + ', height = ' + values_from_drawing_options[31] + ', style = ' + values_from_drawing_options[32] + ', fontcolor = ' + values_from_drawing_options[33] +  ', fillcolor = ' + values_from_drawing_options[34] + ' ]'             
                
                if findDirs == True and allDirectors :
                    temp_option = '[shape = ' + values_from_drawing_options[28] + ', fixedsize = true, fontsize = ' + values_from_drawing_options[29] +  ', width = ' + values_from_drawing_options[30] + ', height = ' + values_from_drawing_options[31] + ', style = ' + values_from_drawing_options[32] + ', fontcolor = ' + values_from_drawing_options[33] +  ', fillcolor = ' + values_from_drawing_options[34] + ' ]'             
                    
                else :
                    
                    if ibNet [key_temp].nodeType == "H" :
                        temp_option = '[shape = ' + values_from_drawing_options[7] + ', fixedsize = true, fontsize = ' + values_from_drawing_options[8] +  ', width = ' + values_from_drawing_options[9] + ', height = ' + values_from_drawing_options[10] + ', style = ' + values_from_drawing_options[11] + ', fontcolor = ' + values_from_drawing_options[12] +  ', fillcolor = ' + values_from_drawing_options[13] + ' ]'
                
                total_number_of_line = total_number_of_line +1
                s_temp = s_temp + ' "' + key_temp + '"' 
                node_guid_temp = node_guid_temp + '"' + key_temp + '" ' + temp_option + "\n"

            gv.write (node_guid_temp)        
            gv.write (s_temp + "}\n")
            
        
        else : 
            s_temp = '{rank = same ' + l3  
        
           
            for x, key_temp in enumerate (new_rank_list[i]):
     
                temp_option = '[shape = ' + values_from_drawing_options[7] + ', fixedsize = true, fontsize = ' + values_from_drawing_options[8] +  ', width = ' + values_from_drawing_options[9] + ', height = ' + values_from_drawing_options[10] + ', style = ' + values_from_drawing_options[11] + ', fontcolor = ' + values_from_drawing_options[12] +  ', fillcolor = ' + values_from_drawing_options[13] + ' ]'
                    
                if ibNet [key_temp].nodeType == "S":                                    
                    temp_option = '[shape = ' + values_from_drawing_options[21] + ', fixedsize = true, fontsize = ' + values_from_drawing_options[22] +  ', width = ' + values_from_drawing_options[23] + ', height = ' + values_from_drawing_options[24] + ', style = ' + values_from_drawing_options[25] + ', fontcolor = ' + values_from_drawing_options[26] +  ', fillcolor = ' + values_from_drawing_options[27] + ' ]'
                            
                total_number_of_line = total_number_of_line +1                                 
                s_temp = s_temp + ' "' + key_temp + '"' 
                node_guid_temp = node_guid_temp + '"' + key_temp + '" '  + temp_option + "\n"

            gv.write (node_guid_temp)        
            gv.write (s_temp + "}\n")
    
    new_rank_list.reverse()

     
    if findDirs == True and allDirectors  :

            for z, key in enumerate (new_rank_list):
                    total_len = len(new_rank_list)        
            
                    for x, key2 in enumerate (key):
                        inside_dict = {}
                        x = x + 1        
                        list_len = len(key)
                        
                        if key2 in allDirectors :
                            direct_node_temp =  allDirectors[key2]
                            directorPeerList_temp = direct_node_temp.directorPeerList
                            for i in range(len(directorPeerList_temp)) :
                                direct_port_temp = direct_node_temp.directorPeerList [i] 
                                if direct_port_temp.peerNodeType == "S" or direct_port_temp.peerNodeType == "H": 
                                    inside_dict[direct_port_temp.peerNodeGUID] = 1

                        else : 
                            node_temp = ibNet [key2]  
                            ports = int (node_temp.nodePortCount) # 37이 들어간다.        
                            for i in range(list_len) :
                                if x+i == list_len :
                                    break                          
                                elif node_temp.nodeType == "H" :
                                    for p in range (1,ports+1):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다. 
                        
                                        port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                        if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                            link_temp = port_temp.portLink    # Get Link structure for this port              
                                            if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                                if key[x+i] == link_temp.peerNodeGUID :
                                                    inside_dict[link_temp.peerNodeGUID] = 1

                                elif node_temp.nodeType == "S" :
                                    for p in range (1,ports):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다. 
                        
                                        port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                        if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                            link_temp = port_temp.portLink    # Get Link structure for this port              
                                            if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                                if key[x+i] == link_temp.peerNodeGUID :
                                                    inside_dict[link_temp.peerNodeGUID] = 1
                                else  :      
                                    warn_return2.append("Something wrong occured in nodeType, please check ibnetdiscovery file")         
                                 
 
                        for y in range(z, total_len) :
                            if key2 in allDirectors :
                                break
                            
                            else :
                                y = y + 1
                                if y == total_len :
                                    break
                                temp = new_rank_list[y]
                                for i, key3 in enumerate (temp):
                                    if node_temp.nodeType == "H" :
                                        for p in range (1,ports+1):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다. 
                        
                                            port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                            if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                                link_temp = port_temp.portLink    # Get Link structure for this port              
                                                if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                                    if key3 == link_temp.peerNodeGUID :
                                                        inside_dict[link_temp.peerNodeGUID] = 1

                                    if node_temp.nodeType == "S" :
                                        for p in range (1,ports):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다. 
                                            port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                            if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                                link_temp = port_temp.portLink    # Get Link structure for this port              
                                                if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                                    if key3 == link_temp.peerNodeGUID :
                                                        inside_dict[link_temp.peerNodeGUID] = 1
    
                        New_boxGraph[key2] = inside_dict


            for i, key in enumerate (New_boxGraph):   # For each Node GUID or Director GUID in boxGraph
                nd = New_boxGraph [key]    # Get the dictionary of neighbors 

                                                                
                for j, key2 in enumerate (nd):    # Get each of the neighbor GUIDs
             
                        node_temp1 = ibNet [key2]     
                        s_temp = ""
                        s3_cable_temp = ""      
                        s1_temp_penwidth = ""                             
                             
                        if node_temp1.nodeType == "H" : 
                            if key in allDirectors :
                                s_temp = "red"     
                                s1_temp_penwidth = "10" 
                            else :
                                s_temp = values_from_drawing_options[35]   
                                
                        elif key in allDirectors :
                            s_temp = values_from_drawing_options[36]         
                        else : 
                            node_temp = ibNet [key]     
                            if node_temp.nodeType  == "H"  :
                                    s_temp = values_from_drawing_options[35]      
                            else : 
                                    for i, temp_list in enumerate (boxRankLists):  
                                        if i == 0 :
                                            if key2 in boxRankLists[0] : 
                                                    s_temp = values_from_drawing_options[36] 
                                            else : 
                                                    s_temp = values_from_drawing_options[37] 

                        if showCableCount == 1 :
                           
                            if key in allDirectors : 
                                if node_temp1.nodeType == "S" :
                                    
                                    if key2 in boxGraph : 
                                        s3_cable_temp =  ",labelfloat=false, label=" + '"' + str(boxGraph[key2][key]) + '"'          
                                    
                                    if key in boxGraph :     
                                        if key2 in boxGraph[key] :                
                                            s3_cable_temp =  ",labelfloat=false, label=" + '"' + str(boxGraph[key][key2]) + '"'                     
                                
                            if (node_temp.nodeType == "S" ) and (node_temp1.nodeType == "S") :

                                    if key2 in boxGraph : 
                                        if key in boxGraph[key2] :
                                            s3_cable_temp =  ",labelfloat=false, label=" + '"' + str(boxGraph[key2][key]) + '"'  
                                    if key in boxGraph :          
                                        if key2 in boxGraph[key] :                                                     
                                            s3_cable_temp =  ",labelfloat=false, label=" + '"' + str(boxGraph[key][key2]) + '"'                 
                                                           
                        s = '"' + key + '" -- "' + key2 + '" [color=' + s_temp  + s3_cable_temp + '];'
                                            

                        if s1_temp_penwidth :
                            s = '"' + key + '" -- "' + key2 + '" [penwidth=' + s1_temp_penwidth  + ', color=' + s_temp  + '];'        
                            warn_messages = "End_Host server directly connected to Director switch, please check : " + key2
                            warn_return2.append(warn_messages)    
                        total_number_of_line = total_number_of_line +1                                   
                        gv.write (s +"\n")      
      
    else :        
            for z, key in enumerate (new_rank_list):
                    total_len = len(new_rank_list)        
            
                    for x, key2 in enumerate (key):
                        inside_dict = {}
                        x = x + 1        
                        list_len = len(key)
                        node_temp = ibNet [key2]  
                        ports = int (node_temp.nodePortCount)        

                        for i in range(list_len) :
                            if x+i == list_len :
                                break                          
                            elif node_temp.nodeType == "H" :
 
                                                    
                                for p in range (1,ports+1):  #마지막 말번은 Aggre 제외 하기 위함. 그리고 1번은,,port0s는 없기 때문이다. 
                    
                                    port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                    if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                        link_temp = port_temp.portLink    # Get Link structure for this port              
                                        if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                            if key[x+i] == link_temp.peerNodeGUID :
                                                inside_dict[link_temp.peerNodeGUID] = 1
                         

                            elif node_temp.nodeType == "S" :
                                for p in range (1,ports):  #This is to exclude Aggregate node. And it starts from 1, because There is no port0s. 
                    
                                    port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                    if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                        link_temp = port_temp.portLink    # Get Link structure for this port              
                                        if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                            if key[x+i] == link_temp.peerNodeGUID :
                                                inside_dict[link_temp.peerNodeGUID] = 1
 
                            else  :      
                                warn_return2.append("Something wrong occured in nodeType, please check ibnetdiscovery file")         
                                

                        for y in range(z, total_len) :
                            y = y + 1
                            
                            if y == total_len :
                                break
                            temp = new_rank_list[y]

                            for i, key3 in enumerate (temp):
            
                                if node_temp.nodeType == "H" :
                                    for p in range (1,ports+1):  
                    
                                        port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                        if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                            link_temp = port_temp.portLink    # Get Link structure for this port              
                                            if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                                if key3 == link_temp.peerNodeGUID :
                                                    inside_dict[link_temp.peerNodeGUID] = 1

                                if node_temp.nodeType == "S" :
                                    for p in range (1,ports):  
                    
                                        port_temp = node_temp.nodePortList [p]    # Get Port structure for this port
                                        if port_temp.portType == "IB" and port_temp.portConnected == "Y":
                                            link_temp = port_temp.portLink    # Get Link structure for this port              
                                            if link_temp.peerType == "S" or link_temp.peerType == "H":    
                                                if key3 == link_temp.peerNodeGUID :
                                                    inside_dict[link_temp.peerNodeGUID] = 1
                        New_boxGraph[key2] = inside_dict
         
            
            for i, key in enumerate (New_boxGraph):   # For each Node GUID or Director GUID in boxGraph
                nd = New_boxGraph [key]    # Get the dictionary of neighbors          
                                              
                for j, key2 in enumerate (nd):    # Get each of the neighbor GUIDs
                    
                        s1_temp_penwidth = ""       
                        s3_cable_temp = ""                               
                        node_temp = ibNet [key]     
                        node_temp1 = ibNet [key2]    
                        s_temp = ""
                                                               
                        if node_temp.nodeType  == "H"  :                            
                            s_temp = values_from_drawing_options[35]
                                
                        elif node_temp1.nodeType == "H"  :
                                if ("CS85" in node_temp.nodeDesc) or ("CS75" in node_temp.nodeDesc)  : 
                                    s_temp = "red"     
                                    s1_temp_penwidth = "10" 
                                    
                                elif len(boxRankLists) >= 2 :
                                     for i in range (1, len(boxRankLists)) :
                                        if key in boxRankLists[i] :
                                            s_temp = "red"     
                                            s1_temp_penwidth = "10" 
                                            break
                                        else : 
                                            s_temp = values_from_drawing_options[35]
                                                                                
                                    
                                else :                                 
                                    s_temp = values_from_drawing_options[35]

                        else : 
                                for i, temp_list in enumerate (boxRankLists):  
                                    if i == 0 :
                                        if key2 in boxRankLists[0] : 
                                                s_temp = values_from_drawing_options[36] 
                                        else : 
                                                s_temp = values_from_drawing_options[37] 
                       
                        if showCableCount == 1 :
                           
                            if (node_temp.nodeType == "S" ) and (node_temp1.nodeType == "S") :

                                    if key2 in boxGraph : 
                                        if key in boxGraph[key2] :
                                            s3_cable_temp =  ",labelfloat=false, label=" + '"' + str(boxGraph[key2][key]) + '"'  
                                    if key in boxGraph :          
                                        if key2 in boxGraph[key] :                                                     
                                            s3_cable_temp =  ",labelfloat=false, label=" + '"' + str(boxGraph[key][key2]) + '"'                 
                                                           
                        s = '"' + key + '" -- "' + key2 + '" [color=' + s_temp  + s3_cable_temp + '];'
                        if s1_temp_penwidth :
                            s = '"' + key + '" -- "' + key2 + '" [penwidth=' + s1_temp_penwidth  + ', color=' + s_temp  + s3_cable_temp + '];'        
                            warn_messages = "End_Host server directly connected to Director switch, please check : " + key2
                            warn_return2.append(warn_messages)   
                        total_number_of_line = total_number_of_line +1                            
                        gv.write (s +"\n")      
    
    gv.write ("}\n")                
    gv.close ()
    if total_number_of_line > 4200 : # Graphviz fails to draw map in VISIO, This is Graphize limitation i guess. Not my script issue.
        warn_return2.append("If total number of gv line is more than 4200, Graphviz sometimes fails to draw map in VISIO. This is Graphize limitation i guess. Not my script issue. You can try, but if you fails to draw in VISIO, I recommend you only run switch gv file in VISIO, not host gv") 



        
#### end of Drawing End host server ####

def initialization_All_values ():

    global spineGUIDs  
    global genTimeAndDate
    global ibNet
    global islDict
    global Boxes
    global Spines
    global Leafs
    global allDirectors
    global rtfEOL
    global rtfColors 
    global nodeColors 
    global resolveDirectors
    global findDirs 
    global dontDrawBox 
    global defaultPortColor 
    global currentLinkWidths
    global currentPeerGUIDs 
    global allHCAs
    global hcasBySwitch 
    global hcasByDirector 
    global portSpeed
    global hcasWithVPorts
    global warn_return     #This is to warn Invalid unicat LID number
    global warn_return1    #This is to warn Mcast LID number
    global warn_return2    #This is to warn Any errors 
    global hdrx
    global boxGraph
    boxGraph = {}
    
    hdrx = []    
    spineGUIDs = []    
    genTimeAndDate = "???"
    ibNet = {}
    islDict = {}
    Boxes = {}
    Spines = {}
    Leafs = {}
    allDirectors = {}
    rtfEOL = "\\line\n"
    rtfColors = 0
    nodeColors = {}
    resolveDirectors = True
    findDirs = True
    dontDrawBox = {}
    defaultPortColor = 130 * [" "]    # Used by the 'show split port switch' routines
    currentLinkWidths = 130 * [" "]
    currentPeerGUIDs = 130 * [" "]
    allHCAs = {}
    hcasBySwitch = {}
    hcasByDirector = {}
    portSpeed = {}
    hcasWithVPorts = 0
    warn_return = []  #This is to warn Invalid unicat LID number
    warn_return1 = [] #This is to warn Mcast LID number
    warn_return2 = [] #This is to warn Any errors 

    buildDirectorMaps ()    # Create data structures for use by ProcessDirector3
    s = putRTFColorTbl (rtfColorSet)    # Initialize rtfColorIndex dictionary, then:
    buildNodeRTFStrings ()

class Ui_MainWindow(QtWidgets.QDialog):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.dd = QtWidgets.QMainWindow()
        self.otherWindow = SubWindow()
        self.otherWindow.setupUi(self.dd)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1154, 1063)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font1 = QtGui.QFont()
        font1.setPointSize(15)  # this is for Major numbering.
        MainWindow.setWindowTitle("Drawing IB Topo from ibnetdiscover 1.0 (HyungKwang Choi, s99225078@gmail.com)")             
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("alternate-background-color: rgb(130, 130, 130);\n"
"border-color: rgb(0, 0, 0);")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(30, 30, 341, 31))
        self.label_15.setFont(font1)
        self.label_15.setObjectName("label_15")
        self.label_15.setText("1. Import \"ibnetdiscovery\" file")
                
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setEnabled(True)
        self.pushButton_10.setGeometry(QtCore.QRect(50, 70, 441, 61))
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setText("Click to import Ibnetdiscovery file")
        self.pushButton_10.setStyleSheet("background-color: rgba(98, 211, 162, 255)")
                        
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(30, 150, 291, 31))
        self.label_16.setFont(font1)
        self.label_16.setObjectName("label_16")
        self.label_16.setText("2. Drawing options for Switches")
                
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(50, 190, 441, 271))
        self.groupBox_6.setObjectName("groupBox_6")
        
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_7.setGeometry(QtCore.QRect(12, 46, 421, 31))
        self.groupBox_7.setObjectName("groupBox_7")
        
        self.label_28 = QtWidgets.QLabel(self.groupBox_7)
        self.label_28.setGeometry(QtCore.QRect(10, 7, 161, 21))
        self.label_28.setObjectName("label_28")
        self.label_28.setText("Combine ASICs into Directors?")     
        
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_7)
        self.radioButton_2.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setText("No")
                
        self.radioButton_1 = QtWidgets.QRadioButton(self.groupBox_7)
        self.radioButton_1.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_1.setChecked(True)
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_1.setText("yes")
                
        self.groupBox_10 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_10.setGeometry(QtCore.QRect(10, 84, 421, 31))
        self.groupBox_10.setObjectName("groupBox_10")
        
        self.label_36 = QtWidgets.QLabel(self.groupBox_10)
        self.label_36.setGeometry(QtCore.QRect(10, 7, 281, 21))
        self.label_36.setObjectName("label_36")
        self.label_36.setText("Speed Visio by showing \'n\' similar L1 switches as one box?")
                
        self.lineEdit_1 = QtWidgets.QLineEdit(self.groupBox_10)
        self.lineEdit_1.setGeometry(QtCore.QRect(300, 7, 31, 16))
        self.lineEdit_1.setStyleSheet("background: rgb(255, 255, 255); ")
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_1.setText("1")
        self.lineEdit_1.setEnabled(False)  
                        
        self.label_19 = QtWidgets.QLabel(self.groupBox_10)
        self.label_19.setGeometry(QtCore.QRect(340, 7, 51, 16))
        self.label_19.setObjectName("label_19")
        self.label_19.setText("(1~100)")
                
        self.groupBox_48 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_48.setGeometry(QtCore.QRect(10, 122, 421, 31))
     
        self.groupBox_48.setObjectName("groupBox_48")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_48)
        self.radioButton_4.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.setText("No")
                
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_48)
        self.radioButton_3.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_3.setChecked(False)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setText("yes")       
        
        self.label_35 = QtWidgets.QLabel(self.groupBox_48)
        self.label_35.setGeometry(QtCore.QRect(10, 7, 221, 21))
        self.label_35.setObjectName("label_35")
        self.label_35.setText("Put Switch & Director names in Visio boxes?")
                
        self.groupBox_67 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_67.setGeometry(QtCore.QRect(10, 196, 421, 31))

        self.groupBox_67.setObjectName("groupBox_67")
        self.label_32 = QtWidgets.QLabel(self.groupBox_67)
        self.label_32.setGeometry(QtCore.QRect(10, 7, 241, 21))
        self.label_32.setObjectName("label_32")
        self.label_32.setText("Label Visio inter-switch lines with the # of cables?")

        self.radioButton_9 = QtWidgets.QRadioButton(self.groupBox_67)
        self.radioButton_9.setGeometry(QtCore.QRect(300, 7, 40, 17))
        self.radioButton_9.setChecked(True)
        self.radioButton_9.setObjectName("radioButton_9")
        self.radioButton_9.setText("yes")
                 
        self.radioButton_10 = QtWidgets.QRadioButton(self.groupBox_67)
        self.radioButton_10.setGeometry(QtCore.QRect(350, 7, 51, 17))
        self.radioButton_10.setChecked(False)
        self.radioButton_10.setObjectName("radioButton_10")
        self.radioButton_10.setText("No")

        self.groupBox_158 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_158.setGeometry(QtCore.QRect(10, 232, 421, 31))
        self.groupBox_158.setObjectName("groupBox_158")
        
        self.label_33 = QtWidgets.QLabel(self.groupBox_158)
        self.label_33.setGeometry(QtCore.QRect(10, 7, 281, 21))
        self.label_33.setObjectName("label_33")
        self.label_33.setText("Choose how Visio shows # of cables in inter-switch lines")
                
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_158)
        self.radioButton_5.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_5.setText("1")
        self.radioButton_5.setEnabled(False)  
                
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_158)
        self.radioButton_6.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_6.setChecked(False)
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_6.setText("2")
        self.radioButton_6.setEnabled(False)  
                
        self.groupBox_240 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_240.setGeometry(QtCore.QRect(10, 159, 421, 31))
        self.groupBox_240.setObjectName("groupBox_240")
        
        self.label_34 = QtWidgets.QLabel(self.groupBox_240)
        self.label_34.setGeometry(QtCore.QRect(10, 7, 211, 21))
        self.label_34.setObjectName("label_34")
        self.label_34.setText("Name template(s) to help find L1 switches")
        
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_240)
        self.lineEdit_3.setGeometry(QtCore.QRect(300, 7, 31, 16))
        self.lineEdit_3.setStyleSheet("background: rgb(255, 255, 255); ")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setText("No")
        self.lineEdit_3.setEnabled(False)  
                        
        self.groupBox_148 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_148.setGeometry(QtCore.QRect(10, 8, 421, 31))
        self.groupBox_148.setObjectName("groupBox_148")
        
        self.label_308 = QtWidgets.QLabel(self.groupBox_148)
        self.label_308.setGeometry(QtCore.QRect(10, 7, 131, 21))
        self.label_308.setObjectName("label_308")
        self.label_308.setText("Drawing End Host server")     
                
        self.radioButton_7 = QtWidgets.QRadioButton(self.groupBox_148)
        self.radioButton_7.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_7.setChecked(False)
        self.radioButton_7.setObjectName("radioButton_7")
        self.radioButton_7.setText("Yes")
                  
        self.radioButton_8 = QtWidgets.QRadioButton(self.groupBox_148)
        self.radioButton_8.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_8.setChecked(True)
        self.radioButton_8.setText("No")
        self.radioButton_8.setObjectName("radioButton_8")
        
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(50, 960, 441, 61))
        self.pushButton_12.setFont(font1)
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_12.setStyleSheet("background-color: rgba(98, 211, 162, 255)")
        self.pushButton_12.setText("5. Running")
                
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(30, 620, 291, 21))
        self.label_23.setFont(font1)
        self.label_23.setObjectName("label_23")
        self.label_23.setText("4. Files to create")
        
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(510, 30, 621, 991))
        self.textBrowser_2.setStyleSheet("font: 10pt \"Fixedsys\";\n"
"background-color: rgb(0, 0, 0);\n"
"color: rgb(0, 255, 72);")
        self.textBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser_2.setReadOnly(True)
        self.textBrowser_2.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.textBrowser_2.setObjectName("textBrowser_2")
#        self.textBrowser_2.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        self.textBrowser_2.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\">\n"                    
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Fixedsys\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:22pt;\">Running output displayed (error/warning..)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:22pt;\"><br /></p></body></html>")
                
        self.groupBox_310 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_310.setGeometry(QtCore.QRect(50, 650, 441, 301))
        self.groupBox_310.setObjectName("groupBox_310")

        self.groupBox_312 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_312.setGeometry(QtCore.QRect(10, 10, 421, 31))
        self.groupBox_312.setObjectName("groupBox_312")
        self.label_378 = QtWidgets.QLabel(self.groupBox_312)
        self.label_378.setGeometry(QtCore.QRect(10, 7, 161, 21))
        self.label_378.setObjectName("label_378")
        self.label_378.setText("xx_graphviz.gv")              
        self.radioButton_230 = QtWidgets.QRadioButton(self.groupBox_312)
        self.radioButton_230.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_230.setChecked(True)
        self.radioButton_230.setObjectName("radioButton_230")
        self.radioButton_230.setText("yes")
        self.radioButton_229 = QtWidgets.QRadioButton(self.groupBox_312)
        self.radioButton_229.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_229.setChecked(False)
        self.radioButton_229.setObjectName("radioButton_229")
        self.radioButton_229.setText( "No")
                
        self.groupBox_332 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_332.setGeometry(QtCore.QRect(10, 47, 421, 31))
        self.groupBox_332.setObjectName("groupBox_332")
        self.label_400 = QtWidgets.QLabel(self.groupBox_332)
        self.label_400.setGeometry(QtCore.QRect(10, 7, 141, 21))
        self.label_400.setObjectName("label_400")
        self.label_400.setText("xx_warnings.rtf")
        self.radioButton_17 = QtWidgets.QRadioButton(self.groupBox_332)
        self.radioButton_17.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_17.setChecked(False)
        self.radioButton_17.setObjectName("radioButton_17")
        self.radioButton_17.setText("yes")    
        self.radioButton_13 = QtWidgets.QRadioButton(self.groupBox_332)
        self.radioButton_13.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_13.setChecked(True)
        self.radioButton_13.setObjectName("radioButton_13")
        self.radioButton_13.setText("No")
                
        self.groupBox_342 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_342.setGeometry(QtCore.QRect(10, 83, 421, 31))
        self.groupBox_342.setObjectName("groupBox_342")
        self.label_411 = QtWidgets.QLabel(self.groupBox_342)
        self.label_411.setGeometry(QtCore.QRect(10, 7, 101, 21))
        self.label_411.setObjectName("label_411")
        self.label_411.setText( "xx_switches.rtf")                       
        self.radioButton_224 = QtWidgets.QRadioButton(self.groupBox_342)
        self.radioButton_224.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_224.setChecked(False)
        self.radioButton_224.setObjectName("radioButton_224")
        self.radioButton_224.setText("yes")
        self.radioButton_225 = QtWidgets.QRadioButton(self.groupBox_342)
        self.radioButton_225.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_225.setChecked(True)
        self.radioButton_225.setObjectName("radioButton_225")
        self.radioButton_225.setText("No")

           
        self.groupBox_352 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_352.setGeometry(QtCore.QRect(10, 119, 421, 31))
        self.groupBox_352.setObjectName("groupBox_352")
        self.label_422 = QtWidgets.QLabel(self.groupBox_352)
        self.label_422.setGeometry(QtCore.QRect(10, 7, 141, 21))
        self.label_422.setObjectName("label_422")
        self.label_422.setText( "xx_switches.xlsx")           
        self.radioButton_226 = QtWidgets.QRadioButton(self.groupBox_352)
        self.radioButton_226.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_226.setChecked(False)
        self.radioButton_226.setObjectName("radioButton_226")
        self.radioButton_226.setText("yes")   
        self.radioButton_227 = QtWidgets.QRadioButton(self.groupBox_352)
        self.radioButton_227.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_227.setChecked(True)
        self.radioButton_227.setObjectName("radioButton_227")
        self.radioButton_227.setText("No")     
 
        
        self.groupBox_362 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_362.setGeometry(QtCore.QRect(10, 156, 421, 31))
        self.groupBox_362.setObjectName("groupBox_362")
        self.label_433 = QtWidgets.QLabel(self.groupBox_362)
        self.label_433.setGeometry(QtCore.QRect(10, 7, 131, 21))
        self.label_433.setObjectName("label_433")
        self.label_433.setText("xx_HCAs.rtf")
        self.radioButton_314 = QtWidgets.QRadioButton(self.groupBox_362)
        self.radioButton_314.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_314.setChecked(False)
        self.radioButton_314.setObjectName("radioButton_314")
        self.radioButton_314.setText("yes")   
        self.radioButton_315 = QtWidgets.QRadioButton(self.groupBox_362)
        self.radioButton_315.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_315.setChecked(True)
        self.radioButton_315.setObjectName("radioButton_315")
        self.radioButton_315.setText("No")        
        

        self.groupBox_366 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_366.setGeometry(QtCore.QRect(10, 193, 421, 31))
        self.groupBox_366.setObjectName("groupBox_366")
        self.label_436 = QtWidgets.QLabel(self.groupBox_366)
        self.label_436.setGeometry(QtCore.QRect(10, 7, 131, 21))
        self.label_436.setObjectName("label_436")
        self.label_436.setText("xx_directors.rtf")       
        self.radioButton_320 = QtWidgets.QRadioButton(self.groupBox_366)
        self.radioButton_320.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_320.setChecked(True)
        self.radioButton_320.setText("No")           
        self.radioButton_320.setObjectName("radioButton_320")
        self.radioButton_321 = QtWidgets.QRadioButton(self.groupBox_366)
        self.radioButton_321.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_321.setChecked(False)
        self.radioButton_321.setText("yes")  
        self.radioButton_321.setObjectName("radioButton_321")
        
        
          
        self.groupBox_363 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_363.setGeometry(QtCore.QRect(10, 229, 421, 31))
        self.groupBox_363.setObjectName("groupBox_363")
        self.label_434 = QtWidgets.QLabel(self.groupBox_363)
        self.label_434.setGeometry(QtCore.QRect(10, 7, 131, 21))
        self.label_434.setObjectName("label_434")
        self.label_434.setText("xx_neighborhoods.rtf")
        self.radioButton_317 = QtWidgets.QRadioButton(self.groupBox_363)
        self.radioButton_317.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_317.setChecked(False)
        self.radioButton_317.setObjectName("radioButton_317")
        self.radioButton_317.setText("yes")                   
        self.radioButton_316 = QtWidgets.QRadioButton(self.groupBox_363)
        self.radioButton_316.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_316.setChecked(True)
        self.radioButton_316.setObjectName("radioButton_316")
        self.radioButton_316.setText("No")

                
        self.groupBox_364 = QtWidgets.QGroupBox(self.groupBox_310)
        self.groupBox_364.setGeometry(QtCore.QRect(10, 264, 421, 31))
        self.groupBox_364.setObjectName("groupBox_364")
        self.label_437 = QtWidgets.QLabel(self.groupBox_364)
        self.label_437.setGeometry(QtCore.QRect(10, 7, 181, 21))
        self.label_437.setObjectName("label_437")
        self.label_437.setText("xx_neighborhoods_graphic.rtf.rtf")
        self.radioButton_323 = QtWidgets.QRadioButton(self.groupBox_364)
        self.radioButton_323.setGeometry(QtCore.QRect(300, 7, 51, 17))
        self.radioButton_323.setChecked(False)
        self.radioButton_323.setObjectName("radioButton_323")
        self.radioButton_323.setText("yes")   
        self.radioButton_322 = QtWidgets.QRadioButton(self.groupBox_364)
        self.radioButton_322.setGeometry(QtCore.QRect(350, 7, 41, 17))
        self.radioButton_322.setChecked(True)
        self.radioButton_322.setObjectName("radioButton_322")
        self.radioButton_322.setText("No")
     
                      
        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_14.setGeometry(QtCore.QRect(50, 530, 441, 61))
        self.pushButton_14.setFont(font)
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_14.setText("Click to adjust Shape/Color/Line for all")
                
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(30, 490, 401, 31))
        self.label_18.setFont(font1)
        self.label_18.setObjectName("label_18")
        self.label_18.setText("3. Drawing options for End Host Servers")
                
               
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1154, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionSave_session = QtWidgets.QAction(MainWindow)
        self.actionSave_session.setObjectName("actionSave_session")


        self.pushButton_10.clicked.connect(self.slot_1st)
        self.pushButton_12.clicked.connect(self.slot_2st)
        self.pushButton_14.clicked.connect(self.slot_3st)
                
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_14.setEnabled(False)  

        self.radioButton_7.toggled.connect(self.toggle_option_button_for_Drawing_End_Host_server)   
        self.radioButton_2.toggled.connect(self.combined_ASIC_into_Director)   
        self.radioButton_317.clicked.connect(self.enablig_HCAs)   
        self.radioButton_323.clicked.connect(self.enablig_HCAs)   
        self.radioButton_315.clicked.connect(self.disabling_HCAs)
                     
        self.actionSave_session.setText("Save logs")

    def enablig_HCAs(self):
            self.radioButton_314.setChecked(True)  
            
    
    def disabling_HCAs(self):
            self.radioButton_316.setChecked(True)  
            self.radioButton_322.setChecked(True)  
               
                         
    def toggle_option_button_for_Drawing_End_Host_server(self):
        if self.radioButton_7.isChecked():
            self.pushButton_14.setEnabled(True)                
        else :
            self.pushButton_14.setEnabled(False)  
            
    def combined_ASIC_into_Director(self):
        if self.radioButton_2.isChecked():
            self.radioButton_320.setEnabled(False)  
            self.radioButton_321.setEnabled(False)         
            self.radioButton_316.setEnabled(False)  
            self.radioButton_317.setEnabled(False)          
            self.radioButton_322.setEnabled(False)  
            self.radioButton_323.setEnabled(False)    
            
        else :
            self.radioButton_320.setEnabled(True)  
            self.radioButton_321.setEnabled(True)         
            self.radioButton_316.setEnabled(True)  
            self.radioButton_317.setEnabled(True)          
            self.radioButton_322.setEnabled(True)  
            self.radioButton_323.setEnabled(True)  
            
                      
         
    def slot_1st(self):
        global fnameBase
        global fPath
        global fExt
        global findDirs
        global gvL1BoxesToStack
        global showCableCount
        global lineScheme
        global switchL1NamePatterns
        global putSwitchNamesInBoxes
    
        
        fnameBase = ''    # The filename, minus the extension
        fPath = ''    # The path to the directory containing the file
        fExt = ''    # The file extension of the input file
    
        try : 
            fp=self._openfiledialog()
  
            if fp == None :
                self.textBrowser_2.append("You got a problem when opening or loading a ibnetdiscovery file") 
                raise Exception('Plesse check if you opened correct ibnetdiscovery file or not. ') 

            else : 
                fPath = fp.rpartition('/')[0] + "/"    # Pick off the path to the selected file
                fn = fp.rpartition('/')[2]    # Get the filename + extension
                fExt = fn.rpartition ('.')[2]
            
                if fExt:
                    fnameBase = fn.rpartition ('.')[0]    # Get file name w/o extension
        except Exception as e:
              self.textBrowser_2.setText("Exception occured. Please check if you opened Binary file or right file or else")      
              pass


    def slot_3st(self):           
        self.dd.show()
        

        
    def slot_2st(self):
            
                global fnameBase
                global fPath
                global fExt
                global findDirs
                global gvL1BoxesToStack
                global showCableCount
                global lineScheme
                global switchL1NamePatterns
                global putSwitchNamesInBoxes
                global f
                global wf   
                global hdrx
     
                findDirs = True    # Ask if Tarzan should look for Director boxes among the Switch ASICs

                self.textBrowser_2.setText("\n")   
                                                   
                if self.radioButton_2.isChecked():    #"Combine ASICs into Directors"
                    findDirs = False
 
                gvL1BoxesToStack = 1
                
        
                #try:
                #    gvL1BoxesToStack = max(min(int(self.lineEdit_1.text()),100),1)
                #except:
                #    self.textBrowser_2.setText("Pleae put only Number, not Text")   
                #    gvL1BoxesToStack = 1   
                #    pass
       
                putSwitchNamesInBoxes = False 
                if self.radioButton_3.isChecked():  #"Put Switch & Director names in Visio boxes"  
                    putSwitchNamesInBoxes = True
        

                # Effectively turn off cable labels in Visio output "showCableCount = 1000"    
                # Show labels for all links "showCableCount = 1"    

                showCableCount = 1000
                if self.radioButton_9.isChecked() : 
                    showCableCount = 1       

                                     
             
                lineScheme = 1
                #if self.radioButton_6.isChecked():    
                #    lineScheme = 2
 
                try:
                    switchL1NamePatterns = ["^XX$"]    # Should never match anything
                    if self.lineEdit_3.text() != "^XX$" :
                        s = '^'+re.escape (self.lineEdit_3.text()).replace ("\\*", ".*").replace ("\\?", ".").replace("\\,","$\\,^") + '$' 
                        switchL1NamePatterns = s.split("\\,")    # Create a list of patterns  
       
                except:
                        self.textBrowser_2.setText("switchL1NamePatterns")      
                        switchL1NamePatterns = ["^XX$"] 
                        pass
        
                try :        
                    fname = fPath + fnameBase + "." + fExt    # Assemble the strings returned by doGUI     
                    f = open(fname,'rt', encoding='UTF8')
              
                except:
                      self.textBrowser_2.setText("Please open Ibnetdiscovery file first.")  
                      return None

                self.textBrowser_2.append("#################### Parsing ibnetdiscover file #################")   
                self.textBrowser_2.append("\n")   
                                
        
                processIBNetDiscover ()
                for i in hdrx :
                    self.textBrowser_2.append(i)   
            
                                
                                
                check_Invalid_lid()
                # We now know enough (dates & times) to initialize the Warnings .rtf file
                fc = 25    # Font color; wish we had a better way to specify this (e.g. by color name)   
                wfname = fPath + fnameBase + "_warnings.rtf"
                wf = open (wfname, "w")    # Overwrite the file if it already exists
                wf.write ("{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Lucida Console;}}\n")    # RTF file header
                wf.write (putRTFColorTbl (rtfColorSet) + "\n")    # RTF color table
                wf.write ("\\fs15" + "\n")    # Font size
                wf.write ("\\margl576")    # Margins
                wf.write ("\\margr576")
                wf.write ("\\margt576")
                wf.write ("\\margb576" + "\n")
                wf.write (putIbnetdiscoverNameAndDate () + rtfEOL)
                wf.write (rtfEOL)
                wf.write ("---- WARNINGS" + rtfEOL)
                                       
                if len(warn_return) > 0 :
                    wf.write (" " + rtfEOL)                         
                    wf.write ("#################### Invalid LID detected #######################"+ rtfEOL)   
                    for i in warn_return :
                        wf.write (i+ rtfEOL)   
                     
                if len(warn_return1) > 0 :     
                    wf.write (" " + rtfEOL)   
                    wf.write ("#################### Mcast LID detected #######################"+ rtfEOL)     
  
                    for i in warn_return1 :
                        wf.write (i+ rtfEOL)  
                                        
                buildISLDictionary()
                setAllSwitchAttributes ()    #
                setAllHCAAttributes ()
                checkLinkSpeeds ()    # We now know enough to check for Links at non-optimal speeds
                if findDirs:
                        getDirectors () 
                        addDirsToPortSpeed ()    # Expand portSpeed dictionary so we can also index by Dir pseudo-GUID       
                #
                assignNodeColors() 
         
                if findDirs == True and allDirectors :
                
                    if self.radioButton_314.isChecked() :
                        doHCAReport()
                        self.textBrowser_2.append('"' + fnameBase + "_HCAs.rtf \" created")   
                        
                    if self.radioButton_321.isChecked():
                        showAllDirectors ()
                        self.textBrowser_2.append('"' + fnameBase + "_directors.rtf.gv \" created")  
     
                    if (len (allDirectors) > 0) and (len (ibNet) > 0):    # Could be Clos-5
                        
                        if self.radioButton_317.isChecked():
                            doNeighborhoodReport ()
                            self.textBrowser_2.append('"' + fnameBase + "_neighborhoods.rtf \" created")  
 
                        if self.radioButton_323.isChecked():                       
                            showDirHoods ()
                            self.textBrowser_2.append('"' + fnameBase + "_neighborhoods_graphic.rtf \" created")  

                getBoxGraph ()
                connectBoxGraph ()
                buildBoxFingerprints ()    #### New Box grouping stuff ####
                analyzeBoxGraph ()
                removeDuplicateLinks ()
                
                if self.radioButton_230.isChecked():
                
                    generateGraphViz ()
                    self.textBrowser_2.append('"' + fnameBase + "_graphviz.gv \" created")   
  
                    if self.radioButton_7.isChecked():
                        drawing_EndHosts (self.otherWindow.all_values)  
                        self.textBrowser_2.append('"' + fnameBase + "_graphviz_End_hosts.gv \" created")  
                
                if  self.radioButton_229.isChecked():                
                    try:
                        os.remove(generateGraphViz ())
                    except:
                        self.textBrowser_2.setText("###### Exception occured, while deleting file ######" )  
                        self.textBrowser_2.append(generateGraphViz ())  
            
                                    
                if self.radioButton_224.isChecked():
                      
                    showAllSwitches ()
                    self.textBrowser_2.append('"' + fnameBase + "_switches.rtf \" created")   
                

       
                if hcasWithVPorts > 0:
                    doVPortsReport ()
                    self.textBrowser_2.append('"' + fnameBase + "vports.rtf \" created")  
                         
                if self.radioButton_226.isChecked():
                    doSwitchesXLS ()
                    self.textBrowser_2.append('"' + fnameBase + "_switches.xlsx \" created")  
                
                if len(warn_return2) > 1 :       
                    wf.write (" " + rtfEOL)                                      
                    for i in warn_return2 :
                        wf.write (i+ rtfEOL)  
                    wf.write (" " + rtfEOL)      
                                      
                wf.write ("---- END OF WARNINGS" + rtfEOL)            
                wf.write ("}\n")    # Finish and close the Warnings .rtf file
                wf.close()
            
                if self.radioButton_13.isChecked() : #if selected for xx_warning.rtf creation.
                    try:
                        os.remove(wfname)
                    except:
                        self.textBrowser_2.setText("################ Exception occured, while deleting file ######" )  
                        self.textBrowser_2.append(wfname)  
            
                else :
                    self.textBrowser_2.append('"' + fnameBase + "_warning.rtf \" created")   

                self.textBrowser_2.append("\n")     
                self.textBrowser_2.append("#################### Files creation done ########################")       

                if len(warn_return) > 0 :       
                    self.textBrowser_2.append("\n")      
                    self.textBrowser_2.append("#################### Invalid LID detected #######################")                 
                    for i, key in enumerate(warn_return):
                        i = i + 1
                        warn_message = str(i) + ". " + key
                        self.textBrowser_2.append(warn_message)

                if len(warn_return1) > 0 :       
                    self.textBrowser_2.append("\n") 
                    self.textBrowser_2.append("#################### Mcast LID detected ########################")                 
                    for i, key in enumerate(warn_return1):
                        i = i + 1
                        warn_message1 = str(i) + ". " + key
                        self.textBrowser_2.append(warn_message1)                                
            
       
                warn_return2[:] = (value for value in warn_return2 if "##############" not in value)
                if len(warn_return2) > 0 :       
                    self.textBrowser_2.append("\n")
                    self.textBrowser_2.append("################ Warning (Please refer to '_warning.rtf' file) #########")
                    for i, key in enumerate(warn_return2):
                        i = i + 1
                        #warn_message2 = str(i) + ". " + key
                        self.textBrowser_2.append(key)
        
                initialization_All_values()
    
    def _openfiledialog(self): # OpenFile Dialog, 
        try:

            fileName_open, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open file','./')
            if fileName_open :
                    return fileName_open
            else :
                    return None

        except:
            return None
    
    

if __name__=="__main__":
    import sys
    
    
		#### Initialize stuff ####
		# If Director detection fails, e.g. due to Node Descriptions being corrupted, allow user to 
		# provide a list of Director spine GUIDs (only need one per Director) called spineGUIDs before
		# running Tarzan.  A GUID here is a string containing 16 hex digits.
    try:    
        zz = spineGUIDs    # See if the user has set the spineGUIDs list
    except:
        spineGUIDs = []    # If not, define it as empty
        pass
    
    hdrx = []
    warn_return = [] #This is to warn Invalid unicat LID number
    warn_return1 = []#This is to warn Mcast LID number
    warn_return2 = []#This is to warn Any errors 
    genTimeAndDate = "???"
    ibNet = {}
    islDict = {}
    Boxes = {}
    Spines = {}
    Leafs = {}
    allDirectors = {}
    rtfEOL = "\\line\n"
    rtfColors = 0
    nodeColors = {}
    resolveDirectors = True
    findDirs = True
    dontDrawBox = {}
    defaultPortColor = 130 * [" "]    # Used by the 'show split port switch' routines
    currentLinkWidths = 130 * [" "]
    currentPeerGUIDs = 130 * [" "]
    allHCAs = {}
    hcasBySwitch = {}
    hcasByDirector = {}
    portSpeed = {}
    hcasWithVPorts = 0
    buildDirectorMaps ()    # Create data structures for use by ProcessDirector3
    s = putRTFColorTbl (rtfColorSet)    # Initialize rtfColorIndex dictionary, then:
    buildNodeRTFStrings ()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())