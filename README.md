# Government of Canada – Innovative Solutions Canada Data Quality

This project provides a practical, fully reproducible analysis of data quality issues in the **Innovative Solutions Canada** award recipient dataset, as featured in [this blog post](https://curtispokrant.com/open-data-hidden-mess-what-405-canadian-innovation-grants-reveal-about-government-data-quality/).

## Project Contents

- **analyse_ised_data_quality.py** – Main Python script for data quality analysis (see below)
- **Phase 1 award recipients text.csv** – Raw data from Power Query (Phase 1)
- **Phase 2 award recipients text.csv** – Raw data from Power Query (Phase 2)
- **Power Query M code** for extracting each table (see blog or the repo)
- **ised_awards_cleaned.csv** – Output: Cleaned, enriched dataset
- This README

## Background

Innovative Solutions Canada (ISC) is a federal program designed to stimulate technology research and commercialization in Canadian SMEs. The government publishes award data, but quality issues (formatting, naming, duplication) make analysis difficult.

## How to Use

1. **Get the data**  
   Use the included Power Query code (see blog or repo) to download both award tables from the official ISC website, or use the provided CSV files.

2. **Run the analysis**  
pip install pandas
python analyse_ised_data_quality.py

The script:
- Combines both phases and adds a "Phase" column
- Cleans up award amount fields
- Standardizes department and innovator names
- Checks for city/province mismatches
- Summarizes key stats, issues, and findings

Output: A cleaned CSV, and console stats that match the blog post.

3. **Reproduce or Extend**
- Use or adapt the script to monitor for future data quality regressions
- See comments in code for how to add your own rules

## Highlights

- **100%** of award amount fields required cleaning
- **31%** of rows had department naming inconsistencies
- **12%** of companies had duplicate/variant names
- Several geography mismatches identified

## Why this matters

Poor open data quality wastes citizen time, reduces transparency, and undermines trust. This project shows how *anyone* can audit government data for real-world usability, with free tools and reproducible code.

**Feel free to contribute improvements or submit issues!**

## Links

- [Official Program Page](https://ised-isde.canada.ca/site/innovative-solutions-canada/en)
- [Official Award Data](https://ised-isde.canada.ca/site/innovative-solutions-canada/en/innovative-solutions-canada-awarded-companies)
- [Related blog post](https://curtispokrant.com/open-data-hidden-mess-what-405-canadian-innovation-grants-reveal-about-government-data-quality/)
