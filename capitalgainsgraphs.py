# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 07:42:56 2023

@author: Sarah Lawsky
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import photosettings as cp
import matplotlib.font_manager as font_manager

# Preliminary Items

# gillius_font_path = '/usr/share/fonts/truetype/adf/GilliusADF-Regular.otf'
# gillius_font = font_manager.FontProperties(fname=gillius_font_path).get_name()

times_font_path = '/home/slawsky/.fonts/times.ttf'
font_manager.fontManager.addfont(times_font_path)
times_font = font_manager.FontProperties(fname=times_font_path).get_name()


plt.rcParams.update({
    "text.usetex": False,
    "font.family": times_font,
})



relevant_size = cp.ppt_size
# relevant_size = cp.blog_size

title_pad = 0  # -.3 is good for title below
legend_pad = -.2

color_dict = {'color': {'green': 'green', 'red': 'red'},
              "nocolor": {'green': '0.7', "red": '0.1'}}


def get_title_name(usage, graphnum):
    if usage == "paper":
        return f"Figure {graphnum}: "
    else:
        return ""


def create_title(plt, usage, graphnum, title_text):
    if usage != "vataxreview":
        title_name = get_title_name(usage, graphnum)
        plt.title(f"{title_name}{title_text}")

LLSL = 'NLTCL & NSTCL\nLoss carryforward'
LGSG = 'NLTCG & NSTCG\nNet capital gain'
LLSG = 'NLTCL & NSTCG\nLoss carryforward or capital losses exhausted'
LGSL = 'NLTCG & NSTCL\nLoss carryforward or net capital gain'


def create_loss_fill(ax1, x, y, incolor='color'):
    fillcolor = color_dict[incolor]['green']
    ax1.fill_between(x, -1, -y, color=fillcolor, alpha=0.2,
                     interpolate=True, label='Loss carryforward')


def create_gain_fill(ax1, x, y, incolor='color'):
    fillcolor = color_dict[incolor]['red']
    ax1.fill_between(x, 1, -y, where=(x >= 0), color=fillcolor,
                     alpha=0.2, interpolate=True, label='Net capital gain')


def create_frame(fig, x, ax1):
    ax1.set_xlim([-1, 1])  # Set x limits
    ax1.set_ylim([-1, 1])
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.text(.5, .95, 'Quadrant I (+,+)', va='top', ha='center')
    ax1.text(-.5, .95, 'Quadrant II (-,+)', va='top', ha='center')
    ax1.text(-.5, -.9, 'Quadrant III (-,-)', va='top', ha='center')
    ax1.text(.5, -.9, 'Quadrant IV (+,-)', va='top', ha='center')
    ax1.axvline(0, c='black', ls='--')
    ax1.axhline(0, c='black', ls='--')


def create_linspace():
    return np.linspace(-1, 1, 1000), np.linspace(-1, 1, 1000)


def create_axis_labels(ax1):
    ax1.set_xlabel("LTCG - LTCL")  # Set x label
    ax1.set_ylabel("STCG - STCL")

# Excess of Graphs


def excess_of(fignum, **kwargs):
    usage = kwargs.get('usage', 'paper')
    fig = plt.figure()
    x, y = create_linspace()
    graphnum = "{:02d}".format(fignum)

    ax1 = fig.add_axes([0, 0, 1, 1])
    ax1.set_xlim([0, 1])  # Set x limits
    ax1.set_ylim([0, 1])
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlabel("A")  # Set x label
    ax1.set_ylabel("B")
    ax1.plot([0, 1], [0, 1], color='black', label='A=B')
    ax1.fill_between(x, y, 0, color='white', hatch='x', edgecolor='grey',
                     alpha=0.3, label='A > B; A -* B = A - B', interpolate=True)
    ax1.fill_between(x, y, 1, color='white', hatch='O', edgecolor='grey',
                     alpha=0.3, label='A < B; A -* B = 0', interpolate=True)
    fig.legend(loc='center', bbox_to_anchor=(.5, -.2))
    create_title(plt, usage, graphnum, "Excess Of Divides Numerical Space")
    plt.savefig(f'photos/fig_{graphnum}_excess_of.png',
                bbox_inches="tight", dpi=300)


