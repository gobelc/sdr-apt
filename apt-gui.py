#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.


import sys
import os
sys.path.insert(0, 'extras/')
sys.path.insert(0, 'extras/2019/')
sys.path.insert(0, 'temp/')

from functools import partial
from tempfile import TemporaryFile

import config
import numpy as np
import scipy.io.wavfile as wav
import apt
import utils
import thermal
import calibrate as cal
import time
import matplotlib as mpl
from matplotlib import pyplot as plt
from tkinter import *
import tkinter, tkinter.constants, tkinter.filedialog, tkinter.simpledialog, tkinter.messagebox, tkinter.ttk
from PIL import ImageTk, Image, ImageDraw


'''
Tallerine 2019
'''
import combinar_canales
import denoise
import meteo
import colorizarA



root = Tk(className="SdrApt")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

class APTdata():
    def __init__(self) :
        self.matrix = np.array(())
        self.thermal_matrix = np.array(())
        self.matrix_comb = np.array(())
        self.matrix_RGB = np.array(())
        self.frameA=np.array(())
        self.frameB=np.array(())
        self.telemetry=np.array(())
        self.filename=""
        self.log = "Info..."
        self.counter = 0
        self.image = None


def logScreen(text):
    #self.log = self.log + "\n" + text
    data.counter+=1
    T.insert(END, "\n" + "[" + str(data.counter)+ "] " + text)
    T.see(tkinter.END)


def printImageAttributes():
    # Retrieve the attributes of the image
    imageObject = data.image
    fileFormat      = imageObject.format        # Format of the image
    imageMode       = imageObject.mode          # Mode of the image
    imageSize       = imageObject.size          # Size of the image - tupe of (width, height)
    colorPalette    = imageObject.palette       # Palette used in the image
    logScreen("Format: " +str(fileFormat)+", Mode: "+str(imageMode)+", Size: " +  str(imageSize)+", Color:" + str(colorPalette))


def saveImageAPTCallBack():
    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = dir,title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
    data.filename=root.filename
    img = Image.fromarray(data.matrix)
    data.image=img
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(root.filename)
    logScreen("Imagen guardada en " + root.filename)

def saveImageACallBack():
    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = dir,title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
    data.filename=root.filename
    img = Image.fromarray(data.frameA)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(root.filename)
    logScreen("Imagen guardada en " + root.filename)

def saveImageBCallBack():
    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = dir,title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
    data.filename=root.filename
    img = Image.fromarray(data.frameB)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(root.filename)
    logScreen("Imagen guardada en " + root.filename)

def saveImageRGBCallBack():
    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = dir,title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
    data.filename=root.filename
    img = Image.fromarray(data.matrix_RGB)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(root.filename)
    logScreen("Imagen guardada en " + root.filename)

