"""
 This function converts a given conductivity in to its corresponding Salinity value based on the standard equation from Salinity (PSS-78) ITS-90
"""
import os
import numpy as np
import pandas as pd
from pynverse import inversefunc

def conductivity_to_salinity(conductivity, temp, pressure=0.257):
    a0, a1, a2, a3, a4, a5 = 0.0080, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081
    b0, b1, b2, b3, b4, b5 = 0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144
    A1, A2, A3 = 2.0700E-05, -6.3700E-10, 3.9890E-15
    B1, B2, B3, B4 = 3.4260E-02, 4.4640E-04, 4.2150E-01, -3.1070E-03
    c0, c1, c2, c3, c4 = 6.766097E-01, 2.005640E-02, 1.104259E-04, -6.969800E-07, 1.003100E-09
    c_ratio = 4.2914 # units in S/m

    R = (conductivity/10) / c_ratio  # The ASV measures conductivity in mS/cm and to convert to S/m divide it by 10
    Rp = 1 + (A1*pressure + A2*pressure**2 + A3*pressure**3) / (1 + B1*temp + B2*temp**2 + B3*R + B4*temp*R)
    rT = c0 + c1*temp + c2*temp**2 + c3*temp**3 + c4*temp**4
    RT = R / (rT*Rp)
    k = 0.0162
    x = 400 * RT
    y = 100 * RT
    f_t = (temp - 15) / (1 + k * (temp - 15))  # f(t)
    # Units: psu
    salinity = a0 + a1*RT**0.5 + a2*RT + a3*RT**1.5 + a4*RT**2 + a5*RT**2.5 + ((temp - 15)/(1 + k*(temp-15)))*(b0 + b1*RT**0.5 + b2*RT + b3*RT**1.5 + b4*RT**2 + b5*RT**2.5)
    # Units: psu
    extended_salinity = salinity - (a0/(1+1.5*x + x**2)) - (b0*f_t/(1+y**0.5+y+y**1.5))
    return extended_salinit

conductivity_file_path = r"D:\mss_wq_AllParams_ERDC_June_2023_union.csv"
conductivity_salinity_from_file(conductivity_file_path)