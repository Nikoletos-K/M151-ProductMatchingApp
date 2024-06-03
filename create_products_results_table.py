import os
import pandas as pd

# Define directories
amazon_dir = "./amazon"
bestbuy_dir = "./bestbuy"
predictions_dir = "./predictions"

# Function to get the number of rows in a CSV file
def get_num_rows(file_path):
    df = pd.read_csv(file_path)
    return len(df)

# List to hold the statistics for each dataset
stats = []

# Iterate over prediction files
for filename in os.listdir(predictions_dir):
    if filename.endswith("_duplicates.csv"):
        file_path = os.path.join(predictions_dir, filename)
        search_term = filename.replace('_duplicates.csv', '').replace('_', ' ')  # Convert underscores to spaces
        
        # Get number of rows in the predictions file (same products)
        same_products = get_num_rows(file_path)
        
        # Construct file paths for Amazon and BestBuy
        amazon_file = os.path.join(amazon_dir, f"{filename.replace('_duplicates.csv', '')}.csv")
        bestbuy_file = os.path.join(bestbuy_dir, f"{filename.replace('_duplicates.csv', '')}.csv")
        
        # Get number of rows in Amazon and BestBuy files
        amazon_products = get_num_rows(amazon_file)
        bestbuy_products = get_num_rows(bestbuy_file)
        
        # Append statistics to the list
        stats.append({"Search Term": search_term, "Amazon": amazon_products, "BestBuy": bestbuy_products, "Same Products": same_products})

# Create a DataFrame with the statistics
stats_df = pd.DataFrame(stats)

# Function to create LaTeX table with borders and caption, and center align the table
def create_latex_table(df, caption, label):
    num_cols = len(df.columns)
    column_format = "|".join(["c"] * (num_cols + 1))
    latex_table = df.to_latex(index=False,
                              caption=caption,
                              label=label,
                              column_format=f"|{column_format}|",
                              escape=False)
    table_env = "\\begin{table}[h]\n\\centering\n" + latex_table + "\\end{table}\n"
    return table_env

# Generate LaTeX table
latex_table = create_latex_table(stats_df, "Product Comparison Specifications. \\newline \\textbf{Note:} This table provides an overview of the product comparisons, including the number of products in Amazon, BestBuy, and the number of same products identified.", "tab:product_comparison_specs")

# Write the LaTeX table to a file
with open("./tables/product_comparison_stats.tex", "w") as f:
    f.write(latex_table)

print("LaTeX table generated and saved as product_comparison_stats.tex")
