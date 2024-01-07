# Overview

This Project implements an awesome Algorithm that helps EV Charger Suppliers to understand the route between two locations, and help make installation decisions

## Input to be fed into the System

- SoC of the EV before starting the Route
- Range of the EV
- Distance between Point A and Point B
- Threshold Minimum SoC
- Number of EVs to be tested on

## Output from the System

- Number of Charging Stations
- Location Distance of the Charging Stations
- Range Anxiety at each locations

## Libraries

- Collections
- Pandas
- Matplotlib
- Numpy
- csv

## Prerequisites

- CSV with samples of EV's starting SoC (Example file already there in the repo)

## Usage Guide

- Select a route through a map
- Set all the input parameters for the route
- Run ChargingStation.py first to get first set of Outputs (Charging Station Locations, Range Anxiety and SoC at the END)
- Then, Run standard_deviation.py to validate the results from the prior.
