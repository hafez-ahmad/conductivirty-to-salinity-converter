"""
 This function converts a given conductivity in to its corresponding Salinity value based on the standard equation from Salinity (PSS-78) ITS-90
"""
import os
import numpy as np
import pandas as pd
from pynverse import inversefunc

def conductivity_to_salinity(conductivity, temp, pressure=0.257):
    """
    Convert electrical conductivity to salinity using the practical salinity scale (PSS-78).

    Parameters:
        conductivity (float): Electrical conductivity measured in milliSiemens per centimeter (mS/cm).
        temp (float): Water temperature in degrees Celsius.
        pressure (float): Water pressure in decibars. Default is 0.257 decibars.

    Returns:
        float: Salinity value in practical salinity units (PSU).
    """

    # Constants for the salinity conversion equation
    a0, a1, a2, a3, a4, a5 = 0.0080, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081
    b0, b1, b2, b3, b4, b5 = 0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144
    A1, A2, A3 = 2.0700E-05, -6.3700E-10, 3.9890E-15
    B1, B2, B3, B4 = 3.4260E-02, 4.4640E-04, 4.2150E-01, -3.1070E-03
    c0, c1, c2, c3, c4 = 6.766097E-01, 2.005640E-02, 1.104259E-04, -6.969800E-07, 1.003100E-09
    c_ratio = 4.2914  # Conversion ratio from mS/cm to S/m

    # Calculate the electrical conductivity ratio
    R = (conductivity / 10) / c_ratio  # Convert mS/cm to S/m

    # Calculate the pressure compensation factor (Rp)
    Rp = 1 + (A1 * pressure + A2 * pressure**2 + A3 * pressure**3) / (
            1 + B1 * temp + B2 * temp**2 + B3 * R + B4 * temp * R)

    # Calculate the temperature compensation factor (rT)
    rT = c0 + c1 * temp + c2 * temp**2 + c3 * temp**3 + c4 * temp**4

    # Calculate the RT ratio
    RT = R / (rT * Rp)

    # Constants and factors for additional corrections
    k = 0.0162
    x = 400 * RT
    y = 100 * RT
    f_t = (temp - 15) / (1 + k * (temp - 15))  # f(t)

    # Calculate the salinity using the PSS-78 equation
    salinity = a0 + a1 * RT**0.5 + a2 * RT + a3 * RT**1.5 + a4 * RT**2 + a5 * RT**2.5 + (
            (temp - 15) / (1 + k * (temp - 15))) * (
                       b0 + b1 * RT**0.5 + b2 * RT + b3 * RT**1.5 + b4 * RT**2 + b5 * RT**2.5)

    # Apply additional corrections to the salinity value
    extended_salinity = salinity - (a0 / (1 + 1.5 * x + x**2)) - (b0 * f_t / (1 + y**0.5 + y + y**1.5))

    return extended_salinity

def depth_to_pressure(lat):
    depth = 0.254
    g = 9.780318 * (1 + 0.0052788 * (np.sin(lat)) ** 2 + 0.0000236 * (np.sin(lat)) ** 3)
    depth_func = (lambda x: (9.72659 * x - 0.000022512 * x ** 2 + 0.0000000002279 * x ** 3 - 0.00000000000000182 * x ** 4) / (g + 0.5 * 0.000002184 * x))
    invDepth = inversefunc(depth_func)
    pressure = invDepth(depth)
    return  pressure

def conductivity_salinity_from_file(file):
    df = pd.read_csv(file)
    path = os.path.dirname(file)
    out_file_name = os.path.basename(file)[0:-4] + '_salinity_converted.csv'
    out_file_path = os.path.join(path, out_file_name)
    df['salinity_convert'] = df.apply(lambda x: conductivity_to_salinity(x['conductivity'], x['temperature'], depth_to_pressure(x['latitude'])), axis=1)
    df.to_csv(out_file_path)
    print("Conductivity successfully converted to salinity and file saved to: ", out_file_path)

# C = 43 # conductivity in ms/cm
# T = 33 # Temperature in degree celicius
# L = 30.134 #Latitude
# P = depth_to_pressure(L) # Pressure in dBar 0.257 is the default pressure calculated for the ASV depth of 0.254 m
# print("The converted pressure is: ", P)
# salinity_convert = conductivity_to_salinity(C, T, P)
# print(salinity_convert)

conductivity_file_path = r'C:\MSU\GRA\RATasks\conductivity_salinity_converter\mss_geo_temperature_salinity_ERDC_June_2023_union_ed.csv'
conductivity_salinity_from_file(conductivity_file_path)
