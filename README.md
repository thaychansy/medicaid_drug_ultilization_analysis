# Medicaid Drug Utilization Analysis

![Medicaid Logo](https://www.medicaid.gov/themes/custom/medicaid/images/logo/medicaid_logo_green.svg)

## Overview
This repository provides an in-depth analysis of a drug utilization dataset, including data exploration, visualization, and statistical insights. The analysis includes various types of plots, outlier detection, and trends in drug reimbursement by different utilization types. The project is structured in a way that can be easily followed to replicate or extend the analysis.

More information about the data set and an explanation of the data field descriptions can be found [here](https://www.medicaid.gov/medicaid/prescription-drugs/medicaid-drug-rebate-program/index.html).

## Project Structure
- **medicaid_drug_utilization_analysis.ipynb**: Jupyter Notebook containing all analysis code and visualizations.
- **data/processed_drug_utilization_data.csv**: Processed dataset with missing values handled and numerical columns filled.
- **images/**: Directory containing exported images of charts and visualizations.

## Key Analysis
1. **Basic Data Exploration**: Inspecting data types, basic statistics, and missing values.
2. **Data Cleaning**: Handling missing values by filling numerical columns with zeros.
3. **Top Utilized Drugs**: Bar chart displaying the top 10 drugs by units reimbursed.
4. **Total Reimbursement Trends**: Line plot showing the total amount reimbursed by year and quarter.
5. **Medicaid vs. Non-Medicaid Reimbursement**: Comparison bar chart of total Medicaid and non-Medicaid reimbursement.
6. **Correlation Analysis**: Scatter plot showcasing the correlation between the number of prescriptions and total amount reimbursed.
7. **Outlier Detection**: Combined boxplots and histograms for numerical columns to visualize outliers and data distribution.
8. **Utilization Type Analysis**: Bar charts showing total units and total amount reimbursed by utilization type (e.g., FFSU, MCOU).

## Visualizations
Key visualizations include:
- **Boxplots and Histograms**: For detecting outliers and understanding data distribution.
  
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/fe56b255-e6c3-45c4-a3c5-d41088c7cbd3">
  
- **Bar Charts**: Highlighting top drugs by units reimbursed and comparing utilization types.
  
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/e480a8b5-f546-4fb3-80b1-11e3d3311f60">
  

  <img width="800" alt="image" src="https://github.com/user-attachments/assets/9d4840f6-c82c-4eb4-badf-489ed03279eb">

- **Line Plot**: Showing reimbursement trends over time.
  
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/2b25ec4d-97b8-4b06-b0ca-c529d7ad4c42">

- **Scatter Plot**: Correlation analysis between prescriptions and reimbursement.
  
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/a3376c99-5236-4468-8bed-b26413fb3673">


## Getting Started

### Prerequisites
- Python 3.x
- Jupyter Notebook or an equivalent IDE
- Required libraries:
  ```bash
  pip install pandas numpy matplotlib seaborn
  ```

### Running the Analysis
1. Clone this repository:
   ```bash
   git clone https://github.com/thaychansy/medicaid-drug-utilization-analysis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd medicaid-drug-utilization-analysis
   ```
3. Open the Jupyter Notebook:
   ```bash
   jupyter notebook drug_utilization_analysis.ipynb
   ```
4. Run each cell sequentially to reproduce the analysis.

## Dataset
The dataset used in this analysis was taken from the [Medicaid Drug Rebate Program (MDRP) website](https://data.medicaid.gov/dataset/61729e5a-7aa8-448c-8903-ba3e0cd0ea3c/data?conditions[0][resource]=t&conditions[0][property]=state&conditions[0][value]=CA&conditions[0][operator]=%3D). Ensure that the `drug_utilization_dataset.csv` file is placed in the data directory. The dataset should include columns such as:
- `Units Reimbursed`
- `Number of Prescriptions`
- `Total Amount Reimbursed`
- `Medicaid Amount Reimbursed`
- `Non Medicaid Amount Reimbursed`
- `Utilization Type`

## Results and Insights
- **FFSU Dominance**: The analysis revealed that Fee-for-Service Utilization (FFSU) has significantly higher units reimbursed and total reimbursement amounts compared to Managed Care Organization Utilization (MCOU).
- **Outlier Analysis**: Outliers were detected in key numerical columns, helping identify potential data points for deeper investigation.
- **Reimbursement Trends**: Clear trends were observed in reimbursement amounts over different quarters, aiding in understanding temporal patterns.

## Future Work
- **Deeper Analysis by Drug Category**: Identify specific drugs contributing to high reimbursements.
- **Time Series Forecasting**: Extend the analysis to predict future trends.
- **Policy Impact Studies**: Analyze how changes in healthcare policy might affect drug utilization and reimbursement.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements or additional features.

## License
This project is licensed under the MIT License.

## Contact
For any questions or collaboration inquiries, please reach out to [thay.chansy@gmail.com](mailto:thay.chansy@gmail.com).

---

Enjoy exploring drug utilization data and uncovering valuable insights!
