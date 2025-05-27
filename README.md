# Text-to-SQL-

Transform your natural language questions into accurate SQL queries with the power of Google Gemini and a modern Streamlit interface.

## Overview 
This project leverages Google Gemini's powerful generative capabilities to convert natural language questions into SQL queries and execute them on a SQLite database. The interactive frontend is built with Streamlit and styled for a clean, modern UI/UX.

![Project Banner](https://img.shields.io/badge/Built%20With-Streamlit-blue?style=for-the-badge&logo=streamlit)
![Project Banner](https://img.shields.io/badge/LLM-Google%20Gemini-orange?style=for-the-badge&logo=google)



##  Features

-  Natural language to SQL query generation using **Gemini 1.5 Flash**
-  Fully responsive and styled **Streamlit web interface**
-  Instant database querying and results display using **SQLite**
-  Sidebar with sample schema and example queries
-  Interactive metric cards and expandable data rows
-  Custom error handling and feedback UI



## Tech Stack

| Component      | Technology        |
|----------------|------------------|
| LLM API        | Google Gemini    |
| Frontend       | Streamlit        |
| Database       | SQLite           |
| Styling        | Custom HTML/CSS  |
| Language       | Python            |


##  Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/text-to-sql-gemini.git
   cd text-to-sql-gemini

2. **Create a python env**
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. **Setup your api key**
GOOGLE_API_KEY=your_api_key_here

4.Run the application 
streamlit run app.py


## Future Improvements 
- Support for multiple tables and joins 
- History of queries and responses 
- User authentication

## Try it out 
https://pranav-j-g-text-to-sql--app-jatauo.streamlit.app/
