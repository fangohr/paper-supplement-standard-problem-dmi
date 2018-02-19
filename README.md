# paper-supplement-standard-problem-dmi

Electronic and additional information for manuscript on micromagnetic standard
problem DMI

This repository contains scripts and notebooks to reproduce the four standard
problems specified in the paper. The majority of the problems are specified
with a material based on Permalloy (Py):

    D     :: 3     mJ m^-2  
    A     :: 13    pJ m^-1  
    Ms    :: 0.86  MA m^-1  
    Ku    :: 0.4   MJ m^-3   

## One-dimensional problem

A 100 nm  x 5 nm x 5 nm wire made of a Py-like material

![](notebooks/mayavi/one-dim.png)

## Two-dimensional problem

A 100 nm wide and 2 nm thick disk made of a Py-like material

![](notebooks/mayavi/system_2d.png)

## Three-dimensional problem

A 180 nm wide and 20 nm thick FeGe cylinder under an applied field `B`

![](notebooks/mayavi/system_3d_cylinder.png)

Material parameters are

    D     :: 1.58   mJ m^-2  
    A     :: 8.78   pJ m^-1  
    Ms    :: 0.384  MA m^-1
    B     :: 0.4    T

## Dynamics problem

Calculation of the spin wave-spectrum of a Py-like thin film with
Dzyaloshinkii-Moriya interactions.

![](notebooks/mayavi/sws/sws.png)