def saveImageThermalCallBack():
    root.filename = tkinter.filedialog.asksaveasfilename(initialdir = dir,title = "Select file",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
    data.filename=root.filename
    thermal_matrix =  np.array(data.thermal_matrix)
    numrows, numcols = thermal_matrix.shape

    def format_coord(x, y):
        z = -150.0 + thermal_matrix[y, x] * 200 / 255.0
        return z
                
    imgt = Image.fromarray(thermal_matrix)

    y = np.arange(0, numrows-1, 1)
    x = np.arange(0, numcols-1, 1)
    X, Y = np.meshgrid(x, y)
    
    # Calculating the output and storing it in the array Z
    Z = format_coord(X, Y)
    plt.figure(figsize=(8, 6))
    img = plt.imshow(utils.flip(Z), cmap='gnuplot2', interpolation='none', origin='upper')
    plt.grid(True)
    plt.title("Temperatura ($^\circ$C )")
    plt.colorbar(img)
    plt.savefig(root.filename, dpi=300)
    plt.show()
    '''
    fig, ax = plt.subplots(dpi = 300)
    cax = ax.imshow(imgt, cmap='jet')
    ax.format_coord = format_coord
    ax.grid(True)
    cbar = fig.colorbar(cax)
    '''
    logScreen("Imagen guardada en " + root.filename)

def sdrCallBack():
    os.system("gnuradio/AptRx.py")
    
def sdrDatCallBack():
    os.system("gnuradio/AptRxData.py")

def rotateImageCallBack():    
    data.matrix = utils.flip(data.matrix)
    data.frameA = utils.flip(data.frameA)
    data.frameB = utils.flip(data.frameB)
    img = Image.fromarray(data.matrix)
    data.image=img
    logScreen("Imagen rotada.")
    previewImageCallBack(1)

def getThermalImageCallback():
    data.thermal_matrix = thermal.getThermalImage(data.matrix, "15","B")
    logScreen("Imagen térmica creada")

def cacheImageCallBack():
    logScreen("Cargando imagen desde caché.")
    data.matrix = apt.decode(data.filename, cache = True)
    data.frameA = utils.get_frame(data.matrix,'A')
    data.frameB = utils.get_frame(data.matrix,'B')
    logScreen("Imagen cargada desde caché.")
    previewImageCallBack(1)

def decodeImageCallBack():
    root.filename =""
    root.filename = tkinter.filedialog.askopenfilename(initialdir = dir,title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))
    logScreen("Decodificando imagen a partir de la señal APT " + root.filename)
    data.matrix = apt.decode(root.filename, cache = False)
    data.frameA = utils.get_frame(data.matrix,'A')
    data.frameB = utils.get_frame(data.matrix,'B')
    logScreen("Imagen APT generada correctamente.")
    previewImageCallBack(1)

def filterImageCallBack():
    size = tkinter.simpledialog.askinteger("Input", "Disk size",
                                 parent=root,
                                 minvalue=1, maxvalue=100)
    data.matrix = utils.mean_filter(data.matrix,size)
    data.frameA = utils.get_frame(data.matrix,'A')
    data.frameB = utils.get_frame(data.matrix,'B')
    img = Image.fromarray(data.matrix)
    data.image=img
    logScreen("Imagen filtrada.")
    previewImageCallBack(1)


def equalizeImageCallBack():
    data.matrix = utils.equalize_histogram(data.matrix)
    data.frameA = utils.equalize_histogram(data.frameA)
    data.frameB = utils.equalize_histogram(data.frameB)
    img = Image.fromarray(data.matrix)
    data.image=img
    logScreen("Imagen ecualizada.")
    previewImageCallBack(1)

def showImageAPTCallBack():
    img = Image.fromarray(data.matrix)
    img.show()

def showImageACallBack():
    img = Image.fromarray(data.frameA)
    img.show()

def showImageBCallBack():
    img = Image.fromarray(data.frameB)
    img.show()

def showImageCombCallBack():
    img = Image.fromarray(data.matrix_comb)
    img.show()

def showThermalImageCallBack():
    imgt = Image.fromarray(data.thermal_matrix)
    imgt =  np.array(imgt)
    numrows, numcols = imgt.shape

    def format_coord(x, y):
            col = int(x + 0.5)
            row = int(y + 0.5)
            if col >= 0 and col < numcols and row >= 0 and row < numrows:
                z = -150.0 + imgt[row, col] * 200 / 255.0
                return 'x=%1.4f, y=%1.4f, Temperatura = %1.4f grados Celcius' % (x, y, z)
            else:
                return 'x=%1.4f, y=%1.4f' % (x, y)
    
    fig, ax = plt.subplots()
    ax.set_title("Thermal image")
    cax = ax.imshow(imgt, cmap='jet')
    ax.format_coord = format_coord
    cbar = fig.colorbar(cax)
    plt.show()

