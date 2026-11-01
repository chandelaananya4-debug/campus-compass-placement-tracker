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

/* Main dashboard text */
.stApp {
    color: #172b4d !important;
}

/* KPI cards */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #dbe5f1;
    border-radius: 18px;
    padding: 18px;
}

/* Metric labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #475569 !important;
}

/* Metric numbers */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #172b4d !important;
}

/* Headings */
h1, h2, h3 {
    color: #172b4d !important;
}

/* Normal text */
.stMarkdown p,
.stCaption {
    color: #475569;
}

.stApp {background: #f5f7fb;}
.hero {padding: 1.5rem 1.7rem; border-radius: 20px;
background: linear-gradient(115deg,#101b35,#244b78); color:white; margin-bottom:1rem;}
.hero h1 {color:white; margin:0;}
.hero p {color:#c9daf3; margin:.45rem 0 0;}
div[data-testid="stMetric"] {background:white;padding:16px;border:1px solid #e6ebf3;border-radius:14px;}
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
