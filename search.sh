#!/bin/bash

# Create the output directory if it doesn't exist
mkdir -p ./logs

# Define an array of search queries
queries=("samsung monitor" "iphone 13" "wireless headphones" "gaming laptop" "smartwatch" "bluetooth speaker" "external hard drive" "digital camera" "robot vacuum" "4k television")

# Define an array of online stores
stores=("amazon" "bestbuy")

# Iterate over each query and store, run the scraper script
for query in "${queries[@]}"; do
  echo "Starting tasks for product term: " $query
  for store in "${stores[@]}"; do
    # Replace spaces with underscores for the log file name
    log_file="./logs/$(echo $query | tr ' ' '_')_${store}.log"
    
    # Run the command with nohup
    echo "Running: nohup python -u scraper.py --search \"$query\" --max 1000 --retailer $store > $log_file 2>&1 &"
    nohup python -u scraper.py --search "$query" --max 1000 --retailer "$store" > "$log_file" 2>&1 &
  done
  echo "All tasks started."
  # wait
  echo "All tasks completed for product term: " $query
done
