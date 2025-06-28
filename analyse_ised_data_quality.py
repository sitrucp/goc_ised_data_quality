"""
analyse_ised_data_quality.py

Analyzes data quality issues in the Innovative Solutions Canada award dataset
(Phase 1 and Phase 2), as described in:
https://curtispokrant.com/open-data-hidden-mess-what-405-canadian-innovation-grants-reveal-about-government-data-quality/

Requires: pandas (pip install pandas)
Usage:
    Place your two Power Query-exported CSVs in the same directory.
    Adjust filenames if needed.
    python analyse_ised_data_quality.py
"""

import pandas as pd
import numpy as np
import re

# -------- SETTINGS --------
PHASE1_CSV = "Phase 1 award recipients text.csv"
PHASE2_CSV = "Phase 2 award recipients text.csv"
OUTPUT_CLEANED_CSV = "ised_awards_cleaned.csv"
# --------------------------

# 1. Load & Combine Data
def load_data():
    p1 = pd.read_csv(PHASE1_CSV, encoding="utf-8-sig")
    p2 = pd.read_csv(PHASE2_CSV, encoding="utf-8-sig")
    p1["Phase"] = 1
    p2["Phase"] = 2
    df = pd.concat([p1, p2], ignore_index=True)
    return df

df = load_data()

print("Rows: ", len(df))
print("Columns: ", list(df.columns))
print("Phase 1 rows: ", (df['Phase'] == 1).sum())
print("Phase 2 rows: ", (df['Phase'] == 2).sum())

# 2. Award Amount Cleaning
def clean_amount(val):
    if pd.isna(val): return np.nan
    s = (str(val)
         .replace("CAD", "")
         .replace("$", "")
         .replace("\u00A0", "")  # non-breaking space
         .replace(",", "")
         .split("*")[0]
         .strip())
    return pd.to_numeric(s, errors="coerce")

df['Amount_clean'] = df['Awarded amount (*Applicable taxes included)'].apply(clean_amount)

n_bad_amounts = df['Amount_clean'].isna().sum()
bad_amounts_examples = df[df['Amount_clean'].isna()]['Awarded amount (*Applicable taxes included)'].unique()

print(f"\n[Amount] {n_bad_amounts} rows could NOT be parsed as numeric after cleaning.")
print("Examples:", bad_amounts_examples)

total_amount = df['Amount_clean'].sum()
print(f"Total parsed award amount: CAD ${total_amount:,.2f}")

# 3. Department Standardization
def canonical_department(s):
    if pd.isna(s): return ""
    s = s.strip()
    s = re.sub(r"\(.*?\)", "", s)  # remove parenthetical
    s = re.sub(r"\b[Cc]anada\b", "", s)  # remove 'Canada'
    s = s.strip()
    s = re.sub(r"\s+", " ", s)  # collapse whitespace
    return s.lower()

df['Department_canon'] = df['Department'].apply(canonical_department)

departments_raw = df['Department'].nunique()
departments_canon = df['Department_canon'].nunique()
print(f"\n[Department] Raw unique: {departments_raw}, Canonicalized unique: {departments_canon}")

print("Examples of variant department names for 'National Research Council':")
nrc_variants = df[df['Department_canon'].str.contains("national research council")]['Department'].unique()
for v in nrc_variants:
    print(" -", v)

# 4. Innovator Standardization
def canonical_innovator(s):
    if pd.isna(s): return ""
    s = s.lower().strip()
    s = re.sub(r"\binc\.?\b", "inc", s)
    s = re.sub(r"\bltd\.?\b", "ltd", s)
    s = re.sub(r"\blimited\b", "ltd", s)
    s = re.sub(r"\bcorporation\b", "corp", s)
    s = re.sub(r"\s+", " ", s)
    s = s.rstrip(".")
    return s

df['Innovator_canon'] = df['Innovator'].apply(canonical_innovator)

innovators_raw = df['Innovator'].nunique()
innovators_canon = df['Innovator_canon'].nunique()
print(f"\n[Innovator] Raw unique: {innovators_raw}, Canonicalized unique: {innovators_canon}")

# Show some common duplicates
duplicates = (
    df.groupby('Innovator_canon')['Innovator']
    .nunique()
    .reset_index()
    .query('Innovator > 1')
)
if not duplicates.empty:
    print("\nExamples of multiple variants for same company:")
    for row in duplicates.itertuples():
        ex = df[df['Innovator_canon'] == row.Innovator_canon]['Innovator'].unique()
        print(f"- {', '.join(ex)}")

# 5. Province Consistency Check
def city_province_mismatch(row):
    city_field = row['City, Province or Territory']
    province_col = str(row['Province']).strip()
    if not isinstance(city_field, str) or ',' not in city_field:
        return False
    parts = city_field.split(",")
    abbr = parts[-1].strip().upper()
    # Abbreviation to full name map
    province_map = {
        'ON':'Ontario', 'QC':'Quebec', 'BC':'British Columbia', 'AB':'Alberta', 'MB':'Manitoba',
        'SK':'Saskatchewan', 'NB':'New Brunswick', 'NS':'Nova Scotia', 'NL':'Newfoundland and Labrador',
        'PE':'Prince Edward Island', 'YT':'Yukon', 'NT':'Northwest Territories', 'NU':'Nunavut'
    }
    full = province_map.get(abbr, abbr)
    return full != province_col

geo_mismatches = df[df.apply(city_province_mismatch, axis=1)]
print(f"\n[Geography] Province mismatch rows: {len(geo_mismatches)}")
if not geo_mismatches.empty:
    print(geo_mismatches[['City, Province or Territory','Province']])

# 6. Award Date Outliers
award_dates = pd.to_datetime(df['Award date'], errors='coerce')
print(f"\n[Date] Range: {award_dates.min()} to {award_dates.max()}")

# 7. Output cleaned CSV
to_export = df.copy()
to_export['Amount_clean'] = df['Amount_clean']
to_export['Department_canon'] = df['Department_canon']
to_export['Innovator_canon'] = df['Innovator_canon']
to_export.to_csv(OUTPUT_CLEANED_CSV, index=False)
print(f"\n[Done] Cleaned data exported to {OUTPUT_CLEANED_CSV}")
