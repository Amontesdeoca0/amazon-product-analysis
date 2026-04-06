🛒 Amazon Product Analysis Dashboard
📌 Project Overview

This project focuses on analyzing Amazon product data through an end-to-end data pipeline, including web scraping, data cleaning, exploratory data analysis (EDA), and dashboard visualization using Power BI.

The main objective is to extract meaningful insights about product pricing, customer ratings, and review behavior.

⚙️ Tools & Technologies
    • Python (Pandas, BeautifulSoup, Requests)
    • Jupyter Notebooks
    • Power BI
    • Excel

📂 Project Structure
amazon-product-analysis/
│
├── data/
│   ├── raw/
│   │   └── AmazonData.xlsx
│   └── processed/
│       └── AmazonData_clean.xlsx
│
├── notebooks/
│   ├── data_cleaning.ipynb
│   └── eda.ipynb
│
├── src/
│   └── scraper.py
│
├── dashboard/
│   ├── amazon_dashboard.pbix
│   └── amazon_dashboard.pdf
│
├── report/
│   └── eda_report.pdf
│
└── README.md

🔄 Project Workflow
1. Data Collection
    • Built a custom web scraper using Python and BeautifulSoup
    • Extracted product details and customer reviews from Amazon
    • Implemented retry logic and anti-blocking strategies

2. Data Cleaning
    • Removed duplicates (products and reviews)
    • Handled missing values appropriately
    • Standardized numeric fields (price, rating, review count)
    • Converted mixed currencies into USD
    • Removed outliers to ensure data consistency

3. Exploratory Data Analysis (EDA)
    • Analyzed price distribution
    • Evaluated rating patterns
    • Identified review trends over time
    • Explored relationships between price, rating, and popularity

4. Dashboard Development
    • Built an interactive dashboard in Power BI
    • Designed for business-oriented insights
    • Added slicers (filters) for dynamic exploration
    • Included key KPIs and visual storytelling

📊 Key Insights
    • Most products are priced between $15 and $20
    • Over 80% of products have ratings ≥ 4.5, indicating strong customer satisfaction
    • There is no strong correlation between price and rating
    • Review distribution follows a long-tail pattern (few products dominate review volume)
    • The majority of reviews are highly positive (5 stars)
    • Most reviews come from verified purchases, increasing data reliability

📈 Dashboard Features
    • Price distribution analysis
    • Rating distribution visualization
    • Price vs Rating scatter plot
    • Review volume distribution
    • Review trends over time
    • Verified purchase percentage
    • Interactive filters (Price, Rating, Stars, Verified Purchase)

⚠️ Limitations
    • Dataset size is limited
    • Web scraping may be affected by captchas or page restrictions
    • Currency conversion uses a fixed exchange rate assumption
    • Not all products have the same number of reviews

🚀 Future Improvements
    • Implement sentiment analysis on review text
    • Automate data pipeline (ETL)
    • Increase dataset size for better generalization
    • Deploy dashboard online (Power BI Service)
    • Integrate real-time data updates

👤 Author
Adolfo José Montes de Oca López

⭐ Notes
This project demonstrates an end-to-end data analysis workflow, combining data engineering, analysis, and visualization skills.