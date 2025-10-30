#Agri-Climate Q&A System
  An intelligent question-answering system that provides insights into India's agricultural economy and climate patterns by integrating real-time data from multiple     government sources.

🎯 Project Overview
This project was developed for Project Samarth to address the challenge of accessing and analyzing cross-domain data from various government portals. The system can answer complex natural language questions about agriculture and climate by synthesizing data from:

1.Ministry of Agriculture & Farmers Welfare - Crop production data

2.India Meteorological Department - Climate and rainfall data

3.data.gov.in - Official government data portal

✨ Features
1.Natural Language Processing: Understands complex questions in plain English

2.Multi-Source Integration: Combines data from agriculture and climate datasets

3.Real-time Data Access: Fetches live data from government APIs

4.Source Citation: Provides traceable data sources for every answer

5.User-Friendly Interface: Simple web-based chat interface

6.Cross-Domain Insights: Correlates agricultural and climate data

🚀 Quick Start

Prerequisites

1.Python 3.8+
2.pip (Python package manager)

Installation
1.Install dependencies

pip install -r requirements.txt

2.Run the application
python app.py

3.Access the application
  Open your browser and go to: http://localhost:5000

🏗️ System Architecture
The system consists of four main components:

1. Web Interface (templates/index.html)
  #Clean, responsive chat interface
  #Sample questions for quick testing
  #Real-time answer display with source citations

2. Flask Web Server (app.py)
    #Handles HTTP requests and responses
    #Manages the web application lifecycle
    #REST API endpoint for question processing

3. Query Processor (query_processor.py)
  #Natural language query parsing
  #Intent detection and parameter extraction
  #Coordinates data fetching and answer generation
  #Supports multiple query types:
     Rainfall and production comparison
     Extreme production analysis
     Trend correlation
     Policy argument generation


4. Data Fetcher (data_fetcher.py)
  #Integrates with data.gov.in APIs
  #Handles multiple data formats and structures
  #Fallback to sample data when APIs are unavailable
  #Manages authentication and API limits

🔧 Technical Details
Data Sources
1.Agriculture Data: Crop production, yield, area cultivated
2.Climate Data: Rainfall patterns, annual precipitation
3.Real-time APIs: data.gov.in REST APIs with public access keys

#Technologies Used
1.Backend: Flask, Python
2.Frontend: HTML, CSS, JavaScript
3.Data Processing: pandas, requests
4.API Integration: data.gov.in REST APIs

#Key Algorithms
1.Natural language query parsing with regex patterns
2.Multi-source data correlation
3.Real-time API integration with error handling
4.Dynamic answer generation with source attribution
