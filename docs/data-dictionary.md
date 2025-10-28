# Data Dictionary
## Employee Efficiency Analysis Project

---

### Dataset Overview
- **Total Records:** 1,009 employees
- **Total Variables:** 18 columns
- **Data Collection Period:** Survey-based data collection
- **Geographic Coverage:** 5 locations across India
- **Department Coverage:** 7 departments

---

## Variable Definitions

### 1. Employee Identification

| Variable Name | Data Type | Description | Example Values |
|--------------|-----------|-------------|----------------|
| `Emp_id` | String | Unique employee identifier | EMP0001, EMP0002, EMP0003 |

---

### 2. Demographic & Organizational Variables

| Variable Name | Data Type | Description | Possible Values | Notes |
|--------------|-----------|-------------|-----------------|-------|
| `departments` | Categorical | Employee's department | DevOps, Data Analyst, QA, AI Engineer, Software Developer, Support, Product Manager | 7 unique departments |
| `location` | Categorical | Employee's work location | Bangalore, Chennai, Kerala, Hyderabad, Coimbatore | 5 locations across India |
| `Experience` | Categorical | Employee experience level | Beginner, Intermediate, expert | Based on tenure/skill assessment |

---

### 3. Work Mode Variables

| Variable Name | Data Type | Description | Possible Values | Notes |
|--------------|-----------|-------------|-----------------|-------|
| `Current Working platform?` | Categorical | Current work arrangement | hybrid, office, remote | Primary independent variable |
| `Preferred working platform` | Categorical | Employee's preferred work mode | hybrid, online platform, official platform | May differ from current mode |

---

### 4. Productivity Metrics

| Variable Name | Data Type | Description | Range | Mean | Notes |
|--------------|-----------|-------------|-------|------|-------|
| `Working  hrs/week` | Integer | Total weekly working hours | 40-44 | 40.54 | Standard work week |
| `Effective working hours` | Integer | Daily effective/focused work hours | 5-7 | 6.01 | Hours of productive work per day |
| `Task_per_day` | Float | Average tasks completed daily | 0.29-1.29 | 0.79 | Task complexity varies by role |
| `Completed projects` | Integer | Number of projects completed | 2-9 | 5.54 | Over a specific time period |
| `Productivity_Score` | Float | Calculated productivity score | 0.0-10.0 | 2.92 | **Primary dependent variable** |

---

### 5. Wellbeing Metrics

| Variable Name | Data Type | Description | Range | Mean | Notes |
|--------------|-----------|-------------|-------|------|-------|
| `wellbeing_score` | Float | Employee wellbeing/satisfaction score | 0.12-0.95 | 0.57 | **Primary dependent variable** - Normalized scale |

---

### 6. Work Environment & Support Variables

| Variable Name | Data Type | Description | Possible Values | Impact |
|--------------|-----------|-------------|-----------------|--------|
| `prefer working in team or solo` | Categorical | Work preference | based on task, both, solo, team | Flexibility indicator |
| `Does your team provide you support at work whenever needed?` | Categorical | Team support availability | yes, sometimes, no | Strong wellbeing predictor |
| `provide resources and tools` | Categorical | Resource accessibility | always, sometimes, never | Impacts productivity |
| `clear work objectives` | Categorical | Frequency of goal clarity | daily, weekly, projectwise | Management effectiveness indicator |
| `constructive feedback` | Categorical | Feedback frequency | only during evaluation, sometimes, regularly, no | Development support indicator |
| `training in hybrid work` | Binary | Hybrid work training received | yes, No | Adaptation support |

---

## Key Metric Calculations

### Productivity Score Calculation
The `Productivity_Score` is a composite metric derived from:
- Tasks completed per day
- Number of completed projects
- Effective working hours
- Working hours per week

**Formula:** Normalized weighted average of productivity indicators (scale: 0-10)

### Wellbeing Score Calculation
The `wellbeing_score` is a normalized metric (scale: 0-1) representing:
- Employee satisfaction
- Work-life balance
- Stress levels
- Overall job satisfaction

---

## Data Quality Notes

### Completeness
- **Missing Values:** 0% - All 1,009 records are complete
- **Unique Identifiers:** 100% unique employee IDs

### Data Validation
- All categorical variables have been standardized
- Numeric ranges validated against business logic
- Experience levels aligned with industry standards

### Limitations
- Self-reported survey data may contain subjective bias
- Cross-sectional data (single point in time)
- No longitudinal tracking of individual employees

---

## Variable Relationships

### Primary Analysis Variables
- **Independent Variable:** `Current Working platform?` (office, hybrid, remote)
- **Dependent Variables:** 
  - `Productivity_Score`
  - `wellbeing_score`

### Control Variables
- Department
- Location
- Experience level
- Support systems (team support, resources, feedback)

### Moderating Variables
- Training in hybrid work
- Resource availability
- Team support

---

## Usage Guidelines

### For Analysis
1. Use `Current Working platform?` to segment productivity/wellbeing comparisons
2. Control for department and experience when comparing work modes
3. Consider support variables as moderating factors
4. Normalize scores when comparing across different scales

### For Visualization
- Productivity Score: Best visualized with bar charts, box plots
- Wellbeing Score: Best visualized with violin plots, scatter plots
- Work Mode Comparisons: Side-by-side comparisons or grouped visualizations

---

**Last Updated:** October 28, 2025  
**Version:** 1.0  
**Contact:** [Your Name/Project Owner]