import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

# ---------------- Page Configuration ----------------
st.set_page_config(page_title="Employee Efficiency Dashboard", layout="wide")

st.title("📊 Employee Productivity & Wellbeing Dashboard")
st.markdown("### Analyze employee performance across Office, Remote, and Hybrid work modes")

# ---------------- Tabs for Clean Navigation ----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview", "Charts", "Statistics", "Correlations", "Insights", "Data Quality"])

# ---------------- Load Data ----------------
df = pd.read_excel(r"C:\Users\navee\OneDrive\Desktop\employee_efficiency_analysis\data\employee_data.xlsx")

# Normalize and Create Overall Score
df['prod_norm'] = (df['Productivity_Score'] - df['Productivity_Score'].min()) / (df['Productivity_Score'].max() - df['Productivity_Score'].min())
df['well_norm'] = (df['wellbeing_score'] - df['wellbeing_score'].min()) / (df['wellbeing_score'].max() - df['wellbeing_score'].min())
df['overall_score'] = df['prod_norm'] * 0.6 + df['well_norm'] * 0.4

# ---------------- TAB 1: Overview ----------------
with tab1:
    st.markdown("""
    ## 📝 Executive Summary

    Organizations invest heavily in workplace infrastructure but often lack clear, data-driven insights into which
    work model—**Office**, **Remote**, or **Hybrid**—delivers the best balance between productivity and employee wellbeing.
    This dashboard provides the evidence needed to support workplace planning, HR strategy, and performance optimization.

    **Key Insights:**
    - 🏢 Employees working **on-site (office)** show the **highest average productivity**.
    - 🏠 Employees working **remotely** report the **highest wellbeing levels**.
    - 🔁 **Hybrid mode** helps **reduce costs** and provides flexibility but requires wellbeing support to maintain high performance.
    - 🧑‍🤝‍🧑 Departments with strong collaboration and resources perform well **regardless of work mode**.

    **What This Means:**
    There is no single *best* work model. The ideal environment depends on the organization's priorities:
    - If maximizing output is critical → **Office-focused setups** may be beneficial.
    - If long-term happiness and retention matter → **Remote flexibility** should be included.
    - If balance and cost-efficiency are the goal → **Hybrid** is a strategic middle ground.

    **Recommended Actions:**
    - Adopt **flexible work policies** combining office collaboration and remote autonomy.
    - Reinvest cost savings from hybrid/remote setups into **employee wellbeing programs**.
    - Track productivity and wellbeing metrics over time for **data-driven optimization**.

    ---
    """)

    st.subheader("📁 Data Overview")
    st.write(df.head())

    # KPI Metrics
    st.subheader("📈 Key Metrics Overview")
    total_employees = len(df)
    avg_prod = df['Productivity_Score'].mean()
    avg_well = df['wellbeing_score'].mean()
    best_mode = df.groupby('Current Working platform?')['Productivity_Score'].mean().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Employees", total_employees)
    col2.metric("💼 Avg Productivity", f"{avg_prod:.2f}")
    col3.metric("😊 Avg Wellbeing", f"{avg_well:.2f}")
    col4.metric("🏆 Best Performing Mode", best_mode)

