# HGCAL ECON Testing local DB
Scripts to create, parse and plot the local DB informations from Fermilab Robot testing for ECON. 

# Setting up the environment
To setup the database on ```cmsnghcal01``` use the following command
```
sudo mongod -dbpath <PATH/TO/DB/FOLDER>
```
currently I have an example database setup at ```acampbell/DATABASE``` on ```cmsnghcal01```

# Creating and uploading files to the database
to create and upload a database on ```cmsnghcal01``` run the file ```create_db.py```.

The file takes the following arguments: 

```--path``` this is the path to the JSON files you want to upload

```--dbname``` the name of the database you want to create

```--dbaddress``` this is the address of the database the default is ```27017``` and this value will be important later when setting up your own local ssh tunnel

Then the json files will be split into various tables and uploaded into the database as defined here https://github.com/dnoonan08/econ_json_parsing/blob/acampbel-updates/DB_scripts/json_uploader.py#L42-L435

# Querying the database
if you would like to query the database from your own local machine use the following ssh commmand

```ssh -f -N -L 27017:localhost:27017 chiptest```

note: ```27017``` is the address of the database on ```cmsnghcal01``` if you provide a different value when creating the database please make sure that it matches the command 

Then to request specific data from the database, please use the database class https://github.com/dnoonan08/econ_json_parsing/blob/acampbel-updates/DB_scripts/dbClass.py

The database class needs to be intialized with the ```dbaddress```
The database class has predefined functions to request information. The class has the following functions:

- pllCapbankWidthPlot:
  - This function requests the pll capbank width information. The function takes the following arguments:
    - ```lowerLim``` and ```upperLim``` these are set to ```None``` by default but if you provide arguments for these, the function will return the pll capbank width for chips only in that specified number range
    - ```voltage```: this expects a string ```'1p08'```, ```'1p2'```, or ```'1p32'``` to request information for 1.08, 1.2, or 1.32 volts respectively
    - ```econType```: this expects a string ```'ECONT'``` or ```'ECOND'``` to request information for ECONT or ECOND, respectively
  - Note that the argument descriptions will be the same for the following functions
- prbsMaxWidthPlot:
  - This function will request the information for prbs max width and takes the same arguments as above
- etxMaxWidthPlot:
  - This function will request the information for etx delay scan max width and takes the same arguments as above
- getVoltageAndCurrent:
  - This function will request the information for the voltage and current and takes the same arguments as above
- getBISTInfo:
  - This function will request the information for the bist test result and first failing voltage and takes the same arguments as above
- phaseScan2DPlot
  - This function request the Phase scan errors to make the 2D scan of the phase setting vs channel plot
    - The function takes similar arguments as above except ```lowerLim``` and ```upperLim``` are replaced with ```chipNum``` since these plots are for individual chips
- delayScan2DPlot
  - This function request the delay scan bitcounts and error counts to make the 2D plots and has the same arguments as above
- getFractionOfTestsPassed
  - This function gets the fractions of test passing for each chip and it takes ```econType``` as an argument to differentiate between ECOND and ECONT
- getTestingSummaries
  - This function creates a dataframe of testing summaries to be used in making summary plots and takes ```econType``` as an argument to differentiate between ECOND and ECONT

New funtions will be added as the needs of testing progress

# Plotting
Plotting scripts for each function of the database class have been created. 

Most of the plotting scripts take the following arguments:
- ```dbaddress``` the address of the database you are connecting to
- ```odir``` the output directory for the plots

The plot scripts for the 2D phase and delay scan errors take the additional arguments:
- ```chipNum``` the chip number you want to make the plot of
- ```voltage``` the voltage at which you want the plot created, expects a string ```'1p08'```, ```'1p2'```, or ```'1p32'```
- ```econType``` expects a string ```'ECOND'``` or ```'ECONT'```