def excess_of_A_B(fignum, **kwargs):
    usage = kwargs.get('usage', 'paper')
    fig = plt.figure()
    x, y = create_linspace()
    graphnum = "{:02d}".format(fignum)

    ax1 = fig.add_axes([-1, -1, 1, 1])
    ax1.set_xlim([-1, 1])  # Set x limits
    ax1.set_ylim([-1, 1])
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.text(-.05, .01, "(0,0)", va='bottom', ha='center')
    ax1.set_xlabel("A - B")  # Set x label
    ax1.set_ylabel("A -* B")
    ax1.plot([0, 1], [0, 1], color='black', linewidth=3)
    ax1.plot([0, -1], [0, 0], color='black', linewidth=4)
    ax1.axvline(0, c='black', ls='--')
    ax1.axhline(0, c='black', ls='--')

    create_title(plt, usage, graphnum, "Subtraction vs. Excess Of")

    plt.savefig(f'photos/fig_{graphnum}_excess_of_A_B.png',
                bbox_inches="tight", dpi=300)


def cliff(fignum, **kwargs):
    usage = kwargs.get('usage', 'paper')
    fig = plt.figure()
    x, y = np.linspace(0, 3000, 1000), np.linspace(0, 3000, 1000)
    graphnum = "{:02d}".format(fignum)

    ax1 = fig.add_axes([0, 0, 1, 1])
    ax1.set_xlim([0, 5000])  # Set x limits
    ax1.set_ylim([0, 5000])
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xticks([3000])
    ax1.set_yticks([3000])

    formatter = FuncFormatter(lambda x, _: '${:,.0f}'.format(x))
    ax1.xaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_formatter(formatter)

    ax1.plot([0, 3000], [0, 0], color='black', linewidth=3)
    ax1.plot([3000, 5000], [3000, 5000], color='black', linewidth=2)

    ax1.scatter([3000], [0], color='black', s=50, zorder=9)
    ax1.scatter([3000], [3000], edgecolor='black',
                facecolor='white', s=50, zorder=2)

    # Set x label
    ax1.set_xlabel("Excess of Capital Losses Over Capital Gains")
    ax1.set_ylabel("Loss Carryforward")
    create_title(plt, usage, graphnum, "The Cliff Example: No Adjusted Taxable Income")
    plt.savefig(f'photos/fig_{graphnum}_cliff.png',
                bbox_inches="tight", dpi=300)


# Net Capital Loss Graphs


def taxable_income_base():
    fig = plt.figure()
    x, y = np.linspace(0, 3000, 1000), np.linspace(0, 3000, 1000)

    ax1 = fig.add_axes([0, 0, 1, 1])
    ax1.set_xlim([0, 5000])  # Set x limits
    ax1.set_ylim([0, 5000])
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xticks([3000])
    ax1.set_yticks([3000])

    formatter = FuncFormatter(lambda x, _: '${:,.0f}'.format(x))
    ax1.xaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_formatter(formatter)

    ax1.set_xlabel("Adjusted Taxable Income")  # Set x label
    ax1.set_ylabel("Excess of Capital Losses Over Capital Gains")
    return fig, ax1, x, y


def net_cap_loss(fignum, **kwargs):
    usage = kwargs.get('usage', 'paper')
    graphnum = "{:02d}".format(fignum)
    fig, ax1, x, y = taxable_income_base()
    ax1.plot([0, 5000], [3000, 3000], color='black', linestyle='--',
             label='Maximum usable excess losses; 1211(b)(1)')
    ax1.fill_between([0, 5000], 3000, 5000, color='white', hatch='x',
                     edgecolor='grey', alpha=.2, label='Net Capital Loss')
    fig.legend(loc='center', bbox_to_anchor=(.5, legend_pad))
    create_title(plt, usage, graphnum, "Net Capital Loss")
    plt.savefig(f'photos/fig_{graphnum}_net_cap_loss.png',
                bbox_inches="tight", dpi=300)


