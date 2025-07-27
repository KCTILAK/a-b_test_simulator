import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import plotly.express as px

st.set_page_config(page_title="A/B Test Simulator", layout="centered")

st.title("🧪 A/B Test Simulator")
st.markdown("Simulate and analyse A/B test results using conversion rates and sample sizes.")

# Sidebar inputs
st.sidebar.header("Simulation Parameters")
n_A = st.sidebar.slider("Sample size for Group A", 100, 10000, 1000)
p_A = st.sidebar.slider("Conversion rate for Group A (%)", 0, 100, 10) / 100

n_B = st.sidebar.slider("Sample size for Group B", 100, 10000, 1000)
p_B = st.sidebar.slider("Conversion rate for Group B (%)", 0, 100, 12) / 100

# Simulate conversions
group_A = np.random.binomial(1, p_A, n_A)
group_B = np.random.binomial(1, p_B, n_B)

df = pd.DataFrame({
    'group': ['A'] * n_A + ['B'] * n_B,
    'converted': np.concatenate([group_A, group_B])
})

# T-test
t_stat, p_value = stats.ttest_ind(group_A, group_B)
lift = group_B.mean() - group_A.mean()

# Results
st.subheader("📊 Test Summary")
st.markdown(f"**Group A Conversion Rate:** {group_A.mean():.2%}")
st.markdown(f"**Group B Conversion Rate:** {group_B.mean():.2%}")
st.markdown(f"**Absolute Lift:** {lift:.2%}")
st.markdown(f"**T-Statistic:** {t_stat:.4f}")
st.markdown(f"**P-Value:** {p_value:.4f}")
st.markdown(f"**Significant?** {'✅ Yes' if p_value < 0.05 else '❌ No'}")

# Chart
conversion_df = pd.DataFrame({
    "Group": ["A", "B"],
    "Conversion Rate": [group_A.mean(), group_B.mean()]
})
fig = px.bar(conversion_df, x="Group", y="Conversion Rate", title="Conversion Rates by Group", text_auto=".2%")
st.plotly_chart(fig, use_container_width=True)
