# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 10:13:46 2022

@author: Sarah
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "sans-serif",
    "font.sans-serif": "Gill Sans MT",
})


class Sizing:
    def __init__(self, figsizeover, figsizeup, labelsize, xticksize, yticksize, titlesize, datalabelsize, markersize, linesize):
        self.figsizeover = figsizeover
        self.figsizeup = figsizeup
        self.labelsize = labelsize
        self.xticksize = xticksize
        self.yticksize = yticksize
        self.titlesize = titlesize
        self.datalabelsize = datalabelsize
        self.markersize = markersize
        self.linesize = linesize


ppt_size = Sizing(14.5, 9, 28, 16, 18, 32, 16, 10, 4)

blog_size = Sizing(5.33, 3.07, 9, 8, 9, 14, 9, 3, 2)


def set_binwidth(mini, maxi):
    dif = maxi - mini
    if dif < 100:
        return 10
    elif dif < 500:
        return 50
    elif dif < 1000:
        return 100
    else:
        return 1000


def graph_settings(xlabeltext, ylabeltext, title, typepic=ppt_size):
    fig, ax = plt.subplots(figsize=(typepic.figsizeover, typepic.figsizeup))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlabel(xlabeltext, fontsize=typepic.labelsize)
    plt.ylabel(ylabeltext, fontsize=typepic.labelsize)
    plt.title(title, fontsize=typepic.titlesize)


def graph_hist(x_series, xlabeltext, ylabeltext, title, filetitle, color="brown", typepic=ppt_size):
    fig, ax = plt.subplots(figsize=(typepic.figsizeover, typepic.figsizeup))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    binwidth = set_binwidth(min(x_series), max(x_series))
    mini = int(min(x_series) / binwidth) * binwidth

    plt.hist(x_series, bins=range(mini, max(x_series) + binwidth,
                                  binwidth), color=color, clip_on=False, edgecolor="black")
    plt.xlabel(xlabeltext, fontsize=typepic.labelsize)
    plt.ylabel(ylabeltext, fontsize=typepic.labelsize)
    plt.title(title, fontsize=typepic.titlesize)

    plt.xticks(fontsize=typepic.xticksize)
    plt.yticks(fontsize=typepic.yticksize)

    plt.savefig(f'database_photos/{filetitle}.png',
                bbox_inches="tight", dpi=300)


def graph_bar(x_series, y_series, xlabeltext, ylabeltext, title, filetitle, percent="No", color="brown", ylabeladjust=.05, typepic=ppt_size):
    fig, ax = plt.subplots(figsize=(typepic.figsizeover, typepic.figsizeup))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.bar(x_series, y_series, color=color, clip_on=False)

    plt.xlabel(xlabeltext, fontsize=typepic.labelsize)
    plt.ylabel(ylabeltext, fontsize=typepic.labelsize)
    plt.title(title, fontsize=typepic.titlesize)

    if percent == "Yes":
        fmt = '%.0f%%'
        yticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(yticks)
        perad = "%"
    else:
        perad = ""

    plt.xticks(x_series, fontsize=typepic.xticksize, rotation=0)
    plt.yticks(fontsize=typepic.yticksize)

    for index in range(len(x_series)):
        ax.text(x_series[index], y_series[index] + ylabeladjust,
                str(y_series[index]) + perad, fontsize=typepic.datalabelsize, ha="center")

    plt.savefig(f'database_photos/{filetitle}.png',
                bbox_inches="tight", dpi=300)


def two_lines(x_series, y_series_1, y_series_2, xlabeltext, ylabeltext1, ylabeltext2, title, filetitle, percent="No", color1="brown", color2="blue", ylabeladjust=.05, typepic=ppt_size):
    fig, ax = plt.subplots(figsize=(typepic.figsizeover, typepic.figsizeup))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.plot(x_series, y_series_1, color=color1,
            clip_on=False, label=ylabeltext1)
    ax2 = ax.twinx()
    ax2.plot(x_series, y_series_2, color=color2,
             clip_on=False, label=ylabeltext1)

    plt.xlabel(xlabeltext, fontsize=typepic.labelsize)
    ax.set_ylabel(ylabeltext1, fontsize=typepic.labelsize)
    plt.title(title, fontsize=typepic.titlesize)
    ax2.set_ylabel(ylabeltext2, fontsize=typepic.labelsize)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    ax.legend()

    if percent == "Yes":
        fmt = '%.0f%%'
        yticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(yticks)
        perad = "%"
    else:
        perad = ""

    plt.xticks(x_series, fontsize=typepic.xticksize, rotation=0)
    plt.yticks(fontsize=typepic.yticksize)

    # for index in range(len(x_series)):
    #    ax.text(x_series[index],y_series[index]+ylabeladjust,str(y_series[index])+perad,fontsize=typepic.datalabelsize,ha="center")

    plt.savefig(f'{filetitle}.png', bbox_inches="tight", dpi=300)