def previewImageCallBack(e):
    image = Image.fromarray(data.matrix)
    [imageSizeWidth, imageSizeHeight] = image.size
    console_width = T.winfo_width()
    console_height = T.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    space_height = screen_height - console_height-200
    image = image.resize((int(imageSizeWidth*space_height/imageSizeHeight), space_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    panel.configure(image=img)
    panel.image = img



def colorizarButtoncallback(matrix_infrared,matrix_visible,a,b):
    data.matrix_RGB = colorizarA.colorizar(matrix_infrared,matrix_visible,a,b)
    logScreen("Imagen RGB realizada correctamente.")
    return

def imageToRGBCallBack():
    rootRGB = Tk()
    rootRGB.title("Colorizar imagen")

    # Add a grid
    mainframe = Frame(rootRGB)
    mainframe.grid(sticky='N,W,E,S' )
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    mainframe.pack(pady = 200, padx = 200)

    # Create a Tkinter variable
    tkvar = StringVar(rootRGB)

    # Dictionary with options
    choices = {'Canal A','Canal B'}

    tkvar.set('Canal A') # set the default option

    popupMenu = OptionMenu(mainframe, tkvar, *choices)
    Label(mainframe, text="Seleccionar el canal infrarrojo").grid(row = 1, column = 1)
    popupMenu.grid(row = 2, column =1)

    if tkvar.get() == 'Canal A':
        matrix_infrared = data.frameA
        matrix_visible = data.frameB
    else:
        matrix_infrared = data.frameB
        matrix_visible = data.frameA
    
    a=[111,81,0,110,109]
    b=[255,110,80,129,129]

    '''
    outfile = TemporaryFile()
    np.save(outfile, a)
    '''
 
    action_with_arg = partial(colorizarButtoncallback, matrix_infrared,matrix_visible,a,b)
    button1=Button(mainframe, text="Colorizar", command=lambda:[rootRGB.destroy(),action_with_arg()])
    button1.grid(row=4, column=1)

    rootRGB.mainloop()

    return

def calibrateImageCallBack():
    logScreen("Calibrando imagen...")
    data.matrix = cal.calibrate(data.matrix,frame_name="A", debug=False, cache=False) # La imagen se puede calibrar con cualquiera de los dos Telemetry Frame
    data.frameA = utils.get_frame(data.matrix,'A')
    data.frameB = utils.get_frame(data.matrix,'B') 
    img = Image.fromarray(data.matrix)
    data.image=img   
    logScreen("Imagen calibrada correctamente.")
    previewImageCallBack(1)

def nullCallback():
    return

def tallerineCallback():
    tkinter.messagebox.showinfo("sdr-apt", "Esta función está siendo desarrollada en Tallerine...")
    return

def nubosidadCallback():
    cantfilas,cantcolumnas = (data.frameB).shape
    #
    x1 = tkinter.simpledialog.askinteger("Input", "x1", parent=root,
                                 minvalue=0, maxvalue=cantcolumnas)
    y1 = tkinter.simpledialog.askinteger("Input", "y1",
                                 parent=root,
                                 minvalue=0, maxvalue=cantfilas)
    x2 = tkinter.simpledialog.askinteger("Input", "x21",
                                 parent=root,
                                 minvalue=0, maxvalue=cantcolumnas)
    y2 = tkinter.simpledialog.askinteger("Input", "y2",
                                 parent=root,
                                 minvalue=0, maxvalue=cantfilas)
    pos = []
    pos.append(x1)
    pos.append(y1)
    pos.append(x2)
    pos.append(y2)

    a = meteo.indice_nubosidad(data.frameB,pos, nivel=180)
    tkinter.messagebox.showinfo("Indice de Nubosidad", "Nubosidad: " + str(a) + "%.")
    img = Image.fromarray(data.frameA)
    draw = ImageDraw.Draw(img)
    draw.rectangle(pos,fill=None, outline='red')
    img.show() 
    return

def plot_xy_frameA():
    utils.plot_image(data.frameA,"Frame A")

def plot_xy_frameB():
    utils.plot_image(data.frameB,"Frame B")

def filtrarMedianaCallback():
    n1 = tkinter.simpledialog.askfloat("Input", "Sensitividad",
                                 parent=root,
                                 minvalue=0., maxvalue=255.)
    n2 = tkinter.simpledialog.askinteger("Input", "Número de pasadas",
                                 parent=root,
                                 minvalue=1, maxvalue=10.)

    data.matrix = denoise.filtro_mediana(data.matrix,sensitivity = n1, pasadas = n2)
    data.frameA = utils.get_frame(data.matrix,'A')
    data.frameB = utils.get_frame(data.matrix,'B') 
    img = Image.fromarray(data.matrix)
    data.image=img
    logScreen("Imagen filtrada correctamente.")
    previewImageCallBack(1)
    return   

def combinarCallback():
    #tkMessageBox.showinfo("sdr-apt", "Esta función está siendo desarrollada en Tallerine...")
    n1 = tkinter.simpledialog.askfloat("Input", "Multiplicador Canal A",
                                 parent=root,
                                 minvalue=-10., maxvalue=10.)
    n2 = tkinter.simpledialog.askfloat("Input", "Multiplicador Canal B",
                                 parent=root,
                                 minvalue=-10., maxvalue=10.)
    data.matrix_comb = combinar_canales.combinar(data.matrix,n1,n2)
    logScreen("Imagen combinada correctamente.")
    img = Image.fromarray(data.matrix_comb)
    img.show()
    return 


data = APTdata()

#IMAGE

#MENU
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="Archivo", menu=filemenu)
filemenu.add_command(label="Abrir APT", command=decodeImageCallBack)
filemenu.add_command(label="Abrir desde cache", command=cacheImageCallBack)
filemenu.add_command(label="Recibir desde SDR (RTL-SDR)", command=sdrCallBack)
filemenu.add_command(label="Recibir desde dat file", command=sdrDatCallBack)

filemenu.add_separator()
filemenu.add_command(label="Guardar imagen APT", command=saveImageAPTCallBack)
filemenu.add_command(label="Guardar imagen Canal A", command=saveImageACallBack)
filemenu.add_command(label="Guardar imagen Canal B", command=saveImageBCallBack)
filemenu.add_command(label="Guardar imagen RGB", command=saveImageRGBCallBack)
filemenu.add_command(label="Guardar imagen térmica", command=saveImageThermalCallBack)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)

