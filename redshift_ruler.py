# Cosmology Ruler Bookmark:
# Marque-Page Cosmologique
# by Hervé Dole, Université Paris-Saclay
# 20240102 
#
# See publication in arXiv:2401.03929
# http://arxiv.org/abs/2401.03929
#
# Please cite Dole (2024) arXiv:2401.03929 if you like or use this bookmark
#
# Creates a (vertical) 2-sided bookmark with 5 axes :
# redshift z
# age of Universe at redshift z in Gyr
# lookback time at redshift z in Gyr
# arcsec for 1 proper kpc in arcsec
# again redshift z for more acurate reading
#
# Generates a pdf and a png file:
# python redshift_ruler.py 
#
# Planck18 cosmology used
# Astropy cosmology package used:
# https://docs.astropy.org/en/stable/cosmology/index.html
#


import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
import numpy as np
from astropy.cosmology import Planck18, z_at_value
import astropy.units as u

#--------------------------------------------
# RECTO of BOOKMARK : LARGE REDSHIFT RANGE
#--------------------------------------------

# SETUP REDSHIFT RANGE
# to be computed and displayed
# there are more ticks than displayed numerical values; this is why there are 2 arrays 
redshiftarray = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 1, 1.3, 1.7, 2, 2.5, 3 ,4, 5, 6, 7, 10, 13, 15, 20, 30, 40, 50, 70, 100, 130, 200, 300, 400, 500, 700, 1000] 
redshift_minplot = np.min(redshiftarray)
redshift_maxplot = np.max(redshiftarray)
labels_redshiftarray = ["0.1", "", "0.2", "0.3", "0.4", "0.5", "", "0.7", "1", "1.3", "1.7", "2", "2.5", "3" ,"4", "5", "6", "7", "10", "13", "", "20", "30", "40", "50", "70", "100", "130","200", "300", "400", "500","700", "1000"] 

# age of the Universe to be displayed
ages = np.array([12.3, 12., 11.5, 11., 10., 9., 8., 7., 6, 5, 4, 3, 2, 1.3, 1, 0.8, 0.5, 0.3, 0.2, 0.1, 0.05, 0.03, 0.02, 0.01, 0.005, 0.003, 0.001, 0.0005])*u.Gyr
# warning: make sure ages fill the displayed redshift range and do not go beyond: otherwise dummy plot

# lookback time to be displayed
ages4loopbacktime = np.array([13.786, 13.785, 13.783, 13.78, 13.77, 13.75,  13.7, 13.6, 13.5, 13.3, 13.0, 12.5, 12., 11., 10, 9, 8, 7, 6., 5., 4., 3., 2.5, 2., 1.5])*u.Gyr
# warning: make sure lookback times fill the displayed redshift range and do not go beyond: otherwise dummy plot

# redshift where to write angular diameter distance in arcsec/kpc
redshift4arcsec = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5,  0.7, 1, 1.3, 2, 3 ,4,  7, 10, 13, 20, 30, 40, 50, 70, 100, 130, 200, 300, 400,  600, 900] 


# COSMOLOGY PART
#---------------
# for use of Cosmology Astropy package: look at
# https://learn.astropy.org/tutorials/redshift-plot.html
# https://docs.astropy.org/en/stable/api/astropy.cosmology.FLRW.html#astropy.cosmology.FLRW

cosmo = Planck18

# define redshift values 
# Get age in Gyr for each redshift 
age_time_gyr = cosmo.age(redshiftarray)
age_time_gyr_ticks = [np.log10(z_at_value(cosmo.age, age)) for age in ages]

# Get age in Gyr for each redshift (loopback time)
lookback_time_gyr = cosmo.lookback_time(redshiftarray)
lookback_time_gyr_ticks = [np.log10(z_at_value(cosmo.lookback_time, age)) for age in ages4loopbacktime]

# Get arcsec for each physical kpc at z
arcsec_per_kpc_proper = cosmo.arcsec_per_kpc_proper(redshift4arcsec)
arcsec_per_kpc_proper_ticks = redshift4arcsec


# DISPLAY PART
#---------------

def setup_axes(fig, pos):
    ax = fig.add_subplot(pos, axes_class=axisartist.Axes)
    ax.axis[:].set_visible(False)
    ax.axis["x"] = ax.new_floating_axis(1, 0.5)
    return ax


plt.rcParams.update({
    "axes.titlesize": "medium",
    "axes.titley": 1.0,
})

plt.rcParams['text.usetex'] = True
plt.rcParams['axes.autolimit_mode'] = 'round_numbers'

fig = plt.figure(figsize=(2, 12))
fig.subplots_adjust(bottom=0.025, top=0.88, left=0.05, right=0.95)

