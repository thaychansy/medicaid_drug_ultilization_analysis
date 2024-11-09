# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style="whitegrid")

# Function to handle missing values
def handle_missing_values(df):
    """
    Handle missing values by filling them with appropriate strategies.
    """
    # Fill numerical columns with the median
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    # Fill categorical columns with the mode
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    if 'Year' in df.columns:
        df['Year'] = df['Year'].astype('category')
        
    if 'NDC' in df.columns:
        df['NDC'] = df['NDC'].astype('category')

    if 'Labeler Code' in df.columns:
        df['Labeler Code'] = df['Labeler Code'].astype('category')

    if 'Product Code' in df.columns:
        df['Product Code'] = df['Product Code'].astype('category')
    
    if 'Package Size' in df.columns:
        df['Package Size'] = df['Package Size'].astype('category')
    
    if 'Quarter' in df.columns:
        df['Quarter'] = df['Quarter'].astype('category')

    return df

# Function to perform EDA on drug utilization data and generate summary table
def perform_eda_on_drug_utilization(df):
    """
    Perform basic EDA on the drug utilization data.
    """
    if df.empty:
        st.write("No data available for EDA.")
        return

    # Display summary statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Responsive layout with columns
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Top 10 Drugs by Total ($) Reimbursement"):
            if 'Product Name' in df.columns and 'Total Amount Reimbursed' in df.columns:
                summary_table = (df.groupby('Product Name')
                                .agg({'Total Amount Reimbursed': 'sum'})
                                .sort_values(by='Total Amount Reimbursed', ascending=False)
                                .head(10))
                st.bar_chart(summary_table['Total Amount Reimbursed'])

    with col2:
        with st.expander("Top 10 Drugs by Units Reimbursed"):
            if 'Product Name' in df.columns and 'Units Reimbursed' in df.columns:
                summary_table = (df.groupby('Product Name')
                                .agg({'Units Reimbursed': 'sum'})
                                .sort_values(by='Units Reimbursed', ascending=False)
                                .head(10))
                st.bar_chart(summary_table['Units Reimbursed'])

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
        
# Function to add search functionality with filter by column drop-down
def search_data(df):
    """
    Add a search function for querying the data and generating dashboards based on user input.
    Includes a filter-by-column option for more targeted searches.
    """
    st.subheader("Search the Dataset (Update: 10/21/24)")

    # Search query input
    search_query = st.text_input("Enter a search term (e.g., drug name, type):")

    # Column selection drop-down
    column_options = ['All Columns'] + list(df.columns)
    selected_column = st.selectbox("Select a column to search in:", column_options)

    if search_query:
        if selected_column == 'All Columns':
            # Search across all columns
            search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        else:
            # Search within the selected column
            search_results = df[df[selected_column].astype(str).str.contains(search_query, case=False)]

        if not search_results.empty:
            st.write(f"Results for '{search_query}' in '{selected_column}':")
            st.dataframe(search_results)

            # Generate summary charts based on the search results
            col5, col6 = st.columns(2)
            with col5:
                st.subheader(f"Total Amount ($) Reimbursed ('{search_query}')")
                if 'Product Name' in search_results.columns and 'Total Amount Reimbursed' in search_results.columns:
                    summary_table = (search_results.groupby('Product Name')
                                    .agg({'Total Amount Reimbursed': 'sum'})
                                    .sort_values(by='Total Amount Reimbursed', ascending=False)
                                    .head(10))
                    st.bar_chart(summary_table['Total Amount Reimbursed'])

            with col6:
                st.subheader(f"Units Reimbursed ('{search_query}')")
                if 'Product Name' in search_results.columns and 'Units Reimbursed' in search_results.columns:
                    summary_table = (search_results.groupby('Product Name')
                                    .agg({'Units Reimbursed': 'sum'})
                                    .sort_values(by='Units Reimbursed', ascending=False)
                                    .head(10))
                    st.bar_chart(summary_table['Units Reimbursed'])

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

            st.subheader(f"Medicaid vs. Non-Medicaid Amount ($) Reimbursed ('{search_query}')")
            if 'Medicaid Amount Reimbursed' in search_results.columns and 'Non Medicaid Amount Reimbursed' in search_results.columns:
                medicaid_comparison = search_results[['Medicaid Amount Reimbursed', 'Non Medicaid Amount Reimbursed']].sum()
                medicaid_comparison_df = pd.DataFrame(medicaid_comparison, columns=['Total Amount'])
                medicaid_comparison_df.index.name = 'Reimbursement Type'
                st.bar_chart(medicaid_comparison_df)
        else:
            st.write(f"No results found for '{search_query}' in '{selected_column}'.")
    else:
        st.dataframe(df)

# Main function for Streamlit app
def main():
    st.title("MDRP California State Drug Utilization Dashboard 2024")
    
    # Automatically load the CSV file
    file_path = 'data/drug_utilization_data.csv'  # Replace with your CSV file path
    try:
        df = pd.read_csv(file_path)
        df = handle_missing_values(df)
        
        # Add search functionality
        search_data(df)
        
        # Perform EDA
        perform_eda_on_drug_utilization(df)
        
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
        
        # Run the main function for Streamlit app
if __name__ == "__main__":
    main()