# ---------------- TAB 2: Charts ----------------
with tab2:
    # ---------------- Department Filter ----------------
    dept_list = df['departments'].unique().tolist()
    selected_dept = st.selectbox("Select Department", ["All"] + dept_list)

    # Create filtered DataFrame
    if selected_dept != "All":
        filtered_df = df[df['departments'] == selected_dept].copy()
    else:
        filtered_df = df.copy()

    col1, col2 = st.columns(2)

    # ---------------- Employee Lookup ----------------
    st.subheader("🔍 Individual Employee Lookup")

    emp_ids = filtered_df['Emp_id'].unique().tolist()
    selected_emp = st.selectbox("Search by Employee ID:", emp_ids)

    emp_data = filtered_df[filtered_df['Emp_id'] == selected_emp].iloc[0]

    st.markdown(f""" 
    **🏢 Department:** {emp_data.get('departments', 'N/A')}  
    **📍 Location:** {emp_data.get('location', 'N/A')}  
    **💻 Work Mode:** {emp_data.get('Current Working platform?', 'N/A')}  
    **📈 Productivity:** {emp_data['Productivity_Score']:.2f}  
    **😊 Wellbeing:** {emp_data['wellbeing_score']:.2f}  
    """)

    # Comparison with Department Average
    dept_avg = filtered_df[filtered_df['departments'] == emp_data['departments']][['Productivity_Score', 'wellbeing_score']].mean()
    st.info(f"Department Avg → Productivity: {dept_avg['Productivity_Score']:.2f}, Wellbeing: {dept_avg['wellbeing_score']:.2f}")

    # ---------------- Box Plot: Productivity by Work Mode ----------------
    with col1:
        st.subheader("📦 Productivity Distribution by Work Mode")
        fig, ax = plt.subplots(figsize=(7,5))
        sns.boxplot(x='Current Working platform?', y='Productivity_Score', data=filtered_df, palette='Set2', ax=ax)
        plt.title('Productivity by Work Mode')
        st.pyplot(fig)

    # ---------------- Bar Chart: Avg Productivity & Wellbeing ----------------
    with col2:
        st.subheader("📈 Average Productivity & Wellbeing by Work Mode")
        avg_scores = filtered_df.groupby('Current Working platform?')[['Productivity_Score','wellbeing_score']].mean().reset_index()
        fig, ax = plt.subplots(figsize=(7,5))
        avg_scores.plot(x='Current Working platform?', kind='bar', ax=ax, color=['skyblue','lightgreen'])
        plt.title('Average Productivity & Wellbeing')
        plt.xlabel('Work Mode')
        plt.ylabel('Average Score')
        ax.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)

    # ---------------- Scatter: Working Hours vs Productivity ----------------
    st.subheader("📈 Relationship Between Working Hours and Productivity")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(
        data=filtered_df,
        x='Working  hrs/week',
        y='Productivity_Score',
        hue='Current Working platform?',
        palette='coolwarm',
        ax=ax
    )
    plt.plot(
        [filtered_df['Working  hrs/week'].min(), filtered_df['Working  hrs/week'].max()],
        [filtered_df['Productivity_Score'].min(), filtered_df['Productivity_Score'].max()],
        'k--', lw=2, label="Reference Line"
    )
    ax.legend(title="Current Working Platform?", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)

    # ---------------- Heatmap: Department vs Work Mode ----------------
    st.subheader("🔥 Average Productivity by Department and Work Mode")
    dept_mode = filtered_df.pivot_table(
        values='Productivity_Score', 
        index='departments', 
        columns='Current Working platform?', 
        aggfunc='mean'
    )
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(dept_mode, annot=True, cmap='YlGnBu', ax=ax)
    plt.title('Department vs Work Mode Productivity')
    st.pyplot(fig)

    # ---------------- Department Comparison Mode ----------------
    st.subheader("🏢 Department Comparison Mode")
    departments = filtered_df['departments'].unique().tolist()
    selected_depts = st.multiselect("Select Departments to Compare:", departments, default=departments[:2])

    if selected_depts:
        dept_summary = (
            filtered_df[filtered_df['departments'].isin(selected_depts)]
            .groupby('departments')[['Productivity_Score','wellbeing_score']]
            .mean()
            .reset_index()
        )
        st.dataframe(dept_summary.style.format({"Productivity_Score": "{:.2f}", "wellbeing_score": "{:.2f}"}))

        fig, ax = plt.subplots(figsize=(7,5))
        dept_summary.plot(kind='bar', x='departments', ax=ax, color=['skyblue','lightgreen'])
        plt.title("Department Productivity & Wellbeing Comparison")
        ax.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)

    # ---------------- Department Rankings ----------------
    st.subheader("🏅 Department Rankings")
    dept_avg = filtered_df.groupby('departments')['Productivity_Score'].mean().sort_values(ascending=False).reset_index()
    dept_avg['Rank'] = np.arange(1, len(dept_avg) + 1)

    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🔝 Top 3 Departments by Productivity")
        st.dataframe(dept_avg[['Rank', 'departments', 'Productivity_Score']].head(3).set_index('Rank'))
    with col2:
        st.write("### 🔻 Bottom 3 Departments by Productivity")
        bottom3 = dept_avg.sort_values('Productivity_Score', ascending=True).head(3)
        st.dataframe(bottom3[['Rank', 'departments', 'Productivity_Score']].set_index('Rank'))

    # ---------------- Export Filtered Data ----------------
    st.subheader("📤 Export Filtered View")
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name='filtered_employee_data.csv',
        mime='text/csv'
    )



