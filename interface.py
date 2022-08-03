#!/usr/bin/env python3
from PyQt5.QtWidgets import QFileDialog, QLabel, QSpinBox, QPlainTextEdit, QToolBar, QMainWindow, QApplication, QLineEdit, QAction, QStatusBar, QMenu, QMessageBox
from PyQt5.QtGui import QIcon, QKeySequence, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from parser import parse
from sys import argv,exit

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin,self).__init__()
           
        # Windows Settings
        self.setMinimumSize(600,400)
        self.setWindowIcon(QIcon("Assets/icon.png"))

        # Central Widget
        self.exam=QPlainTextEdit()
        self.setCentralWidget(self.exam)
        
        # Menus
        self.mFile=QMenu("File")
        self.mEdit=QMenu("Edit")
        self.mGen=QMenu("Generate")
        self.mInf=QMenu("Generate")
        
        # Menu Items
        ## File Menu
        self.aOpen=QAction(QIcon("Assets/open.png"),"Open")
        self.aNew=QAction(QIcon("Assets/new.png"),"New")
        if self.windowTitle().endswith("*") and QMessageBox.warning(self,"Creating New Project","Opening a new project may cause to lose unsaved data. Do you want to continue?",QMessageBox.Yes,QMessageBox.No)==QMessageBox.No: return
        self.aSave=QAction(QIcon("Assets/save.png"),"Save")
        self.aSaveAs=QAction(QIcon("Assets/save_as.png"),"Save As")
        self.aQuit=QAction(QIcon("Assets/quit.png"),"Quit")
        ## Edit Menu
        self.aSelectAll=QAction(QIcon("Assets/select_all.png"),"Select All")
        self.aCut=QAction(QIcon("Assets/cut.png"),"Cut")
        self.aCopy=QAction(QIcon("Assets/copy.png"),"Copy")
        self.aPaste=QAction(QIcon("Assets/paste.png"),"Paste")
        self.aUndo=QAction(QIcon("Assets/undo.png"),"Undo")
        self.aRedo=QAction(QIcon("Assets/redo.png"),"Redo")
        ## Generate Menu
        self.aGenerate=QAction(QIcon("Assets/generate.png"),"Generate Exam")
        self.aGenerateAs=QAction(QIcon("Assets/generate_as.png"),"Generate Exam As")
        ## Information Menu
        self.aHelp=QAction(QIcon("Assets/help.png"),"Help")
        self.aAbout=QAction(QIcon("Assets/about.png"),"About")

        # Toolbar Items
        self.lTitle=QLabel(" Exam Title ")
        self.eTitle=QLineEdit()
        self.lTime=QLabel(" Exam Time ")
        self.sTime=QSpinBox()
        self.lAnswerKey=QLabel(" Answer Key ")
        self.eAnswerKey=QLineEdit()
        self.aFontDsc=QAction(QIcon("Assets/font_size_descrease.png"),"Descrease Font Size")
        self.aFontDef=QAction(QIcon("Assets/font_size_default.png"),"Use Default Font Size")
        self.aFontAsc=QAction(QIcon("Assets/font_size_increase.png"),"Increase Font Size")

        # Entry Limitations
        self.eAnswerKey.setValidator(QRegExpValidator(QRegExp("^[A-Ea-e]+$")))
        self.sTime.setRange(1,999)
        self.sTime.setSingleStep(1)
        self.sTime.setValue(10)

        # Connect Functions
        self.exam.textChanged.connect(self.setSaveStar)
        self.eTitle.textChanged.connect(self.setSaveStar)
        self.eAnswerKey.textChanged.connect(self.setSaveStar)
        self.sTime.valueChanged.connect(self.setSaveStar)
        self.aGenerate.triggered.connect(self.generateExam)
        self.aGenerateAs.triggered.connect(lambda:self.generateExam(True))
        self.aSave.triggered.connect(self.saveContent)
        self.aSaveAs.triggered.connect(lambda:self.saveContent(True))
        self.aOpen.triggered.connect(self.openContent)
        self.aNew.triggered.connect(self.newContent)
        self.aFontAsc.triggered.connect(lambda:self.setFontSize("+"))
        self.aFontDef.triggered.connect(lambda:self.setFontSize("="))
        self.aFontDsc.triggered.connect(lambda:self.setFontSize("-"))
        self.aSelectAll.triggered.connect(self.exam.selectAll)
        self.aCut.triggered.connect(self.exam.cut)
        self.aCopy.triggered.connect(self.exam.copy)
        self.aPaste.triggered.connect(self.exam.paste)
        self.aUndo.triggered.connect(self.exam.undo)
        self.aRedo.triggered.connect(self.exam.redo)
        self.aHelp.triggered.connect(self.showHelp)
        self.aAbout.triggered.connect(self.showAbout)

        # Toolbar Settings
        self.toolBar=QToolBar(self)
        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setMovable(False)
        self.addToolBar(self.toolBar)

        # Statusbar & Messages
        self.status=QStatusBar()
        self.setStatusBar(self.status)
       
        # Add Actions to Menus
        self.mFile.addActions([self.aNew,self.aOpen,self.aSave,self.aSaveAs,self.aQuit])
        self.mEdit.addActions([self.aUndo,self.aRedo,self.aCopy,self.aCut,self.aPaste,self.aSelectAll])
        self.mGen.addActions([self.aGenerate,self.aGenerateAs])
        self.mInf.addActions([self.aHelp,self.aAbout])
        
        # Add Menus to Menubar
        self.menu=self.menuBar()
        self.menu.addMenu(self.mFile)
        self.menu.addMenu(self.mEdit)
        self.menu.addMenu(self.mGen)
        self.menu.addMenu(self.mInf)

        # Add Items to Toolbar
        self.toolBar.addActions([self.aSave,self.aSaveAs,self.aOpen,self.aNew])
        self.toolBar.addSeparator()
        for widget in (self.lTitle,self.eTitle,self.lAnswerKey,self.eAnswerKey,self.lTime,self.sTime):
            self.toolBar.addWidget(widget)
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.aFontDsc,self.aFontDef,self.aFontAsc])
        self.toolBar.addSeparator()
        self.toolBar.addActions([self.aGenerate,self.aGenerateAs])
        
        # Keyboard Shortcuts
        ## File Menu
        self.aNew.setShortcut(QKeySequence("Ctrl+N"))
        self.aOpen.setShortcut(QKeySequence("Ctrl+O"))
        self.aSave.setShortcut(QKeySequence("Ctrl+S"))
        self.aSaveAs.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.aQuit.setShortcut(QKeySequence("Alt+F4"))
        # Edit Menu
        self.aSelectAll.setShortcut(QKeySequence("Ctrl+A"))
        self.aCut.setShortcut(QKeySequence("Ctrl+X"))
        self.aCopy.setShortcut(QKeySequence("Ctrl+C"))
        self.aPaste.setShortcut(QKeySequence("Ctrl+P"))
        self.aUndo.setShortcut(QKeySequence("Ctrl+Z"))
        self.aRedo.setShortcut(QKeySequence("Ctrl+Y"))
        ## Generate Menu
        self.aGenerate.setShortcut(QKeySequence("F5"))
        self.aGenerateAs.setShortcut(QKeySequence("F6"))
        ## Text Size
        self.aFontDsc.setShortcut(QKeySequence("Ctrl+-"))
        self.aFontDef.setShortcut(QKeySequence("Ctrl+="))
        self.aFontAsc.setShortcut(QKeySequence("Ctrl++"))
        ## Information
        self.aHelp.setShortcut(QKeySequence("F1"))
        self.aAbout.setShortcut(QKeySequence("F2"))
        
        # Other Variables
        self.inpFile="Untitled Exam"
        self.outFile="index"
        self.saved=False
        self.gened=False
        self.content=""
        self.time=10
        self.title=""
        self.answerKey=""
        self.fontSize=14

        # Set Font Size
        self.exam.setStyleSheet("font-size:"+str(self.fontSize)+"pt; font-family: monospace;")

        # Show Window
        self.show()
        self.setSaveStar()

    def generateData(self):
        return self.eTitle.text()+"\n"+self.exam.toPlainText()+"\n"+self.sTime.text()+"\n"+self.eAnswerKey.text().upper()

    def saveContent(self,saveAs:bool=False):
        if saveAs or (not self.saved):
            url=QFileDialog.getSaveFileName(self,"Save Exam Draft",self.eTitle.text(),"Examinator Project File (*.exm)")[0]
            if url.split("/")[-1]!="":
                self.inpFile=url 
                lastSlash=url.split("/")[-1]
                url=lastSlash if lastSlash[-4:]!=".exm" else lastSlash[:-4]
                self.saved=True
        if self.saved:
            file=open(self.inpFile+".exm" if self.inpFile[-4:]!=".exm" else self.inpFile,"w",encoding="UTF-8")
            file.write(self.generateData())
            file.close()
            self.content=self.exam.toPlainText()
            self.time=self.sTime.value()
            self.title=self.eTitle.text()
            self.answerKey=self.eAnswerKey.text()
            self.setSaveStar()
            self.status.showMessage("Document saved successfully.")

    def newContent(self):
        message=QMessageBox(QMessageBox.Warning,"Opening Draft","Opening a draft may cause to lose unsaved data. Do you want to continue?",parent=self)
        message.addButton(QMessageBox.Cancel)
        message.addButton(QMessageBox.Discard)
        message.setDefaultButton(QMessageBox.Cancel)
        if self.windowTitle().endswith("*") and message.exec_()==QMessageBox.Cancel: return
        self.inpFile="Untitled Exam"
        self.outFile="index"
        self.saved=False
        self.gened=False
        self.content=""
        self.exam.setPlainText("")
        self.sTime.setValue(10)
        self.eTitle.setText("")
        self.eAnswerKey.setText("")

    def setSaveStar(self):
        changed=self.content==self.exam.toPlainText() and self.time==self.sTime.value() and self.title==self.eTitle.text() and self.answerKey==self.eAnswerKey.text()
        self.setWindowTitle(f"Examinator - {self.inpFile.split('/')[-1]}"+("" if changed else "*"))

    def openContent(self):
        message=QMessageBox(QMessageBox.Warning,"Opening Draft","Opening a draft may cause to lose unsaved data. Do you want to continue?",parent=self)
        message.addButton(QMessageBox.Cancel)
        message.addButton(QMessageBox.Discard)
        message.setDefaultButton(QMessageBox.Cancel)
        if self.windowTitle().endswith("*") and message.exec_()==QMessageBox.Cancel: return
        url=QFileDialog.getOpenFileName(self,"Save Exam Draft",self.eTitle.text(),"Examinator Project File (*.exm)")[0]
        if url==None:
            file=QFileDialog().getOpenFileName(self,"Open Exam Draft","./","Examinator Project File (*.exm)")[0]
        else:
            file=url
        if file!="":
            self.inpFile=url
            self.saved=True
            with open(file,"r",encoding="UTF-8") as content:
                lines=content.readlines()
                self.eTitle.setText(lines[0].strip())
                self.sTime.setValue(int(lines[-2].strip()))
                self.eAnswerKey.setText(lines[-1].strip().upper())
                self.exam.setPlainText("".join(lines[1:-2]))
                self.content=self.exam.toPlainText()
                self.setSaveStar()
                self.status.showMessage("Document loaded successfully.")

    def generateExam(self,genAs:bool=False):
        if genAs or (not self.gened):
            url=QFileDialog.getSaveFileName(self,"Generate Exam",self.eTitle.text(),"Hyper Text Markup Language File (*.html)")[0]
            if url.split("/")[-1]!="":
                self.outFile=url 
                lastSlash=url.split("/")[-1]
                url=lastSlash if lastSlash[-4:]!=".exm" else lastSlash[:-4]
                self.gened=True
        if self.gened:
            parse(self.generateData(),self.outFile)
            self.status.showMessage("Exam generated successfully.")

    def setFontSize(self,change:str="="):
        if change=="-" and self.fontSize>8: self.fontSize-=3;
        elif change=="=": self.fontSize=14;
        elif change=="+"and self.fontSize<64: self.fontSize+=3;
        self.exam.setStyleSheet("font-size:"+str(self.fontSize)+"pt; font-family: monospace;")

    def closeEvent(self,event):
        if self.windowTitle().endswith("*"):
            message=QMessageBox(QMessageBox.Critical,"Quit Information","You have unsaved changes. Do you really want to quit?",parent=self)
            message.addButton(QMessageBox.Cancel)
            message.addButton(QMessageBox.Discard)
            message.setDefaultButton(QMessageBox.Cancel)
            if message.exec_()==QMessageBox.Discard:
                return app.quit()
            else: return event.ignore()
        return app.quit()

    def showHelp(self):
        QMessageBox.information(self,"Help Information","""Examinator developed to create interactive exams to use in classrooms for teachers. It can generate plain texts to HTML exams.

There are some restrictions to create:

* To create a new question, you must enter question number and close a paranthesis.
* To create options you must write capital letters from A to E and close a paranthesis.
* Only the last line will be bold in each question.
* Time must be an integer and declare in minutes.
* Answer key must be write in this format: ABCDE
* Answer key must be same length with question number.
* Extra line breaks may not be a problem.
* Correction score calculated by:
    First question's option count = n
    1/(n-1)
  So if there are 5 options, correction score must be -0.25, if 4 then -0.33.
* Exam score will be calculated out of 100 points.

Example questions:

1) Who is the developer of Examintor?

A) Furkan Baytekin
B) Linus Torvalds
C) Richard Stallman
D) Gabe Newell
E) Dennis Ritchie

2) I. Python
II. Java Script
III. C

Which are low level programming languages?

A) Only II
B) Only III
C) I & II
D) II & III
E) I, II & III

The files created with this program can directly run on every browser even if it is mobile browser. You can copy and move or send it to anyone.
""")
    def showAbout(self):
        QMessageBox.information(self,"About Examinator","""Examinator developed by Furkan Baytekin under GNU GPLv3.

It's a free software for teachers to  make them to create interactive exams to solve with and on classrooms.

Do not use directly on online exams. It contains answer keys on a java script variable, so students can reach it.

This program developed to use on group activities.""")

app=QApplication(argv)
win=MainWin()

exit(app.exec_())