def net_cap_loss_with_carryforward(fignum, **kwargs):
    incolor = kwargs.get('incolor', 'nocolor')
    usage = kwargs.get('usage', 'paper')
    graphnum = "{:02d}".format(fignum)
    fillcolor = color_dict[incolor]['green']
    fig, ax1, x, y = taxable_income_base()
    ax1.plot([0, 5000], [3000, 3000], color='black', linestyle='--',
             label='Maximum usable excess losses; 1211(b)(1)')
    ax1.fill_between([0, 5000], 3000, 5000, color=fillcolor,
                     edgecolor='grey', alpha=.2, label='Loss Carryforward')
    ax1.fill_between([0, 5000], 3000, 5000, color='white', hatch='x',
                     edgecolor='grey', alpha=.2, label='Net Capital Loss')
    fig.legend(loc='center', bbox_to_anchor=(.5, legend_pad))
    create_title(plt, usage, graphnum, "The Statute: Net Capital Loss and Loss Carryforward")
    plt.savefig(f'photos/fig_{graphnum}_net_cap_loss_carryforward.png',
                bbox_inches="tight", dpi=300)


def low_income(fignum, **kwargs):
    incolor = kwargs.get('incolor', 'nocolor')
    usage = kwargs.get('usage', 'paper')
    graphnum = "{:02d}".format(fignum)
    fillcolor = color_dict[incolor]['green']
    fig, ax1, x, y = taxable_income_base()
    ax1.plot([0, 5000], [3000, 3000], color='black', linestyle='--',
             label='Maximum usable excess losses; 1211(b)(1)')
    ax1.fill_between([0, 5000], 3000, 5000, color='white', hatch='x',
                     edgecolor='grey', alpha=.2, label='Net Capital Loss')
    ax1.fill_between([0, 5000], 3000, 5000, color=fillcolor,
                     edgecolor='grey', alpha=.2, label='Loss Carryforward')
    ax1.plot([0, 3000], [0, 3000], color='black',
             label='Excess Losses = Adjusted Taxable Income')
    ax1.plot([3000, 3000], [0, 3000], color='black', linestyle='--')
    ax1.fill_between(y, 3000, y, color='white', hatch='o', edgecolor='grey',
                     alpha=0.2, label='Adjusted Taxable Income < Excess Losses', interpolate=True)
    fig.legend(loc='center', bbox_to_anchor=(.5, legend_pad))
    create_title(plt, usage, graphnum, "The Statute: Loss Carryforward and Low Income")

    plt.savefig(f'photos/fig_{graphnum}_low_income.png',
                bbox_inches="tight", dpi=300)


def low_income_with_dot(fignum, **kwargs):
    incolor = kwargs.get('incolor', 'nocolor')
    usage = kwargs.get('usage', 'paper')
    graphnum = "{:02d}".format(fignum)
    fillcolor = color_dict[incolor]['green']
    fig, ax1, x, y = taxable_income_base()
    ax1.plot([0, 5000], [3000, 3000], color='black', linestyle='--',
             label='Maximum usable excess losses; 1211(b)(1)')
    ax1.fill_between([0, 5000], 3000, 5000, color='white', hatch='x',
                     edgecolor='grey', alpha=.2, label='Net Capital Loss')
    ax1.fill_between([0, 5000], 3000, 5000, color=fillcolor,
                     edgecolor='grey', alpha=.2, label='Loss Carryforward')
    ax1.plot([0, 3000], [0, 3000], color='black',
             label='Excess Losses = Adjusted Taxable Income')
    ax1.plot([3000, 3000], [0, 3000], color='black', linestyle='--')
    ax1.fill_between(y, 3000, y, color='white', hatch='o', edgecolor='grey',
                     alpha=0.2, label='Adjusted Taxable Income < Excess Losses', interpolate=True)
    ax1.scatter(1000, 2000, color='black')
    ax1.text(950, 2000, '(\$1000,\$2500)',
             verticalalignment='bottom', horizontalalignment='right')

    create_title(plt, usage, graphnum, "The Statute: Loss Carryforward and Low Income Example")

    fig.legend(loc='center', bbox_to_anchor=(.5, legend_pad))

    plt.savefig(f'photos/fig_{graphnum}_low_income_with_dot.png',
                bbox_inches="tight", dpi=300)