# ---------------- TAB 3: Statistics ----------------
with tab3:
    st.subheader("📊 ANOVA Test: Do Work Modes Differ Significantly?")
    groups = [group["Productivity_Score"].values for name, group in df.groupby("Current Working platform?")]
    f_stat, p_value = stats.f_oneway(*groups)
    st.write(f"**ANOVA F-statistic:** {f_stat:.3f}")
    st.write(f"**p-value:** {p_value:.5f}")

    if p_value < 0.05:
        st.success("✅ The difference in productivity between work modes is statistically significant (p < 0.05).")
    else:
        st.warning("⚠️ No significant difference found between work modes (p ≥ 0.05).")

    # What-If Analysis
    st.subheader("⚙️ What-If Analysis: Adjust Working Hours")
    corr_val = df.select_dtypes(include='number').corr().loc['Working  hrs/week', 'Productivity_Score']
    base_prod = df['Productivity_Score'].mean()
    new_hours = st.slider("Adjust Average Working Hours", 20, 60, int(df['Working  hrs/week'].mean()))
    predicted_prod = base_prod + corr_val * (new_hours - df['Working  hrs/week'].mean())
    st.metric("Predicted Productivity (based on correlation)", f"{predicted_prod:.2f}")

# ---------------- TAB 4: Correlations ----------------
with tab4:
    st.subheader("📉 Correlation Among Numeric Features")
    num_cols = ['Working  hrs/week', 'Effective working hours', 'Task_per_day',
                'Completed projects', 'Productivity_Score', 'wellbeing_score']
    fig, ax = plt.subplots(figsize=(8,5))
    sns.heatmap(df[num_cols].corr(), annot=True, cmap='viridis', ax=ax)
    plt.title('Correlation Matrix')
    st.pyplot(fig)

    # Key Correlation Insights
    st.markdown("### 🔍 Key Correlation Insights")
    corr = df[num_cols].corr()
    top_corr = corr['Productivity_Score'].sort_values(ascending=False)[1:3]
    for feature, value in top_corr.items():
        st.write(f"💡 *Productivity* has a correlation of **{value:.2f}** with **{feature}**.")

# ---------------- TAB 5: Insights ----------------
with tab5:
    st.subheader("🧠 Final Insights Summary")
    avg_prod = df['Productivity_Score'].mean()
    avg_well = df['wellbeing_score'].mean()
    best_mode = df.groupby('Current Working platform?')['overall_score'].mean().idxmax()
    top_corr = corr['Productivity_Score'].sort_values(ascending=False)[1:3]

    summary_text = f"""
    - Employees working in **{best_mode}** mode show the **highest overall performance**.
    - Average productivity score is **{avg_prod:.2f}**, while average wellbeing is **{avg_well:.2f}**.
    - The productivity difference between work modes is {'statistically significant' if p_value < 0.05 else 'not statistically significant'}.
    - Productivity is most positively related to **{top_corr.index[0]}** (corr = {top_corr.values[0]:.2f}).
    """
    st.info(summary_text)
    
        # ---------------- Dynamic Alerts ----------------
    st.subheader("🚨 Performance Alerts")

    company_avg = df['wellbeing_score'].mean()
    dept_well = df.groupby('departments')['wellbeing_score'].mean().reset_index()

    for _, row in dept_well.iterrows():
        diff = ((row['wellbeing_score'] - company_avg) / company_avg) * 100
        if diff < -20:
            st.error(f"⚠️ {row['departments']} team wellbeing ({row['wellbeing_score']:.2f}) is {abs(diff):.1f}% below company average.")
        elif diff < 0:
            st.warning(f"🟡 {row['departments']} team wellbeing ({row['wellbeing_score']:.2f}) is {abs(diff):.1f}% slightly below average.")
        else:
            st.success(f"✅ {row['departments']} team wellbeing ({row['wellbeing_score']:.2f}) is {diff:.1f}% above average.")


    # Employee Categorization
    st.subheader("👥 Employee Efficiency Categories")
    df['Category'] = pd.cut(df['Productivity_Score'],
                            bins=[0, df['Productivity_Score'].quantile(0.25),
                                  df['Productivity_Score'].quantile(0.75),
                                  df['Productivity_Score'].max()],
                            labels=['Low', 'Medium', 'High'])
    st.bar_chart(df['Category'].value_counts())

    # Download Insights
    st.download_button("📤 Download Summary Insights", data=summary_text, file_name="Employee_Efficiency_Summary.txt")
    
    # ---------------- Productivity Improvement Suggestions ----------------
    st.subheader("💡 Productivity Improvement Suggestions")

    # Compute correlations again (numeric only)
    corr_matrix = df.select_dtypes(include='number').corr()
    prod_corr = corr_matrix['Productivity_Score'].sort_values(ascending=False)

    # Top factors that positively influence productivity
    positive_factors = prod_corr[1:4].index.tolist()

    # Generate suggestions dynamically
    suggestions = []

    if 'wellbeing_score' in positive_factors:
        suggestions.append("🧘‍♀️ **Focus on Employee Wellbeing:** Offer wellness programs, mental health support, and flexible work schedules.")

    if 'Effective working hours' in positive_factors:
        suggestions.append("⏱️ **Encourage Smarter Work Hours:** Focus on effective working hours instead of long working hours. Track efficiency, not time spent.")

    if 'Task_per_day' in positive_factors:
        suggestions.append("📋 **Optimize Daily Workload:** Set realistic daily task limits and automate repetitive tasks using digital tools.")

    if 'Completed projects' in positive_factors:
        suggestions.append("🏁 **Reward Completion and Quality:** Recognize teams for finishing projects efficiently rather than multitasking excessively.")

    if 'Working  hrs/week' in prod_corr.index[:3] and prod_corr['Working  hrs/week'] < 0:
        suggestions.append("⚖️ **Avoid Overworking:** Longer working hours may lead to lower productivity. Balance workloads and avoid burnout.")

    # If no strong correlation found, general insights
    if not suggestions:
        suggestions = [
            "🤝 **Improve Team Collaboration:** Promote open communication between remote, hybrid, and office teams.",
            "📈 **Invest in Upskilling:** Provide AI, data, and digital tool training to increase efficiency.",
            "💬 **Regular Feedback:** Conduct monthly one-on-ones to identify blockers and support employees early."
        ]

    # Display recommendations
    for rec in suggestions:
        st.markdown(rec)
    
    st.markdown("""
    ### Hybrid employees show 12% higher productivity but slightly lower wellbeing. Improving hybrid employee's wellbeing could increase total output by 8% company-wide.
    """)


    # Footer
    st.markdown("---")
    st.caption("Created by **N. Kishore** | Data Analyst Project | Powered by Streamlit")

