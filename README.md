# AntabGMVA

<b>"That is a very comfortable way to manage ANTAB files"</b><br>
 - Alan Roy (MPIfR), 2024

The so-called ANTAB files will be sent to Principle Investigators (PIs) of Global mm-VLBI Array (GMVA) observations. The ANTAB files contain lots of metadata such as the system temperature (Tsys) that was measured/monitored by each of the GMVA antenna stations during the observations. The Tsys measurements are essential in the amplitude calibration of GMVA data to generate science-ready data products. But unfortunately, the metadata are not complete and there are almost always erroneous values in them.

This Python program allows GMVA users to 

Four Advantages
* AIPS/CASA(rPICARD)-readable format
* Erroneous Tsys values
* Overview/expectation about the data
* Create the convenient All-in-One ANTAB file


## Installation
The latest version is v24.813. Install it via `pip`.
```
$ pip install antabgmva
```
If the installation was successful, `antabgmva` should be in the list:
```
$ pip list
```

Requirements
* `Python3.x`: v3.8 and v3.12 checked, but the lower versions of `Python3` should also be fine.
* `Numpy`
* `Matplotlib`
* `Scipy`

Others
* It is recommended to use the `IPython` interface (v7.x and v8.x checked).
* Not all the matplotlib backends were checked, but it works with `Qt5Agg` and `tkagg`.




## How to Use?
Manual/Tutorial



## Contact Info.

The MPIfR correlation team


## Citation




## Important notes

Careful GLT - delimeter & Day-format



---

Thank you for visiting.
