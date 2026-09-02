# Task 3 - Data Cleaning

## Retail Store Sales Dataset

This project demonstrates professional data cleaning techniques using Python, Pandas, NumPy, and Jupyter Notebook.

The objective was to transform a deliberately messy retail sales dataset into a clean, consistent, and analysis-ready dataset while documenting each cleaning decision.

## Technologies Used

- Python
- Pandas
- NumPy
- Jupyter Notebook

## Dataset

The dataset contains retail store transaction records with information about:

- Transaction ID
- Customer ID
- Category
- Item
- Price Per Unit
- Quantity
- Total Spent
- Payment Method
- Location
- Transaction Date
- Discount Applied

## Data Cleaning Process

### 1. Data Quality Assessment

The original dataset contained:

- 12,575 rows
- 11 columns
- 7,229 missing values
- 0 duplicate rows
- Incorrect data types in several columns

### 2. Missing Data Handling

Different strategies were applied based on the characteristics of each column:

- `Item` → Missing values replaced with `"Unknown"`
- `Price Per Unit` → Median imputation
- `Quantity` → Median imputation
- `Total Spent` → Recalculated using `Price Per Unit × Quantity`
- `Discount Applied` → Mode imputation

### 3. Duplicate Removal

Duplicate rows were checked and none were found.

- Duplicate rows before cleaning: 0
- Duplicate rows removed: 0

### 4. Standardisation

Text fields were checked for inconsistent formatting and leading/trailing whitespace.

The categorical values were already consistent, so no unnecessary category mappings were applied.

### 5. Data Type Correction

The following corrections were performed:

- `Transaction ID` → String
- `Customer ID` → String
- `Transaction Date` → Datetime
- `Quantity` → Integer
- `Discount Applied` → Boolean
- Monetary columns → Float

### 6. Outlier Detection

The IQR method was used to detect numerical outliers.

Results:

| Column | Outliers |
|---|---:|
| Price Per Unit | 0 |
| Quantity | 0 |
| Total Spent | 60 |

The 60 `Total Spent` outliers all had a value of 410.

These values were retained because they represent valid transactions:

`41 × 10 = 410`

Therefore, the observations were not removed or capped.

## Before vs After

| Metric | Before Cleaning | After Cleaning |
|---|---:|---:|
| Rows | 12,575 | 12,575 |
| Missing Values | 7,229 | 0 |
| Duplicate Rows | 0 | 0 |
| Correct Data Types | 8/11 | 11/11 |

## Output

The cleaned dataset is saved as:

```text
data/cleaned_dataset.csv