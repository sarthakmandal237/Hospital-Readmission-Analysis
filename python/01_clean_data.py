"""
Hospital Readmission & Cost Leakage Analysis
Step 1: Data Cleaning + Readmission Flag Engineering

Source: Diabetes 130-US Hospitals for Years 1999-2008 (Strack et al., 2014)
Input : diabetic_data.csv  (101,766 encounters x 50 columns)
Output: cleaned_encounters.csv        -> full cleaned dataset (all encounters)
        cleaned_encounters_analysis.csv -> analysis-ready dataset (deduped + excludes expired/hospice)
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# 1. LOAD  (dataset uses "?" as its missing-value marker, not blank/NaN)
# ---------------------------------------------------------------------------
df = pd.read_csv("diabetic_data.csv", na_values="?", low_memory=False)
print(f"Loaded: {df.shape[0]:,} encounters, {df.shape[1]} columns")

# ---------------------------------------------------------------------------
# 2. DROP COLUMNS THAT ARE UNUSABLE
# ---------------------------------------------------------------------------
# weight is 97% missing -> not usable
df = df.drop(columns=["weight"])

# examide and citoglipton have a single constant value across all rows (no variance)
for col in ["examide", "citoglipton"]:
    if col in df.columns and df[col].nunique() <= 1:
        df = df.drop(columns=[col])

# ---------------------------------------------------------------------------
# 3. HANDLE MISSING VALUES MEANINGFULLY (not just drop)
# ---------------------------------------------------------------------------
# max_glu_serum / A1Cresult missing = "test was not performed" -> keep as its own category
df["max_glu_serum"] = df["max_glu_serum"].fillna("Not Tested")
df["A1Cresult"] = df["A1Cresult"].fillna("Not Tested")

# medical_specialty / payer_code missing = "not recorded" -> keep as its own category
df["medical_specialty"] = df["medical_specialty"].fillna("Not Specified")
df["payer_code"] = df["payer_code"].fillna("Not Specified")

# race: small amount missing -> label explicitly rather than drop rows
df["race"] = df["race"].fillna("Unknown")

# diag_1/2/3: drop the ~24 rows missing the PRIMARY diagnosis (diag_1) since it's core to the analysis
df = df.dropna(subset=["diag_1"])

# ---------------------------------------------------------------------------
# 4. MAP KEY ID CODES TO READABLE LABELS
#    (mappings match the official IDs_mapping.csv published with this dataset)
# ---------------------------------------------------------------------------
admission_type_map = {
    1: "Emergency", 2: "Urgent", 3: "Elective", 4: "Newborn",
    5: "Not Available", 6: "NULL", 7: "Trauma Center", 8: "Not Mapped"
}
discharge_disposition_map = {
    1: "Discharged to Home", 2: "Discharged/transferred to another short term hospital",
    3: "Discharged/transferred to SNF", 4: "Discharged/transferred to ICF",
    5: "Discharged/transferred to another type of inpatient care institution",
    6: "Discharged/transferred to home with home health service",
    7: "Left AMA", 8: "Discharged/transferred to home under care of Home IV provider",
    9: "Admitted as an inpatient to this hospital",
    10: "Neonate discharged to another hospital for neonatal aftercare",
    11: "Expired", 12: "Still patient or expected to return for outpatient services",
    13: "Hospice / home", 14: "Hospice / medical facility",
    15: "Discharged/transferred within this institution to Medicare approved swing bed",
    16: "Discharged/transferred/referred another institution for outpatient services",
    17: "Discharged/transferred/referred to this institution for outpatient services",
    18: "NULL", 19: "Expired at home. Medicaid only, hospice.",
    20: "Expired in a medical facility. Medicaid only, hospice.",
    21: "Expired, place unknown. Medicaid only, hospice.",
    22: "Discharged/transferred to another rehab fac including rehab units of a hospital",
    23: "Discharged/transferred to a long term care hospital",
    24: "Discharged/transferred to a nursing facility certified for Medicaid",
    25: "Not Mapped", 26: "Unknown/Invalid",
    27: "Discharged/transferred to a federal health care facility",
    28: "Discharged/transferred/referred to a psychiatric hospital",
    29: "Discharged/transferred to a Critical Access Hospital",
    30: "Discharged/transferred to another Type of Health Care Institution"
}
admission_source_map = {
    1: "Physician Referral", 2: "Clinic Referral", 3: "HMO Referral",
    4: "Transfer from a hospital", 5: "Transfer from a Skilled Nursing Facility",
    6: "Transfer from another health care facility", 7: "Emergency Room",
    8: "Court/Law Enforcement", 9: "Not Available", 10: "Transfer from critical access hospital",
    11: "Normal Delivery", 12: "Premature Delivery", 13: "Sick Baby", 14: "Extramural Birth",
    15: "Not Available", 17: "NULL", 18: "Transfer From Another Home Health Agency",
    19: "Readmission to Same Home Health Agency", 20: "Not Mapped", 21: "Unknown/Invalid",
    22: "Transfer from hospital inpt/same fac reslt in a sep claim",
    23: "Born inside this hospital", 24: "Born outside this hospital",
    25: "Transfer from Ambulatory Surgery Center", 26: "Transfer from Hospice"
}

df["admission_type"] = df["admission_type_id"].map(admission_type_map)
df["discharge_disposition"] = df["discharge_disposition_id"].map(discharge_disposition_map)
df["admission_source"] = df["admission_source_id"].map(admission_source_map)

# ---------------------------------------------------------------------------
# 5. BUILD THE READMISSION FLAGS  (this is the core target for the project)
# ---------------------------------------------------------------------------
# Original field has 3 classes: "NO", ">30", "<30"
df["readmitted_30d"] = (df["readmitted"] == "<30").astype(int)          # binary: readmitted within 30 days (the costly, penalty-triggering event)
df["readmitted_any"] = (df["readmitted"] != "NO").astype(int)           # binary: any readmission at all

# ---------------------------------------------------------------------------
# 6. FEATURE ENGINEERING FOR THE "COST LEAKAGE" ANALYSIS
# ---------------------------------------------------------------------------
# Prior healthcare utilization -> proxy for high-risk / high-cost patients
df["prior_visits_total"] = df["number_outpatient"] + df["number_emergency"] + df["number_inpatient"]
df["high_utilizer_flag"] = (df["prior_visits_total"] >= 5).astype(int)

# Group primary diagnosis (diag_1) ICD-9 codes into clinical categories
def categorize_diagnosis(code):
    try:
        code = str(code)
        if code.startswith("V") or code.startswith("E"):
            return "Other"
        code_num = float(code)
    except ValueError:
        return "Other"
    if 390 <= code_num <= 459 or code_num == 785:
        return "Circulatory"
    elif 460 <= code_num <= 519 or code_num == 786:
        return "Respiratory"
    elif 520 <= code_num <= 579 or code_num == 787:
        return "Digestive"
    elif 250 <= code_num < 251:
        return "Diabetes"
    elif 800 <= code_num <= 999:
        return "Injury"
    elif 710 <= code_num <= 739:
        return "Musculoskeletal"
    elif 580 <= code_num <= 629 or code_num == 788:
        return "Genitourinary"
    elif 140 <= code_num <= 239:
        return "Neoplasms"
    else:
        return "Other"

df["diag_1_category"] = df["diag_1"].apply(categorize_diagnosis)

# Simple length-of-stay cost proxy (illustrative daily rate; adjust with real hospital finance data if available)
DAILY_COST_ESTIMATE = 2500   # placeholder $/day — swap for actual hospital cost data if you have it
df["est_stay_cost"] = df["time_in_hospital"] * DAILY_COST_ESTIMATE

# ---------------------------------------------------------------------------
# 7. SAVE FULL CLEANED DATASET (all encounters, deduplication left to analyst)
# ---------------------------------------------------------------------------
df.to_csv("cleaned_encounters.csv", index=False)
print(f"Saved cleaned_encounters.csv: {df.shape[0]:,} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------------------
# 8. BUILD ANALYSIS-READY DATASET
#    - Exclude encounters where patient died or went to hospice (can't be meaningfully "readmitted")
#    - Deduplicate to one encounter per patient (keep the one with the longest stay,
#      following the same approach used in the original Strack et al. study)
# ---------------------------------------------------------------------------
expired_hospice_ids = [11, 13, 14, 19, 20, 21]
df_analysis = df[~df["discharge_disposition_id"].isin(expired_hospice_ids)].copy()
print(f"Removed {len(df) - len(df_analysis):,} expired/hospice encounters")

df_analysis = (
    df_analysis.sort_values("time_in_hospital", ascending=False)
    .drop_duplicates(subset="patient_nbr", keep="first")
)
print(f"Deduplicated to one encounter/patient: {df_analysis.shape[0]:,} rows")

df_analysis.to_csv("cleaned_encounters_analysis.csv", index=False)
print(f"Saved cleaned_encounters_analysis.csv: {df_analysis.shape[0]:,} rows, {df_analysis.shape[1]} columns")

# ---------------------------------------------------------------------------
# 9. QUICK SUMMARY
# ---------------------------------------------------------------------------
print("\n--- Readmission rate (analysis dataset) ---")
print(df_analysis["readmitted"].value_counts(normalize=True).round(3) * 100)

print("\n--- 30-day readmission rate by diagnosis category ---")
print(
    df_analysis.groupby("diag_1_category")["readmitted_30d"]
    .mean()
    .sort_values(ascending=False)
    .round(3) * 100
)

print("\n--- Estimated cost tied to 30-day readmissions ---")
readmit_cost = df_analysis.loc[df_analysis["readmitted_30d"] == 1, "est_stay_cost"].sum()
print(f"${readmit_cost:,.0f}  (illustrative, based on ${DAILY_COST_ESTIMATE}/day placeholder rate)")