def taxable_income_all(fignum, **kwargs):
    incolor = kwargs.get('incolor', 'nocolor')
    usage = kwargs.get('usage', 'paper')
    graphnum = "{:02d}".format(fignum)
    fillcolor = color_dict[incolor]['green']
    fig, ax1, x, y = taxable_income_base()
    ax1.plot([0, 5000], [3000, 3000], color='black', linestyle='--',
             label='Maximum usable excess losses; 1211(b)(1)')
    ax1.fill_between([0, 5000], 3000, 5000, color='white', hatch='x',
                     edgecolor='grey', alpha=.2, label='Net Capital Loss')
    ax1.fill_between([0, 5000], 3000, 5000, color=fillcolor,
                     edgecolor='grey', alpha=.2, label='Loss Carryforward')
    ax1.plot([0, 3000], [0, 3000], color='black',
             label='Excess Losses = Adjusted Taxable Income')
    ax1.plot([3000, 3000], [0, 3000], color='black', linestyle='--')

    ax1.fill_between(y, 3000, y, color='white', hatch='o', edgecolor='grey',
                     alpha=0.2, label='Adjusted Taxable Income < Excess Losses', interpolate=True)
    ax1.fill_between(y, 3000, y, color=fillcolor, alpha=0.2)
    fig.legend(loc='center', bbox_to_anchor=(.5, legend_pad))
    create_title(plt, usage, graphnum, "The Fix: Loss Carryforward and Low Income")
    plt.savefig(f'photos/fig_{graphnum}_low_income_correct_carryforward.png',
                bbox_inches="tight", dpi=300)

# Cap Gain Summary Graphs


def create_ST_fill(ax1, x, y):
    ax1.fill_between(x, 0, 1, color='white', hatch='x', edgecolor='grey',
                     alpha=0.3, label='STCG>STCL (NSTCG)', interpolate=True)


def create_LT_fill(ax1, x, y):
    ax1.fill_between(x, -1, 1, where=x >= 0, color='white', edgecolor='grey',
                     hatch='o', alpha=0.3, label='LTCG>LTCL (NLTCG)', interpolate=True)


def create_no_fill_graph(fignum, **kwargs):
    usage = kwargs.get('usage', 'paper')
    graphnum = "{:02d}".format(fignum)
    fig = plt.figure()
    x, y = create_linspace()
    ax1 = fig.add_axes([0, 0, 1, 1])
    create_frame(fig, x, ax1)
    create_axis_labels(ax1)
    create_title(plt, usage, graphnum, "LTCG - LTCL vs. STCG - STCL")
    plt.savefig(f'photos/fig_{graphnum}_all_frame.png',
                bbox_inches="tight", dpi=300)


def create_lt_fill_graph(fignum, **kwargs):

    usage = kwargs.get('usage', 'paper')
    fig = plt.figure()
    x, y = create_linspace()
    ax1 = fig.add_axes([0, 0, 1, 1])
    graphnum = "{:02d}".format(fignum)

    create_LT_fill(ax1, x, y)
    create_frame(fig, x, ax1)
    create_axis_labels(ax1)
    fig.legend(loc='center', bbox_to_anchor=(.5, -.2))
    create_title(plt, usage, graphnum, "Net Long Term Capital Gain")
    plt.savefig(f'photos/fig_{graphnum}_lt_fill.png',
                bbox_inches="tight", dpi=300)


