# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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

    return df

# Function to perform EDA on drug utilization data and generate summary table
def perform_eda_on_drug_utilization(df):
    """
    Perform basic EDA on the drug utilization data.
    """
    if df.empty:
        st.write("No data available for EDA.")
        return

    # Generate summary table of top drugs by total reimbursement
    st.write("### Top 10 Drugs by Total Reimbursement")
    if 'Product Name' in df.columns and 'Total Amount Reimbursed' in df.columns:
        summary_table = (df.groupby('Product Name')
                        .agg({'Total Amount Reimbursed': 'sum'})
                        .sort_values(by='Total Amount Reimbursed', ascending=False)
                        .head(10))
        # Display bar chart for top 10 drugs by total reimbursement
        st.bar_chart(summary_table['Total Amount Reimbursed'])
        
    # Generate summary table of top drugs by units reimbursed
    st.write("### Top 10 Drugs by Units Reimbursed")
    if 'Product Name' in df.columns and 'Units Reimbursed' in df.columns:
        summary_table = (df.groupby('Product Name')
                        .agg({'Units Reimbursed': 'sum'})
                        .sort_values(by='Units Reimbursed', ascending=False)
                        .head(10))
        # Display bar chart for top 10 drugs by units reimbursed
        st.bar_chart(summary_table['Units Reimbursed'])

    # Analysis 5 - Drug Utilization Trends by Utilization Type
    utilization_trends = df.groupby('Utilization Type')[['Units Reimbursed', 'Total Amount Reimbursed']].sum().reset_index()
    utilization_trends
    
    # Plot total units reimbursed by utilization type
    st.write("### Total Units Reimbursed by Utilization Type")
    st.bar_chart(utilization_trends.set_index('Utilization Type')['Units Reimbursed'])

    # Plot total amount reimbursed by utilization type
    st.write("### Total Amount Reimbursed by Utilization Type")
    st.bar_chart(utilization_trends.set_index('Utilization Type')['Total Amount Reimbursed'])
    
# Function to add search functionality
def search_data(df):
    """
    Add a search function for querying the data based on user input.
    """
    st.write("### Search the Dataset")
    search_query = st.text_input("Enter a search term (e.g., drug name, type):")
    
    if search_query:
        search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        if not search_results.empty:
            st.write(f"Results for '{search_query}':")
            st.dataframe(search_results)
        else:
            st.write(f"No results found for '{search_query}'.")
    else:
        st.dataframe(df)

# Main function for Streamlit app
def main():
    st.title("MDRP California State Drug Utilization Dashboard")
    
    # Automatically load the CSV file
    file_path = 'data/drug_utilization_data.csv'  # Replace with your CSV file path
    try:
        df = pd.read_csv(file_path)
        df = handle_missing_values(df)
        
        # Add search functionality
        search_data(df)
        
        # Perform EDA
        perform_eda_on_drug_utilization(df)
        
        # Analysis 3 - Medicaid vs. Non-Medicaid Amount Comparison
        st.write("### Medicaid vs. Non-Medicaid Amount Comparison")
        if 'Medicaid Amount Reimbursed' in df.columns and 'Non Medicaid Amount Reimbursed' in df.columns:
            # Sum of Medicaid and Non-Medicaid reimbursements, scaled to thousands
            medicaid_comparison = df[['Medicaid Amount Reimbursed', 'Non Medicaid Amount Reimbursed']].sum() / 1_000  # Scale to thousands
            medicaid_comparison_df = pd.DataFrame(medicaid_comparison, columns=['Total Amount'])
            medicaid_comparison_df.index.name = 'Reimbursement Type'
            
            # Plot comparison of Medicaid vs Non-Medicaid amounts
            st.bar_chart(medicaid_comparison_df)
        else:
            st.warning("Columns for 'Medicaid Amount Reimbursed' or 'Non Medicaid Amount Reimbursed' are not available in the dataset.")
        
        # Add footer
        st.markdown("---")
        st.markdown("**MDRP California State Drug Utilization Dashboard** - Developed by Thay Chansy | © 2024")
        
    except FileNotFoundError:
        st.error(f"CSV file not found at the specified path: {file_path}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        

# Run the main function for Streamlit app
if __name__ == "__main__":
    main()