# left axis: z
ax1 = setup_axes(fig, 151)
ax1.set_ylim(redshift_minplot, redshift_maxplot)
ax1.set_yscale('log')
ax1.set_yticks(redshiftarray, labels=labels_redshiftarray)
ax1.axis["x"].set_axislabel_direction("+")

# axis 2: age
ax2 = setup_axes(fig, 152)
ax2.axis["x"].set_axislabel_direction("+")
ax2.set_ylim(np.log10(redshift_minplot), np.log10(redshift_maxplot)) 
ax2.set_yticks(age_time_gyr_ticks)
ax2.set_yticklabels(['{:g}'.format(age) for age in ages.value])


#axis 3: lookback time
ax3 = setup_axes(fig, 153)
ax3.axis["x"].set_axislabel_direction("+")
ax3.set_ylim(np.log10(redshift_minplot), np.log10(redshift_maxplot))
ax3.set_yticks(lookback_time_gyr_ticks)
ax3.set_yticklabels(['{:g}'.format(age) for age in ages4loopbacktime.value])

#axis 4: arcsec for 1 kpc physical
ax4 = setup_axes(fig, 154)
ax4.axis["x"].set_axislabel_direction("+")
ax4.set_ylim(redshift_minplot, redshift_maxplot)
ax4.set_yscale('log')
ax4.set_yticks(arcsec_per_kpc_proper_ticks)
ax4.set_yticklabels(['{:,.2f}'.format(arcsec) for arcsec in arcsec_per_kpc_proper.value])

#axis 5: z again
ax5 = setup_axes(fig, 155)
ax5.set_ylim(redshift_minplot, redshift_maxplot)
ax5.set_yscale('log')
ax5.set_yticks(redshiftarray, labels=labels_redshiftarray)
ax5.axis["x"].set_axislabel_direction("+")

# Axes legend
label_axis1 = "redshift z [0.1, 1000] in log scale"
plt.figtext(0.06, .38, label_axis1 , fontsize=9, ha='center', rotation='vertical', zorder=2)
label_axis2 = "age [Gyr]"
plt.figtext(0.26, .43, label_axis2 , fontsize=9, ha='center', rotation='vertical', zorder=2)
label_axis3 = "lookback time [Gyr]"
plt.figtext(0.45, .41, label_axis3 , fontsize=9, ha='center', rotation='vertical', zorder=2)
label_axis4 = "angle for 1 kpc [arcsec]"
plt.figtext(0.63, .40, label_axis4 , fontsize=9, ha='center', rotation='vertical', zorder=2)
label_axis5 = "redshift z"
plt.figtext(0.81, .43, label_axis5 , fontsize=9, ha='center', rotation='vertical', zorder=2)


# Top and Bottom Texts
# Top text
title_us1 = "{\\bf Cosmology Ruler Bookmark}"
title_fr1 = "{\\bf Marque-page cosmologique}"

params1 = "$\\Omega_{m} = 0.310 \\, \\, \\Omega_{\\Lambda} = 0.690 $"      
params2 = "$H_0 = 67.6 \\, \\rm{km}/\\rm{s}/\\rm{Mpc} $"

ref1 = "(Planck Collab., 2020, A\\&A, 641, A1) "

legend1 = "Age and time in Gyr. Angle "
legend2 = "(for 1 kpc proper) in arcsec."

textzrange = "Recto: $z \\in [0.1, 1000]$ in log scale"

plt.figtext(0.5, .99, title_us1 , fontsize=9, ha='center')

plt.figtext(0.5, .98, title_fr1 , fontsize=9, ha='center')

plt.figtext(0.5, .96, params1, fontsize=9, ha='center')
plt.figtext(0.5, .95, params2, fontsize=9, ha='center')

plt.figtext(0.5, .94, ref1, fontsize=6.5, ha='center')

plt.figtext(0.5, .925, legend1, fontsize=9, ha='center')
plt.figtext(0.5, .915, legend2, fontsize=9, ha='center')

plt.figtext(0.5, .895, textzrange, fontsize=9, ha='center')

# Bottom text
bottom_text = "H. Dole - Université Paris-Saclay - 2024"
plt.figtext(0.5, .0098, bottom_text, fontsize=7., ha='center')
bottom_text2 = "arXiv:2401.03929"
plt.figtext(0.5, .003, bottom_text2, fontsize=7., ha='center')

# dpi quality; 300 recommended
dpi = 300

# save bookmark recto
plt.savefig("CosmologyRulerBookmark_Recto_v0.png", dpi=dpi)
plt.savefig("CosmologyRulerBookmark_Recto_v0.pdf", dpi=dpi)

