# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")

# Function to handle missing values
def handle_missing_values(df):
    """Handles missing values in numerical and categorical columns."""
    # Fill numerical columns with the median
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Fill categorical columns with the mode
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    # Convert specific columns to categorical if present
    for cat_col in ['Year', 'NDC', 'Labeler Code', 'Product Code', 'Package Size', 'Quarter']:
        if cat_col in df.columns:
            df[cat_col] = df[cat_col].astype('category')

    return df

# Function to display summary statistics and charts
def display_summary_statistics(df):
    """Displays summary statistics and grouped data for total reimbursement and units."""
    st.subheader("Summary Statistics for Entire Dataset")
    st.write(df.describe())

    with st.expander("Summary Statistics by Product Name"):
        grouped_stats = df.groupby('Product Name')[['Total Amount Reimbursed', 'Units Reimbursed']].sum().reset_index()
        st.dataframe(grouped_stats)

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Top 10 Drugs by Total ($) Reimbursement"):
            if 'Product Name' in df.columns and 'Total Amount Reimbursed' in df.columns:
                top_reimbursed = (df.groupby('Product Name')['Total Amount Reimbursed']
                                  .sum().sort_values(ascending=False).head(10))
                st.bar_chart(top_reimbursed)

    with col2:
        with st.expander("Top 10 Drugs by Units Reimbursed"):
            if 'Product Name' in df.columns and 'Units Reimbursed' in df.columns:
                top_units = (df.groupby('Product Name')['Units Reimbursed']
                             .sum().sort_values(ascending=False).head(10))
                st.bar_chart(top_units)

    with st.expander("Drug Utilization Trends by Utilization Type"):
        utilization_trends = df.groupby('Utilization Type')[['Units Reimbursed', 'Total Amount Reimbursed']].sum().reset_index()
        st.dataframe(utilization_trends)

        col3, col4 = st.columns(2)
        with col3:
            st.write("### Total Units Reimbursed")
            st.bar_chart(utilization_trends.set_index('Utilization Type')['Units Reimbursed'])
        with col4:
            st.write("### Total Amount ($) Reimbursed")
            st.bar_chart(utilization_trends.set_index('Utilization Type')['Total Amount Reimbursed'])

# Function for search functionality
def search_data(df):
    """Allows users to search data based on a query and display filtered results with summary charts."""
    st.subheader("Search the Dataset")
    search_query = st.text_input("Enter a search term (e.g., drug name, type):")
    selected_column = st.selectbox("Select a column to search in:", ['All Columns'] + list(df.columns))

    if search_query:
        if selected_column == 'All Columns':
            search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        else:
            search_results = df[df[selected_column].astype(str).str.contains(search_query, case=False)]

        if not search_results.empty:
            st.write(f"Results for '{search_query}' in '{selected_column}':")
            st.dataframe(search_results)
            
            col5, col6 = st.columns(2)
            with col5:
                st.subheader(f"Total Amount ($) Reimbursed ('{search_query}')")
                if 'Product Name' in search_results.columns and 'Total Amount Reimbursed' in search_results.columns:
                    top_reimbursed = (search_results.groupby('Product Name')['Total Amount Reimbursed']
                                      .sum().sort_values(ascending=False).head(10))
                    st.bar_chart(top_reimbursed)

            with col6:
                st.subheader(f"Units Reimbursed ('{search_query}')")
                if 'Product Name' in search_results.columns and 'Units Reimbursed' in search_results.columns:
                    top_units = (search_results.groupby('Product Name')['Units Reimbursed']
                                 .sum().sort_values(ascending=False).head(10))
                    st.bar_chart(top_units)

            st.subheader(f"Utilization Type Analysis ('{search_query}')")
            if 'Utilization Type' in search_results.columns:
                utilization_trends = search_results.groupby('Utilization Type')[['Units Reimbursed', 'Total Amount Reimbursed']].sum().reset_index()
                st.dataframe(utilization_trends)
                
                col7, col8 = st.columns(2)
                with col7:
                    st.subheader(f"Total Units Reimbursed by Utilization Type ('{search_query}')")
                    st.bar_chart(utilization_trends.set_index('Utilization Type')['Units Reimbursed'])
                with col8:
                    st.subheader(f"Total Amount ($) Reimbursed by Utilization Type ('{search_query}')")
                    st.bar_chart(utilization_trends.set_index('Utilization Type')['Total Amount Reimbursed'])
        else:
            st.write(f"No results found for '{search_query}' in '{selected_column}'.")
    else:
        st.dataframe(df)

# Main function for the Streamlit app
def main():
    st.title("MDRP California State Drug Utilization Dashboard 2024")

    file_path = 'data/drug_utilization_data.csv'  # Replace with your file path
    try:
        df = pd.read_csv(file_path)
        df = handle_missing_values(df)

        # Search data and display results
        search_data(df)

        # Display EDA summary
        display_summary_statistics(df)

        with st.expander("Medicaid vs. Non-Medicaid Amount ($) Comparison"):
            if 'Medicaid Amount Reimbursed' in df.columns and 'Non Medicaid Amount Reimbursed' in df.columns:
                medicaid_comparison = df[['Medicaid Amount Reimbursed', 'Non Medicaid Amount Reimbursed']].sum()
                medicaid_comparison_df = pd.DataFrame(medicaid_comparison, columns=['Total Amount'])
                medicaid_comparison_df.index.name = 'Reimbursement Type'
                st.bar_chart(medicaid_comparison_df)
            else:
                st.warning("Columns for 'Medicaid Amount Reimbursed' or 'Non Medicaid Amount Reimbursed' are not available in the dataset.")

        st.markdown("---")
        st.markdown("**MDRP California State Drug Utilization Dashboard** - Developed by Thay Chansy | © 2024")

    except FileNotFoundError:
        st.error(f"CSV file not found at the specified path: {file_path}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
