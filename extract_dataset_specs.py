import os
import pandas as pd

# Define the directories and expected columns
directories = ["./amazon", "./bestbuy"]
columns = ["Title", "Price", "Link", "Description", "id"]

# Function to get statistics from a CSV file
def get_csv_stats(file_path):
    df = pd.read_csv(file_path)
    num_records = len(df)
    non_nan_counts = df.notna().sum()
    return num_records, non_nan_counts

# List to hold the statistics for each dataset
stats = []

# Iterate over directories and files
for directory in directories:
    retailer = os.path.basename(directory)  # Extract retailer name from directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            num_records, non_nan_counts = get_csv_stats(file_path)
            search_term = filename.replace('_', ' ').replace('.csv', '')  # Convert underscores to spaces
            file_stats = {"Search Term": search_term, "Retailer": retailer, "Records": num_records}
            non_nan_counts = non_nan_counts.drop('id')  # Remove id column
            file_stats.update(non_nan_counts.to_dict())
            stats.append(file_stats)

# Create a DataFrame with the statistics
stats_df = pd.DataFrame(stats)
stats_df.fillna(0, inplace=True)  # Replace NaN with 0 for missing columns

# Split the DataFrame into two based on the retailer
amazon_stats_df = stats_df[stats_df['Retailer'] == 'amazon']
bestbuy_stats_df = stats_df[stats_df['Retailer'] == 'bestbuy']

# Function to create LaTeX table with borders and caption, and center align the table
def create_latex_table(df, caption, label):
    num_cols = len(df.columns)
    column_format = "|".join(["c"] * (num_cols + 1))
    latex_table = df.to_latex(index=False,
                              caption=caption,
                              label=label,
                              column_format=f"|{column_format}|",
                              escape=False)
    centered_table = "\\begin{table}[h]\n\\centering\n" + latex_table + "\\end{table}\n"
    return centered_table

# Generate LaTeX tables
amazon_latex_table = create_latex_table(amazon_stats_df, "Amazon Dataset Specifications. \\newline \\textbf{Note:} This table provides an overview of the Amazon datasets used, including the number of records and non-NaN values per column.", "tab:amazon_dataset_specs")
bestbuy_latex_table = create_latex_table(bestbuy_stats_df, "BestBuy Dataset Specifications. \\newline \\textbf{Note:} This table provides an overview of the BestBuy datasets used, including the number of records and non-NaN values per column.", "tab:bestbuy_dataset_specs")

# Write the LaTeX tables to separate files
os.makedirs("./tables", exist_ok=True)
with open("./tables/amazon_dataset_stats.tex", "w") as f:
    f.write(amazon_latex_table)

with open("./tables/bestbuy_dataset_stats.tex", "w") as f:
    f.write(bestbuy_latex_table)

print("LaTeX tables generated and saved as amazon_dataset_stats.tex and bestbuy_dataset_stats.tex")