#plt.show()



















#--------------------------------------------
# VERSO of BOOKMARK : SMALLER REDSHIFT RANGE
#--------------------------------------------

# SETUP REDSHIFT RANGE
# there are more ticks than displayed numerical values; this is why there are 2 arrays 
redshiftarray = [0.0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30] 
redshift_minplot = np.min(redshiftarray)
redshift_maxplot = np.max(redshiftarray)
labels_redshiftarray = ["0", "1", "2",  "3" ,"4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"] 
redshiftarray2 = [0.0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.5, 27, 27.5, 28, 28.5, 29, 29.5, 30] 

# ages to be displayed: more ticks than displayed numerical values; this is why there are 2 arrays 
ages = np.array([10, 7, 6, 5, 4, 3,  2, 1.7, 1.3, 1, 0.8, 0.9, 0.7, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.27, 0.25, 0.23, 0.2, 0.18, 0.17, 0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.105, 0.1])*u.Gyr
ages2 = np.array([13., 12., 11., 10, 9, 8, 7, 6, 5, 4.5, 4, 3.5, 3, 2.5, 2, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5,  0.45,  0.4, 0.39, 0.38, 0.37, 0.36, 0.35, 0.34, 0.33, 0.32, 0.31, 0.3, 0.29, 0.28, 0.27, 0.26, 0.25, 0.24, 0.23, 0.22, 0.21, 0.2,  0.19,  0.18,  0.17, 0.16, 0.15,  0.14,  0.13,  0.12,  0.11, 0.105, 0.1])*u.Gyr
# warning: make sure ages fill the displayed redshift range and do not go beyond: otherwise dummy plot

# lookback time to be displayed: more ticks than displayed numerical values; this is why there are 2 arrays 
ages4loopbacktime = np.array([13.686, 13.68, 13.67, 13.65, 13.62, 13.6, 13.57, 13.55, 13.5, 13.4, 13.3, 13.2, 13.1, 13.0, 12.8, 12.5, 12., 11., 10, 9, 8, 7, 5,   1.0, ])*u.Gyr
ages4loopbacktime2 = np.array([13.686, 13.683, 13.68, 13.675, 13.67, 13.66, 13.65, 13.64, 13.63, 13.62, 13.61, 13.6, 13.59, 13.58, 13.57, 13.56, 13.55, 13.54, 13.53, 13.52, 13.51, 13.5, 13.45, 13.4, 13.35, 13.3, 13.2, 13.1, 13.0, 12.9, 12.8, 12.7, 12.6, 12.5, 12.25, 12., 11.5, 11., 10, 9, 8, 7, 5,   1.0, ])*u.Gyr
# warning: make sure lookback times fill the displayed redshift range and do not go beyond: otherwise dummy plot

# redshift where to write angular diameter distance in arcsec/kpc
redshift4arcsec = [0.25, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30] 


# COSMOLOGY PART
#---------------
# for use of Cosmology Astropy package: look at
# https://learn.astropy.org/tutorials/redshift-plot.html
# https://docs.astropy.org/en/stable/api/astropy.cosmology.FLRW.html#astropy.cosmology.FLRW

cosmo = Planck18

# define redshift values : linear values but numbers spaced evenly on a log scale
#redshiftarray = np.logspace(np.log10(redshift_minplot), np.log10(redshift_maxplot))

# Get age in Gyr for each redshift 
age_time_gyr = cosmo.age(redshiftarray)
age_time_gyr_ticks = [z_at_value(cosmo.age, age) for age in ages]
age_time_gyr_ticks2 = [z_at_value(cosmo.age, age) for age in ages2] # more ticks without labels to display

# Get age in Gyr for each redshift (loopback time)
lookback_time_gyr = cosmo.lookback_time(redshiftarray)
lookback_time_gyr_ticks = [z_at_value(cosmo.lookback_time, age) for age in ages4loopbacktime]
lookback_time_gyr_ticks2 = [z_at_value(cosmo.lookback_time, age) for age in ages4loopbacktime2]

# Get arcsec for each physical kpc at z
arcsec_per_kpc_proper = cosmo.arcsec_per_kpc_proper(redshift4arcsec)
arcsec_per_kpc_proper_ticks = redshift4arcsec


# DISPLAY PART
#---------------

def setup_axes(fig, pos):
    ax = fig.add_subplot(pos, axes_class=axisartist.Axes)
    ax.axis[:].set_visible(False)
    ax.axis["x"] = ax.new_floating_axis(1, 0.5)
    return ax


plt.rcParams.update({
    "axes.titlesize": "medium",
    "axes.titley": 1.0,
})

