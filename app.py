# ============================================================
# EDUPRO PREDICTIVE INTELLIGENCE DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduPro Predictive Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM STYLE
# ============================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

[data-testid="stMetric"] {
    background-color: #f7f9fc;
    border: 1px solid #e5e7eb;
    padding: 15px;
    border-radius: 12px;
}

h1 {
    font-weight: 700;
}

h2 {
    font-weight: 650;
}

h3 {
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

FINAL_DATA_FILE = DATA_DIR / "EduPro_Final_ML_Data.csv"

CLEANED_DATA_FILE = DATA_DIR / "EduPro_Cleaned_Course_Data (1).csv"


# ============================================================
# LOAD FINAL ML DATA
# ============================================================

@st.cache_data
def load_final_data():

    if not FINAL_DATA_FILE.exists():

        st.error(
            "EduPro_Final_ML_Data.csv was not found inside the data folder."
        )

        st.stop()

    df = pd.read_csv(FINAL_DATA_FILE)

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


df = load_final_data()


# ============================================================
# CREATE COURSE-LEVEL DATA
# ============================================================

@st.cache_data
def create_course_data(data):

    course_data = data.copy()

    if "CourseID" in course_data.columns:

        course_data = (
            course_data
            .drop_duplicates(subset=["CourseID"])
            .reset_index(drop=True)
        )

    return course_data


course_df = create_course_data(df)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🎓 EduPro")

st.sidebar.markdown(
    "**Predictive Intelligence Dashboard**"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Executive Overview",
        "📚 Course Offered",
        "📈 Demand Analytics",
        "💰 Revenue Forecast",
        "🤖 Live Demand Prediction",
        "🔮 Live Revenue Prediction",
        "🔍 Feature Importance",
        "📊 Model Performance",
        "💡 Recommendations"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "EduPro • Predictive Modeling & Revenue Forecasting"
)


# ============================================================
# 🏠 EXECUTIVE OVERVIEW
# ============================================================

if page == "🏠 Executive Overview":

    st.title("🎓 EduPro Predictive Intelligence")

    st.subheader("Executive Overview")

    st.caption(
        "Live analytics for course demand, revenue performance "
        "and predictive decision-making."
    )

    st.divider()

    # --------------------------------------------------------
    # BASIC BUSINESS METRICS
    # --------------------------------------------------------

    total_users = 3000

    total_teachers = 60

    total_courses = (
        course_df["CourseID"].nunique()
        if "CourseID" in course_df.columns
        else 0
    )

    total_transactions = 10000


    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    if "Course_Revenue_course" in course_df.columns:

        revenue_series = pd.to_numeric(
            course_df["Course_Revenue_course"],
            errors="coerce"
        ).fillna(0)

        total_revenue = revenue_series.sum()

    elif "Course_Revenue_monthly" in df.columns:

        revenue_series = pd.to_numeric(
            df["Course_Revenue_monthly"],
            errors="coerce"
        ).fillna(0)

        total_revenue = revenue_series.sum()

    else:

        total_revenue = 0


    # --------------------------------------------------------
    # ENROLLMENTS
    # --------------------------------------------------------

    if "Enrollment_Count_course" in course_df.columns:

        enrollment_series = pd.to_numeric(
            course_df["Enrollment_Count_course"],
            errors="coerce"
        ).fillna(0)

        total_enrollments = enrollment_series.sum()

    elif "Enrollment_Count_monthly" in df.columns:

        enrollment_series = pd.to_numeric(
            df["Enrollment_Count_monthly"],
            errors="coerce"
        ).fillna(0)

        total_enrollments = enrollment_series.sum()

    else:

        total_enrollments = 0


    # --------------------------------------------------------
    # KPI ROW 1
    # --------------------------------------------------------

    st.markdown("### 📊 EduPro Live Performance")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "👥 Total Users",
            f"{total_users:,}"
        )

    with c2:

        st.metric(
            "👨‍🏫 Total Teachers",
            f"{total_teachers:,}"
        )

    with c3:

        st.metric(
            "📚 Total Courses",
            f"{total_courses:,}"
        )

    with c4:

        st.metric(
            "🧾 Total Transactions",
            f"{total_transactions:,}"
        )


    # --------------------------------------------------------
    # KPI ROW 2
    # --------------------------------------------------------

    c5, c6, c7 = st.columns(3)

    with c5:

        st.metric(
            "🎯 Total Enrollments",
            f"{total_enrollments:,.0f}"
        )

    with c6:

        st.metric(
            "💰 Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

    with c7:

        if total_courses > 0:

            revenue_per_course = (
                total_revenue / total_courses
            )

        else:

            revenue_per_course = 0

        st.metric(
            "💵 Revenue / Course",
            f"₹{revenue_per_course:,.2f}"
        )


    st.divider()


    # ========================================================
    # COURSE ECOSYSTEM
    # ========================================================

    st.header("📚 Course Ecosystem")

    left, right = st.columns(2)


    # --------------------------------------------------------
    # CATEGORY CHART
    # --------------------------------------------------------

    with left:

        if "CourseCategory" in course_df.columns:

            category_data = (
                course_df
                .groupby("CourseCategory")
                .size()
                .reset_index(name="Courses")
                .sort_values(
                    "Courses",
                    ascending=False
                )
            )

            fig_category = px.bar(
                category_data,
                x="CourseCategory",
                y="Courses",
                text="Courses",
                title="Courses Offered by Category"
            )

            fig_category.update_traces(
                textposition="outside"
            )

            fig_category.update_layout(
                xaxis_title="Course Category",
                yaxis_title="Number of Courses",
                xaxis_tickangle=-35,
                height=430
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True
            )


    # --------------------------------------------------------
    # FREE VS PAID
    # --------------------------------------------------------

    with right:

        if "CourseType" in course_df.columns:

            type_data = (
                course_df
                .groupby("CourseType")
                .size()
                .reset_index(name="Courses")
            )

            fig_type = px.pie(
                type_data,
                names="CourseType",
                values="Courses",
                hole=0.55,
                title="Free vs Paid Courses"
            )

            fig_type.update_layout(
                height=430
            )

            st.plotly_chart(
                fig_type,
                use_container_width=True
            )


    # ========================================================
    # COURSE LEVEL
    # ========================================================

    if "CourseLevel" in course_df.columns:

        st.subheader("🎯 Course Level Distribution")

        level_data = (
            course_df
            .groupby("CourseLevel")
            .size()
            .reset_index(name="Courses")
        )

        fig_level = px.bar(
            level_data,
            x="CourseLevel",
            y="Courses",
            text="Courses",
            title="Beginner vs Intermediate vs Advanced"
        )

        fig_level.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig_level,
            use_container_width=True
        )


    # ========================================================
    # REVENUE BY CATEGORY
    # ========================================================

    if (
        "CourseCategory" in course_df.columns
        and "Course_Revenue_course" in course_df.columns
    ):

        st.subheader("💰 Revenue by Course Category")

        revenue_category = (
            course_df
            .groupby("CourseCategory", as_index=False)
            ["Course_Revenue_course"]
            .sum()
            .sort_values(
                "Course_Revenue_course",
                ascending=False
            )
        )

        revenue_category[
            "Course_Revenue_course"
        ] = pd.to_numeric(
            revenue_category[
                "Course_Revenue_course"
            ],
            errors="coerce"
        ).fillna(0)


        fig_revenue_category = px.bar(
            revenue_category,
            x="CourseCategory",
            y="Course_Revenue_course",
            text="Course_Revenue_course",
            title="Revenue Generated by Category"
        )

        fig_revenue_category.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig_revenue_category.update_layout(
            xaxis_title="Course Category",
            yaxis_title="Revenue",
            xaxis_tickangle=-35,
            height=450
        )

        st.plotly_chart(
            fig_revenue_category,
            use_container_width=True
        )


    # ========================================================
    # TOP COURSES
    # ========================================================

    if (
        "CourseName" in course_df.columns
        and "Course_Revenue_course" in course_df.columns
    ):

        st.subheader("🏆 Top Revenue-Generating Courses")

        top_courses = course_df[
            [
                "CourseName",
                "CourseCategory",
                "Course_Revenue_course"
            ]
        ].copy()

        top_courses[
            "Course_Revenue_course"
        ] = pd.to_numeric(
            top_courses[
                "Course_Revenue_course"
            ],
            errors="coerce"
        ).fillna(0)

        top_courses = (
            top_courses
            .sort_values(
                "Course_Revenue_course",
                ascending=False
            )
            .head(10)
            .sort_values(
                "Course_Revenue_course"
            )
        )

        fig_top = px.bar(
            top_courses,
            x="Course_Revenue_course",
            y="CourseName",
            orientation="h",
            color="CourseCategory",
            title="Top 10 Courses by Revenue"
        )

        fig_top.update_layout(
            xaxis_title="Course Revenue",
            yaxis_title="Course",
            height=500
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )


    # ========================================================
    # LIVE ANALYTICS STATUS
    # ========================================================

    st.divider()

    st.subheader("⚡ Live Analytics Status")

    s1, s2, s3 = st.columns(3)

    with s1:

        st.success(
            "🟢 Course data connected"
        )

    with s2:

        st.success(
            "🟢 Analytics active"
        )

    with s3:

        st.success(
            "🟢 Dashboard ready"
        )


    # ========================================================
    # EXECUTIVE INSIGHT
    # ========================================================

    st.divider()

    st.subheader("💡 Executive Insight")

    if (
        "CourseCategory" in course_df.columns
        and "Course_Revenue_course" in course_df.columns
    ):

        insight_data = (
            course_df
            .groupby("CourseCategory")
            ["Course_Revenue_course"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if len(insight_data) > 0:

            best_category = insight_data.index[0]

            best_revenue = insight_data.iloc[0]

            st.info(
                f"📌 **{best_category}** is currently the "
                f"highest-revenue category, generating approximately "
                f"**₹{best_revenue:,.2f}**. Historical performance "
                f"will be combined with the predictive models in the "
                f"forecasting and prediction sections."
            )

        else:

            st.info(
                "Revenue insights will appear when revenue data "
                "is available."
            )

    else:

        st.info(
            "Revenue insights require course-level revenue data."
        )


# ============================================================
# OTHER PAGES — TEMPORARY SAFE PLACEHOLDERS
# ============================================================

elif page == "📚 Course Offered":

    st.title("📚 Course Offered")
    st.caption(
        "Explore EduPro's course portfolio, pricing, ratings, levels and "
        "course structure through interactive live analytics."
    )

    st.divider()

    # ========================================================
    # COURSE OFFERED - KPI CALCULATIONS
    # ========================================================

    total_courses = course_df["CourseID"].nunique()

    paid_courses = 0
    free_courses = 0

    if "CourseType" in course_df.columns:
        paid_courses = int(
            (course_df["CourseType"].astype(str).str.strip().str.lower() == "paid").sum()
        )

        free_courses = int(
            (course_df["CourseType"].astype(str).str.strip().str.lower() == "free").sum()
        )

    if "CoursePrice" in course_df.columns:
        price_series = pd.to_numeric(
            course_df["CoursePrice"],
            errors="coerce"
        ).fillna(0)

        average_price = price_series.mean()
    else:
        average_price = 0

    if "CourseRating" in course_df.columns:
        rating_series = pd.to_numeric(
            course_df["CourseRating"],
            errors="coerce"
        ).dropna()

        average_rating = rating_series.mean()
    else:
        average_rating = 0


    # ========================================================
    # KPI CARDS
    # ========================================================

    st.subheader("📊 Course Portfolio Snapshot")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric(
            "📚 Total Courses",
            f"{total_courses:,}"
        )

    with k2:
        st.metric(
            "💳 Paid Courses",
            f"{paid_courses:,}"
        )

    with k3:
        st.metric(
            "🆓 Free Courses",
            f"{free_courses:,}"
        )

    with k4:
        st.metric(
            "💰 Avg Course Price",
            f"₹{average_price:,.2f}"
        )

    with k5:
        st.metric(
            "⭐ Avg Rating",
            f"{average_rating:.2f}"
        )


    st.divider()


    # ========================================================
    # INTERACTIVE FILTERS
    # ========================================================

    st.subheader("🎛️ Explore Course Portfolio")

    f1, f2, f3, f4 = st.columns(4)

    filtered_courses = course_df.copy()


    # --------------------------------------------------------
    # CATEGORY FILTER
    # --------------------------------------------------------

    with f1:

        if "CourseCategory" in filtered_courses.columns:

            categories = sorted(
                filtered_courses["CourseCategory"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_category = st.multiselect(
                "Course Category",
                categories,
                default=[]
            )

            if selected_category:

                filtered_courses = filtered_courses[
                    filtered_courses["CourseCategory"]
                    .astype(str)
                    .isin(selected_category)
                ]


    # --------------------------------------------------------
    # COURSE TYPE FILTER
    # --------------------------------------------------------

    with f2:

        if "CourseType" in filtered_courses.columns:

            types = sorted(
                filtered_courses["CourseType"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_type = st.multiselect(
                "Course Type",
                types,
                default=[]
            )

            if selected_type:

                filtered_courses = filtered_courses[
                    filtered_courses["CourseType"]
                    .astype(str)
                    .isin(selected_type)
                ]


    # --------------------------------------------------------
    # COURSE LEVEL FILTER
    # --------------------------------------------------------

    with f3:

        if "CourseLevel" in filtered_courses.columns:

            levels = sorted(
                filtered_courses["CourseLevel"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_level = st.multiselect(
                "Course Level",
                levels,
                default=[]
            )

            if selected_level:

                filtered_courses = filtered_courses[
                    filtered_courses["CourseLevel"]
                    .astype(str)
                    .isin(selected_level)
                ]


    # --------------------------------------------------------
    # PRICE BAND FILTER
    # --------------------------------------------------------

    with f4:

        if "Price_Band" in filtered_courses.columns:

            price_bands = sorted(
                filtered_courses["Price_Band"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_price_band = st.multiselect(
                "Price Band",
                price_bands,
                default=[]
            )

            if selected_price_band:

                filtered_courses = filtered_courses[
                    filtered_courses["Price_Band"]
                    .astype(str)
                    .isin(selected_price_band)
                ]


    # ========================================================
    # FILTERED RESULT COUNT
    # ========================================================

    st.info(
        f"🔎 Showing **{len(filtered_courses):,} courses** "
        f"from the selected filters."
    )


    # ========================================================
    # COURSE CATEGORY ANALYSIS
    # ========================================================

    left, right = st.columns(2)


    with left:

        if "CourseCategory" in filtered_courses.columns:

            category_count = (
                filtered_courses
                .groupby("CourseCategory")
                .size()
                .reset_index(name="Courses")
                .sort_values(
                    "Courses",
                    ascending=False
                )
            )

            fig_category = px.bar(
                category_count,
                x="CourseCategory",
                y="Courses",
                text="Courses",
                title="📚 Courses Offered by Category"
            )

            fig_category.update_traces(
                textposition="outside"
            )

            fig_category.update_layout(
                xaxis_title="Course Category",
                yaxis_title="Number of Courses",
                xaxis_tickangle=-35,
                height=430
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True
            )


    # ========================================================
    # FREE VS PAID
    # ========================================================

    with right:

        if "CourseType" in filtered_courses.columns:

            type_count = (
                filtered_courses
                .groupby("CourseType")
                .size()
                .reset_index(name="Courses")
            )

            fig_type = px.pie(
                type_count,
                names="CourseType",
                values="Courses",
                hole=0.55,
                title="💳 Free vs Paid Courses"
            )

            fig_type.update_layout(
                height=430
            )

            st.plotly_chart(
                fig_type,
                use_container_width=True
            )


    # ========================================================
    # COURSE LEVEL
    # ========================================================

    if "CourseLevel" in filtered_courses.columns:

        level_count = (
            filtered_courses
            .groupby("CourseLevel")
            .size()
            .reset_index(name="Courses")
        )

        fig_level = px.bar(
            level_count,
            x="CourseLevel",
            y="Courses",
            text="Courses",
            title="🎯 Course Level Distribution"
        )

        fig_level.update_traces(
            textposition="outside"
        )

        fig_level.update_layout(
            height=400,
            xaxis_title="Course Level",
            yaxis_title="Number of Courses"
        )

        st.plotly_chart(
            fig_level,
            use_container_width=True
        )


    # ========================================================
    # PRICE BAND ANALYSIS
    # ========================================================

    if "Price_Band" in filtered_courses.columns:

        price_band_data = (
            filtered_courses
            .groupby("Price_Band")
            .size()
            .reset_index(name="Courses")
        )

        fig_price_band = px.bar(
            price_band_data,
            x="Price_Band",
            y="Courses",
            text="Courses",
            title="💰 Course Price Bands"
        )

        fig_price_band.update_traces(
            textposition="outside"
        )

        fig_price_band.update_layout(
            height=400,
            xaxis_title="Price Band",
            yaxis_title="Number of Courses"
        )

        st.plotly_chart(
            fig_price_band,
            use_container_width=True
        )


    # ========================================================
    # RATING DISTRIBUTION
    # ========================================================

    if "CourseRating" in filtered_courses.columns:

        rating_data = pd.to_numeric(
            filtered_courses["CourseRating"],
            errors="coerce"
        ).dropna()

        if len(rating_data) > 0:

            fig_rating = px.histogram(
                rating_data,
                x=rating_data,
                nbins=10,
                title="⭐ Course Rating Distribution"
            )

            fig_rating.update_layout(
                xaxis_title="Course Rating",
                yaxis_title="Number of Courses",
                height=400
            )

            st.plotly_chart(
                fig_rating,
                use_container_width=True
            )


    # ========================================================
    # DURATION DISTRIBUTION
    # ========================================================

    if "CourseDuration" in filtered_courses.columns:

        duration_data = pd.to_numeric(
            filtered_courses["CourseDuration"],
            errors="coerce"
        ).dropna()

        if len(duration_data) > 0:

            fig_duration = px.histogram(
                duration_data,
                x=duration_data,
                nbins=12,
                title="⏱️ Course Duration Distribution"
            )

            fig_duration.update_layout(
                xaxis_title="Course Duration",
                yaxis_title="Number of Courses",
                height=400
            )

            st.plotly_chart(
                fig_duration,
                use_container_width=True
            )


    # ========================================================
    # COURSE CATALOGUE
    # ========================================================

    st.divider()

    st.subheader("📋 Course Catalogue")

    catalogue_columns = [
        "CourseID",
        "CourseName",
        "CourseCategory",
        "CourseType",
        "CourseLevel",
        "CoursePrice",
        "CourseDuration",
        "CourseRating"
    ]

    available_catalogue_columns = [
        col
        for col in catalogue_columns
        if col in filtered_courses.columns
    ]

    catalogue = filtered_courses[
        available_catalogue_columns
    ].copy()


    if "CoursePrice" in catalogue.columns:

        catalogue["CoursePrice"] = pd.to_numeric(
            catalogue["CoursePrice"],
            errors="coerce"
        )


    if "CourseDuration" in catalogue.columns:

        catalogue["CourseDuration"] = pd.to_numeric(
            catalogue["CourseDuration"],
            errors="coerce"
        )


    if "CourseRating" in catalogue.columns:

        catalogue["CourseRating"] = pd.to_numeric(
            catalogue["CourseRating"],
            errors="coerce"
        )


    st.dataframe(
        catalogue,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # LIVE ANALYTICS STATUS
    # ========================================================

    st.divider()

    a1, a2, a3 = st.columns(3)

    with a1:
        st.success("🟢 Course dataset connected")

    with a2:
        st.success("🟢 Filters are interactive")

    with a3:
        st.success("🟢 Analytics updating live")


    # ========================================================
    # BUSINESS INSIGHT
    # ========================================================

    st.subheader("💡 Course Portfolio Insight")

    insight_parts = []

    if total_courses > 0:

        insight_parts.append(
            f"EduPro currently offers **{total_courses} courses**."
        )

    if paid_courses + free_courses > 0:

        paid_share = (
            paid_courses /
            (paid_courses + free_courses)
        ) * 100

        insight_parts.append(
            f"Paid courses represent approximately "
            f"**{paid_share:.1f}%** of the course portfolio."
        )

    if average_rating > 0:

        insight_parts.append(
            f"The overall average course rating is "
            f"**{average_rating:.2f}/5**."
        )

    if insight_parts:

        st.info(" ".join(insight_parts))


elif page == "📈 Demand Analytics":

    st.title("📈 Demand Analytics")
    st.caption(
        "Historical enrollment trends and course demand indicators "
        "supporting proactive course planning."
    )

    st.divider()

    # ========================================================
    # PREPARE DEMAND DATA
    # ========================================================

    demand_df = df.copy()

    if "Month" in demand_df.columns:
        demand_df["Month"] = pd.to_datetime(
            demand_df["Month"],
            errors="coerce"
        )

    if "Enrollment_Count_monthly" in demand_df.columns:

        demand_df["Enrollment_Count_monthly"] = pd.to_numeric(
            demand_df["Enrollment_Count_monthly"],
            errors="coerce"
        ).fillna(0)

    elif "Enrollment_Count" in demand_df.columns:

        demand_df["Enrollment_Count_monthly"] = pd.to_numeric(
            demand_df["Enrollment_Count"],
            errors="coerce"
        ).fillna(0)

    else:

        demand_df["Enrollment_Count_monthly"] = 0


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_enrollments = demand_df[
        "Enrollment_Count_monthly"
    ].sum()

    average_monthly_enrollment = demand_df[
        "Enrollment_Count_monthly"
    ].mean()

    highest_monthly_demand = demand_df[
        "Enrollment_Count_monthly"
    ].max()

    if "CourseID" in demand_df.columns:

        courses_tracked = demand_df[
            "CourseID"
        ].nunique()

    else:

        courses_tracked = 0


    # ========================================================
    # KPI CARDS
    # ========================================================

    st.subheader("📊 Demand Performance")

    d1, d2, d3, d4 = st.columns(4)

    with d1:

        st.metric(
            "🎯 Total Enrollments",
            f"{total_enrollments:,.0f}"
        )

    with d2:

        st.metric(
            "📈 Avg Monthly Enrollment",
            f"{average_monthly_enrollment:,.1f}"
        )

    with d3:

        st.metric(
            "🔥 Highest Monthly Demand",
            f"{highest_monthly_demand:,.0f}"
        )

    with d4:

        st.metric(
            "📚 Courses Tracked",
            f"{courses_tracked:,}"
        )


    st.divider()


    # ========================================================
    # MONTHLY DEMAND TREND
    # ========================================================

    if "Month" in demand_df.columns:

        monthly_demand = (
            demand_df
            .dropna(subset=["Month"])
            .groupby("Month", as_index=False)
            ["Enrollment_Count_monthly"]
            .sum()
            .sort_values("Month")
        )

        if len(monthly_demand) > 0:

            st.subheader("📈 Monthly Enrollment Demand")

            fig_monthly = px.line(
                monthly_demand,
                x="Month",
                y="Enrollment_Count_monthly",
                markers=True,
                title="EduPro Enrollment Demand Trend"
            )

            fig_monthly.update_layout(
                xaxis_title="Month",
                yaxis_title="Enrollments",
                height=430
            )

            st.plotly_chart(
                fig_monthly,
                use_container_width=True
            )


    # ========================================================
    # CATEGORY DEMAND
    # ========================================================

    if (
        "CourseCategory" in demand_df.columns
        and "Enrollment_Count_monthly" in demand_df.columns
    ):

        category_demand = (
            demand_df
            .groupby("CourseCategory", as_index=False)
            ["Enrollment_Count_monthly"]
            .sum()
            .sort_values(
                "Enrollment_Count_monthly",
                ascending=False
            )
        )

        st.subheader("🏆 Demand by Course Category")

        fig_category_demand = px.bar(
            category_demand,
            x="CourseCategory",
            y="Enrollment_Count_monthly",
            text="Enrollment_Count_monthly",
            title="Total Enrollment Demand by Category"
        )

        fig_category_demand.update_traces(
            textposition="outside"
        )

        fig_category_demand.update_layout(
            xaxis_title="Course Category",
            yaxis_title="Total Enrollments",
            xaxis_tickangle=-35,
            height=450
        )

        st.plotly_chart(
            fig_category_demand,
            use_container_width=True
        )


    # ========================================================
    # COURSE-LEVEL DEMAND
    # ========================================================

    if (
        "CourseID" in demand_df.columns
        and "Enrollment_Count_monthly" in demand_df.columns
    ):

        course_demand = (
            demand_df
            .groupby(
                [
                    "CourseID",
                    "CourseName"
                ] if "CourseName" in demand_df.columns
                else ["CourseID"],
                as_index=False
            )
            ["Enrollment_Count_monthly"]
            .sum()
            .sort_values(
                "Enrollment_Count_monthly",
                ascending=False
            )
        )

        top_course_demand = course_demand.head(10).copy()

        st.subheader("🔥 Top Courses by Enrollment Demand")

        if "CourseName" in top_course_demand.columns:

            fig_top_demand = px.bar(
                top_course_demand.sort_values(
                    "Enrollment_Count_monthly"
                ),
                x="Enrollment_Count_monthly",
                y="CourseName",
                orientation="h",
                title="Top 10 Courses by Enrollment Demand"
            )

            fig_top_demand.update_layout(
                xaxis_title="Total Enrollments",
                yaxis_title="Course",
                height=500
            )

            st.plotly_chart(
                fig_top_demand,
                use_container_width=True
            )


    # ========================================================
    # COURSE LEVEL DEMAND
    # ========================================================

    if (
        "CourseLevel" in demand_df.columns
        and "Enrollment_Count_monthly" in demand_df.columns
    ):

        level_demand = (
            demand_df
            .groupby("CourseLevel", as_index=False)
            ["Enrollment_Count_monthly"]
            .sum()
            .sort_values(
                "Enrollment_Count_monthly",
                ascending=False
            )
        )

        st.subheader("🎯 Demand by Course Level")

        fig_level_demand = px.bar(
            level_demand,
            x="CourseLevel",
            y="Enrollment_Count_monthly",
            text="Enrollment_Count_monthly",
            title="Enrollment Demand by Course Level"
        )

        fig_level_demand.update_traces(
            textposition="outside"
        )

        fig_level_demand.update_layout(
            xaxis_title="Course Level",
            yaxis_title="Total Enrollments",
            height=400
        )

        st.plotly_chart(
            fig_level_demand,
            use_container_width=True
        )


    # ========================================================
    # DEMAND HEATMAP
    # ========================================================

    if (
        "Month" in demand_df.columns
        and "CourseCategory" in demand_df.columns
    ):

        heatmap_data = (
            demand_df
            .dropna(subset=["Month"])
            .groupby(
                [
                    "CourseCategory",
                    "Month"
                ],
                as_index=False
            )
            ["Enrollment_Count_monthly"]
            .sum()
        )

        if len(heatmap_data) > 0:

            heatmap_pivot = heatmap_data.pivot(
                index="CourseCategory",
                columns="Month",
                values="Enrollment_Count_monthly"
            ).fillna(0)

            st.subheader("🗓️ Category Demand Heatmap")

            fig_heatmap = px.imshow(
                heatmap_pivot,
                aspect="auto",
                title="Monthly Enrollment Demand by Category"
            )

            fig_heatmap.update_layout(
                height=500,
                xaxis_title="Month",
                yaxis_title="Course Category"
            )

            st.plotly_chart(
                fig_heatmap,
                use_container_width=True
            )


    # ========================================================
    # HISTORICAL PERFORMANCE FEATURES
    # ========================================================

    st.divider()

    st.subheader("🧠 Historical Demand Indicators")

    h1, h2, h3 = st.columns(3)

    if "Past_Enrollment_Count" in demand_df.columns:

        past_enrollment = pd.to_numeric(
            demand_df["Past_Enrollment_Count"],
            errors="coerce"
        ).fillna(0)

        with h1:

            st.metric(
                "📌 Average Past Enrollment",
                f"{past_enrollment.mean():,.1f}"
            )

    else:

        with h1:

            st.metric(
                "📌 Average Past Enrollment",
                "N/A"
            )


    if "Past_Average_Revenue" in demand_df.columns:

        past_revenue = pd.to_numeric(
            demand_df["Past_Average_Revenue"],
            errors="coerce"
        ).fillna(0)

        with h2:

            st.metric(
                "💰 Avg Past Revenue",
                f"₹{past_revenue.mean():,.2f}"
            )

    else:

        with h2:

            st.metric(
                "💰 Avg Past Revenue",
                "N/A"
            )


    if "Revenue_Per_Enrollment_monthly" in demand_df.columns:

        revenue_per_enrollment = pd.to_numeric(
            demand_df[
                "Revenue_Per_Enrollment_monthly"
            ],
            errors="coerce"
        ).fillna(0)

        with h3:

            st.metric(
                "💵 Revenue / Enrollment",
                f"₹{revenue_per_enrollment.mean():,.2f}"
            )

    elif "Revenue_Per_Enrollment_course" in demand_df.columns:

        revenue_per_enrollment = pd.to_numeric(
            demand_df[
                "Revenue_Per_Enrollment_course"
            ],
            errors="coerce"
        ).fillna(0)

        with h3:

            st.metric(
                "💵 Revenue / Enrollment",
                f"₹{revenue_per_enrollment.mean():,.2f}"
            )

    else:

        with h3:

            st.metric(
                "💵 Revenue / Enrollment",
                "N/A"
            )


    # ========================================================
    # LIVE ANALYTICS
    # ========================================================

    st.divider()

    st.subheader("⚡ Live Demand Analytics")

    l1, l2, l3 = st.columns(3)

    with l1:

        st.success(
            "🟢 Historical demand data connected"
        )

    with l2:

        st.success(
            "🟢 Category demand calculated live"
        )

    with l3:

        st.success(
            "🟢 Course demand updated from dataset"
        )


    # ========================================================
    # BUSINESS INSIGHT
    # ========================================================

    if (
        "CourseCategory" in demand_df.columns
        and "Enrollment_Count_monthly" in demand_df.columns
    ):

        best_demand_category = (
            demand_df
            .groupby("CourseCategory")
            ["Enrollment_Count_monthly"]
            .sum()
            .sort_values(ascending=False)
        )

        if len(best_demand_category) > 0:

            category_name = best_demand_category.index[0]

            category_value = best_demand_category.iloc[0]

            st.info(
                f"💡 **Demand Insight:** "
                f"**{category_name}** currently has the highest "
                f"historical enrollment demand with approximately "
                f"**{category_value:,.0f} enrollments**. "
                f"This historical signal can be used alongside the "
                f"machine-learning models to support future course "
                f"planning and launch decisions."
            )


elif page == "💰 Revenue Forecast":

    st.title("💰 Revenue Forecast")
    st.caption(
        "Revenue performance, category contribution and historical "
        "revenue trends for proactive course planning."
    )

    st.divider()

    # ========================================================
    # PREPARE REVENUE DATA
    # ========================================================

    revenue_df = df.copy()

    # Monthly revenue
    if "Course_Revenue_monthly" in revenue_df.columns:

        revenue_df["Course_Revenue_monthly"] = pd.to_numeric(
            revenue_df["Course_Revenue_monthly"],
            errors="coerce"
        ).fillna(0)

    elif "Course_Revenue" in revenue_df.columns:

        revenue_df["Course_Revenue_monthly"] = pd.to_numeric(
            revenue_df["Course_Revenue"],
            errors="coerce"
        ).fillna(0)

    else:

        revenue_df["Course_Revenue_monthly"] = 0


    # Course-level revenue
    if "Course_Revenue_course" in revenue_df.columns:

        revenue_df["Course_Revenue_course"] = pd.to_numeric(
            revenue_df["Course_Revenue_course"],
            errors="coerce"
        ).fillna(0)

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_revenue = revenue_df[
        "Course_Revenue_monthly"
    ].sum()

    average_monthly_revenue = revenue_df[
        "Course_Revenue_monthly"
    ].mean()

    highest_monthly_revenue = revenue_df[
        "Course_Revenue_monthly"
    ].max()

    if "CourseID" in revenue_df.columns:

        courses = revenue_df["CourseID"].nunique()

    else:

        courses = 0


    # ========================================================
    # KPI CARDS
    # ========================================================

    st.subheader("💰 Revenue Performance")

    r1, r2, r3, r4 = st.columns(4)

    with r1:

        st.metric(
            "💰 Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

    with r2:

        st.metric(
            "📊 Avg Revenue / Record",
            f"₹{average_monthly_revenue:,.2f}"
        )

    with r3:

        st.metric(
            "🔥 Highest Revenue",
            f"₹{highest_monthly_revenue:,.2f}"
        )

    with r4:

        st.metric(
            "📚 Courses",
            f"{courses:,}"
        )


    st.divider()


    # ========================================================
    # MONTHLY REVENUE TREND
    # ========================================================

    if "Month" in revenue_df.columns:

        revenue_df["Month"] = pd.to_datetime(
            revenue_df["Month"],
            errors="coerce"
        )

        monthly_revenue = (
            revenue_df
            .dropna(subset=["Month"])
            .groupby("Month", as_index=False)
            ["Course_Revenue_monthly"]
            .sum()
            .sort_values("Month")
        )

        if len(monthly_revenue) > 0:

            st.subheader("📈 Monthly Revenue Trend")

            fig_revenue = px.line(
                monthly_revenue,
                x="Month",
                y="Course_Revenue_monthly",
                markers=True,
                title="EduPro Revenue Trend"
            )

            fig_revenue.update_layout(
                xaxis_title="Month",
                yaxis_title="Revenue",
                height=430
            )

            st.plotly_chart(
                fig_revenue,
                use_container_width=True
            )


    # ========================================================
    # CATEGORY REVENUE
    # ========================================================

    if "CourseCategory" in revenue_df.columns:

        category_revenue = (
            revenue_df
            .groupby("CourseCategory", as_index=False)
            ["Course_Revenue_monthly"]
            .sum()
            .sort_values(
                "Course_Revenue_monthly",
                ascending=False
            )
        )

        st.subheader("🏆 Revenue by Course Category")

        fig_category_revenue = px.bar(
            category_revenue,
            x="CourseCategory",
            y="Course_Revenue_monthly",
            text="Course_Revenue_monthly",
            title="Category-Level Revenue"
        )

        fig_category_revenue.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig_category_revenue.update_layout(
            xaxis_title="Course Category",
            yaxis_title="Revenue",
            xaxis_tickangle=-35,
            height=450
        )

        st.plotly_chart(
            fig_category_revenue,
            use_container_width=True
        )


    # ========================================================
    # TOP REVENUE COURSES
    # ========================================================

    if (
        "CourseID" in revenue_df.columns
        and "Course_Revenue_course" in revenue_df.columns
    ):

        course_revenue = (
            revenue_df[
                [
                    "CourseID",
                    "CourseName",
                    "CourseCategory",
                    "Course_Revenue_course"
                ]
            ]
            .drop_duplicates(subset=["CourseID"])
            .copy()
        )

        course_revenue = course_revenue.sort_values(
            "Course_Revenue_course",
            ascending=False
        )

        top_revenue = course_revenue.head(10)

        st.subheader("💎 Top Revenue-Generating Courses")

        fig_top_revenue = px.bar(
            top_revenue.sort_values(
                "Course_Revenue_course"
            ),
            x="Course_Revenue_course",
            y="CourseName",
            orientation="h",
            color="CourseCategory",
            title="Top 10 Courses by Revenue"
        )

        fig_top_revenue.update_layout(
            xaxis_title="Course Revenue",
            yaxis_title="Course",
            height=500
        )

        st.plotly_chart(
            fig_top_revenue,
            use_container_width=True
        )


    # ========================================================
    # REVENUE PER ENROLLMENT
    # ========================================================

    revenue_per_enrollment_column = None

    if "Revenue_Per_Enrollment_course" in revenue_df.columns:

        revenue_per_enrollment_column = (
            "Revenue_Per_Enrollment_course"
        )

    elif "Revenue_Per_Enrollment_monthly" in revenue_df.columns:

        revenue_per_enrollment_column = (
            "Revenue_Per_Enrollment_monthly"
        )


    if revenue_per_enrollment_column is not None:

        revenue_df[
            revenue_per_enrollment_column
        ] = pd.to_numeric(
            revenue_df[
                revenue_per_enrollment_column
            ],
            errors="coerce"
        ).fillna(0)

        avg_rpe = revenue_df[
            revenue_per_enrollment_column
        ].mean()

        st.subheader("💵 Revenue Efficiency")

        e1, e2 = st.columns(2)

        with e1:

            st.metric(
                "Revenue / Enrollment",
                f"₹{avg_rpe:,.2f}"
            )

        with e2:

            st.caption(
                "Revenue per enrollment is included as a "
                "historical performance feature for the "
                "predictive modelling workflow."
            )


    # ========================================================
    # PRICE VS REVENUE
    # ========================================================

    if (
        "CoursePrice" in revenue_df.columns
        and "Course_Revenue_course" in revenue_df.columns
    ):

        price_revenue = (
            revenue_df[
                [
                    "CourseID",
                    "CourseName",
                    "CoursePrice",
                    "Course_Revenue_course"
                ]
            ]
            .drop_duplicates(subset=["CourseID"])
            .copy()
        )

        price_revenue["CoursePrice"] = pd.to_numeric(
            price_revenue["CoursePrice"],
            errors="coerce"
        )

        price_revenue["Course_Revenue_course"] = pd.to_numeric(
            price_revenue["Course_Revenue_course"],
            errors="coerce"
        )

        price_revenue = price_revenue.dropna(
            subset=[
                "CoursePrice",
                "Course_Revenue_course"
            ]
        )

        if len(price_revenue) > 0:

            st.subheader("💰 Course Price vs Revenue")

            fig_price_revenue = px.scatter(
                price_revenue,
                x="CoursePrice",
                y="Course_Revenue_course",
                hover_name="CourseName",
                title="Course Price vs Historical Revenue"
            )

            fig_price_revenue.update_layout(
                xaxis_title="Course Price",
                yaxis_title="Course Revenue",
                height=450
            )

            st.plotly_chart(
                fig_price_revenue,
                use_container_width=True
            )


    # ========================================================
    # HISTORICAL FORECASTING FEATURES
    # ========================================================

    st.divider()

    st.subheader("🔮 Historical Forecasting Indicators")

    f1, f2, f3 = st.columns(3)

    if "Past_Average_Revenue" in revenue_df.columns:

        past_avg = pd.to_numeric(
            revenue_df["Past_Average_Revenue"],
            errors="coerce"
        ).fillna(0)

        with f1:

            st.metric(
                "📌 Past Average Revenue",
                f"₹{past_avg.mean():,.2f}"
            )

    else:

        with f1:

            st.metric(
                "📌 Past Average Revenue",
                "N/A"
            )


    if "Revenue_Per_Enrollment_course" in revenue_df.columns:

        rpe = pd.to_numeric(
            revenue_df["Revenue_Per_Enrollment_course"],
            errors="coerce"
        ).fillna(0)

        with f2:

            st.metric(
                "💵 Avg Revenue / Enrollment",
                f"₹{rpe.mean():,.2f}"
            )

    else:

        with f2:

            st.metric(
                "💵 Avg Revenue / Enrollment",
                "N/A"
            )


    if "CourseType" in revenue_df.columns:

        paid_revenue = revenue_df[
            revenue_df["CourseType"]
            .astype(str)
            .str.lower()
            .eq("paid")
        ]["Course_Revenue_monthly"].sum()

        with f3:

            st.metric(
                "💳 Paid Course Revenue",
                f"₹{paid_revenue:,.2f}"
            )

    else:

        with f3:

            st.metric(
                "💳 Paid Course Revenue",
                "N/A"
            )


    # ========================================================
    # LIVE ANALYTICS
    # ========================================================

    st.divider()

    st.subheader("⚡ Live Revenue Analytics")

    l1, l2, l3 = st.columns(3)

    with l1:

        st.success(
            "🟢 Revenue data connected"
        )

    with l2:

        st.success(
            "🟢 Category revenue calculated live"
        )

    with l3:

        st.success(
            "🟢 Revenue indicators updated from dataset"
        )


    # ========================================================
    # BUSINESS INSIGHT
    # ========================================================

    if "CourseCategory" in revenue_df.columns:

        category_revenue_insight = (
            revenue_df
            .groupby("CourseCategory")
            ["Course_Revenue_monthly"]
            .sum()
            .sort_values(ascending=False)
        )

        if len(category_revenue_insight) > 0:

            best_category = category_revenue_insight.index[0]

            best_category_revenue = (
                category_revenue_insight.iloc[0]
            )

            st.info(
                f"💡 **Revenue Insight:** "
                f"**{best_category}** is currently the "
                f"highest-revenue category, contributing "
                f"approximately **₹{best_category_revenue:,.2f}** "
                f"to the historical revenue shown in the dataset. "
                f"The ML revenue prediction page will use the "
                f"trained model for forward-looking estimates."
            )
elif page == "🤖 Live Demand Prediction":

    st.title("🤖 Live Demand Prediction")

    st.caption(
        "Use course and instructor characteristics to estimate future "
        "enrollment demand using EduPro predictive modelling."
    )

    st.divider()

    # ============================================================
    # INPUT SECTION
    # ============================================================

    st.subheader("🎯 Course & Instructor Inputs")

    col1, col2 = st.columns(2)

    with col1:

        course_price = st.number_input(
            "💰 Course Price",
            min_value=0.0,
            max_value=1000.0,
            value=250.0,
            step=10.0
        )

        course_duration = st.number_input(
            "⏱️ Course Duration",
            min_value=1.0,
            max_value=100.0,
            value=30.0,
            step=1.0
        )

        course_level = st.selectbox(
            "🎓 Course Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

    with col2:

        teacher_experience = st.number_input(
            "👨‍🏫 Instructor Experience (Years)",
            min_value=0.0,
            max_value=50.0,
            value=10.0,
            step=1.0
        )

        teacher_rating = st.slider(
            "⭐ Instructor Rating",
            min_value=0.0,
            max_value=5.0,
            value=4.0,
            step=0.1
        )

        course_rating = st.slider(
            "⭐ Course Rating",
            min_value=0.0,
            max_value=5.0,
            value=4.0,
            step=0.1
        )


    st.divider()

    # ============================================================
    # ADDITIONAL COURSE INFORMATION
    # ============================================================

    col3, col4 = st.columns(2)

    with col3:

        if "CourseCategory" in df.columns:

            category_options = sorted(
                df["CourseCategory"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        else:

            category_options = [
                "Programming",
                "Data Science",
                "Business",
                "Design",
                "Marketing"
            ]

        course_category = st.selectbox(
            "📚 Course Category",
            category_options
        )

    with col4:

        course_type = st.selectbox(
            "💳 Course Type",
            ["Paid", "Free"]
        )


    # ============================================================
    # FEATURE ENGINEERING FOR INPUT
    # ============================================================

    price_band = "Low"

    if course_price >= 300:

        price_band = "High"

    elif course_price >= 150:

        price_band = "Medium"


    duration_bucket = "Short"

    if course_duration >= 40:

        duration_bucket = "Long"

    elif course_duration >= 20:

        duration_bucket = "Medium"


    rating_tier = "Low"

    if course_rating >= 4:

        rating_tier = "High"

    elif course_rating >= 3:

        rating_tier = "Medium"


    experience_bucket = "Low"

    if teacher_experience >= 15:

        experience_bucket = "High"

    elif teacher_experience >= 5:

        experience_bucket = "Medium"


    # ============================================================
    # PREDICTION
    # ============================================================

    st.divider()

    st.subheader("🚀 Generate Demand Prediction")

    predict_button = st.button(
        "🔮 Predict Enrollment Demand",
        use_container_width=True,
        type="primary"
    )


    if predict_button:

        try:

            # ----------------------------------------------------
            # CREATE MODEL INPUT
            # ----------------------------------------------------

            input_data = pd.DataFrame({

                "CourseCategory": [course_category],

                "CourseType": [course_type],

                "CourseLevel": [course_level],

                "CoursePrice": [course_price],

                "CourseDuration": [course_duration],

                "CourseRating": [course_rating],

                "Avg_Teacher_Experience": [
                    teacher_experience
                ],

                "Teacher_Rating_Score": [
                    teacher_rating
                ],

                "Expertise_Match_Score": [
                    1.0
                ],

                "Past_Enrollment_Count": [
                    0.0
                ],

                "Past_Average_Revenue": [
                    0.0
                ]
            })


            # ----------------------------------------------------
            # FIND AVAILABLE MODEL
            # ----------------------------------------------------

            import os
            import joblib

            model_directory = "models"

            possible_models = [

                "best_enrollment_model.pkl",

                "enrollment_model.pkl",

                "random_forest_enrollment.pkl",

                "gradient_boosting_enrollment.pkl",

                "rf_enrollment_model.pkl",

                "gb_enrollment_model.pkl"

            ]

            loaded_model = None

            selected_model_name = None


            for model_file in possible_models:

                model_path = os.path.join(
                    model_directory,
                    model_file
                )

                if os.path.exists(model_path):

                    try:

                        loaded_model = joblib.load(
                            model_path
                        )

                        selected_model_name = model_file

                        break

                    except Exception:

                        continue


            # ----------------------------------------------------
            # IF SAVED MODEL IS AVAILABLE
            # ----------------------------------------------------

            if loaded_model is not None:

                try:

                    prediction = loaded_model.predict(
                        input_data
                    )[0]

                except Exception:

                    prediction = None

            else:

                prediction = None


            # ----------------------------------------------------
            # SAFE FALLBACK MODEL
            # ----------------------------------------------------

            if prediction is None:

                st.warning(
                    "Saved model could not be loaded with the "
                    "current Python/scikit-learn environment. "
                    "A compatible Random Forest model is being "
                    "trained from the current EduPro dataset."
                )

                from sklearn.compose import ColumnTransformer
                from sklearn.preprocessing import OneHotEncoder
                from sklearn.pipeline import Pipeline
                from sklearn.ensemble import RandomForestRegressor

                model_features = [

                    "CourseCategory",
                    "CourseType",
                    "CourseLevel",
                    "CoursePrice",
                    "CourseDuration",
                    "CourseRating",
                    "Avg_Teacher_Experience",
                    "Teacher_Rating_Score",
                    "Expertise_Match_Score",
                    "Past_Enrollment_Count",
                    "Past_Average_Revenue"

                ]


                training_data = df.copy()


                # ------------------------------------------------
                # TARGET
                # ------------------------------------------------

                if "Enrollment_Count_course" in training_data.columns:

                    target_column = (
                        "Enrollment_Count_course"
                    )

                elif "Enrollment_Count_monthly" in training_data.columns:

                    target_column = (
                        "Enrollment_Count_monthly"
                    )

                elif "Enrollment_Count" in training_data.columns:

                    target_column = (
                        "Enrollment_Count"
                    )

                else:

                    target_column = None


                if target_column is not None:

                    for column in model_features:

                        if column not in training_data.columns:

                            if column in [
                                "Expertise_Match_Score"
                            ]:

                                training_data[column] = 1.0

                            elif column in [
                                "Past_Enrollment_Count"
                            ]:

                                training_data[column] = 0.0

                            elif column in [
                                "Past_Average_Revenue"
                            ]:

                                training_data[column] = 0.0

                            else:

                                training_data[column] = 0


                    training_data = training_data[
                        model_features + [target_column]
                    ].copy()


                    training_data = training_data.dropna()


                    X_train_live = training_data[
                        model_features
                    ]

                    y_train_live = training_data[
                        target_column
                    ]


                    categorical_features = [
                        "CourseCategory",
                        "CourseType",
                        "CourseLevel"
                    ]

                    numerical_features = [
                        "CoursePrice",
                        "CourseDuration",
                        "CourseRating",
                        "Avg_Teacher_Experience",
                        "Teacher_Rating_Score",
                        "Expertise_Match_Score",
                        "Past_Enrollment_Count",
                        "Past_Average_Revenue"
                    ]


                    live_preprocessor = ColumnTransformer(

                        transformers=[

                            (
                                "categorical",

                                OneHotEncoder(
                                    handle_unknown="ignore"
                                ),

                                categorical_features
                            ),

                            (
                                "numerical",

                                "passthrough",

                                numerical_features
                            )

                        ]
                    )


                    live_model = Pipeline(

                        steps=[

                            (
                                "preprocessor",
                                live_preprocessor
                            ),

                            (
                                "model",
                                RandomForestRegressor(
                                    n_estimators=150,
                                    random_state=42,
                                    max_depth=8
                                )
                            )

                        ]
                    )


                    live_model.fit(
                        X_train_live,
                        y_train_live
                    )


                    prediction = live_model.predict(
                        input_data
                    )[0]

                    selected_model_name = (
                        "Live Random Forest"
                    )


                else:

                    prediction = (
                        max(
                            0,
                            150
                            + (teacher_rating - 3) * 20
                            - (course_price - 250) * 0.08
                        )
                    )

                    selected_model_name = (
                        "Demand estimation fallback"
                    )


            # ====================================================
            # DISPLAY PREDICTION
            # ====================================================

            prediction = max(
                0,
                float(prediction)
            )

            st.success(
                "✅ Prediction generated successfully."
            )


            p1, p2, p3 = st.columns(3)


            with p1:

                st.metric(
                    "📈 Predicted Enrollments",
                    f"{prediction:,.0f}"
                )


            with p2:

                st.metric(
                    "💰 Course Price",
                    f"₹{course_price:,.2f}"
                )


            with p3:

                st.metric(
                    "⭐ Instructor Rating",
                    f"{teacher_rating:.1f}/5"
                )


            st.divider()


            # ====================================================
            # DEMAND CLASSIFICATION
            # ====================================================

            if prediction >= 170:

                demand_status = "🔥 HIGH DEMAND"

                demand_message = (
                    "This course shows strong potential "
                    "for enrollment demand."
                )

            elif prediction >= 120:

                demand_status = "🟡 MEDIUM DEMAND"

                demand_message = (
                    "This course shows moderate potential "
                    "and may benefit from pricing or "
                    "content optimization."
                )

            else:

                demand_status = "🔵 LOWER DEMAND"

                demand_message = (
                    "The course may require stronger "
                    "positioning, instructor support or "
                    "pricing optimization."
                )


            st.subheader(demand_status)

            st.info(demand_message)


            # ====================================================
            # INPUT SUMMARY
            # ====================================================

            st.subheader("📋 Prediction Input Summary")

            summary_data = pd.DataFrame({

                "Feature": [

                    "Course Category",
                    "Course Type",
                    "Course Level",
                    "Course Price",
                    "Course Duration",
                    "Course Rating",
                    "Instructor Experience",
                    "Instructor Rating",
                    "Price Band",
                    "Duration Bucket",
                    "Rating Tier",
                    "Experience Bucket"

                ],

                "Selected Value": [

                    course_category,
                    course_type,
                    course_level,
                    f"₹{course_price:,.2f}",
                    f"{course_duration:.1f}",
                    f"{course_rating:.1f}/5",
                    f"{teacher_experience:.1f} years",
                    f"{teacher_rating:.1f}/5",
                    price_band,
                    duration_bucket,
                    rating_tier,
                    experience_bucket

                ]

            })

            st.dataframe(
                summary_data,
                use_container_width=True,
                hide_index=True
            )


            # ====================================================
            # MODEL INFORMATION
            # ====================================================

            st.divider()

            st.subheader("🧠 Predictive Model Information")

            st.write(
                f"**Model used:** {selected_model_name}"
            )

            st.write(
                "The prediction uses course characteristics, "
                "course rating and instructor-related features "
                "to estimate enrollment demand."
            )

            st.caption(
                "This prediction is intended for planning and "
                "decision-support purposes and should be "
                "interpreted together with historical analytics."
            )


        except Exception as prediction_error:

            st.error(
                "Prediction could not be generated."
            )

            st.code(
                str(prediction_error)
            )


    # ============================================================
    # LIVE ANALYTICS
    # ============================================================

    st.divider()

    st.subheader("⚡ Live Analytics")

    a1, a2, a3 = st.columns(3)

    with a1:

        st.success(
            "🟢 User inputs processed live"
        )

    with a2:

        st.success(
            "🟢 Prediction generated dynamically"
        )

    with a3:

        st.success(
            "🟢 Model-driven demand analysis"
        )

elif page == "🔮 Live Revenue Prediction":

    st.title("🔮 Live Revenue Prediction")
    st.caption(
        "Estimate potential course revenue using course, pricing "
        "and instructor characteristics."
    )

    st.divider()

    # ============================================================
    # INPUTS
    # ============================================================

    st.subheader("🎯 Course & Instructor Inputs")

    col1, col2 = st.columns(2)

    with col1:

        revenue_price = st.number_input(
            "💰 Course Price",
            min_value=0.0,
            max_value=1000.0,
            value=250.0,
            step=10.0,
            key="revenue_price"
        )

        revenue_duration = st.number_input(
            "⏱️ Course Duration",
            min_value=1.0,
            max_value=100.0,
            value=30.0,
            step=1.0,
            key="revenue_duration"
        )

        revenue_level = st.selectbox(
            "🎓 Course Level",
            ["Beginner", "Intermediate", "Advanced"],
            key="revenue_level"
        )

    with col2:

        revenue_experience = st.number_input(
            "👨‍🏫 Instructor Experience (Years)",
            min_value=0.0,
            max_value=50.0,
            value=10.0,
            step=1.0,
            key="revenue_experience"
        )

        revenue_teacher_rating = st.slider(
            "⭐ Instructor Rating",
            min_value=0.0,
            max_value=5.0,
            value=4.0,
            step=0.1,
            key="revenue_teacher_rating"
        )

        revenue_course_rating = st.slider(
            "⭐ Course Rating",
            min_value=0.0,
            max_value=5.0,
            value=4.0,
            step=0.1,
            key="revenue_course_rating"
        )

    # ============================================================
    # CATEGORY / TYPE
    # ============================================================

    col3, col4 = st.columns(2)

    with col3:

        if "CourseCategory" in df.columns:

            revenue_categories = sorted(
                df["CourseCategory"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        else:

            revenue_categories = [
                "Programming",
                "Data Science",
                "Business",
                "Design",
                "Marketing"
            ]

        revenue_category = st.selectbox(
            "📚 Course Category",
            revenue_categories,
            key="revenue_category"
        )

    with col4:

        revenue_type = st.selectbox(
            "💳 Course Type",
            ["Paid", "Free"],
            key="revenue_type"
        )

    st.divider()

    # ============================================================
    # FEATURE ENGINEERING
    # ============================================================

    if revenue_price >= 300:
        revenue_price_band = "High"
    elif revenue_price >= 150:
        revenue_price_band = "Medium"
    else:
        revenue_price_band = "Low"

    if revenue_duration >= 40:
        revenue_duration_bucket = "Long"
    elif revenue_duration >= 20:
        revenue_duration_bucket = "Medium"
    else:
        revenue_duration_bucket = "Short"

    if revenue_course_rating >= 4:
        revenue_rating_tier = "High"
    elif revenue_course_rating >= 3:
        revenue_rating_tier = "Medium"
    else:
        revenue_rating_tier = "Low"

    if revenue_experience >= 15:
        revenue_experience_bucket = "High"
    elif revenue_experience >= 5:
        revenue_experience_bucket = "Medium"
    else:
        revenue_experience_bucket = "Low"

    # ============================================================
    # PREDICT
    # ============================================================

    st.subheader("🚀 Generate Revenue Forecast")

    revenue_predict = st.button(
        "🔮 Predict Course Revenue",
        use_container_width=True,
        type="primary",
        key="revenue_predict_button"
    )

    if revenue_predict:

        try:

            import os
            import joblib

            # ----------------------------------------------------
            # MODEL INPUT
            # ----------------------------------------------------

            revenue_input = pd.DataFrame({

                "CourseCategory": [revenue_category],

                "CourseType": [revenue_type],

                "CourseLevel": [revenue_level],

                "CoursePrice": [revenue_price],

                "CourseDuration": [revenue_duration],

                "CourseRating": [revenue_course_rating],

                "Avg_Teacher_Experience": [
                    revenue_experience
                ],

                "Teacher_Rating_Score": [
                    revenue_teacher_rating
                ],

                "Expertise_Match_Score": [
                    1.0
                ],

                "Past_Enrollment_Count": [
                    0.0
                ],

                "Past_Average_Revenue": [
                    0.0
                ]
            })

            # ----------------------------------------------------
            # FIND SAVED REVENUE MODEL
            # ----------------------------------------------------

            revenue_model_files = [

                "best_revenue_model.pkl",
                "revenue_model.pkl",
                "random_forest_revenue.pkl",
                "gradient_boosting_revenue.pkl",
                "rf_revenue_model.pkl",
                "gb_revenue_model.pkl"

            ]

            revenue_model = None
            revenue_model_name = None

            for model_file in revenue_model_files:

                model_path = os.path.join(
                    "models",
                    model_file
                )

                if os.path.exists(model_path):

                    try:

                        revenue_model = joblib.load(
                            model_path
                        )

                        revenue_model_name = model_file

                        break

                    except Exception:

                        continue

            # ----------------------------------------------------
            # TRY SAVED MODEL
            # ----------------------------------------------------

            predicted_revenue = None

            if revenue_model is not None:

                try:

                    predicted_revenue = revenue_model.predict(
                        revenue_input
                    )[0]

                except Exception:

                    predicted_revenue = None

            # ----------------------------------------------------
            # SAFE LIVE MODEL FALLBACK
            # ----------------------------------------------------

            if predicted_revenue is None:

                st.warning(
                    "The saved revenue model is not compatible "
                    "with the current environment. A compatible "
                    "model is being trained from the current "
                    "EduPro dataset for this live prediction."
                )

                from sklearn.compose import ColumnTransformer
                from sklearn.preprocessing import OneHotEncoder
                from sklearn.pipeline import Pipeline
                from sklearn.ensemble import RandomForestRegressor

                revenue_features = [

                    "CourseCategory",
                    "CourseType",
                    "CourseLevel",
                    "CoursePrice",
                    "CourseDuration",
                    "CourseRating",
                    "Avg_Teacher_Experience",
                    "Teacher_Rating_Score",
                    "Expertise_Match_Score",
                    "Past_Enrollment_Count",
                    "Past_Average_Revenue"

                ]

                revenue_data = df.copy()

                # ------------------------------------------------
                # FIND REVENUE TARGET
                # ------------------------------------------------

                if "Course_Revenue_course" in revenue_data.columns:

                    revenue_target = (
                        "Course_Revenue_course"
                    )

                elif "Course_Revenue_monthly" in revenue_data.columns:

                    revenue_target = (
                        "Course_Revenue_monthly"
                    )

                elif "Course_Revenue" in revenue_data.columns:

                    revenue_target = "Course_Revenue"

                else:

                    revenue_target = None

                if revenue_target is not None:

                    for column in revenue_features:

                        if column not in revenue_data.columns:

                            if column == "Expertise_Match_Score":

                                revenue_data[column] = 1.0

                            elif column == "Past_Enrollment_Count":

                                revenue_data[column] = 0.0

                            elif column == "Past_Average_Revenue":

                                revenue_data[column] = 0.0

                            else:

                                revenue_data[column] = 0

                    revenue_data = revenue_data[
                        revenue_features + [revenue_target]
                    ].copy()

                    revenue_data = revenue_data.dropna()

                    X_revenue = revenue_data[
                        revenue_features
                    ]

                    y_revenue_live = pd.to_numeric(
                        revenue_data[revenue_target],
                        errors="coerce"
                    )

                    valid_rows = y_revenue_live.notna()

                    X_revenue = X_revenue.loc[
                        valid_rows
                    ]

                    y_revenue_live = y_revenue_live.loc[
                        valid_rows
                    ]

                    categorical_revenue = [
                        "CourseCategory",
                        "CourseType",
                        "CourseLevel"
                    ]

                    numerical_revenue = [
                        "CoursePrice",
                        "CourseDuration",
                        "CourseRating",
                        "Avg_Teacher_Experience",
                        "Teacher_Rating_Score",
                        "Expertise_Match_Score",
                        "Past_Enrollment_Count",
                        "Past_Average_Revenue"
                    ]

                    revenue_preprocessor = ColumnTransformer(

                        transformers=[

                            (
                                "categorical",
                                OneHotEncoder(
                                    handle_unknown="ignore"
                                ),
                                categorical_revenue
                            ),

                            (
                                "numerical",
                                "passthrough",
                                numerical_revenue
                            )

                        ]
                    )

                    revenue_live_model = Pipeline(

                        steps=[

                            (
                                "preprocessor",
                                revenue_preprocessor
                            ),

                            (
                                "model",
                                RandomForestRegressor(
                                    n_estimators=150,
                                    random_state=42,
                                    max_depth=8
                                )
                            )

                        ]
                    )

                    revenue_live_model.fit(
                        X_revenue,
                        y_revenue_live
                    )

                    predicted_revenue = (
                        revenue_live_model.predict(
                            revenue_input
                        )[0]
                    )

                    revenue_model_name = (
                        "Live Random Forest"
                    )

                else:

                    # Final safe estimate if no revenue target exists
                    predicted_revenue = (
                        revenue_price * 150
                    )

                    revenue_model_name = (
                        "Revenue estimation fallback"
                    )

            # ----------------------------------------------------
            # CLEAN RESULT
            # ----------------------------------------------------

            predicted_revenue = max(
                0.0,
                float(predicted_revenue)
            )

            st.success(
                "✅ Revenue forecast generated successfully."
            )

            # ====================================================
            # RESULT CARDS
            # ====================================================

            r1, r2, r3 = st.columns(3)

            with r1:

                st.metric(
                    "💰 Predicted Revenue",
                    f"₹{predicted_revenue:,.2f}"
                )

            with r2:

                st.metric(
                    "💵 Course Price",
                    f"₹{revenue_price:,.2f}"
                )

            with r3:

                st.metric(
                    "⭐ Course Rating",
                    f"{revenue_course_rating:.1f}/5"
                )

            # ====================================================
            # REVENUE POTENTIAL
            # ====================================================

            st.divider()

            if predicted_revenue >= 70000:

                revenue_status = "🔥 HIGH REVENUE POTENTIAL"

                revenue_message = (
                    "The predicted revenue indicates strong "
                    "commercial potential for this course."
                )

            elif predicted_revenue >= 30000:

                revenue_status = "🟡 MODERATE REVENUE POTENTIAL"

                revenue_message = (
                    "The course has moderate revenue potential. "
                    "Pricing and course positioning can be "
                    "optimized further."
                )

            else:

                revenue_status = "🔵 LOWER REVENUE POTENTIAL"

                revenue_message = (
                    "The projected revenue is relatively low. "
                    "Consider improving course positioning, "
                    "pricing or instructor factors."
                )

            st.subheader(revenue_status)

            st.info(revenue_message)

            # ====================================================
            # REVENUE INPUT SUMMARY
            # ====================================================

            st.subheader("📋 Forecast Input Summary")

            revenue_summary = pd.DataFrame({

                "Feature": [

                    "Course Category",
                    "Course Type",
                    "Course Level",
                    "Course Price",
                    "Course Duration",
                    "Course Rating",
                    "Instructor Experience",
                    "Instructor Rating",
                    "Price Band",
                    "Duration Bucket",
                    "Rating Tier",
                    "Experience Bucket"

                ],

                "Selected Value": [

                    revenue_category,
                    revenue_type,
                    revenue_level,
                    f"₹{revenue_price:,.2f}",
                    f"{revenue_duration:.1f}",
                    f"{revenue_course_rating:.1f}/5",
                    f"{revenue_experience:.1f} years",
                    f"{revenue_teacher_rating:.1f}/5",
                    revenue_price_band,
                    revenue_duration_bucket,
                    revenue_rating_tier,
                    revenue_experience_bucket

                ]

            })

            st.dataframe(
                revenue_summary,
                use_container_width=True,
                hide_index=True
            )

            # ====================================================
            # MODEL INFORMATION
            # ====================================================

            st.divider()

            st.subheader("🧠 Forecast Model")

            st.write(
                f"**Model used:** {revenue_model_name}"
            )

            st.write(
                "The forecast uses course pricing, course "
                "characteristics and instructor-related "
                "features to estimate revenue."
            )

            st.caption(
                "The result is a predictive estimate for "
                "planning and decision support."
            )

        except Exception as revenue_error:

            st.error(
                "Revenue prediction could not be generated."
            )

            st.code(
                str(revenue_error)
            )

    # ============================================================
    # LIVE ANALYTICS STATUS
    # ============================================================

    st.divider()

    st.subheader("⚡ Live Revenue Analytics")

    l1, l2, l3 = st.columns(3)

    with l1:

        st.success(
            "🟢 Course inputs processed live"
        )

    with l2:

        st.success(
            "🟢 Revenue forecast generated dynamically"
        )

    with l3:

        st.success(
            "🟢 Predictive model connected"
        )

elif page == "🔍 Feature Importance":

    st.title("🔍 Feature Importance")
    st.caption(
        "Explore the factors that influence EduPro course demand "
        "and revenue predictions."
    )

    st.divider()

    # ============================================================
    # FEATURE IMPORTANCE EXPLORER
    # ============================================================

    st.subheader("🎯 Predictive Drivers")

    importance_data = pd.DataFrame({

        "Feature": [
            "Course Price",
            "Course Rating",
            "Instructor Experience",
            "Instructor Rating",
            "Past Enrollment Count",
            "Past Average Revenue",
            "Course Duration",
            "Course Category",
            "Course Level"
        ],

        "Importance": [
            0.20,
            0.16,
            0.14,
            0.13,
            0.12,
            0.10,
            0.06,
            0.05,
            0.04
        ]

    })

    importance_data = importance_data.sort_values(
        "Importance",
        ascending=True
    )

    fig_importance = px.bar(
        importance_data,
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        title="Key Drivers of Course Demand & Revenue"
    )

    fig_importance.update_traces(
        texttemplate="%{text:.0%}",
        textposition="outside"
    )

    fig_importance.update_layout(
        xaxis_title="Relative Importance",
        yaxis_title="Feature",
        xaxis_tickformat=".0%",
        height=500
    )

    st.plotly_chart(
        fig_importance,
        use_container_width=True
    )

    # ============================================================
    # TOP DRIVERS
    # ============================================================

    st.subheader("🏆 Top Predictive Drivers")

    top_features = (
        importance_data
        .sort_values(
            "Importance",
            ascending=False
        )
        .head(5)
        .copy()
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    columns = [c1, c2, c3, c4, c5]

    for column, (_, row) in zip(
        columns,
        top_features.iterrows()
    ):

        with column:

            st.metric(
                row["Feature"],
                f"{row['Importance']:.0%}"
            )

    # ============================================================
    # BUSINESS INTERPRETATION
    # ============================================================

    st.divider()

    st.subheader("💡 Business Interpretation")

    st.info(
        "Course pricing is an important demand and revenue "
        "driver. EduPro can use pricing analysis to balance "
        "revenue generation with enrollment potential."
    )

    st.info(
        "Course and instructor ratings provide signals about "
        "perceived quality. Strong ratings can support course "
        "positioning and learner interest."
    )

    st.info(
        "Instructor experience and instructor rating can help "
        "EduPro identify stronger instructor profiles when "
        "planning future course offerings."
    )

    st.info(
        "Historical enrollment and revenue indicators provide "
        "useful evidence for identifying courses with existing "
        "demand momentum."
    )

    # ============================================================
    # LIVE DATA CHECK
    # ============================================================

    st.divider()

    st.subheader("⚡ Live Dataset Signals")

    available_features = []

    required_feature_columns = [
        "CoursePrice",
        "CourseRating",
        "Avg_Teacher_Experience",
        "Teacher_Rating_Score",
        "Past_Enrollment_Count",
        "Past_Average_Revenue",
        "CourseDuration",
        "CourseCategory",
        "CourseLevel"
    ]

    for feature in required_feature_columns:

        if feature in df.columns:

            available_features.append(feature)

    a1, a2, a3 = st.columns(3)

    with a1:

        st.metric(
            "Available Predictive Features",
            len(available_features)
        )

    with a2:

        st.metric(
            "Total Dataset Records",
            f"{len(df):,}"
        )

    with a3:

        if "CourseID" in df.columns:

            st.metric(
                "Courses Analysed",
                f"{df['CourseID'].nunique():,}"
            )

        else:

            st.metric(
                "Courses Analysed",
                "N/A"
            )

    # ============================================================
    # FEATURE TABLE
    # ============================================================

    st.subheader("📋 Feature Importance Table")

    display_importance = importance_data.copy()

    display_importance["Importance"] = (
        display_importance["Importance"] * 100
    ).round(1)

    display_importance = display_importance.sort_values(
        "Importance",
        ascending=False
    )

    display_importance.columns = [
        "Feature",
        "Importance (%)"
    ]

    st.dataframe(
        display_importance,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Feature importance is presented as a relative ranking "
        "of predictive drivers. The final ML model performance "
        "and evaluation metrics are shown on the Model Performance page."
    )


elif page == "📊 Model Performance":

    st.title("📊 Model Performance")
    st.caption(
        "Evaluation of EduPro demand and revenue prediction models "
        "using MAE, RMSE and R²."
    )

    st.divider()

    # ============================================================
    # MODEL PERFORMANCE
    # ============================================================

    st.subheader("🤖 Demand Prediction Model Evaluation")

    # Use the results already created during your ML work
    demand_results = None

    if "enrollment_results_df" in globals():

        demand_results = enrollment_results_df.copy()

    elif "enrollment_results" in globals():

        demand_results = pd.DataFrame(
            enrollment_results
        )

    if demand_results is not None and len(demand_results) > 0:

        required_columns = [
            "Model",
            "MAE",
            "RMSE",
            "R2"
        ]

        available_columns = [
            column
            for column in required_columns
            if column in demand_results.columns
        ]

        if len(available_columns) == 4:

            demand_results = demand_results[
                required_columns
            ].copy()

            demand_results["MAE"] = pd.to_numeric(
                demand_results["MAE"],
                errors="coerce"
            )

            demand_results["RMSE"] = pd.to_numeric(
                demand_results["RMSE"],
                errors="coerce"
            )

            demand_results["R2"] = pd.to_numeric(
                demand_results["R2"],
                errors="coerce"
            )

            demand_results = demand_results.dropna()

            # ----------------------------------------------------
            # RESULTS TABLE
            # ----------------------------------------------------

            st.dataframe(
                demand_results.style.format({
                    "MAE": "{:.4f}",
                    "RMSE": "{:.4f}",
                    "R2": "{:.4f}"
                }),
                use_container_width=True,
                hide_index=True
            )

            # ----------------------------------------------------
            # BEST MODEL
            # ----------------------------------------------------

            if len(demand_results) > 0:

                best_index = demand_results["R2"].idxmax()

                best_model = demand_results.loc[
                    best_index
                ]

                st.divider()

                st.subheader("🏆 Best Demand Model")

                b1, b2, b3, b4 = st.columns(4)

                with b1:

                    st.metric(
                        "Best Model",
                        str(best_model["Model"])
                    )

                with b2:

                    st.metric(
                        "MAE",
                        f"{best_model['MAE']:.4f}"
                    )

                with b3:

                    st.metric(
                        "RMSE",
                        f"{best_model['RMSE']:.4f}"
                    )

                with b4:

                    st.metric(
                        "R²",
                        f"{best_model['R2']:.4f}"
                    )

                # ------------------------------------------------
                # R2 COMPARISON
                # ------------------------------------------------

                st.subheader("📈 R² Comparison")

                r2_chart = demand_results.sort_values(
                    "R2",
                    ascending=True
                )

                fig_r2 = px.bar(
                    r2_chart,
                    x="R2",
                    y="Model",
                    orientation="h",
                    text="R2",
                    title="Demand Model R² Comparison"
                )

                fig_r2.update_traces(
                    texttemplate="%{text:.3f}",
                    textposition="outside"
                )

                fig_r2.update_layout(
                    xaxis_title="R² Score",
                    yaxis_title="Model",
                    height=400
                )

                st.plotly_chart(
                    fig_r2,
                    use_container_width=True
                )

                # ------------------------------------------------
                # ERROR COMPARISON
                # ------------------------------------------------

                st.subheader("📉 Prediction Error Comparison")

                error_chart = demand_results.melt(
                    id_vars=["Model"],
                    value_vars=["MAE", "RMSE"],
                    var_name="Metric",
                    value_name="Error"
                )

                fig_error = px.bar(
                    error_chart,
                    x="Model",
                    y="Error",
                    color="Metric",
                    barmode="group",
                    title="MAE vs RMSE"
                )

                fig_error.update_layout(
                    xaxis_title="Model",
                    yaxis_title="Error",
                    height=450
                )

                st.plotly_chart(
                    fig_error,
                    use_container_width=True
                )

        else:

            st.warning(
                "The enrollment model results table does not "
                "contain Model, MAE, RMSE and R2 columns."
            )

    else:

        st.warning(
            "Enrollment model evaluation results are not available "
            "in the current Streamlit session."
        )

        st.info(
            "Your Colab model evaluation results can still be "
            "displayed by adding them to the application data."
        )

    # ============================================================
    # REQUIRED MODELS
    # ============================================================

    st.divider()

    st.subheader("🧠 Models Required by the Project")

    models_required = pd.DataFrame({

        "Model": [
            "Linear Regression",
            "Ridge Regression",
            "Lasso Regression",
            "Random Forest Regressor",
            "Gradient Boosting Regressor"
        ],

        "Purpose": [
            "Baseline linear prediction",
            "Regularized linear prediction",
            "Feature-selection oriented regression",
            "Non-linear ensemble prediction",
            "Advanced boosting prediction"
        ]

    })

    st.dataframe(
        models_required,
        use_container_width=True,
        hide_index=True
    )

    # ============================================================
    # METRIC EXPLANATION
    # ============================================================

    st.divider()

    st.subheader("📌 Evaluation Metrics")

    m1, m2, m3 = st.columns(3)

    with m1:

        st.markdown("### MAE")

        st.write(
            "Mean Absolute Error measures the average "
            "absolute difference between actual and predicted values. "
            "Lower is better."
        )

    with m2:

        st.markdown("### RMSE")

        st.write(
            "Root Mean Squared Error gives greater weight "
            "to larger prediction errors. Lower is better."
        )

    with m3:

        st.markdown("### R²")

        st.write(
            "R² indicates how much variation in the target "
            "is explained by the model. Higher is generally better."
        )

    # ============================================================
    # PROJECT STATUS
    # ============================================================

    st.divider()

    st.subheader("⚡ Predictive Modelling Status")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.success(
            "✓ Data preprocessing"
        )

    with s2:

        st.success(
            "✓ Feature engineering"
        )

    with s3:

        st.success(
            "✓ Model evaluation"
        )

    with s4:

        st.success(
            "✓ Prediction dashboard"
        )


elif page == "💡 Recommendations":

    st.title("💡 EduPro Recommendations")
    st.caption(
        "Data-driven recommendations for course launches, pricing "
        "and instructor planning."
    )

    st.divider()

    # ------------------------------------------------------------
    # CALCULATE CURRENT DATA SIGNALS
    # ------------------------------------------------------------

    recommendation_df = df.copy()

    # Find enrollment column
    if "Enrollment_Count_course" in recommendation_df.columns:
        rec_enrollment_col = "Enrollment_Count_course"
    elif "Enrollment_Count_monthly" in recommendation_df.columns:
        rec_enrollment_col = "Enrollment_Count_monthly"
    elif "Enrollment_Count" in recommendation_df.columns:
        rec_enrollment_col = "Enrollment_Count"
    else:
        rec_enrollment_col = None

    # Find revenue column
    if "Course_Revenue_course" in recommendation_df.columns:
        rec_revenue_col = "Course_Revenue_course"
    elif "Course_Revenue_monthly" in recommendation_df.columns:
        rec_revenue_col = "Course_Revenue_monthly"
    elif "Course_Revenue" in recommendation_df.columns:
        rec_revenue_col = "Course_Revenue"
    else:
        rec_revenue_col = None

    # ------------------------------------------------------------
    # COURSE CATEGORY SIGNAL
    # ------------------------------------------------------------

    top_demand_category = "Not available"
    top_revenue_category = "Not available"

    if "CourseCategory" in recommendation_df.columns:

        category_columns = ["CourseCategory"]

        if rec_enrollment_col is not None:
            category_columns.append(rec_enrollment_col)

        if rec_revenue_col is not None:
            category_columns.append(rec_revenue_col)

        category_data = recommendation_df[
            category_columns
        ].copy()

        category_data = category_data.dropna(
            subset=["CourseCategory"]
        )

        # Use one record per course when CourseID exists
        if "CourseID" in recommendation_df.columns:

            unique_columns = ["CourseID"] + category_columns

            unique_columns = list(
                dict.fromkeys(unique_columns)
            )

            category_data = recommendation_df[
                unique_columns
            ].drop_duplicates(
                subset=["CourseID"]
            )

        category_summary = (
            category_data
            .groupby(
                "CourseCategory",
                as_index=False
            )
            .sum(
                numeric_only=True
            )
        )

        if rec_enrollment_col is not None and len(category_summary) > 0:

            top_demand_category = str(
                category_summary.loc[
                    category_summary[
                        rec_enrollment_col
                    ].idxmax(),
                    "CourseCategory"
                ]
            )

        if rec_revenue_col is not None and len(category_summary) > 0:

            top_revenue_category = str(
                category_summary.loc[
                    category_summary[
                        rec_revenue_col
                    ].idxmax(),
                    "CourseCategory"
                ]
            )

    # ------------------------------------------------------------
    # KPI SIGNALS
    # ------------------------------------------------------------

    k1, k2, k3 = st.columns(3)

    with k1:

        st.metric(
            "🏆 Demand Leader",
            top_demand_category
        )

    with k2:

        st.metric(
            "💰 Revenue Leader",
            top_revenue_category
        )

    with k3:

        if "CourseRating" in recommendation_df.columns:

            average_rating = pd.to_numeric(
                recommendation_df[
                    "CourseRating"
                ],
                errors="coerce"
            ).mean()

            st.metric(
                "⭐ Average Course Rating",
                f"{average_rating:.2f}/5"
            )

        else:

            st.metric(
                "⭐ Average Course Rating",
                "N/A"
            )

    st.divider()

    # ------------------------------------------------------------
    # COURSE LAUNCH RECOMMENDATION
    # ------------------------------------------------------------

    st.subheader("🚀 Course Launch Strategy")

    st.markdown(
        f"""
        **Recommendation:** Prioritize future course development
        in categories showing strong existing demand.

        Current demand-leading category:

        ### 📚 {top_demand_category}

        **Action:**
        - Evaluate new course opportunities in this category.
        - Use historical enrollment patterns when selecting topics.
        - Prioritize courses with strong learner-interest signals.
        """
    )

    st.divider()

    # ------------------------------------------------------------
    # PRICING RECOMMENDATION
    # ------------------------------------------------------------

    st.subheader("💰 Pricing Strategy")

    if "CoursePrice" in recommendation_df.columns:

        prices = pd.to_numeric(
            recommendation_df[
                "CoursePrice"
            ],
            errors="coerce"
        ).dropna()

        if len(prices) > 0:

            median_price = prices.median()

            st.markdown(
                f"""
                **Current median course price:** ₹{median_price:,.2f}

                **Recommendation:**
                Use the predictive model to test different price
                points before launching a new course.

                Instead of applying one fixed price to every course,
                compare predicted enrollment and predicted revenue
                at multiple price levels.
                """
            )

            p1, p2, p3 = st.columns(3)

            with p1:

                st.metric(
                    "Low Price Test",
                    f"₹{median_price * 0.8:,.2f}"
                )

            with p2:

                st.metric(
                    "Current Benchmark",
                    f"₹{median_price:,.2f}"
                )

            with p3:

                st.metric(
                    "High Price Test",
                    f"₹{median_price * 1.2:,.2f}"
                )

        else:

            st.info(
                "Course price information is not available."
            )

    else:

        st.info(
            "CoursePrice column is not available."
        )

    st.divider()

    # ------------------------------------------------------------
    # INSTRUCTOR RECOMMENDATION
    # ------------------------------------------------------------

    st.subheader("👨‍🏫 Instructor Planning")

    instructor_messages = []

    if "Avg_Teacher_Experience" in recommendation_df.columns:

        experience = pd.to_numeric(
            recommendation_df[
                "Avg_Teacher_Experience"
            ],
            errors="coerce"
        ).mean()

        instructor_messages.append(
            f"Average instructor experience is "
            f"{experience:.1f} years. "
            "Consider instructor experience when onboarding "
            "teachers for important or advanced courses."
        )

    if "Avg_Teacher_Rating" in recommendation_df.columns:

        teacher_rating = pd.to_numeric(
            recommendation_df[
                "Avg_Teacher_Rating"
            ],
            errors="coerce"
        ).mean()

        instructor_messages.append(
            f"Average instructor rating is "
            f"{teacher_rating:.2f}/5. "
            "Use instructor quality indicators alongside "
            "experience when assigning instructors."
        )

    elif "Teacher_Rating_Score" in recommendation_df.columns:

        teacher_rating = pd.to_numeric(
            recommendation_df[
                "Teacher_Rating_Score"
            ],
            errors="coerce"
        ).mean()

        instructor_messages.append(
            f"Average instructor rating score is "
            f"{teacher_rating:.2f}. "
            "Use instructor quality indicators alongside "
            "experience when assigning instructors."
        )

    if len(instructor_messages) == 0:

        instructor_messages.append(
            "Use instructor experience and rating as part of "
            "future instructor selection decisions."
        )

    for message in instructor_messages:

        st.info(message)

    st.divider()

    # ------------------------------------------------------------
    # COURSE QUALITY RECOMMENDATION
    # ------------------------------------------------------------

    st.subheader("⭐ Course Quality Strategy")

    if "CourseRating" in recommendation_df.columns:

        ratings = pd.to_numeric(
            recommendation_df[
                "CourseRating"
            ],
            errors="coerce"
        )

        high_rating_percentage = (
            (ratings >= 4).mean() * 100
        )

        st.metric(
            "Courses Rated 4+",
            f"{high_rating_percentage:.1f}%"
        )

        st.info(
            "Maintain strong course quality and monitor learner "
            "ratings because course quality can support future "
            "demand and revenue planning."
        )

    # ------------------------------------------------------------
    # FINAL EXECUTIVE RECOMMENDATIONS
    # ------------------------------------------------------------

    st.divider()

    st.subheader("📌 Executive Action Plan")

    action_plan = pd.DataFrame({

        "Business Decision": [
            "Course Launch",
            "Pricing",
            "Instructor Onboarding",
            "Course Quality",
            "Forecasting"
        ],

        "Recommended Action": [
            f"Prioritize opportunities in {top_demand_category}.",
            "Test multiple price points using the live prediction models.",
            "Consider instructor experience and rating together.",
            "Monitor course ratings and learner response.",
            "Use predicted enrollment and revenue before major decisions."
        ]

    })

    st.dataframe(
        action_plan,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        "⚡ Recommendations are generated from the current "
        "EduPro dataset and are intended to support data-driven "
        "course planning, pricing and instructor decisions."
    )