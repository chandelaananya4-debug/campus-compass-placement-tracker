import os
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Campus Compass", page_icon="🎓", layout="wide")

DATA_PATH = Path("data/placement_tracker.csv")
DATA_PATH.parent.mkdir(exist_ok=True)

FIELDS = ("student_id","name","department","graduation_year","cgpa","status","company","package_lpa")
STATUSES = ["Applied","Interviewing","Placed","Not Placed"]

DEMO_RECORDS = [
    {"student_id":"STU101","name":"Aarav Shah","department":"CSE","graduation_year":2027,"cgpa":8.7,"status":"Placed","company":"TechNova","package_lpa":8.5},
    {"student_id":"STU102","name":"Diya Patil","department":"IT","graduation_year":2027,"cgpa":9.1,"status":"Placed","company":"CloudPeak","package_lpa":10.0},
    {"student_id":"STU103","name":"Kabir Joshi","department":"ECE","graduation_year":2027,"cgpa":7.8,"status":"Interviewing","company":"ByteWorks","package_lpa":np.nan},
    {"student_id":"STU104","name":"Meera Rao","department":"CSE","graduation_year":2027,"cgpa":8.2,"status":"Applied","company":"—","package_lpa":np.nan},
    {"student_id":"STU105","name":"Ishaan Kulkarni","department":"IT","graduation_year":2027,"cgpa":7.4,"status":"Not Placed","company":"—","package_lpa":np.nan},
    {"student_id":"STU106","name":"Sara Khan","department":"AIML","graduation_year":2027,"cgpa":8.9,"status":"Placed","company":"TechNova","package_lpa":7.2},
    {"student_id":"STU107","name":"Vivaan Deshmukh","department":"ECE","graduation_year":2027,"cgpa":8.0,"status":"Applied","company":"—","package_lpa":np.nan},
    {"student_id":"STU108","name":"Anaya Singh","department":"CSE","graduation_year":2027,"cgpa":9.4,"status":"Placed","company":"DataSpring","package_lpa":12.0},
    {"student_id":"STU109","name":"Rehan Shaikh","department":"AIML","graduation_year":2027,"cgpa":7.9,"status":"Interviewing","company":"CloudPeak","package_lpa":np.nan},
    {"student_id":"STU110","name":"Tara Nair","department":"IT","graduation_year":2027,"cgpa":8.5,"status":"Placed","company":"ByteWorks","package_lpa":9.0},
]

