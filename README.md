# social-media-analytics-group-4
# Social Media Analytics Pipeline  

This project is a comprehensive **batch data processing pipeline** designed to analyze social media data, focusing on sentiment analysis, engagement metrics, and trending topics. The pipeline efficiently processes large-scale data using **PySpark**, stores results in **Amazon S3**, and provides **visualizations** through advanced tools for actionable insights.  

---

## Key Features  

- **Data Extraction**: Fetches social media data using the Twitter API based on user-defined queries.  
- **Data Transformation**: Cleans and preprocesses raw data for further analysis.  
- **Batch Processing**: Uses PySpark to compute sentiment scores and engagement metrics in batches.  
- **Data Storage**: Saves processed data in Amazon S3 for scalability and future analysis.  
- **Visualization**: Generates dashboards for sentiment trends, engagement metrics, and emerging topics.  

---

## Technology Stack  

- **Programming Languages**: Python  
- **Big Data Processing**: Apache Spark (PySpark)  
- **Data Storage**: Amazon S3  
- **Visualization**: Power BI / Tableau  
- **APIs**: Twitter API for data extraction  
- **Libraries**: TextBlob for sentiment analysis  

---

## Application Flow  

1. **Data Extraction**: Fetch raw tweets/posts based on keywords.  
2. **Data Transformation**: Preprocess the text (clean, normalize).  
3. **Batch Processing**: Compute sentiment scores and engagement metrics.  
4. **Data Storage**: Save results to S3 for further analysis.  

---

## Future Enhancements  

- Real-time data streaming and analytics.  
- Advanced NLP models like BERT for sentiment analysis.  
- Multi-platform integration with other social media APIs.  
- Predictive analytics for trend forecasting.  

---

## How to Run  
1. Clone the repository:  
   ```bash  
   git clone <repository_url>

2. Install Dependencies:
   '''powershell
   pip install -r requirements.txt
   
3. run the application
   '''powershell
   streamlit app.py  


