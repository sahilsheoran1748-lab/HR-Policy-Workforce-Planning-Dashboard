
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Enterprise HR Workforce Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

DATA_PATH = "data/hr_workforce_analytics.csv"

df = pd.read_csv(DATA_PATH)

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.title("📊 Enterprise HR Workforce Dashboard")

st.markdown(
    """
    **HR Policy & Governance Project | 2026–2027**

    This interactive dashboard presents workforce planning,
    hiring requirements, growth projections, and strategic
    skill priorities based on the project dataset.
    """
)

st.divider()

# ------------------------------------------------------------
# KPI CALCULATIONS
# ------------------------------------------------------------

current_total = int(df["Current_Headcount_Q3_2026"].sum())
target_total = int(df["Target_Headcount_Q3_2027"].sum())
additional_hires = target_total - current_total

overall_growth = (additional_hires / current_total) * 100

# ------------------------------------------------------------
# KPI CARDS
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Workforce",
        current_total
    )

with col2:
    st.metric(
        "Target Workforce",
        target_total
    )

with col3:
    st.metric(
        "Additional Hires",
        additional_hires
    )

with col4:
    st.metric(
        "Calculated Growth",
        f"{overall_growth:.2f}%"
    )

st.divider()

# ------------------------------------------------------------
# DEPARTMENT FILTER
# ------------------------------------------------------------

st.subheader("🔎 Department Analysis")

department_options = ["All Departments"] + df["Department"].tolist()

selected_department = st.selectbox(
    "Select Department",
    department_options
)

if selected_department == "All Departments":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["Department"] == selected_department
    ]

# ------------------------------------------------------------
# DEPARTMENT DETAILS
# ------------------------------------------------------------

if selected_department != "All Departments":

    row = filtered_df.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Headcount",
            int(row["Current_Headcount_Q3_2026"])
        )

    with col2:
        st.metric(
            "Target Headcount",
            int(row["Target_Headcount_Q3_2027"])
        )

    with col3:
        st.metric(
            "Additional Hires",
            int(row["Additional_Hires_Required"])
        )

    with col4:
        st.metric(
            "Growth",
            f'{row["Calculated_Growth_Percent"]:.2f}%'
        )

    st.info(
        f'Strategic Skill Priority: {row["Strategic_Skill_Priority"]}'
    )

# ------------------------------------------------------------
# CHART 1 — CURRENT VS TARGET
# ------------------------------------------------------------

st.subheader("📈 Current vs Target Workforce")

chart_data = filtered_df[
    [
        "Department",
        "Current_Headcount_Q3_2026",
        "Target_Headcount_Q3_2027"
    ]
].copy()

chart_data = chart_data.rename(
    columns={
        "Current_Headcount_Q3_2026": "Current Workforce",
        "Target_Headcount_Q3_2027": "Target Workforce"
    }
)

chart_data = chart_data.melt(
    id_vars="Department",
    var_name="Workforce Type",
    value_name="Employees"
)

fig1 = px.bar(
    chart_data,
    x="Department",
    y="Employees",
    color="Workforce Type",
    barmode="group",
    title="Current vs Target Workforce"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ------------------------------------------------------------
# CHART 2 — ADDITIONAL HIRING
# ------------------------------------------------------------

st.subheader("👥 Additional Hiring Requirement")

fig2 = px.bar(
    filtered_df,
    x="Department",
    y="Additional_Hires_Required",
    title="Additional Employees Required"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ------------------------------------------------------------
# CHART 3 — GROWTH PROJECTION
# ------------------------------------------------------------

st.subheader("📊 Workforce Growth Projection")

fig3 = px.bar(
    filtered_df,
    x="Department",
    y="Calculated_Growth_Percent",
    title="Calculated Workforce Growth (%)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ------------------------------------------------------------
# DATA TABLE
# ------------------------------------------------------------

st.subheader("📋 Workforce Planning Data")

display_columns = [
    "Department",
    "Current_Headcount_Q3_2026",
    "Growth_Projection_Percent",
    "Target_Headcount_Q3_2027",
    "Additional_Hires_Required",
    "Strategic_Skill_Priority"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------------------------
# DOWNLOAD DATA
# ------------------------------------------------------------

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Current Analysis",
    data=csv_data,
    file_name="hr_workforce_analysis.csv",
    mime="text/csv"
)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Enterprise HR Policy & Employee Handbook | "
    "2026–2027 | Internship Project"
)
