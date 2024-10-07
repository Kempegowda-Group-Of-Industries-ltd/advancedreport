import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Advanced Reporting & Dashboards",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📊 Advanced Reporting & Dashboards")
st.write("Gain insights into your inventory and supply chain performance by uploading your data.")

# Sidebar header
st.sidebar.header("File Upload Section")

# Create an 'uploads' directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# File upload logic
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Save the uploaded file to the 'uploads' directory
    save_path = os.path.join("uploads", uploaded_file.name)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success(f"File successfully saved at: {save_path}")

    # Read the uploaded CSV file
    df = pd.read_csv(save_path)

    # Displaying the data
    st.subheader("Uploaded Data Preview")
    st.write("Here is a preview of your inventory data:")
    st.dataframe(df)

    # Displaying basic statistics
    st.subheader("Basic Data Statistics")
    st.write("Some basic statistics of your data:")
    st.write(df.describe())

    # Filter and visualize data
    st.sidebar.subheader("Analysis Options")
    category = st.sidebar.selectbox("Select Item Category", df["Category"].unique())

    # Filter data by selected category
    filtered_df = df[df["Category"] == category]
    st.subheader(f"Data for Category: {category}")
    st.dataframe(filtered_df)

    # Bar Chart for Inventory Count by Location
    st.markdown("### Inventory Count by Location")
    count_chart = px.bar(df, x="Location", y="Count", color="Item", title='Inventory Count by Location',
                          labels={'Location': 'Location', 'Count': 'Inventory Count'},
                          template='plotly_dark')
    st.plotly_chart(count_chart, use_container_width=True)

    # Pie Chart for Total Value Distribution
    st.markdown("### Total Value Distribution")
    value_distribution = df.groupby("Item")["Value"].sum().reset_index()
    pie_chart = px.pie(value_distribution, names='Item', values='Value', 
                        title='Total Value Distribution by Item',
                        template='plotly_dark')
    st.plotly_chart(pie_chart, use_container_width=True)

    # Line Chart for Total Count Over Time (Assuming 'Date' column exists)
    if 'Date' in df.columns:
        st.markdown("### Total Inventory Count Over Time")
        line_chart = px.line(df, x="Date", y="Count", color="Category", 
                              title='Total Inventory Count Over Time',
                              labels={'Date': 'Date', 'Count': 'Total Inventory Count'},
                              template='plotly_dark')
        st.plotly_chart(line_chart, use_container_width=True)

    # Additional insights
    st.subheader("Insights")
    st.write(f"**Total Count for {category}:** {filtered_df['Count'].sum()}")
    st.write(f"**Total Value for {category}:** ${filtered_df['Value'].sum():,.2f}")

else:
    st.sidebar.info("Please upload a CSV file to get started.")
    st.write("Awaiting file upload...")

# Footer
st.markdown("""<hr>
    <small>Developed by Your Name. Powered by Streamlit.</small>
    """, unsafe_allow_html=True)
