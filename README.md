# AntabGMVA

<b>"That is a very comfortable way to manage ANTAB files"</b><br>
_&ensp;- Alan Roy (MPIfR), 2024_

Principle Investigators (PIs) of Global mm-VLBI Array ([GMVA](https://www3.mpifr-bonn.mpg.de/div/vlbi/globalmm/)) observations will receive the so-called ANTAB files. The ANTAB files contain lots of metadata such as the system temperature (Tsys) that was measured/monitored by each of the GMVA antenna stations during the observations. The Tsys measurements are essential in the amplitude calibration of GMVA data to generate science-ready data products. But unfortunately, the metadata are not complete and there are almost always erroneous values in them.

AntabGMVA is a Python program that allows GMVA users to manage the GMVA ANTAB files easily.

## Why it is useful
* Convert some of the unusual ANTAB formats into the AIPS/CASA(rPICARD)-readable format
* Replace erroneous Tsys values with reasonable values by using linear interpolation
* Create the convenient All-in-One ANTAB file instead of carrying all those individual data files
* Get an overview/expectation about the individual antennas of your GMVA data (i.e., data quality)


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
A complete Manual/Tutorial pdf file is at [tutorial/AntabGMVA_tutorial.pdf](https://github.com/greendw/AntabGMVA/blob/main/tutorial/AntabGMVA_tutorial.pdf).

This program is very easy to use. Example datasets for the tutorial are at [examples/](https://github.com/greendw/AntabGMVA/tree/main/examples).




## Citation
If you use this program in your publication, please cite ASCL:TBD




## Contact Info.
About the Code
* Daewon Kim (Max-Planck-Institut für Radioastronomie; MPIfR)
* Email: dwkim@mpifr-bonn.mpg.de (or dwkimastro@gmail.com)

For GMVA metadata Query
* TBD@TBD

GMVA data are processed by the MPIfR correlator in Bonn, Germany. Then the correlation team will send the processed GMVA data (FITS-IDI) to PIs with the metadata (ANTAB, WX, etc.).




## Important notes
Any useful information will be added here.



---

Thank you for visiting.

