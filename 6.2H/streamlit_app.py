import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ----------------------------
# Load CSV safely
# ----------------------------
csv_file = '/Users/ayushjain/Desktop/SIT225 DATA CAPTURE CODES/HD TASK/gyrooo_data.csv'


try:
    data = pd.read_csv(csv_file)
    if data.empty:
        st.warning("CSV file is empty. Please check your data.")
        st.stop()
except FileNotFoundError:
    st.error(f"File '{csv_file}' not found. Please check the path.")
    st.stop()
except pd.errors.EmptyDataError:
    st.error(f"CSV file '{csv_file}' is empty or malformed.")
    st.stop()

# ----------------------------
# Session state for navigation
# ----------------------------
if 'start_idx' not in st.session_state:
    st.session_state.start_idx = 0

# ----------------------------
# Dashboard UI
# ----------------------------
st.title("Gyroscope Data Dashboard")

# Chart type
chart_type = st.selectbox("Select Chart Type", ["Line", "Scatter", "Distribution"])

# Axis selection
axes = st.multiselect("Select Axes", ['x', 'y', 'z'], default=['x','y','z'])

# Number of samples to display
num_samples = st.number_input(
    "Number of Samples",
    min_value=1,
    max_value=len(data),
    value=50
)

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous"):
        st.session_state.start_idx = max(0, st.session_state.start_idx - num_samples)
with col2:
    if st.button("Next"):
        st.session_state.start_idx += num_samples

start_idx = st.session_state.start_idx
subset = data.iloc[start_idx:start_idx + num_samples][axes]

# ----------------------------
# Plotting
# ----------------------------
st.write(f"Displaying samples {start_idx} to {start_idx + num_samples}")

if chart_type == "Line":
    st.line_chart(subset)
else:
    fig, ax = plt.subplots()
    if chart_type == "Scatter":
        if len(axes) >= 2:
            ax.scatter(subset[axes[0]], subset[axes[1]])
            ax.set_xlabel(axes[0])
            ax.set_ylabel(axes[1])
        else:
            st.warning("Select at least 2 axes for Scatter plot")
    elif chart_type == "Distribution":
        subset.plot(kind='hist', ax=ax, bins=20)
    st.pyplot(fig)

# ----------------------------
# Summary table
# ----------------------------
st.subheader("Data Summary")
st.write(subset.describe())

# ----------------------------
# Auto-refresh every 10 seconds
# ----------------------------
st.write("Dashboard will refresh every 10 seconds to load new data.")
time.sleep(10)
st.experimental_rerun()
