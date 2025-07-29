import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
import plotly.express as px
import math

st.set_page_config(page_title="A/B Test Simulator", layout="centered")

st.title("🧪 A/B Test Simulator")
st.markdown("Simulate and analyse A/B test results or upload your own data.")

# --- File uploader for real CSV ---
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV (columns: group, converted)", type="csv")

# --- OR simulate ---
st.sidebar.markdown("### 🔧 Or Simulate Test Below")

n_A = st.sidebar.slider("Sample size: Group A", 100, 10000, 1000)
p_A = st.sidebar.slider("Conversion rate: Group A (%)", 0, 100, 10) / 100

n_B = st.sidebar.slider("Sample size: Group B", 100, 10000, 1000)
p_B = st.sidebar.slider("Conversion rate: Group B (%)", 0, 100, 12) / 100

# --- Data source ---
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    group_A = df[df['group'] == 'A']['converted'].astype(int).values
    group_B = df[df['group'] == 'B']['converted'].astype(int).values
else:
    group_A = np.random.binomial(1, p_A, n_A)
    group_B = np.random.binomial(1, p_B, n_B)
    df = pd.DataFrame({
        'group': ['A'] * n_A + ['B'] * n_B,
        'converted': np.concatenate([group_A, group_B])
    })

# --- Calculations ---
mean_A, mean_B = group_A.mean(), group_B.mean()
lift = mean_B - mean_A
relative_lift = lift / mean_A if mean_A else 0

t_stat, p_value = stats.ttest_ind(group_A, group_B)
effect_size = (mean_B - mean_A) / np.sqrt(((group_A.var() + group_B.var()) / 2))

# --- Confidence Intervals ---
def compute_ci(successes, n, z=1.96):
    p = successes / n
    margin = z * np.sqrt((p * (1 - p)) / n)
    return p - margin, p + margin

ci_A = compute_ci(group_A.sum(), len(group_A))
ci_B = compute_ci(group_B.sum(), len(group_B))

# --- Display results ---
st.subheader("📊 Test Summary")
st.markdown(f"**Group A Conversion:** {mean_A:.2%} (95% CI: {ci_A[0]:.2%} – {ci_A[1]:.2%})")
st.markdown(f"**Group B Conversion:** {mean_B:.2%} (95% CI: {ci_B[0]:.2%} – {ci_B[1]:.2%})")
st.markdown(f"**Absolute Lift:** {lift:.2%}")
st.markdown(f"**Relative Lift:** {relative_lift:.2%}")
st.markdown(f"**T-Statistic:** {t_stat:.4f}")
st.markdown(f"**P-Value:** {p_value:.4f}")
st.markdown(f"**Cohen's d (Effect Size):** {effect_size:.4f}")

# --- Interpretation ---
st.markdown("### 📌 Interpretation")
if p_value < 0.05:
    if lift > 0:
        st.success("✅ Variant B performed significantly better than A.")
    else:
        st.warning("⚠️ Variant B underperformed significantly.")
else:
    st.info("❌ No statistically significant difference detected.")

# --- Chart ---
conversion_df = pd.DataFrame({
    "Group": ["A", "B"],
    "Conversion Rate": [mean_A, mean_B]
})
fig = px.bar(conversion_df, x="Group", y="Conversion Rate", text_auto=".2%",
             title="Conversion Rates by Group", color="Group")
st.plotly_chart(fig, use_container_width=True)

# --- Sample Size Estimator ---
st.markdown("### 📐 Sample Size Calculator")
mde_input = st.slider("Minimum Detectable Effect (%)", 1, 20, 5) / 100
power = st.slider("Statistical Power", 0.7, 0.99, 0.8)

analysis = TTestIndPower()
required_n = analysis.solve_power(effect_size=mde_input, power=power, alpha=0.05, alternative='two-sided')

st.markdown(f"📊 To detect a {mde_input:.2%} lift with {power:.0%} power, you need **~{int(required_n)} users per group**.")
