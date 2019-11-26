#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Receptor APT NOAA
# Author: Departamento de Telecomunicaciones - iie - Fing- UdelaR
# Description: Receptor APT NOAA
# Generated: Mon Mar 18 18:02:15 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from datetime import datetime
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sip
import sys
import time


class SdrApt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Receptor APT NOAA")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Receptor APT NOAA")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "SdrApt")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.trans = trans = 1
        self.samp_rate = samp_rate = 960000
        self.prefix = prefix = "/home/gonzalo/workspace/sdr-apt/wav/"
        self.fcd_freq = fcd_freq = 137100000
        self.cutoff = cutoff = 40
        self.xlate_filter_taps = xlate_filter_taps = firdes.low_pass(1, samp_rate*2, cutoff*1000, trans*1000, firdes.WIN_HAMMING, 6.76)
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = fcd_freq
        self.recfile2 = recfile2 = prefix +"am_demod/"+ datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".wav"
        self.recfile = recfile = prefix +"fm_demod/"+ datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".wav"
        self.lpf_cutoff = lpf_cutoff = 40000
        self.lna_gain_0 = lna_gain_0 = 30
        self.delay = delay = 0
        self.bpf_lp = bpf_lp = 500
        self.bpf_hp = bpf_hp = 5000
        self.af_gain = af_gain = 1.5

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, "Senal en recepcion")
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, "Demodulacion FM")
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, "Detector de envolvente")
        self.top_layout.addWidget(self.tab)
        self._lna_gain_0_options = (0, 10, 20, 30, 35, )
        self._lna_gain_0_labels = ("0 dB", "+ 10 dB", "+ 20 dB", "+ 30 dB", "+ 35 dB", )
        self._lna_gain_0_tool_bar = Qt.QToolBar(self)
        self._lna_gain_0_tool_bar.addWidget(Qt.QLabel("Ganancia SDR (dB)"+": "))
        self._lna_gain_0_combo_box = Qt.QComboBox()
        self._lna_gain_0_tool_bar.addWidget(self._lna_gain_0_combo_box)
        for label in self._lna_gain_0_labels: self._lna_gain_0_combo_box.addItem(label)
        self._lna_gain_0_callback = lambda i: Qt.QMetaObject.invokeMethod(self._lna_gain_0_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._lna_gain_0_options.index(i)))
        self._lna_gain_0_callback(self.lna_gain_0)
        self._lna_gain_0_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_lna_gain_0(self._lna_gain_0_options[i]))
        self.top_grid_layout.addWidget(self._lna_gain_0_tool_bar, 1,4,1,1)
        self._fcd_freq_options = (137620000, 137912500, 137100000, 93900000, )
        self._fcd_freq_labels = ("NOAA 15", "NOAA 18", "NOAA 19", "Oceano FM", )
        self._fcd_freq_group_box = Qt.QGroupBox("Seleccionar Satelite")
        self._fcd_freq_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._fcd_freq_button_group = variable_chooser_button_group()
        self._fcd_freq_group_box.setLayout(self._fcd_freq_box)
        for i, label in enumerate(self._fcd_freq_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._fcd_freq_box.addWidget(radio_button)
        	self._fcd_freq_button_group.addButton(radio_button, i)
        self._fcd_freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._fcd_freq_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._fcd_freq_options.index(i)))
        self._fcd_freq_callback(self.fcd_freq)
        self._fcd_freq_button_group.buttonClicked[int].connect(
        	lambda i: self.set_fcd_freq(self._fcd_freq_options[i]))
        self.top_grid_layout.addWidget(self._fcd_freq_group_box, 1,1, 1,2)
        self._delay_range = Range(0, 5, 1, 0, 200)
        self._delay_win = RangeWidget(self._delay_range, self.set_delay, "Delay", "counter_slider", float)
        self.tab_layout_2.addWidget(self._delay_win)
        self._cutoff_range = Range(10, 48, 1, 40, 200)
        self._cutoff_win = RangeWidget(self._cutoff_range, self.set_cutoff, "Frecuencia de corte LPF (kHz)", "counter_slider", float)
        self.top_grid_layout.addWidget(self._cutoff_win, 2,1,1,1)
        self._bpf_lp_range = Range(200, 500, 10, 500, 100)
        self._bpf_lp_win = RangeWidget(self._bpf_lp_range, self.set_bpf_lp, "Band Pass Filter Lp", "counter_slider", float)
        self.tab_layout_2.addWidget(self._bpf_lp_win)
        self._bpf_hp_range = Range(800, 8000, 10, 5000, 100)
        self._bpf_hp_win = RangeWidget(self._bpf_hp_range, self.set_bpf_hp, "Band Pass Filter Hp", "counter_slider", float)
        self.tab_layout_2.addWidget(self._bpf_hp_win)
        self._af_gain_range = Range(0, 3, .1, 1.5, 100)
        self._af_gain_win = RangeWidget(self._af_gain_range, self.set_af_gain, "Volumen audio", "dial", float)
        self.top_grid_layout.addWidget(self._af_gain_win, 2,4,1,1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: x
        
        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("Frecuencia Portadora"+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 1,3,1,1)
          
        self._trans_range = Range(1, 40, .2, 1, 200)
        self._trans_win = RangeWidget(self._trans_range, self.set_trans, "Ancho LPF (kHz)", "counter_slider", float)
        self.top_grid_layout.addWidget(self._trans_win, 2,3,1,1)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=20800,
                decimation=48000,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=96000,
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	96000, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        
        if not True:
          self.qtgui_waterfall_sink_x_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)
        
        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_0_win)
        self.qtgui_time_sink_x_2_0 = qtgui.time_sink_c(
        	1024, #size
        	96000, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_2_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_2_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_2_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_2_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_2_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_0_win)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
        	2080, #size
        	2080*2, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1_0.set_update_time(.5)
        self.qtgui_time_sink_x_1_0.set_y_axis(0, 0.4)
        
        self.qtgui_time_sink_x_1_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.4, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(True)
        
        if not True:
          self.qtgui_time_sink_x_1_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
        	1024, #size
        	20800, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0_1.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0_1.enable_tags(-1, False)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_1.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_time_sink_x_0_1_win)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
        	1024, #size
        	20800, #samp_rate
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0_0_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0_0_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._qtgui_time_sink_x_0_0_0_win)
        self.qtgui_freq_sink_x_1_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	20800, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_1_0.disable_legend()
        
        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_1_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_freq_sink_x_1_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	2048, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	96000, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(fcd_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(lna_gain_0, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self._lpf_cutoff_range = Range(10000, 50000, 1, 40000, 100)
        self._lpf_cutoff_win = RangeWidget(self._lpf_cutoff_range, self.set_lpf_cutoff, "Low Pass Filter cutoff", "counter_slider", float)
        self.tab_layout_0.addWidget(self._lpf_cutoff_win)
        self.low_pass_filter_1_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	30, 96000, cutoff*1000, 500, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	10, 20800, 2000, 500, firdes.WIN_HAMMING, 6.76))
        self.hilbert_fc_0_0 = filter.hilbert_fc(5, firdes.WIN_HAMMING, 6.76)
        self.blocks_wavfile_sink_1_0 = blocks.wavfile_sink(recfile2, 1, 4160, 16)
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink(recfile, 1, 20800, 16)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((af_gain, ))
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(11, 1/11., 4000)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 5)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, delay)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.band_pass_filter_0 = filter.interp_fir_filter_fff(1, firdes.band_pass(
        	1, 48000, bpf_lp, bpf_hp, 200, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0_0 = analog.wfm_rcv(
        	quad_rate=96000,
        	audio_decimation=2,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0_0, 0), (self.audio_sink_0_0, 0))    
        self.connect((self.analog_wfm_rcv_0_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.blocks_wavfile_sink_0_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.hilbert_fc_0_0, 0))    
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))    
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_wavfile_sink_1_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.qtgui_time_sink_x_1_0, 0))    
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))    
        self.connect((self.hilbert_fc_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_delay_0_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))    
        self.connect((self.low_pass_filter_1_0, 0), (self.analog_wfm_rcv_0_0, 0))    
        self.connect((self.low_pass_filter_1_0, 0), (self.qtgui_freq_sink_x_0_0, 0))    
        self.connect((self.low_pass_filter_1_0, 0), (self.qtgui_time_sink_x_2_0, 0))    
        self.connect((self.low_pass_filter_1_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_1_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.qtgui_freq_sink_x_1_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.qtgui_time_sink_x_0_0_0, 1))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.qtgui_time_sink_x_0_1, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SdrApt")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate*2, self.cutoff*1000, self.trans*1000, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate*2, self.cutoff*1000, self.trans*1000, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile(self.prefix +"fm_demod/"+ datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".wav")
        self.set_recfile2(self.prefix +"am_demod/"+ datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + ".wav")

    def get_fcd_freq(self):
        return self.fcd_freq

    def set_fcd_freq(self, fcd_freq):
        self.fcd_freq = fcd_freq
        self._fcd_freq_callback(self.fcd_freq)
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.fcd_freq))
        self.osmosdr_source_0.set_center_freq(self.fcd_freq, 0)

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate*2, self.cutoff*1000, self.trans*1000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(30, 96000, self.cutoff*1000, 500, firdes.WIN_HAMMING, 6.76))

    def get_xlate_filter_taps(self):
        return self.xlate_filter_taps

    def set_xlate_filter_taps(self, xlate_filter_taps):
        self.xlate_filter_taps = xlate_filter_taps

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label_0)))

    def get_recfile2(self):
        return self.recfile2

    def set_recfile2(self, recfile2):
        self.recfile2 = recfile2
        self.blocks_wavfile_sink_1_0.open(self.recfile2)

    def get_recfile(self):
        return self.recfile

    def set_recfile(self, recfile):
        self.recfile = recfile
        self.blocks_wavfile_sink_0_0.open(self.recfile)

    def get_lpf_cutoff(self):
        return self.lpf_cutoff

    def set_lpf_cutoff(self, lpf_cutoff):
        self.lpf_cutoff = lpf_cutoff

    def get_lna_gain_0(self):
        return self.lna_gain_0

    def set_lna_gain_0(self, lna_gain_0):
        self.lna_gain_0 = lna_gain_0
        self._lna_gain_0_callback(self.lna_gain_0)
        self.osmosdr_source_0.set_gain(self.lna_gain_0, 0)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0_0.set_dly(self.delay)

    def get_bpf_lp(self):
        return self.bpf_lp

    def set_bpf_lp(self, bpf_lp):
        self.bpf_lp = bpf_lp
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, 48000, self.bpf_lp, self.bpf_hp, 200, firdes.WIN_HAMMING, 6.76))

    def get_bpf_hp(self):
        return self.bpf_hp

    def set_bpf_hp(self, bpf_hp):
        self.bpf_hp = bpf_hp
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, 48000, self.bpf_lp, self.bpf_hp, 200, firdes.WIN_HAMMING, 6.76))

    def get_af_gain(self):
        return self.af_gain

    def set_af_gain(self, af_gain):
        self.af_gain = af_gain
        self.blocks_multiply_const_vxx_0_0.set_k((self.af_gain, ))


def main(top_block_cls=SdrApt, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