def create_st_fill_graph(fignum, **kwargs):

    usage = kwargs.get('usage', 'paper')
    fig = plt.figure()
    x, y = create_linspace()
    graphnum = "{:02d}".format(fignum)
    ax1 = fig.add_axes([0, 0, 1, 1])
    create_ST_fill(ax1, x, y)

    create_frame(fig, x, ax1)
    create_axis_labels(ax1)
    fig.legend(loc='center', bbox_to_anchor=(.5, -.2))
    create_title(plt, usage, graphnum, "Net Short Term Capital Gain")

    plt.savefig(f'photos/fig_{graphnum}_st_fill.png',
                bbox_inches="tight", dpi=300)


def create_hash_labels_graph(fignum, **kwargs):
    usage = kwargs.get('usage', 'paper')
    graphnum = "{:02d}".format(fignum)
    LongLossShortLoss = LLSL
    LongGainShortGain = LGSG
    LongLossShortGain = LLSG
    LongGainShortLoss = LGSL
    fig = plt.figure()
    x, y = create_linspace()
    ax1 = fig.add_axes([0, 0, 1, 1])

    create_ST_fill(ax1, x, y)
    create_LT_fill(ax1, x, y)
    create_frame(fig, x, ax1)
    create_axis_labels(ax1)

    ax1.text(-.5, -.5, LongLossShortLoss, va='top', ha='center')
    ax1.text(.5, .5, LongGainShortGain, va='top', ha='center')
    ax1.text(.5, -.5, LongGainShortLoss, va='top', ha='center')
    ax1.text(-.5, .5, LongLossShortGain, va='top', ha='center')

    fig.legend(loc='center', bbox_to_anchor=(.5, -.2))

    create_title(plt, usage, graphnum, "NLTCG and NSTCG")

    plt.savefig(f'photos/fig_{graphnum}_hash_labels.png',
                bbox_inches="tight", dpi=300)


def with_dividing_line(fignum, **kwargs):
    incolor = kwargs.get('incolor', 'nocolor')
    usage = kwargs.get('usage', 'paper')
    LongLossShortLoss = LLSL
    LongGainShortGain = LGSG

    fig = plt.figure()
    x, y = create_linspace()
    ax1 = fig.add_axes([0, 0, 1, 1])
    graphnum = "{:02d}".format(fignum)

    create_ST_fill(ax1, x, y)
    create_LT_fill(ax1, x, y)
    create_frame(fig, x, ax1)
    create_axis_labels(ax1)

    # dividing line from top to bottom
    ax1.plot([-1, 1], [1, -1], color='black',
             label='LTCG - LTCL = STCL - STCG')

    ax1.text(-.5, -.4,
             f'{LongLossShortLoss}\n1212(b)(1)(A) + 1212(b)(1)(B):\nNSTCL + NLTCL', va='top', ha='center')
    ax1.text(.5, .5, f'{LongGainShortGain}\nNLTCG', va='top', ha='center')

    ax1.text(-.66, .4, 'NLTCL > NSTCG\nLoss carryforward\n1212(b)(1)(B):\nNLTCL - NSTCG',
             va='top', ha='center')
    ax1.text(.2, -.5, 'NSTCL > NLTCG\nLoss carryforward\n1212(b)(1)(A):\nNSTCL - NLTCG',
             va='top', ha='center')
    ax1.text(-.35, .85, 'NLTCL < NSTCG\nLosses exhausted',
             va='top', ha='center')
    ax1.text(.66, -.2, 'NLTCG > NSTCL\nNet capital gain\nNLTCG-NSTCL',
             va='top', ha='center')

    create_loss_fill(ax1, x, y, incolor)
    create_gain_fill(ax1, x, y, incolor)

    create_title(plt, usage, graphnum, "Loss Carryforward and Net Capital Gain (Preliminary)")

    fig.legend(loc='center', bbox_to_anchor=(.5, -.2))

    plt.savefig(f'photos/fig_{graphnum}_dividing_line.png',
                bbox_inches="tight", dpi=300)