processmenu = Menu(menu)
menu.add_cascade(label="Procesar", menu=processmenu)
processmenu.add_command(label="Calibrar", command=calibrateImageCallBack)
processmenu.add_command(label="Imagen Térmica (Ch3-A)", command=getThermalImageCallback)
processmenu.add_command(label="Rotar", command=rotateImageCallBack)
processmenu.add_command(label="Filtro de mediana", command=filterImageCallBack)
processmenu.add_command(label="Ecualizar histograma", command=equalizeImageCallBack)
processmenu.add_separator()
processmenu.add_command(label="Indice nubosidad", command=nubosidadCallback)
processmenu.add_command(label="Falso Color I", command=tallerineCallback)
processmenu.add_command(label="Falso Color II", command=tallerineCallback)
processmenu.add_command(label="Combinar canales", command=combinarCallback)
processmenu.add_command(label="Filtrar ruido", command=filtrarMedianaCallback)




viewmenu = Menu(menu)
menu.add_cascade(label="Ver", menu=viewmenu)
viewmenu.add_command(label="Imagen APT", command=showImageAPTCallBack)
viewmenu.add_command(label="Canal A", command=showImageACallBack)
viewmenu.add_command(label="Canal B", command=showImageBCallBack)
viewmenu.add_command(label="Imagen térmica", command=showThermalImageCallBack)
viewmenu.add_command(label="Imagen combinada", command=showImageCombCallBack)
viewmenu.add_command(label="Info de imagen", command=printImageAttributes)
viewmenu.add_command(label="(x;y) Canal A", command=plot_xy_frameA)
viewmenu.add_command(label="(x;y) Canal B", command=plot_xy_frameB)


##IMAGE
panel = Label(root)
panel.grid(row=0,column=1)


S = Scrollbar(root)
T = Text(root, width=200, height=3)
T.config(bg='black',fg = '#80ff00')

S.grid(row=1,column=0,sticky=W)
T.grid(row=1,column=1,columnspan=1)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

root.bind("<Return>", previewImageCallBack)

root.mainloop()
