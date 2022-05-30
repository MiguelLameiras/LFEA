# -*- coding: utf-8 -*-
from ctypes import sizeof
import re
import io
import os
import base64

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['ytick.direction'] = 'in'
matplotlib.rcParams['xtick.direction'] = 'in'

from scipy.interpolate import CubicSpline
import numpy as np
from scipy.optimize import curve_fit
from lmfit.models import ExpressionModel
from lmfit import Parameters,models

class Plot:
    def __init__(self,x,y,xerr,yerr,xerror = None, yerror = None,expression = None,parameters = None,xlog = None , ylog = None, Title = "Title", xaxisTitle = "X-Axis", yaxisTitle = "Y-Axis"):
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr = yerr
        self.xerror = xerror
        self.yerror = yerror
        self.expression = expression
        self.parameters = Parameters()
        self.Title = Title
        self.xaxisTitle = xaxisTitle
        self.yaxisTitle = yaxisTitle
        self.datacolor = 'black'
        self.fitcolor = 'blue'
        self.xlog = xlog
        self.ylog = ylog
        self.xmin = 0
        self.ymin = -2
        self.xmax = 10
        self.ymax = 2
        self.xauto = 0
        self.yauto = 0
        self.xticks = 1
        self.yticks = 1
        self.legend = 0
        self.marker_style = "."
        self.marker_size = 3
        self.legend_name = "Data"

    def Make_Plot(self,plot):
        #Fazer plot do ficheiro
        if(plot == "Fit" ):
            #Calcular o fit da função
            function = ExpressionModel(self.expression)
            params = self.parameters
            result = function.fit(self.y, params, x=self.x)
            #Criar uma função continua com o fit
            x_continuo = np.linspace(min(self.x),max(self.x),1000)
            new_prediction = result.eval(x=x_continuo)
            #Plot do fit
            if(self.xerror == True and self.yerror == True ):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,markersize=self.marker_size,fmt=self.marker_style,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            elif(self.xerror == True):
                plt.errorbar(self.x, self.y, xerr = self.xerr,markersize=self.marker_size,fmt=self.marker_style,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            elif(self.yerror == True):
                plt.errorbar(self.x, self.y, yerr = self.yerr,markersize=self.marker_size,fmt=self.marker_style,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            else:
                plt.plot(self.x,self.y,self.marker_style, markersize=self.marker_size,color = self.datacolor)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3,color = self.fitcolor)

        elif(plot == "Interpolate" ):      
            cs = CubicSpline(self.x,self.y,bc_type='natural')
            x_continuo = np.linspace(min(self.x),max(self.x),1000)
            #Plot do fit
            if(self.xerror == True and self.yerror == True ):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt = self.marker_style, markersize=self.marker_size,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)
            elif(self.xerror == True):
                plt.errorbar(self.x, self.y, xerr = self.xerr,fmt = self.marker_style, markersize=self.marker_size,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)
            elif(self.yerror == True):
                plt.errorbar(self.x, self.y, yerr = self.yerr,fmt = self.marker_style, markersize=self.marker_size,color = self.datacolor ,ecolor = self.datacolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)
            else:
                plt.plot(self.x,self.y, self.marker_style,markersize=self.marker_size,color = self.datacolor)
                plt.plot(x_continuo,cs(x_continuo), 'r',color = self.fitcolor)  
        
        if(plot == "Scatter" ):  
            #Plot do fit
            if(self.xerror == True and self.yerror == True):
                plt.errorbar(self.x, self.y,markersize=self.marker_size, xerr = self.xerr, yerr = self.yerr,fmt=self.marker_style,color = self.datacolor ,ecolor = self.datacolor,capthick=1, capsize=5)
            elif(self.xerror == True):
                plt.errorbar(self.x, self.y,markersize=self.marker_size, xerr = self.xerr,fmt=self.marker_style,color = self.datacolor ,ecolor = self.datacolor,capthick=1, capsize=5)
            elif(self.yerror == True):
                plt.errorbar(self.x, self.y,markersize=self.marker_size, yerr = self.yerr,fmt=self.marker_style,color = self.datacolor ,ecolor = self.datacolor,capthick=1, capsize=5)
            else:
                plt.plot(self.x,self.y, self.marker_style,markersize=self.marker_size,color = self.datacolor)      

        #Titulos dos eixos
        plt.title(self.Title, fontsize=18)
        plt.xlabel(self.xaxisTitle, fontsize=18)
        plt.ylabel(self.yaxisTitle, fontsize=18)
        #Adicionar Legenda
        if(self.legend == 1):  plt.legend([self.legend_name, 'Fit'], loc='best')

        ax = plt.gca()

        if(self.xscale): ax.set_xscale(self.xscale)
        if(self.xauto == False):
            ax.set_xlim([self.xmin, self.xmax])
            ax.xaxis.set_major_locator(tck.MultipleLocator(base=self.xticks))# this locator puts ticks at regular intervals

        if(self.yscale): ax.set_yscale(self.yscale)
        if(self.yauto == False):
            ax.set_ylim([self.ymin, self.ymax])
            ax.yaxis.set_major_locator(tck.MultipleLocator(base=self.yticks))# this locator puts ticks at regular intervals

        if(self.xscale == "linear"): ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        if(self.yscale == "linear"): ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        
        if(plot == "Fit"):
            print("\n\u001b[38;5;3m\u001b[7m                         Fit Report:                           \u001b[0m\n")
            print("[[Fit Model]]\n    " + self.expression)
            print(result.fit_report())
            print("\n\u001b[38;5;3m\u001b[7m                                                               \u001b[0m")

        return plt
