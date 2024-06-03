#!/bin/bash
# conda activate proapp
# Array of search terms
queries=("samsung monitor" "iphone 13" "wireless headphones" "gaming laptop" "smartwatch" "bluetooth speaker" "external hard drive" "digital camera" "robot vacuum" "4k television")

# Loop through each search term
for query in "${queries[@]}"; do
    # Replace spaces with underscores to match the file naming convention
    filename=$(echo "$query" | tr ' ' '_')
    
    # Construct the file paths
    file1="./amazon/${filename}.csv"
    file2="./bestbuy/${filename}.csv"
    
    # Check if both files exist
    if [[ -f "$file1" && -f "$file2" ]]; then
        echo "Running deduplication for: $query"
        echo "File 1: $file1"
        echo "File 2: $file2"
        python deduplicate.py --d1 "$file1" --d2 "$file2" > "./links/${filename}_links.csv"
        python create_products_results_table.py
    else
        echo "Skipping $query. One or both files are missing:"
        if [[ ! -f "$file1" ]]; then
            echo "  Missing: $file1"
        fi
        if [[ ! -f "$file2" ]]; then
            echo "  Missing: $file2"
        fi
    fi
done