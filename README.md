# Imágenes satelitales NOAA APT con SDR  :satellite:

Framework para la demodulación, decodificación y procesamiento de imágenes de satélites meteorológicos NOAA. 

![](images/imagen_calibrada.png)


Basado parcialmente en [apt-decoder](https://github.com/zacstewart/apt-decoder).


## Instalación en Linux

### Dependencias necesarias de Python

- Numpy
- Scipy
- PIL
- Matplotlib

Pueden instalarse via pip mediante el comando:

``sudo pip install numpy scipy matplotlib Pillow``

Descargar sdr-apt, puede hacerlo desde terminal con el siguiente comando:

``git clone https://github.com/gobelc/sdr-apt.git``


## Demodulación

La demodulación se realiza en GnuRadio mediante el flowgraph **AptRx.grc**, disponible en la carpeta gnuradio. La primera vez que se ejecute debe modificarse el campo "value" del bloque "Prefix" para incluir la ruta correcta.

El flowgraph **AptRx-data.grc** tiene como entrada una grabación de satélite registrada con un SDR, un archivo IQ de muestra se puede decargar [desde aquí](https://iie.fing.edu.uy/investigacion/grupos/artes-old/noaa/2019.01.05.16.36.27.dat).


## Interfaz gráfica
Se puede correr en terminal con ``python apt-gui.py``

![](images/apt-gui.png)