The following plot scripts are currently available with example plots created using the scripts:
- bistThreshold1DHist.py:
  - uses the function ```getBISTInfo``` from the database class to request the first failing voltage and create a 1D histogram of the bist threshold using Ramneet's plot
  - ![Bist_Threshold_ECON-D](https://github.com/user-attachments/assets/9100444e-48af-4aca-ae11-b3cdde7f3342)
- currentDraw1DHist.py:
  - uses the function ```getVoltageAndCurrent``` from the database class to request the voltage and current distribution from ECOND and ECONT and plots the distribution using Ramneet's code
  - ![Power_ECON-D](https://github.com/user-attachments/assets/8433a2a4-bf17-48af-b368-c31dcfe36695)
- erxPhaseWidth1DHist.py:
  - uses the function ```prbsMaxWidthPlot``` from the database class to request the prbs max width distribution to create the 1D distribtuion from Ramneet's plots
  - Creates plots for each voltage and for ECOND and ECONT
  - ![Phase_width__of_all_eRx_ECON-D  1 2](https://github.com/user-attachments/assets/2d8fa4f8-bc76-422f-a504-9f4802ed7cf2)
- erxPhaseWidth2DHist.py:
  - uses the function ```prbsMaxWidthPlot``` from the database class to request the prbs max width distribution to create the 2D distribtuion from Yulun's plots
  - ![eRxPhaseScan2D_ECOND](https://github.com/user-attachments/assets/5dc66c2b-2ca3-4290-9d07-b1986c97780d)
- etxDelayWidth1DHist.py
  - uses the function ```etxMaxWidthPlot``` from the database class to request the delay max width distribution to create the 1D distribtuion from Ramneet's plots
  - cretes a plot for each voltage and for ECOND and ECONT
  - ![Phase_width__of_all_eRx_ECON-D  1 2](https://github.com/user-attachments/assets/fd8fbacb-6c68-4462-9319-41652c122c15)
- etxDelayWidth2DHist.py
  - uses the function ```etxMaxWidthPlot``` from the database class to request the delay max width distribution to create the 2D distribtuion from Yulun's plots
  - ![eRxPhaseScan2D_ECOND](https://github.com/user-attachments/assets/4a421e9f-fee4-44f8-8b48-60cda8ff5199)
- pllCapbankWidth1DHist.py:
  - uses the function ```pllCapbankWidthPlot``` from the database class to create a 1D distribution of the PLL capbank width plot for ECOND and ECONT at each voltage from Ramneet's plots
  - ![ECON-D_Capbank_Width  1 2](https://github.com/user-attachments/assets/b35fe92f-2d2e-4db1-8193-58bb51b7c3de)
- pllCapbankWidth2DHist.py:
  - uses the function ```pllCapbankWidthPlot``` from the database class to create a 2D distribution of the PLL capbank width plot for ECOND and ECONT from Yulun's plots
  - ![pllCapbankWidth2DHist_ECOND](https://github.com/user-attachments/assets/554bbf11-96da-4f1a-959a-b90e01a47edc)
- summaryPlots.py:
  - uses the functions ```getFractionOfTestsPassed``` and ```getTestingSummaries``` from the database class to create summary plots from Marko's plots for ECOND and ECONT
  - ![summary_ECOND](https://github.com/user-attachments/assets/2d67cfd0-17ef-4a31-b72a-e35fb4b93a0b)
  - ![summary_tests_failed_ECOND](https://github.com/user-attachments/assets/d5cbc9d4-3f71-4361-b305-e54ba1597415)
- DelayScanTransmissionErrors2Dhist.py:
  - uses the function ```delayScan2DPlot``` to get the bitcount and errcount to make a 2D plot of the delay scan transmission errors
  - ![ECOND_chip_101_delayScan_1p2](https://github.com/user-attachments/assets/a3522e3d-8c3d-430f-bba4-e60309e5dd5a)
- PhaseScanTransmissionErrors2Dhist.py
  - uses the function ```phaseScan2DPlot``` to get the errcount to make a 2D plot of the phase scan transmission errors
  - ![chip_101_phaseScanErrors_ECOND_1p2](https://github.com/user-attachments/assets/ecf33994-6116-4dc6-9bd3-52f4ad472ca9)

Finally, there is the ```run_all.sh``` script which will run all the plotting scripts that will be continuously updated throughout testing (all scripts minus the 2D delay/phase scan error plots as these need to be done manually for specific chips)







  









