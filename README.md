# EduPro Predictive Analytics Dashboard

## Project Overview

EduPro Predictive Analytics Dashboard is a machine learning and data analytics project developed for an online learning platform.

The project analyses course enrollment, revenue, course characteristics, and instructor-related information. It also uses machine learning models to predict course enrollment demand and forecast course revenue.

An interactive Streamlit dashboard was developed to combine historical analysis, visualizations, machine learning predictions, model evaluation, and recommendations in one application.


## Objectives

- Analyse course enrollment and revenue patterns.
- Understand course and instructor performance.
- Prepare and clean the dataset for analysis.
- Develop a model for enrollment demand prediction.
- Develop a model for revenue forecasting.
- Compare different machine learning regression models.
- Evaluate models using MAE, RMSE, and R².
- Provide live enrollment and revenue predictions.
- Develop an interactive Streamlit dashboard.
- Provide recommendations for course planning and pricing decisions.

## Dataset

The final dataset contains 720 records and 27 attributes, representing 60 courses observed over 12 months.

The dataset includes information related to: 

- Course category
- Course type
- Course level
- Course price
- Course duration
- Course rating
- Monthly enrollment
- Monthly revenue
- Past enrollment
- Past average revenue
- Instructor experience
- Instructor rating
- Number of teachers
- Expertise match
- Revenue per enrollment

## Machine Learning Models

Five regression models were evaluated:

1. Linear Regression
2. Ridge Regression
3. Lasso Regression
4. Random Forest
5. Gradient Boosting

### Selected Models

- Enrollment Demand: Lasso Regression
- Revenue Forecasting: Ridge Regression

The revenue forecasting model achieved an R² score of 0.9459 using Ridge Regression.

## Dashboard Features

The Streamlit application contains the following sections:

- Executive Overview
- Course Offered
- Enrollment and Demand Analytics
- Revenue Forecast
- Live ML Prediction
- Model Performance
- Feature Importance
- Recommendations

## Live Prediction

The dashboard allows users to enter course and instructor information and generate predicted enrollment and revenue values using the trained machine learning models.
https://sonal-edupropredictive.streamlit.app/

## Project Structure

```text
EduPro_Predictive/
│
├── app.py
├── requirements.txt
│
├── data/
│   ├── EduPro_Cleaned_Course_Data (1).csv
│   └── EduPro_Final_ML_Data.csv
│
└── models/
    ├── enrollment_model.pkl
    ├── revenue_model.pkl
    └── preprocessor.pkl
