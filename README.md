# 🏥 Hospital Readmission & Cost Leakage Analysis

An end-to-end Data Analytics project that analyzes real hospital encounter data using **Python, SQL, Excel, and Power BI**. The project identifies which patient segments, diagnoses, and admission types drive avoidable 30-day readmissions, calculates the cost exposure tied to those readmissions, and builds an interactive Power BI dashboard to help hospital operations and finance teams prioritize interventions.

---

## 🎯 Business Problem

A hospital wants to know which patient segments, diagnoses, and admission types drive avoidable 30-day readmissions, and how much cost exposure that represents, so operations and finance can prioritize where to intervene. The hospital knew readmissions were a problem but had no clear view of:

- What the actual 30-day readmission rate is, and where it's concentrated
- Which diagnoses, age groups, and admission types carry the highest risk
- Whether high-utilizer patients (frequent prior ER/inpatient visits) are a distinct, higher-risk segment
- How much dollar exposure is tied to these readmissions

This project answers all four questions by moving from raw data to cleaning and feature engineering, then SQL business queries, exploratory analysis, a cost model, and finally an interactive dashboard.

---

## 📌 Project Objectives

- Clean and organize raw patient encounter data.
- Engineer readmission, utilization, and cost features.
- Analyze readmission patterns using SQL queries.
- Perform exploratory data analysis (EDA) using Python.
- Build a cost-leakage model in Excel.
- Build an interactive Power BI dashboard.
- Extract meaningful business insights to support decision-making.

This is a **diagnostic analysis project. No machine learning or predictive modeling** is used.

---

## 🛠️ Tech Stack

- **Python**
  - Pandas
  - Matplotlib
  - Seaborn

- **Database**
  - MySQL

- **Spreadsheet**
  - Excel (formulas, cost modeling)

- **Visualization**
  - Power BI

---

## 📂 Project Structure

```
hospital_readmission_project/
│
├── data/
│   ├── raw/
│   │   └── diabetic_data.csv
│   └── clean/
│       └── diabetic_data_clean.csv
│
├── sql/
│   ├── 01_create_table.sql
│   └── patient_encounters.csv
│
├── python/
│   ├── 01_clean_data.py
│   └── eda_analysis.py
│
├── excel/
│   └── cost_leakage_model.xlsx
│
├── powerBI/
│   ├── hospital_readmission.pbix
│   └── powerbi_data_export.csv
│
└── README.md
```

---

## 🧹 Data Preparation

Here's what was done to get the raw data ready for analysis, in simple terms:

- Replaced missing values (shown as `?` in the raw file) with proper blanks
- Removed columns that were mostly empty and not useful (like `weight`, which was missing for 97% of patients)
- Converted coded numbers (like `1`, `2`, `3`) into readable labels (like "Emergency", "Urgent", "Elective")
- Removed patients who passed away or went to hospice, since they can't be "readmitted"
- Created a simple yes/no column for whether a patient was readmitted within 30 days
- Grouped diagnosis codes into easy-to-read categories (like Diabetes, Circulatory, Injury)
- Flagged "high-utilizer" patients: people who had visited the hospital or ER often before
- Estimated a cost for each hospital visit, since the dataset didn't include real billing amounts (the formula used is explained in the project's data dictionary)

---

## 📈 Exploratory Data Analysis (EDA)

The following analyses were performed using Python (descriptive only, no statistical significance testing):

- 30-Day Readmission Rate by Diagnosis Category
- 30-Day Readmission Rate by Age Group
- 30-Day Readmission Rate by Admission Type
- High-Utilizer vs. Non-High-Utilizer Readmission Rate
- Cost Exposure by Diagnosis Category
- Length of Stay & Medication Count: Readmitted vs. Not Readmitted
- Correlation Between Numeric Utilization Features and Readmission

---

## 🗄️ SQL Analysis

Business insights were generated using MySQL:

- 30-Day Readmission Rate by Diagnosis Category
- 30-Day Readmission Rate by Age Group
- 30-Day Readmission Rate by Admission Type
- High-Utilizer Segment vs. Everyone Else
- Cost Exposure by Diagnosis Category
- Cost Exposure by Discharge Disposition
- Overall Cost Leakage Summary (headline KPI query)

A total of **7 SQL queries** were used for analysis, all built on a single clean table (`patient_encounters`).

---

## 💰 Cost Leakage Model (Excel)

- One workbook with a Raw Data table and a formula-driven Summary sheet
- Cost and readmission rates calculated using SUMIFS/COUNTIFS/AVERAGEIFS, not hardcoded numbers, so the model recalculates if the underlying data changes
- Breakdown by Diagnosis Category, High-Utilizer Segment, and Age Group
- Documented assumptions behind the `estimated_cost` proxy model, since this dataset has no real billing data

---

# 📊 Power BI Dashboard

The dashboard consists of **2 interactive pages**.

## 📄 Page 1 – Executive Overview

Features:

- Total Encounters
- Total Readmissions
- Overall Readmit Rate
- Total Cost Exposure
- 30-Day Readmission Rate by Diagnosis Category
- 30-Day Readmission Rate by Age Group
- Slicers: Admission Type, Diagnosis Category, Age

---

## 📄 Page 2 – Cost Leakage Deep Dive

Features:

- Avg Cost per Readmission
- High-Utilizer Readmit Rate
- Non-Utilizer Readmit Rate
- Top 5 Cost Exposure by Diagnosis 
- Cost Exposure by Age Group

---

## 📸 Dashboard Preview

### 📄 Page 1 – Executive Overview

![Executive Overview](Images/dashboard_page1.png)

---

### 📄 Page 2 – Cost Leakage Deep Dive

![Cost Leakage Deep Dive](Images/dashboard_page2.png)

---

## 📊 Key Business Insights

- Overall 30-day readmission rate is **11.39%** across 99,343 patient encounters.
- **High-utilizer patients** (1+ prior ER or inpatient visit) readmit at **16.22%**, nearly double the **8.45%** rate for everyone else. This is the single strongest segment-level driver found in this analysis.
- **Diabetes** carries the highest readmission rate among diagnosis categories at **13%**, followed closely by Injury and Circulatory cases.
- Readmission risk stays elevated (**10-14%**) across all adult age groups, actually **peaking at ages 20-30**. Only children show a sharp drop-off.
- **Circulatory conditions** alone account for **$61.86M** in cost exposure, more than the next four diagnosis categories combined.
- Patients aged **70–80** drive **$32M** in cost exposure, the highest of any age group.
- Total estimated cost exposure tied to 30-day readmissions is **$198.95M**, averaging **$17,584.83** per readmission.

---

## 📚 Skills Demonstrated

- Data Cleaning & Preparation
- Feature Engineering
- Exploratory Data Analysis
- SQL (Aggregations, Business Querying)
- Excel Financial Modeling
- Power BI Dashboard Design
- Business Analytics & Data Storytelling

---

## 👨‍💻 Author

**[Sarthak Mandal]**