plt.rcParams['text.usetex'] = True
plt.rcParams['axes.autolimit_mode'] = 'round_numbers'

fig = plt.figure(figsize=(2, 12))
fig.subplots_adjust(bottom=0.025, top=0.88, left=0.05, right=0.95)

# left axis: z
ax1 = setup_axes(fig, 151)
ax1.set_ylim(redshift_minplot, redshift_maxplot)
ax1.set_yticks(redshiftarray, labels=labels_redshiftarray)
ax1.axis["x"].set_axislabel_direction("+")

# axis 2: age
ax2 = setup_axes(fig, 152)
ax2.axis["x"].set_axislabel_direction("+")
ax2.set_ylim(redshift_minplot, redshift_maxplot)
ax2.set_yticks(age_time_gyr_ticks)
ax2.set_yticklabels(['{:g}'.format(age) for age in ages.value])
ax2.set_yticks(age_time_gyr_ticks2)


#axis 3: lookback time
ax3 = setup_axes(fig, 153)
ax3.axis["x"].set_axislabel_direction("+")
ax3.set_ylim(redshift_minplot, redshift_maxplot)
ax3.set_yticks(lookback_time_gyr_ticks)
ax3.set_yticklabels(['{:g}'.format(age) for age in ages4loopbacktime.value])
ax3.set_yticks(lookback_time_gyr_ticks2)

#axis 4: arcsec for 1 kpc physical
ax4 = setup_axes(fig, 154)
ax4.axis["x"].set_axislabel_direction("+")
ax4.set_ylim(redshift_minplot, redshift_maxplot)
ax4.set_yticks(arcsec_per_kpc_proper_ticks)
ax4.set_yticklabels(['{:,.2f}'.format(arcsec) for arcsec in arcsec_per_kpc_proper.value])

#axis 5: z again
ax5 = setup_axes(fig, 155)
ax5.set_ylim(redshift_minplot, redshift_maxplot)
ax5.set_yticks(redshiftarray, labels=labels_redshiftarray)
ax5.axis["x"].set_axislabel_direction("+")
ax5.set_yticks(redshiftarray2)


# Axes legend
#label_axis1 = "redshift z"
label_axis1 = "redshift z [0, 30] in linear scale"
plt.figtext(0.06, .38, label_axis1 , fontsize=9, ha='center', rotation='vertical', zorder=2)
#label_axis2 = "age [Gyr]"
plt.figtext(0.26, .43, label_axis2 , fontsize=9, ha='center', rotation='vertical', zorder=2)
#label_axis3 = "lookback time [Gyr]"
plt.figtext(0.45, .41, label_axis3 , fontsize=9, ha='center', rotation='vertical', zorder=2)
#label_axis4 = "angle for 1 kpc [arcsec]"
plt.figtext(0.63, .40, label_axis4 , fontsize=9, ha='center', rotation='vertical', zorder=2)
#label_axis5 = "redshift z"
plt.figtext(0.81, .43, label_axis5 , fontsize=9, ha='center', rotation='vertical', zorder=2)


# Top and Bottom Texts
# Top text

textzrange = "Verso: $z \\in [0, 30]$ linear scale"

plt.figtext(0.5, .99, title_us1 , fontsize=9, ha='center')

plt.figtext(0.5, .98, title_fr1 , fontsize=9, ha='center')

plt.figtext(0.5, .96, params1, fontsize=9, ha='center')
plt.figtext(0.5, .95, params2, fontsize=9, ha='center')

plt.figtext(0.5, .94, ref1, fontsize=6.5, ha='center')

plt.figtext(0.5, .925, legend1, fontsize=9, ha='center')
plt.figtext(0.5, .915, legend2, fontsize=9, ha='center')

plt.figtext(0.5, .895, textzrange, fontsize=9, ha='center')

# Bottom text
plt.figtext(0.5, .0098, bottom_text, fontsize=7., ha='center')
plt.figtext(0.5, .003, bottom_text2, fontsize=7., ha='center')

# save bookmark recto
plt.savefig("CosmologyRulerBookmark_Verso_v0.png", dpi=dpi)
plt.savefig("CosmologyRulerBookmark_Verso_v0.pdf", dpi=dpi)

#plt.show()


# Combine into a single file for easy print
import os
os.system('gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=CosmologyRulerBookmark_v0.pdf -dBATCH CosmologyRulerBookmark_Recto_v0.pdf CosmologyRulerBookmark_Verso_v0.pdf')


#CHECKS & TESTS
#z_at_value(Planck18.age, 0.0007 * u.Gyr) 

#z_at_value(Planck18.lookback_time, 0.0007 * u.Gyr) 

#Planck18.arcsec_per_kpc_proper(0.5)




