# This creates the page for displaying data visualizations.

import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json

with open("data.json", "r") as file:
    data = json.load(file)

calories = []
exercises = []


for item in data["data_points"]:
    exercises.append(item["label"])
    calories.append(item["value"])

st.subheader(data["chart_title"])
st.bar_chart(
    {"Exercise": exercises, "Calories Burned": calories},
    x="Exercise",
    y="Calories Burned"
    )

# PART 1: INTERACTIVE PIE CHART
st.subheader("Interactive Calorie Distribution")

if "exercise_count" not in st.session_state:
    st.session_state.exercise_count = 3
num_exercises = st.slider(
    "How many exercises would you like to compare?" ,
    min_value = 2,
    max_value = len(exercises),
    value = st.session_state.exercise_count
    )
st.session_state.exercise_count = num_exercises
st.write("Number of exercises selected:", num_exercises)

selected_exercises = exercises[:num_exercises]
selected_calories = calories[:num_exercises]

fig, ax = plt.subplots()

ax.pie(
    selected_calories,
    labels = selected_exercises,
    autopct = "%1.1f%%",
    )

ax.set_title("Calorie Distribution by Exercise")

st.pyplot(fig)


##PART 2: GRAPHS FROM data.csv

st.divider()
st.subheader("Most Popular Types of Exercise 🏊‍♀️🚴‍♀️🏋️‍♀️🧘‍♀️🏃‍♀️🚶‍♀️")

survey_data = pd.read_csv("data.csv")
exercise_counts = survey_data["Category"].value_counts()



fig2, ax2 = plt.subplots()

ax2.pie(
    exercise_counts.values,
    labels=exercise_counts.index,
    autopct="%1.1f%%"
)

ax2.set_title("Most Popular Types of Exercise")

st.pyplot(fig2)

st.divider()
st.subheader("Calories Burned While Running 🏃‍♀️")

running_data = survey_data[survey_data["Category"] == "Running"]

running_minutes = running_data["Value"].tolist()

calories_per_minute = 12
running_calories = [minutes * calories_per_minute for minutes in running_minutes]


if "running_duration" not in st.session_state:
    st.session_state.running_duration = 30

max_duration = st.slider(
    "Select the maximum running duration (minutes):",
    min_value=0,
    max_value=max(running_minutes),
    value=min(st.session_state.running_duration, max(running_minutes))
)

st.session_state.running_duration = max_duration

filtered_minutes = []
filtered_calories = []

for i in range(len(running_minutes)):
    if running_minutes[i] <= max_duration:
        filtered_minutes.append(running_minutes[i])
        filtered_calories.append(running_calories[i])

sorted_data = sorted(zip(filtered_minutes, filtered_calories))

if sorted_data:
    filtered_minutes, filtered_calories = zip(*sorted_data)

fig3, ax3 = plt.subplots()

ax3.plot(filtered_minutes, filtered_calories, marker="o")

ax3.set_title("Estimated Calories Burned While Running")
ax3.set_xlabel("Running Duration (minutes)")
ax3.set_ylabel("Estimated Calories Burned")

st.pyplot(fig3)


if filtered_calories:
    mean_calories = sum(filtered_calories) / len(filtered_calories)

    sorted_calories = sorted(filtered_calories)
    n = len(sorted_calories)

    if n % 2 == 1:
        median_calories = sorted_calories[n // 2]
    else:
        median_calories = (sorted_calories[n // 2 - 1] + sorted_calories[n // 2])/ 2

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Mean Calories Burned", f"{mean_calories:.1f} kcal")

    with col2:
        st.metric("Median Calories Burned", f"{median_calories:.1f} kcal")
