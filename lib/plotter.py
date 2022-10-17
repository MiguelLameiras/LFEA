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
matplotlib.rcParams['axes.titlepad'] = 10
matplotlib.rcParams['axes.labelpad'] = 5

from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline
import numpy as np
from scipy.optimize import curve_fit
from lmfit.models import ExpressionModel
from lmfit import Parameters,models,Model
from numpy import exp, loadtxt, pi, sqrt

from scipy.stats import norm
import matplotlib.mlab as mlab

def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (sqrt(2*pi) * wid)) * exp(-(x-cen)**2 / (2*wid**2))

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
        self.errcolor = 'black'
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
            #Plot do fit
            #Calcular o fit da função
            if(self.yerror == True ):
                weights = []
                for i in range(0,len(self.yerr)):
                    weights.append(1/self.yerr[i])
                #print(weights)
                if(self.expression == "gauss"):
                    gmodel = Model(gaussian)
                    result = gmodel.fit(self.y, x=self.x, amp=5, cen=0, wid=5,weights=weights)
                else:
                    function = ExpressionModel(self.expression)
                    params = self.parameters
                    result = function.fit(self.y, params, x=self.x,weights=weights)
                #Criar uma função continua com o fit
                x_continuo = np.linspace(min(self.x),max(self.x),1000)
                new_prediction = result.eval(x=x_continuo)
            else:
                if(self.expression == "gauss"):
                    gmodel = Model(gaussian)
                    result = gmodel.fit(self.y, x=self.x, amp=3000, cen=-5, wid=5)
                else:
                    function = ExpressionModel(self.expression)
                    params = self.parameters
                    result = function.fit(self.y, params, x=self.x)
                #Criar uma função continua com o fit
                x_continuo = np.linspace(min(self.x),max(self.x),1000)
                new_prediction = result.eval(x=x_continuo)


            if(self.xerror == True and self.yerror == True ):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,markersize=self.marker_size,fmt=self.marker_style,color = self.datacolor ,ecolor = self.errcolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            elif(self.xerror == True):
                plt.errorbar(self.x, self.y, xerr = self.xerr,markersize=self.marker_size,fmt=self.marker_style,color = self.datacolor ,ecolor = self.errcolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            elif(self.yerror == True):
                plt.errorbar(self.x, self.y, yerr = self.yerr,markersize=self.marker_size,fmt=self.marker_style,color = self.datacolor ,ecolor = self.errcolor, capthick=1, capsize=5)
                plt.plot(x_continuo,new_prediction, 'r',linewidth=1.3, color = self.fitcolor)
            else:
                plt.plot(self.x,self.y,self.marker_style, markersize=self.marker_size,color = self.datacolor)
                plt.plot(x_continuo,new_prediction, '--',linewidth=1.3,color = self.fitcolor)

        elif(plot == "Interpolate" ):     
            #cs = CubicSpline(self.x,self.y)
            x_continuo = np.linspace(min(self.x),max(self.x),1000)
            f = interp1d(self.x, self.y, kind='cubic')
            spl = UnivariateSpline(self.x, self.y)
            spl.set_smoothing_factor(2)
            #Plot do fit
            if(self.xerror == True and self.yerror == True ):
                plt.errorbar(self.x, self.y, xerr = self.xerr, yerr = self.yerr,fmt = self.marker_style, markersize=self.marker_size,color = self.datacolor ,ecolor = self.errcolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',linewidth=1.3,color = self.fitcolor)
            elif(self.xerror == True):
                plt.errorbar(self.x, self.y, xerr = self.xerr,fmt = self.marker_style, markersize=self.marker_size,color = self.datacolor ,ecolor = self.errcolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',linewidth=1.3,color = self.fitcolor)
            elif(self.yerror == True):
                plt.errorbar(self.x, self.y, yerr = self.yerr,fmt = self.marker_style, markersize=self.marker_size,color = self.datacolor ,ecolor = self.errcolor, capthick=1, capsize=5)
                plt.plot(x_continuo,cs(x_continuo), 'r',linewidth=1.3,color = self.fitcolor)
            else:
                plt.plot(self.x,self.y, self.marker_style,markersize=self.marker_size,color = self.datacolor)
                plt.plot(x_continuo,spl(x_continuo), '--',linewidth=1,color = self.fitcolor)  
        
        if(plot == "Scatter" ):  
            #Plot do fit
            if(self.xerror == True and self.yerror == True):
                plt.errorbar(self.x, self.y,markersize=self.marker_size, xerr = self.xerr, yerr = self.yerr,fmt=self.marker_style,color = self.datacolor ,ecolor =self.errcolor,capthick=1, capsize=5)
            elif(self.xerror == True):
                plt.errorbar(self.x, self.y,markersize=self.marker_size, xerr = self.xerr,fmt=self.marker_style,color = self.datacolor ,ecolor = self.errcolor,capthick=1, capsize=5)
            elif(self.yerror == True):
                plt.errorbar(self.x, self.y,markersize=self.marker_size, yerr = self.yerr,fmt=self.marker_style,color = self.datacolor ,ecolor = self.errcolor,capthick=1, capsize=5)
            else:
                plt.plot(self.x,self.y, self.marker_style,markersize=self.marker_size,color = self.datacolor)      

        if(plot == "Hist" ):
            # Empirical average and variance are computed
            avg = np.mean(self.x)
            var = np.var(self.x)
            # From that, we know the shape of the fitted Gaussian.
            pdf_x = np.linspace(-3,3,100)
            pdf_y = 1.0/np.sqrt(2*np.pi*var)*np.exp(-0.5*(pdf_x-avg)**2/var)

            # Then we plot :
            plt.figure()
            bin_heights, bin_borders, _ = plt.hist(self.x,9,density = 1,align= "left",alpha = 0.65,histtype='bar', ec='black')
            bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
            popt, pcov= curve_fit(gaussian, bin_centers, bin_heights, p0=[1., 0., 1.])
            print(popt)
            print (np.sqrt(np.diag(pcov)))
            plt.plot(pdf_x,pdf_y,'--',color="#b01a1a")
            x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)
            plt.plot(x_interval_for_fit, gaussian(x_interval_for_fit, *popt), color = "#b01a1a")


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
        
        plt.grid(True, which="both")

        if(plot == "Fit"):
            print("\n\u001b[38;5;3m\u001b[7m                         Fit Report:                           \u001b[0m\n")
            print("[[Fit Model]]\n    " + self.expression)
            print(result.fit_report())
            print("\n\u001b[38;5;3m\u001b[7m                                                               \u001b[0m")

        return plt