def load_data():
    if DATA_PATH.exists():
        data = pd.read_csv(DATA_PATH)
    else:
        data = pd.DataFrame(DEMO_RECORDS, columns=FIELDS)
    for col in ["cgpa","package_lpa"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data["student_id"] = data["student_id"].astype(str)
    return data

if "records_df" not in st.session_state:
    st.session_state.records_df = load_data()

df = st.session_state.records_df

# --- Header ---
st.markdown("""
<style>




/* ===== CAMPUS COMPASS: CLEAN DASHBOARD THEME ===== */

.stApp {
    background: #f4f7fc !important;
    color: #172b4d !important;
    font-family: "Segoe UI", sans-serif;
}

/* Default text */
.stApp p,
.stApp label,
.stApp li,
.stApp span {
    color: inherit;
}

/* HERO HEADER */
.hero {
    background: linear-gradient(115deg, #101d39 0%, #274f7d 100%);
    padding: 36px 40px;
    border-radius: 28px;
    margin-bottom: 22px;
}

/* Main title */
.hero h1 {
    color: #ffffff !important;
    font-size: 46px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    opacity: 1 !important;
    text-shadow: none !important;
    margin: 0 0 18px 0;
}

/* Hero description */
.hero p {
    color: #dbeafe !important;
    font-size: 18px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
    text-shadow: none !important;
}

/* KPI CARDS */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e1e8f2 !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 0 4px 16px rgba(22, 43, 77, 0.05);
}

/* KPI labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #52627a !important;
    opacity: 1 !important;
}

/* KPI values */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #14284b !important;
    opacity: 1 !important;
    font-weight: 750 !important;
}

/* Section headings */
.stApp h1:not(.hero h1),
.stApp h2,
.stApp h3 {
    color: #172b4d !important;
    opacity: 1 !important;
    text-shadow: none !important;
}

/* Tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #ffffff !important;
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #edf2fa !important;
}

/* Inputs */
.stApp input,
.stApp textarea {
    color: #172b4d !important;
}

/* Buttons */
.stApp button {
    font-weight: 600;
}

/* ===== DARK NAVIGATION SIDEBAR ===== */

[data-testid="stSidebar"] {
    background: #101d39 !important;
    border-right: 1px solid #263b5d !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #eaf1ff !important;
    opacity: 1 !important;
}

/* Sidebar navigation options */
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 6px 10px !important;
}

/* Navigation hover */
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #20385e !important;
}

/* Selected navigation option */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #274f7d !important;
    border: 1px solid #507eb5 !important;
}

/* Sidebar inputs */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {
    color: #ffffff !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #354765 !important;
}

/* ===== FIX DEPARTMENT / SELECTBOX TEXT COLOR ===== */

/* Selected value inside dropdown */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #252832 !important;
    color: white !important;
    border-color: #414957 !important;
}

/* Selected text */
[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: white !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Dropdown arrow */
[data-testid="stSelectbox"] svg {
    fill: #ffffff !important;
    color: #ffffff !important;
}

/* Open dropdown menu */
[data-baseweb="popover"] ul {
    background-color: #252832 !important;
}

/* Dropdown options */
[data-baseweb="popover"] li {
    background-color: #252832 !important;
    color: #ffffff !important;
}

/* Hover option */
[data-baseweb="popover"] li:hover {
    background-color: #274f7d !important;
    color: #ffffff !important;
}

/* Dropdown option text */
[data-baseweb="popover"] li * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}


</style>
<div class="hero">
<h1>🎓 Campus Compass</h1>
<p>PLACEMENT INTELLIGENCE • Student outcomes, recruiter activity & insights</p>
</div>
""", unsafe_allow_html=True)

st.caption("Prototype • Demo data is fictional. Use authorized, anonymized records for real projects.")

placed = df[df["status"] == "Placed"]
n = len(df)
placed_count = len(placed)
rate = placed_count / n * 100 if n else 0
avg_package = float(np.nanmean(placed["package_lpa"].to_numpy())) if placed["package_lpa"].notna().any() else 0
companies_count = placed["company"].nunique()

m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("Total Students", n)
m2.metric("Placed", placed_count)
m3.metric("Placement Rate", f"{rate:.1f}%")
m4.metric("Hiring Companies", companies_count)
m5.metric("Avg Package", f"{avg_package:.2f} LPA")

# Python structures required by coursework
fields_tuple = FIELDS
student_records_list = df.to_dict(orient="records")
department_set = set(df["department"].dropna().unique())
student_by_id_dict = {r["student_id"]: r for r in student_records_list}

with st.sidebar:
    st.title("🧭 Navigation")
    page = st.radio("Open module", ["Overview","Student Directory","Add / Update Student","Reports & Export"])
    st.divider()
    st.caption("Campus Compass | Cohort placement tracker")

if page == "Overview":
    st.subheader("Placement overview")
    left,right = st.columns(2)
    with left:
        st.markdown("#### Student pipeline")
        status_counts = df["status"].value_counts().reindex(STATUSES, fill_value=0)
        st.bar_chart(status_counts)
    with right:
        st.markdown("#### Placed students by company")
        company_counts = placed.groupby("company").size().sort_values(ascending=False)
        if not company_counts.empty:
            st.bar_chart(company_counts)
        else:
            st.info("No placement records yet.")
    st.markdown("#### Recent student records")
    st.dataframe(df.tail(8), use_container_width=True, hide_index=True)

elif page == "Student Directory":
    st.subheader("Student directory")
    c1,c2,c3 = st.columns([2,1,1])
    query = c1.text_input("Search name, ID or company")
    depts = ["All"] + sorted(df["department"].dropna().astype(str).unique().tolist())
    dept = c2.selectbox("Department", depts)
    status = c3.selectbox("Placement status", ["All"] + STATUSES)
    view = df.copy()
    if query.strip():
        q = query.strip().casefold()
        view = view[view.apply(lambda row: q in str(row["student_id"]).casefold()
                               or q in str(row["name"]).casefold()
                               or q in str(row["company"]).casefold(), axis=1)]
    if dept != "All":
        view = view[view["department"] == dept]
    if status != "All":
        view = view[view["status"] == status]
    st.caption(f"{len(view)} matching record(s)")
    st.dataframe(view, use_container_width=True, hide_index=True)

elif page == "Add / Update Student":
    st.subheader("Student record management")
    st.info("Enter an existing Student ID to update that record, or a new ID to add a student.")
    with st.form("student_form", clear_on_submit=False):
        a,b = st.columns(2)
        sid = a.text_input("Student ID *", placeholder="e.g. STU111").strip()
        name = b.text_input("Student name *")
        c,d = st.columns(2)
        dept = c.selectbox("Department", ["CSE","IT","ECE","AIML","ME","CIVIL","OTHER"])
        year = d.number_input("Graduation year", min_value=2000, max_value=2100, value=2027, step=1)
        e,f = st.columns(2)
        cgpa = e.number_input("CGPA (0–10)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        status_new = f.selectbox("Placement status", STATUSES)
        g,h = st.columns(2)
        company = g.text_input("Company (required if Placed)")
        package = h.number_input("Package (LPA; required if Placed)", min_value=0.0, value=0.0, step=0.5)
        submitted = st.form_submit_button("Save student record", type="primary", use_container_width=True)

    if submitted:
        if not sid or not name.strip():
            st.error("Student ID and student name are required.")
        elif status_new == "Placed" and (not company.strip() or package <= 0):
            st.error("For Placed status, enter a company and package greater than 0.")
        else:
            company_value = company.strip() if status_new == "Placed" else "—"
            package_value = float(package) if status_new == "Placed" else np.nan
            item = {"student_id":sid,"name":name.strip(),"department":dept,
                    "graduation_year":int(year),"cgpa":float(cgpa),"status":status_new,
                    "company":company_value,"package_lpa":package_value}
            new_df = st.session_state.records_df.copy()
            mask = new_df["student_id"].str.casefold() == sid.casefold()
            if mask.any():
                # Keep ID casing as entered; update existing row
                idx = new_df.index[mask][0]
                for key,val in item.items():
                    new_df.at[idx,key] = val
                action = "updated"
            else:
                new_df = pd.concat([new_df,pd.DataFrame([item])],ignore_index=True)
                action = "added"
            st.session_state.records_df = new_df
            st.success(f"Student record {action}.")
            st.dataframe(st.session_state.records_df[st.session_state.records_df["student_id"].str.casefold()==sid.casefold()],
                         use_container_width=True, hide_index=True)
            st.warning("This update is currently in the running app session. Use Reports & Export to download a CSV backup.")

elif page == "Reports & Export":
    st.subheader("Reports & export")
    placed_now = df[df["status"] == "Placed"]
    if not placed_now.empty:
        company_summary = (placed_now.groupby("company")
                           .agg(Placed_Students=("student_id","count"),
                                Average_Package_LPA=("package_lpa","mean"),
                                Highest_Package_LPA=("package_lpa","max"))
                           .round(2).sort_values("Placed_Students",ascending=False))
        st.markdown("#### Company-wise summary")
        st.dataframe(company_summary, use_container_width=True)
        st.download_button("⬇️ Download company summary CSV",
                           company_summary.to_csv().encode("utf-8"),
                           "company_placement_summary.csv","text/csv")
    else:
        st.info("No placed students available for a company summary.")
    st.markdown("#### Full tracker")
    st.download_button("⬇️ Download placement tracker CSV",
                       df.to_csv(index=False).encode("utf-8"),
                       "campus_compass_placement_tracker.csv","text/csv")
    st.caption("For this starter deployment, downloaded files are backups. Session edits may reset when the app restarts.")

st.divider()
st.caption("Campus Compass • Academic prototype | Placement rate currently uses all listed students as denominator.")
