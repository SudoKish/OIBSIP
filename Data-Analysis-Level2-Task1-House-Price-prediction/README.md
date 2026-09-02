# House Price Prediction using Linear Regression

## Overview

This project focuses on predicting house prices using Machine Learning.
A Linear Regression model is trained using the Ames Housing dataset to
predict the sale price of residential properties based on various
property characteristics.

The project follows an end-to-end Machine Learning workflow, including
data exploration, preprocessing, feature encoding, model training,
evaluation, visualization, and model comparison.

## Objective

The main objective is to build and evaluate a Linear Regression model
that can predict house sale prices using relevant numerical and
categorical features.

## Dataset

The project uses the **House Prices: Advanced Regression Techniques**
dataset from Kaggle.

The dataset contains information about residential properties, including
features related to:

- Overall quality
- Living area
- Number of bedrooms and bathrooms
- Garage capacity
- Basement area
- Year built
- Neighborhood
- House style
- Other property characteristics

The target variable is:

- `SalePrice` — the final sale price of the house

The dataset is not included in this repository and should be placed in
the `data/` directory as `train.csv`.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Workflow

1. Load the dataset
2. Perform exploratory data analysis
3. Check missing values and duplicate records
4. Analyze the distribution of house prices
5. Select relevant features
6. Handle missing values
7. Encode categorical features using One-Hot Encoding
8. Perform correlation analysis
9. Split the dataset into training and testing sets
10. Train a Linear Regression model
11. Evaluate the model using MSE, RMSE, and R²
12. Analyze actual vs predicted prices
13. Perform residual analysis
14. Analyze model coefficients
15. Compare Linear Regression with Ridge and Lasso Regression

## Model Evaluation

The models are evaluated using:

- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

Lower MSE and RMSE indicate lower prediction error, while a higher
R² score indicates better explanatory performance.

## Visualizations

The project includes:

- Sale price distribution
- Sale price boxplot
- Correlation heatmap
- Actual vs predicted price scatter plot
- Residual plot
- Feature coefficient analysis
- Model comparison

## Project Structure

```text
Data-Analysis-Level2-Task1-House-Price-prediction/
│
├── data/
│   └── train.csv
│
├── House_Price_Prediction.ipynb
├── README.md
├── requirements.txt
└── .gitignore