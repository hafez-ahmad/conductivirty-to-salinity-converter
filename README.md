# conductivirty-to-salinity-converter
This code converts a given conductivity measurement (millisiemens per centimetre (mS/cm)) value to its corresponding salinity (PSU), given the temperature and water pressure.
If your conductivity was measured with a different unit, you need to update the conversion factor in line 17 of the code.
The code works for three different scenarios:
1) If you have only conductivity and temperature values and you want to use a fixed pressure value, in this case, use the function conductivity_to_salinity and update the default pressure value with your pressure value.
2) You can also use the code to convert depth to pressure by calling the function depth_to_pressure(lat) , given you have latitude input
3) If you have a CSV file with multiple lines of conductivity, temperature and latitude readings, then you can use the function conductivity_salinity_from_file(file) by passing the CSV file as input, and you will get an output CSV file with salinity_convert column holding the converted salinity values. You can use this function with fixed pressure as well. Of course, in this case, make sure you change the pressure on line 44 of the code.
