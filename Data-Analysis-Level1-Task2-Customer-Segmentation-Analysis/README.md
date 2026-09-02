# Customer Segmentation Analysis

## Project Overview

This project performs customer segmentation for an e-commerce business using RFM (Recency, Frequency, Monetary) analysis and K-Means clustering.

The objective is to identify distinct customer groups based on purchasing behaviour and develop targeted marketing strategies for each segment.

## Dataset

The project uses the **Online Retail II dataset** from the UCI Machine Learning Repository.

The dataset contains transaction-level information including:

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

The original dataset is not included in this repository because of its large file size.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## Project Workflow

1. Load and inspect the transaction dataset.
2. Handle missing values and inconsistent records.
3. Remove duplicate transactions.
4. Remove cancelled transactions and invalid quantities/prices.
5. Calculate transaction-level purchase value.
6. Perform descriptive statistical analysis.
7. Create customer-level RFM features.
8. Apply log transformation to reduce the effect of extreme values.
9. Standardize RFM features using `StandardScaler`.
10. Determine the optimal number of clusters using the Elbow Method.
11. Apply K-Means clustering.
12. Visualize customer clusters.
13. Profile each customer segment.
14. Develop targeted marketing recommendations.

## Data Cleaning

The original dataset contained **1,067,371 transactions**.

The following data-quality issues were addressed:

- Missing Customer IDs
- Missing descriptions
- Duplicate transactions
- Cancelled invoices
- Negative quantities
- Non-positive prices

After cleaning, **779,425 valid transactions** remained.

## RFM Analysis

RFM analysis was used to represent customer purchasing behaviour.

### Recency

Number of days since the customer's most recent purchase.

### Frequency

Number of unique invoices/orders made by the customer.

### Monetary

Total amount spent by the customer, calculated using:

`Quantity × Price`

The analysis resulted in **5,878 unique customers**.

## Clustering

The RFM features were log-transformed and standardized using `StandardScaler`.

The Elbow Method was used to evaluate different values of K. Based on the observed reduction in inertia, **K = 4** was selected for the final K-Means model.

## Customer Segments

| Segment | Recency | Frequency | Monetary | Customers |
|---|---:|---:|---:|---:|
| Lost / Low-Value Customers | 394.95 | 1.38 | 317.08 | 1,973 |
| Recent Customers | 28.30 | 3.05 | 857.49 | 1,250 |
| Champions | 27.71 | 19.28 | 10,731.16 | 1,196 |
| At-Risk Customers | 230.07 | 5.06 | 1,948.50 | 1,459 |

## Marketing Recommendations

### Champions

Highly engaged and high-value customers.

**Recommended actions:**

- VIP loyalty programs
- Exclusive offers
- Early access to new products
- Personalized recommendations
- Referral rewards

### Recent Customers

Customers who have purchased recently but have moderate purchase frequency.

**Recommended actions:**

- Cross-selling
- Personalized recommendations
- Loyalty incentives
- Product bundles
- Encouraging repeat purchases

### At-Risk Customers

Customers with meaningful historical purchasing behaviour but high recency values.

**Recommended actions:**

- Win-back campaigns
- Personalized discounts
- Re-engagement emails
- Limited-time offers
- Recommendations based on previous purchases

### Lost / Low-Value Customers

Customers with low purchase frequency, low monetary value, and long periods since their last purchase.

**Recommended actions:**

- Low-cost promotional campaigns
- Seasonal offers
- Selective re-engagement
- Avoid high-cost retention campaigns

## Key Business Insights

- Champions represent the most valuable customer segment based on frequency and monetary value.
- At-Risk customers represent an important opportunity for customer reactivation.
- Lost / Low-Value customers form the largest customer segment.
- Recent Customers have potential to develop into higher-value repeat customers.
- Customer segmentation enables the business to apply different marketing strategies instead of using a single approach for the entire customer base.

## Project Files

```text
Customer_Segmentation_RFM.ipynb
requirements.txt
README.md
.gitignore

