# Product Matching App with pyJedAI

Leveraging the powerful capabilities of **pyJedAI**, this application offers a comprehensive solution for price comparison and feature evaluation, empowering users to make informed purchasing decisions.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Data Collection](#data-collection)
4. [Product Matching with pyJedAI](#product-matching-with-pyjedai)
5. [Datasets](#datasets)
6. [API Usage](#api-usage)
7. [Installation and Deployment](#installation-and-deployment)
8. [Future Work](#future-work)
9. [Contributors](#contributors)

## Overview

The **Product Matching App** aims to provide users with a unified view of similar products listed across different online retailers like Amazon and Best Buy. By utilizing advanced entity linking and product matching algorithms, the application facilitates effective comparison shopping.

### Key Objectives

- **Accurate Product Matching**: Identify and link equivalent products from various e-commerce platforms.
- **Seamless Data Integration**: Combine data from different sources for a comprehensive comparison.
- **Enhanced User Experience**: Provide users with easy access to product comparisons and pricing information.

## Features

- **Web Scraping Bots**: Collect product data from multiple e-commerce sites using tools like BeautifulSoup and Selenium.
- **Dynamic Data Handling**: Manage asynchronous content loading and dynamically generated pages with advanced crawling mechanisms.
- **Product Matching Algorithms**: Utilize pyJedAI's workflows to match similar products from different retailers.
- **Data Storage**: Store matched product data in a SQL database for efficient retrieval and analysis.
- **API Integration**: A Flask-based API to enable seamless interaction and data retrieval for users.

## Data Collection

The data collection process is a critical component of the Product Matching App. We have implemented web scraping bots to gather data from various e-commerce platforms, focusing on essential product attributes such as titles, descriptions, prices, and links. Key strategies include:

- **Headless Browsing**: Using Selenium to mimic human browsing behavior and avoid detection.
- **User-Agent Rotation and Random Delays**: Enhancing bot resilience against anti-scraping measures.
- **Crawling Mechanism**: Visiting individual product pages to extract detailed information, ensuring accuracy and completeness of the dataset.

## Product Matching with pyJedAI

The core functionality of our application revolves around product matching, a process significantly enhanced by **pyJedAI**. By leveraging pyJedAI's advanced workflows, the app performs precise entity linking, allowing for effective comparison between similar products across different platforms.

### pyJedAI Workflows Used:

- **Blocking Workflow**: Groups products based on common attributes to reduce the number of comparisons.
- **Similarity Joins Workflow**: Employs various similarity measures to find matching products.
- **Nearest-Neighbor Workflow**: Utilizes machine learning models to capture semantic similarities between product descriptions.

### Example Matches

The following are examples of product matches identified by the application:

| **Amazon Product**                                                                                                                | **Price (Amazon)** | **Best Buy Product**                                                                                                           | **Price (Best Buy)** |
|------------------------------------------------------------------------------------------------------------------------------------|-------------------|--------------------------------------------------------------------------------------------------------------------------------|----------------------|
| Logitech - G915 LIGHTSPEED Full-size Wireless Mechanical GL Clicky Switch Gaming Keyboard with RGB Backlighting - Black            | $204.99           | Logitech - G915 LIGHTSPEED Full-size Wireless Mechanical GL Clicky Switch Gaming Keyboard with RGB Backlighting - Black         | $204.99              |
| MSI Newest GF63 Thin Gaming Laptop, 15.6" FHD 144Hz, Intel i5-11400H, RTX 3050, 16GB RAM, 512GB NVMe SSD, Windows 11, Aluminum Black | $699.99           | MSI - Bravo 15 15.6" 144hz Gaming Laptop FHD - Ryzen 9-7940HS with 16GB Memory - NVIDA GeForce RTX 4060 - 1TB SSD - Aluminum Black | $1,049.99            |
| Technics HiFi True Wireless Multipoint Bluetooth Earbuds with Noise Cancelling, 3 Device Multipoint Connectivity, Wireless Charging, Impressive Call Quality, LDAC Compatible - EAH-AZ60M2-S (Silver) | $190.26           | Technics - HiFi True Wireless Earbuds with Noise Cancelling and 3 Device Multipoint Connectivity with Wireless Charging - Silver | $224.99              |


## Datasets

Our app relies on datasets compiled from Amazon and Best Buy, covering a variety of products like smartphones, monitors, laptops, and more. The datasets include detailed attributes necessary for effective product matching.

- **Amazon Dataset**: Contains product information such as titles, prices, descriptions, and links.
- **Best Buy Dataset**: Similar structure to the Amazon dataset, focused on capturing the latest pricing and product details.

## API Usage

The app features a Flask-based API that provides endpoints for searching and retrieving matched product data. Users can perform queries to compare product prices and specifications, enhancing their online shopping experience.

### Example Endpoints

- `/search`: Accepts product search queries and returns matched product data from Amazon and Best Buy.
- `/laptops`: Provides a list of available laptop models from Amazon for comparison.

## Installation and Deployment

To deploy the Product Matching App, follow these steps:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute Scraping and Crawling**: To start the web scraping and crawling process, use:
   ```bash
   python -u scraper.py --search "logitech keyboard" --max 1000 --retailer amazon
   ```

3. **Run Deduplication**: To execute the deduplication process:
   ```bash
   python deduplicate.py --d1 "$file1" --d2 "$file2"
   ```

4. **Reproduce Experiments**: To reproduce all experiments, run the following scripts:
   ```bash
    ./search.sh
    ./run_deduplication.sh
    ```

5. **Create Database and Deploy API**: To create the database and deploy the API, execute:

   ```bash
   python to_sql.py
   python api_call.py
   ```

