
# 🛍️ Amazon Product Analysis

End-to-end data analysis project focused on Amazon product listings and customer reviews.  
This project covers the full data pipeline: web scraping, data cleaning, exploratory data analysis (EDA), and interactive dashboard creation using Power BI.

---

## 📌 Project Overview

The goal of this project is to analyze product pricing, customer ratings, and review behavior to extract actionable insights and identify patterns in customer satisfaction and product popularity.

---

## ⚙️ Tech Stack

- Python (Pandas, Requests, BeautifulSoup)
- Jupyter Notebook
- Power BI
- Excel
- Git & GitHub

---

## 📂 Project Structure
amazon-product-analysis/
│
├── data/
│ ├── raw/
│ │ └── AmazonData.xlsx
│ ├── processed/
│ │ └── AmazonData_clean.xlsx
│
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ └── 02_eda.ipynb
│
├── src/
│ └── scraper.py
│
├── dashboard/
│ ├── amazon_dashboard.pbix
│ ├── dashboard_products.png
│ └── dashboard_reviews.png
│
├── reports/
│ └── eda_report.pdf
│
├── .gitignore
├── README.md
└── requirements.txt

---

## 🔍 Key Insights

- Over **80% of products have ratings ≥ 4.5**, indicating strong positive bias.
- Most products are priced between **$15–$20 USD**, suggesting a competitive pricing cluster.
- Review distribution follows a **long-tail pattern**:
  - Few products accumulate thousands of reviews
  - Majority have low review counts
- Verified purchases represent **~99% of reviews**, increasing data reliability.
- No strong correlation between **price and rating**, meaning cheaper products can still be highly rated.

---

## 📊 Dashboard Preview

### Products Analysis
![Products Dashboard](dashboard/products_dashboard.png)

### Reviews Analysis
![Reviews Dashboard](dashboard/reviews_dashboard.png)

---

## 📈 Dashboard Features
- Price distribution analysis
- Rating distribution visualization
- Price vs Rating scatter plot
- Review volume distribution
- Review trends over time
- Verified purchase percentage
- Interactive filters (Price, Rating, Stars, Verified Purchase)

---

## 📈 Business Impact

- Identify pricing sweet spots for competitive positioning
- Detect highly rated products regardless of price
- Understand customer behavior through review patterns
- Support data-driven decision-making in e-commerce strategies

---

## ⚠️ Limitations
- Dataset size is limited
- Web scraping may be affected by captchas or page restrictions
- Currency conversion uses a fixed exchange rate assumption
- Not all products have the same number of reviews

---

## 📌 Future Improvements

- Add sentiment analysis on reviews
- Automate data pipeline (ETL)
- Deploy dashboard online (Power BI Service)
- Expand dataset for more robust insights

---

## 🚀 How to Run the Project

1. Clone the repository:
git clone https://github.com/your-username/amazon-product-analysis.git

2. Install dependencies(optional):
pip install -r requirements.txt

3. Run scraper:
python src/scraper.py

4. Open notebooks for analysis:
- `01_data_cleaning.ipynb`
- `02_eda.ipynb`

5. Open Power BI dashboard:
- `dashboard/amazon_dashboard.pbix`

---

## 👤 Author

Adolfo Montes de Oca  
Data Analyst Project Portfolio

---

⭐ Notes
This project demonstrates an end-to-end data analysis workflow, combining data engineering, analysis, and visualization skills.