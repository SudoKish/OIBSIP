# Retail Sales EDA

## Project Overview

This project performs an Exploratory Data Analysis (EDA) on a retail sales dataset to identify sales trends, customer behaviour patterns, product category performance, and actionable business insights.

The analysis covers transaction data, customer demographics, product categories, pricing, quantity purchased, and total transaction value.

## Objective

The main objective is to analyze retail sales data and uncover patterns that can support data-driven business decisions.

## Dataset

The dataset contains 1,000 retail transactions with the following attributes:

* Transaction ID
* Date
* Customer ID
* Gender
* Age
* Product Category
* Quantity
* Price per Unit
* Total Amount

The dataset does not contain individual product names, so product-level analysis is performed at the product-category level.

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

## Analysis Performed

### 1. Data Inspection

* Dataset dimensions
* Column data types
* Missing-value analysis
* Duplicate-record analysis

### 2. Descriptive Statistics

Calculated:

* Mean
* Median
* Mode
* Standard deviation

for the numerical variables.

### 3. Time Series Analysis

Analyzed:

* Monthly sales trends
* Quarterly sales trends

### 4. Customer Demographics

Analyzed:

* Customer age groups
* Gender distribution
* Average transaction value by age group

### 5. Product Analysis

Analyzed:

* Quantity sold by product category
* Revenue by product category

### 6. Correlation Analysis

A correlation heatmap was used to examine relationships between:

* Age
* Quantity
* Price per Unit
* Total Amount

## Key Findings

* Total revenue across the dataset was **456,000**.
* Average transaction value was **456**.
* Electronics generated the highest category revenue at **156,905**.
* Clothing recorded the highest quantity sold with **894 units**.
* May 2023 was the highest-sales month with **53,150** in revenue.
* Q4 2023 was the strongest quarter with **126,190** in revenue.
* Price per Unit and Total Amount showed a strong positive correlation of **0.85**.
* Quantity and Total Amount showed a moderate positive correlation of **0.37**.
* The Under 18 customer group recorded the highest average transaction value at approximately **534.05**.

## Business Recommendations

1. Strengthen inventory and marketing strategies for the Electronics category because it generated the highest revenue.
2. Increase the average transaction value of Clothing through bundles, complementary products, and premium offerings.
3. Use pricing analysis to identify opportunities for higher-value products and bundles.
4. Plan inventory and promotional activities around historically stronger sales periods.
5. Use customer segmentation to develop more targeted marketing strategies.

## Project Structure

```text
Data-Analysis-Task1-Retail-Sales-EDA/
│
├── Retail_Sales_EDA.ipynb
├── retail_sales.csv
├── README.md
└── .gitignore
```

## Conclusion

The EDA demonstrates that retail performance is influenced by multiple factors, including product pricing, quantity purchased, product category, and seasonal sales patterns. Combining these insights can help businesses improve inventory planning, pricing decisions, marketing strategies, and customer targeting.
