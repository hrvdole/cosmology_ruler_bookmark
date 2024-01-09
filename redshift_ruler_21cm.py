# Cosmology Ruler Bookmark:
# Marque-Page Cosmologique
# by Hervé Dole, Université Paris-Saclay
# 20240102 
# Modified by Adélie Gorce for 21cm cosmology
#
# See publication in arXiv: (soon)
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
import astropy.constants as cst

# Choose rest frequency of reference line
lambda_ref = 0.21  # meters
nu_ref = cst.c.si.value / lambda_ref  # Hz

#--------------------------------------------
# RECTO of BOOKMARK : LARGE REDSHIFT RANGE
#--------------------------------------------

# SETUP REDSHIFT RANGE
# to be displayed
redshiftarray = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 1, 1.3, 1.7, 2, 2.5, 3 ,4, 5, 6, 7, 10, 13, 15, 20, 30, 40, 50, 70, 100])

# age of the Universe to be displayed
ages = np.array([12., 11.5, 11., 10., 9., 8., 7., 6, 5, 4, 3, 2, 1, 0.5, 0.3, 0.2, 0.1, 0.05, 0.03, 0.02])*u.Gyr

# observed wavelengths to be displayed, in meters
lambda_array = np.array([0.25, 0.3, 0.5, 1., 2., 5., 10., 20.])

# observed frequencies to be displayed, in MHz
freq_array = np.array([1200., 1000., 500., 200., 100., 50., 30., 20., 15.])

# COSMOLOGY PART
#---------------
# for use of Cosmology Astropy package: look at
# https://learn.astropy.org/tutorials/redshift-plot.html
# https://docs.astropy.org/en/stable/api/astropy.cosmology.FLRW.html#astropy.cosmology.FLRW

cosmo = Planck18

# define redshift values 
# Get age in Gyr for each redshift 
age_time_gyr = cosmo.age(redshiftarray)
redshifts_for_age_ticks = [z_at_value(cosmo.age, age).value for age in ages]

# Get wavelength in m for each redshift
lambda_for_redshifts = 0.21 * (1. + redshiftarray)
redshifts_for_lambda_ticks = lambda_array / 0.21 - 1.

# Get frequency in MHz for each physical kpc at z
freq_for_redshifts = (cst.c.si / (lambda_for_redshifts * u.m)).to(u.MHz).value
redshifts_for_freq_ticks = nu_ref/1e6 / freq_array - 1.

# get limits of axes
redshift_minplot = np.min(np.r_[redshiftarray, redshifts_for_age_ticks, redshifts_for_freq_ticks, redshifts_for_lambda_ticks])
redshift_maxplot = np.max(np.r_[redshiftarray, redshifts_for_age_ticks, redshifts_for_freq_ticks, redshifts_for_lambda_ticks])

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

fig = plt.figure(figsize=(2, 10))
fig.subplots_adjust(bottom=0.025, top=0.88, left=0.05, right=0.95)

# left axis: z
ax1 = setup_axes(fig, 141)
ax1.set_ylim(np.log10(redshift_minplot), np.log10(redshift_maxplot))
ax1.set_yticks(np.log10(redshiftarray), labels=['{:g}'.format(z) for z in redshiftarray])

# axis 2: age
ax2 = setup_axes(fig, 142)
ax2.set_ylim(np.log10(redshift_minplot), np.log10(redshift_maxplot)) 
ax2.set_yticks(np.log10(redshifts_for_age_ticks), labels=['{:g}'.format(age) for age in ages.value])


#axis 3: wavelength in m
ax3 = setup_axes(fig, 143)
ax3.set_ylim(np.log10(redshift_minplot), np.log10(redshift_maxplot))
ax3.set_yticks(np.log10(redshifts_for_lambda_ticks), labels=['{:g}'.format(lamb) for lamb in lambda_array])

#axis 4: frequency in MHz
ax4 = setup_axes(fig, 144)
ax4.set_ylim(np.log10(redshift_minplot), np.log10(redshift_maxplot))
ax4.set_yticks(np.log10(redshifts_for_freq_ticks), labels=['{:g}'.format(nu) for nu in freq_array])

# Axes legend
label_axis1 = r"Redshift $z$"
plt.figtext(0.06, .5, label_axis1 , fontsize=9, ha='center', va='center', rotation='vertical', zorder=2)
label_axis2 = "Age [Gyr]"
plt.figtext(0.30, .5, label_axis2 , fontsize=9, ha='center', va='center', rotation='vertical', zorder=2)
label_axis3 = "Observed wavelength [m]"
plt.figtext(0.53, .5, label_axis3 , fontsize=9, ha='center', va='center', rotation='vertical', zorder=2)
label_axis4 = "Observed frequency [MHz]"
plt.figtext(0.75, .5, label_axis4 , fontsize=9, ha='center', va='center', rotation='vertical', zorder=2)

# Top and Bottom Texts
# Top text
title_us1 = "{\\bf Cosmology Ruler Bookmark}"
title_fr1 = "{\\bf Marque-page cosmologique}"

params1 = fr"$\Omega_{{m}} = {cosmo.Om0:.3f}, \Omega_{{\Lambda}} = {cosmo.Ode0:.3f} $"      
params2 = rf"$H_{{0}} = {cosmo.H0.value}, \mathrm{{km}}/\mathrm{{s}}/\mathrm{{Mpc}} $"

ref1 = "(Planck Collab., 2020, A\\&A, 641, A1) "

# legend1 = "Age and time in Gyr. Angle "
# legend2 = "(for 1 kpc proper) in arcsec."

# textzrange = "Recto: $z \\in [0.1, 1000]$ in log scale"

plt.figtext(0.5, .98, title_us1 , fontsize=9, ha='center')
plt.figtext(0.5, .965, title_fr1 , fontsize=9, ha='center')

plt.figtext(0.5, .94, params1, fontsize=9, ha='center')
plt.figtext(0.5, .925, params2, fontsize=9, ha='center')

plt.figtext(0.5, .91, ref1, fontsize=6.5, ha='center')

# plt.figtext(0.5, .925, legend1, fontsize=9, ha='center')
# plt.figtext(0.5, .915, legend2, fontsize=9, ha='center')

# plt.figtext(0.5, .895, textzrange, fontsize=9, ha='center')

# Bottom text
bottom_text = r"H. Dole \& A. Gorce"
plt.figtext(0.5, .0098, bottom_text, fontsize=7., ha='center')
bottom_text2 = "Université Paris-Saclay (2024)"
plt.figtext(0.5, .003, bottom_text2, fontsize=7., ha='center')

# dpi quality; 300 recommended
dpi = 300

# save bookmark recto
plt.savefig("CosmologyRulerBookmark_21cm_v0.pdf", dpi=dpi)









