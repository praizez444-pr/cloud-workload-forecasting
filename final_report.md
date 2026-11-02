# Cloud Workload Forecasting and Analysis

## 1. 
Summary

This project studies cloud machine CPU usage by using a selected part of the Azure Public Dataset V2.

The goal is to learn about usage and predict the number of active virtual machines and overall CPU usage for the next two hours.

The data has 1,340,000 CPU readings from 10,000 machines at 134 different times. These times are five minutes apart.

Three ways to predict were tested: using the value a 30-minute average and a simple exponential smoothing method.

The final version uses the value for active VM count and the 30-minute average for overall CPU usage.

## 2. Dataset Understanding and Preparation

### 2.1 Dataset Description

The project uses two source files:

- vm_cpu_readings.csv.gz: CPU usage data for each machine.

- vm_metadata.csv.gz: Information about each virtual machine.

The CPU data has 1,340,000 rows and five columns. The metadata data has 10,000 rows and eleven columns.

Each virtual machine has 134 CPU readings with timestamp that is 300 seconds (5 minutes) apart.

### 2.2 Data Quality Checks

The following checks were done:

- Checked for missing values.

- Checked for duplicated records.

- Made sure the number of unique times was correct.

- Checked that the time difference was five minutes.

- Checked for duplicate virtual machine and time combinations.

- Compared the machine IDs in both datasets.

No missing data or duplicates were found. All 10,000 virtual machine IDs in the CPU dataset matched the metadata records.

### 2.3 Construction of the Target Variable 

The data was grouped by time to create two target variables:

**Active VM Count:** The number of distinct virtual machines with a CPU reading at each timestamp.

**Aggregate CPU Utilization:** The average of CPU readings for all machines at each timestamp.

The final data has 134 observations.

The active VM count remained constant at 10,000 during the time period.

## 3. Exploratory Data Analysis

### 3.1 Aggregate CPU Utilization

The development period had 110 observations.

Statistics for CPU usage were:

| Statistic | Value |
|---|---:|
| Mean | 9.4141% |
Standard deviation | 0.1936 |
| Minimum | 9.1116% |
| Median | 9.3781% |
| Maximum | 9.9122%

The CPU usage was mostly around 9.4%.

There was an increase around timestamp 16,500 to 21,000 seconds then it declined.

No clear repeating pattern was found in the available data.

### 3.2 VM-Level Utilization and High-Load Analysis

Even though overall CPU utilization was low,  individual VMs readings showed a wider distribution.

In the dataset the highest average CPU usage for a single VM was about 99.95%.

In the development period:

- On average, 127 VMs recorded CPU utilization above 80%.

- On average 88 VMs recorded CPU utilization above 90%.

- On average 57 VMs recorded CPU utilization above 95%.

The most VMs above 80% was 146 at timestamp 17,400 seconds.

This shows that low overall CPU usage does not mean all VMs have sufficient headroom.

## 4. Forecasting Methodology

### 4.1 Chronological Data Split

The 134 aggregate observations were split into:

- Development period: 110 observations.

- Holdout period: final 24 observations.

The holdout period is two hours because each observation is five minutes apart.

### 4.2 Forecasting Approaches

Three methods were compared.

**Persistence Forecasting**

This method uses the observed value as the forecast for future predictions.

It was used for active VM count since the count stayed at 10,000.

**30-Minute Moving Average**

This method calculates the mean of the six recent observations and uses it to predict CPU utilization for the next 24 steps.

**Simple Exponential Smoothing**

This method assigns greater weight to recent data while keeping information from earlier data.

### 4.3 Time-Aware Validation

Three expanding window tests were done:

- First window: 80 historical observations, followed by 10 validation observations.

- Second window: 90 historical observations, followed by 10 validation observations.

- Third window: 100 historical observations, followed by 10 validation observations.

The evaluation metrics used were Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE). Lower values indicates better forecast accuracy.

### 4.4 Validation Results

The results from 30 validation observations were:

| Forecasting Method | MAE | RMSE |
|---|---:|---:|
| Persistence | 0.095084 0.116737 |
| 30-Minute Moving Average | 0.081640 | 0.099295 |
| Simple Exponential Smoothing | 0.075040 | 0.094381 |

Simple Exponential Smoothing had the lowest validation errors.

Compared to persistence SES had 21.1% lower MAE and 19.2% lower RMSE.

The moving average also did better than persistence with 14.1% lower MAE and 15.0% lower RMSE.

### 4.5 Holdout Forecast Evaluation

The final implementation used persistence for VM count and the 30-minute moving average for aggregate CPU utilization.

The moving average forecast produced:

| Metric | Result |
|---|---:|
| CPU MAE | 0.133565 |
| CPU RMSE | 0.171289 |
| CPU NRMSE | 1.85% |
| Active VM Count MAE 0 |
Active VM Count RMSE | 0 |

The actual mean aggregate CPU utilization during the holdout period was approximately 9.2690% while the forecast average was about 9.1909%.

The positive error of about 0.0781 percentage points shows the moving average slightly underestimated the aggregate CPU utilization.

Even though SES did best during validation, the moving average had lower errors in the holdout comparison:

- Moving Average MAE: 0.133565; RMSE: 0.171289.

- SES MAE: 0.145371; RMSE: 0.183428.

**Evaluation limitation:** Both methods were compared after their forecasts were made.

## 5. Operational Analysis and Recommendations

### 5.1 Capacity and Headroom

The overall CPU utilization was low, averaging about 9.4% during the development period.

However, VM-level analysis showed that some machines redorded utilizaton above 90% and 95%

Recommended operational actions are:

1. Watch CPU utilization at each individual VM level.

2. Set up alerts for sustained high CPU utilization.

3. Look into machines taht repeatedly records utilization above 80%.

4. Check workload distribution and find issues with resources.

5. Maintain appropriate capacity headroom based on individual VM behaviour and service requirements.

A fixed capacity reduction is not recommended from aggregate CPU averages alone.

### 5.2 Forecasting Improvements

Possible future improvements include:

- Use longer data to check for daily or weekly patterns.

- Forcasting individual VM workloads or workload groups.

## 6. Limitations

The analysis has some issues:

- The development period is nine hours, which is not enough to see longer patterns.

- The moving average produces a constant forecast across the 24-steps.

- Aggregate CPU utilization can hide high utilization on individual virtual machines.

- The dataset is a selected part and may not show all behaviors in a real cloud.

- The post-hoc holdout comparison is not an independent final model-selection assessment.

## 7. Conclusion

This project shows a way to study cloud workloads and predict them for a short-term.

The final implementaion uses persistence for VM count and the 30-minute moving average for aggregate CPU utilization.

The analysis also highlights an important finding: relatively low aggregate CPU utilization can coexist with high utilization on individual virtual machines.

So cloud planning should combine both the predictions and the VM-level monitoring so that sufficient resourde headroom will be appropriated

## 8. Reproducibility

Install the dependencies:

pip install -r requirements.txt

Run the forecasting code from the project root:

python src/forecast.py

This scripts generates predictions.csv with 24 forecasted observations, including:

- timestamp

- active_vm_count

- aggregate_cpu_utilization

