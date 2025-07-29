# 🧪 A/B Test Simulator

This Streamlit app lets you simulate and analyse A/B test results or upload your own data. It calculates statistical significance, lift, effect size, confidence intervals, and sample size requirements.

## 🚀 Features

- Simulate conversion data for two groups
- Upload your own CSV dataset (`group`, `converted`)
- Run t-tests and calculate:
  - Absolute and relative lift
  - Cohen’s d (effect size)
  - Confidence intervals
  - P-value and statistical interpretation
- Visualise conversion rates with Plotly
- Estimate required sample size for desired power and MDE

## 📂 Sample CSV Format

You can upload your own dataset in CSV format with these **two columns**:

```csv
group,converted
A,1
A,0
B,1
B,0
...
