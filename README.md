# Cloud Workload Forecasting & Analysis

## Project Overview

This project analyses historical cloud virtual machine (VM) CPU utilization and forecasts future workload behaviour using time-series forecasting techniques.

The goal is to estimate:
- The number of active virtual machines.
- Aggregate CPU utilization.

## Dataset

The project uses a curated subset of Azure Public Dataset V2.

- 10,000 virtual machines.
- 134 observations per VM.
- 5-minute observation intervals.
- 1,340,000 VM-level CPU records.

## Methodology
The project follows these steps:
1. Data loading and quality checks.
2. Aggregation of VM-level CPU readings by timestamp.
3. Exploratory data analysis.
4. Chronological development and holdout split.
5. Time-aware validation and baseline comparison.
6. Forecast generation and evaluation.

The first 110 timestamps are used for development, while the final 24 timestamps form the forecast horizon.
The holdout observations are excluded from model fitting and model selection.

## Forecasting Methods

The following methods were compared:

- Persistence forecasting.
- 30-minute moving average.
- Simple Exponential Smoothing.

Simple Exponential Smoothing achieved the lowest validation MAE and RMSE and was therefore selected for the final aggregate CPU utilization forecast.


## Project Structure

cloud-workload-forecasting/
├── challenge_data/
├── notebooks/
│   └── 01_data_understanding.ipynb
├── src/
│   └── forecast.py
├── predictions.csv
├── final_report.md
└── final_report.pdf
├── requirements.txt
├── .gitignore
├── README.md
