import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("C:/Users/USER/Documents/Data Analyst/hospital-readmission-analysis/data/clean/diabetic_data_clean.csv")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# --------------------------------------------------
# 1. Readmission rate by diagnosis
# --------------------------------------------------

diagnosis_readmission = df.groupby(
    "diagnosis_category"
)["readmitted_30d"].mean() * 100

diagnosis_readmission = diagnosis_readmission.sort_values(
    ascending=False
)

sns.barplot(
    x=diagnosis_readmission.values,
    y=diagnosis_readmission.index
)

plt.title("30-Day Readmission Rate by Diagnosis")
plt.xlabel("Readmission Rate (%)")
plt.ylabel("Diagnosis")
plt.show()


# --------------------------------------------------
# 2. Readmission rate by age
# --------------------------------------------------

age_readmission = df.groupby("age")["readmitted_30d"].mean() * 100

sns.barplot(
    x=age_readmission.index,
    y=age_readmission.values
)

plt.title("30-Day Readmission Rate by Age")
plt.xlabel("Age Group")
plt.ylabel("Readmission Rate (%)")
plt.xticks(rotation=45)
plt.show()


# --------------------------------------------------
# 3. Readmission rate by admission type
# --------------------------------------------------

admission_readmission = df.groupby(
    "admission_type"
)["readmitted_30d"].mean() * 100

admission_readmission = admission_readmission.sort_values(
    ascending=False
)

sns.barplot(
    x=admission_readmission.values,
    y=admission_readmission.index
)

plt.title("30-Day Readmission Rate by Admission Type")
plt.xlabel("Readmission Rate (%)")
plt.ylabel("Admission Type")
plt.show()


# --------------------------------------------------
# 4. Length of stay: readmitted vs not readmitted
# --------------------------------------------------

sns.boxplot(
    x="readmitted_30d",
    y="time_in_hospital",
    data=df
)

plt.title("Length of Stay: Readmitted vs Not Readmitted")
plt.xlabel("Readmitted Within 30 Days (0 = No, 1 = Yes)")
plt.ylabel("Days in Hospital")
plt.show()


# --------------------------------------------------
# 5. Cost exposure by diagnosis
# --------------------------------------------------

readmitted = df[df["readmitted_30d"] == 1]

cost_by_diagnosis = readmitted.groupby(
    "diagnosis_category"
)["estimated_cost"].sum()

cost_by_diagnosis = cost_by_diagnosis.sort_values(
    ascending=False
)

sns.barplot(
    x=cost_by_diagnosis.values,
    y=cost_by_diagnosis.index
)

plt.title("Total Cost Exposure from 30-Day Readmissions")
plt.xlabel("Estimated Cost")
plt.ylabel("Diagnosis")
plt.show()


# --------------------------------------------------
# Basic findings
# --------------------------------------------------

overall_rate = df["readmitted_30d"].mean() * 100

print("Overall 30-Day Readmission Rate:",
      round(overall_rate, 2), "%")

print(
    "Average hospital stay for readmitted patients:",
    round(
        df[df["readmitted_30d"] == 1]["time_in_hospital"].mean(),
        2
    ),
    "days"
)

print(
    "Average hospital stay for non-readmitted patients:",
    round(
        df[df["readmitted_30d"] == 0]["time_in_hospital"].mean(),
        2
    ),
    "days"
)

print("EDA completed.")