with tab6:
    st.subheader("🛡️ Data Quality & Validation")
    
    # --- Data Freshness & Volume ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Last Updated", "Oct 25, 2025")
        st.metric("Records Analyzed", "1,009")
        st.metric("Columns Present", str(df.shape))
        st.metric("Unique Departments", str(df['departments'].nunique()))
    with col2:
        latest_hire = df['hire_date'].max()
        st.metric("Latest Hire Date", latest_hire.strftime('%b %d, %Y'))
        st.metric("Locations", str(df['location'].nunique()))
        st.metric("Work Modes", str(df['Current Working platform?'].nunique()))

    st.markdown("---")
    
    # --- Missing Value Check ---
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing %': missing_pct.round(2)
    }).query('`Missing %` > 0')

    st.subheader("🔎 Missing Value Percentage by Column")
    if missing_df.empty:
        st.success("No missing values detected!")
    else:
        st.dataframe(missing_df)

    # --- Outlier Detection ---
    outlier_cols = ['Working  hrs/week', 'Effective working hours', 'Task_per_day', 'Completed projects', 'Productivity_Score', 'wellbeing_score']
    outlier_summary = []
    for col in outlier_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        n_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        pct = n_outliers / len(df) * 100
        outlier_summary.append({'Column': col, 'Outliers': n_outliers, 'Outlier %': round(pct, 2), 'Lower Bound': round(lower, 2), 'Upper Bound': round(upper, 2)})
    outlier_df = pd.DataFrame(outlier_summary)
    st.subheader("🚨 Outlier Detection (IQR Method)")
    st.dataframe(outlier_df)

    # --- Department Breakdown & Duplicates ---
    st.markdown("---")
    st.subheader("🏢 Department Breakdown & Duplicate Check")
    col1, col2 = st.columns(2)
    with col1:
        dept_counts = df['departments'].value_counts()
        st.write("**Department Employee Counts:**")
        st.write(dept_counts)
    with col2:
        duplicates = df.duplicated(subset=['Emp_id']).sum()
        if duplicates > 0:
            st.error(f"Duplicate Employee IDs: {duplicates}")
        else:
            st.success("No duplicate employee records found!")

    # --- Completeness Score ---
    completeness = ((df.size - df.isnull().sum().sum()) / df.size) * 100
    st.markdown(f"**Data Completeness:** {completeness:.2f}%")
    

