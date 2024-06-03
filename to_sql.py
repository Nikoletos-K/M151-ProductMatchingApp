import pandas as pd
from sqlalchemy import create_engine

def to_sql():
    # Database connection details
    host = 'sql8.freesqldatabase.com'
    database_name = 'sql8706720'
    user = 'user_name'
    password = 'password'
    port = '3306'

    # Database connection string
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}')

    # Load the datasets that are generated before (scraping and prediction)
    amazon_df = pd.read_csv("gaming_laptop-amazon.csv")
    bestbuy_df = pd.read_csv("gaming_laptop-bestbuy.csv")
    duplicates_df = pd.read_csv("gaming_laptop_duplicates.csv")

    # Merge the datasets using the provided IDs
    merged_df = pd.merge(duplicates_df, amazon_df, left_on='amazon_id', right_on='id')
    merged_df = pd.merge(merged_df, bestbuy_df, left_on='bestbuy_id', right_on='id')

    # Select only the necessary columns
    final_df = merged_df[['Title_x', 'Link_x', 'Description_x', 'Price_x', 'Title_y', 'Link_y', 'Price_y']]

    # Rename the columns for clarity
    final_df.columns = ['Amazon Title', 'Amazon Link', 'Amazon Description', 'Amazon Price', 'Best Buy Title', 'Best Buy Link', 'Best Buy Price']

    # Save the final DataFrame to the database
    final_df.to_sql('gaming_laptops', con=engine, if_exists='replace', index=False)

    print("Data has been saved to the database.")

if __name__ == "__main__":
    to_sql()