def with_dividing_line_and_3000(fignum, **kwargs):
    incolor = kwargs.get('incolor', 'nocolor')
    usage = kwargs.get('usage', 'paper')
    LongGainShortGain = LGSG

    graphnum = "{:02d}".format(fignum)

    fillcolor = color_dict[incolor]['green']

    fig = plt.figure()
    x, y = create_linspace()
    ax1 = fig.add_axes([0, 0, 1, 1])

    create_ST_fill(ax1, x, y)
    create_LT_fill(ax1, x, y)
    create_frame(fig, x, ax1)
    create_axis_labels(ax1)

    # dividing line from top to bottom
    ax1.plot([-1, 1], [1, -1], color='black',
             label='LTCG - LTCL = STCL - STCG')

    ax1.text(-.5, -.5, 'NLTCL and STCL - STCG# > 0\nLoss carryforward\n1212(b)(1)(A) + 1212(b)(1)(B):\n(STCL - STCG#) + NLTCL', va='top', ha='center')
    ax1.text(.5, .5, f'{LongGainShortGain}\nNLTCG', va='top', ha='center')

    ax1.text(-.72, .4, 'NLTCL > (STCL - STCG#)\nLoss carryforward\n1212(b)(1)(B):\nNLTCL - (STCL - STCG#)', va='top', ha='center')
    ax1.text(.25, -.5, '(STCL - STCG#) >\nNLTCG\nLoss carryforward\n1212(b)(1)(A):\n(STCL - STCG#) - NLTCG', va='top', ha='center')
    ax1.text(-.35, .85, 'NLTCL < (STCG# - STCL)\nLosses exhausted',
             va='top', ha='center')
    ax1.text(.66, -.2, 'NLTCG > NSTCL\nNet capital gain\nNLTCG-NSTCL',
             va='top', ha='center')

    # this represents STCG - STCL = LTCG - LTCL + 1212(b)(2)
    z = x + .1

    # offset line; we say negative z because the real thing we want to
    # capture is LTCG - LTCL + 1212(b)(2) < STCL - STCG, not STCL - STCL

    ax1.fill_between(x, -1, -z, color=fillcolor, alpha=0.2,
                     interpolate=True, label='Loss carryforward')
    create_gain_fill(ax1, x, y, incolor)

    ax1.plot(x, -z, linestyle='dotted', color=fillcolor,
             label='LTCG - LTCL + 1212(b)(2) < STCL - STCG')

    fig.legend(loc='center', bbox_to_anchor=(.5, -.2))

    create_title(plt, usage, graphnum, "Loss Carryforward and Net Capital Gain")

    plt.savefig(f'photos/fig_{graphnum}_dividing_line_and_OI.png',
                bbox_inches="tight", dpi=300)


# Function Lists

excess_of_list = [excess_of, excess_of_A_B]

net_cap_loss_list = [net_cap_loss, net_cap_loss_with_carryforward,
                     low_income,
                     low_income_with_dot,
                     cliff,
                     taxable_income_all]

cap_summary_list = [create_no_fill_graph, create_lt_fill_graph,
                    create_st_fill_graph,
                    create_hash_labels_graph, with_dividing_line,
                    with_dividing_line_and_3000]

all_graphs_list = excess_of_list + net_cap_loss_list + cap_summary_list


def create_list_graphs(graphlist, incolor_value="nocolor", usage_value="paper"):
    fig_value = 1
    for item in graphlist:
        item(fignum=fig_value, incolor=incolor_value, usage=usage_value)
        fig_value += 1


create_list_graphs(all_graphs_list,usage_value='vataxreview')
