from dotenv import load_dotenv
load_dotenv()
# load env variables 
import streamlit as st 
import os 
import sqlite3 
import google.generativeai as genai 
import pandas as pd


# Page configuration with custom styling
st.set_page_config(
    page_title='AI-Powered Text-to-SQL Converter',
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 10px rgba(31, 119, 180, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .sql-code {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: #495057;
        margin: 1rem 0;
    }
    
    .result-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .schema-box {
        background: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .example-box {
        background: #f0f8e8;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# api key config 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load gemini and provide query response 
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    full_prompt = f"{prompt[0]}\nQ: {question}\nSQL:"
    response = model.generate_content(full_prompt)
    return response.text


def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    for row in  rows:
        print(row)
    return rows

# prompt  
prompt = ['''
You are an expertised and helpful assistant that converts natural language questions into SQL queries.

Here is the database schema:

Table: STUDENT  
Columns:
- NAME: VARCHAR(25)  
- CLASS: VARCHAR(25)  
- SECTION: VARCHAR(25)  
- MARKS: INT  

Write an SQL query for each question based on this schema.

Example 1:  
Q: Show all students who scored more than 90.  
SQL: SELECT * FROM STUDENT WHERE MARKS > 90;

Example 2:  
Q: List names and marks of students in class 10, section A.  
SQL: SELECT NAME, MARKS FROM STUDENT WHERE CLASS = '10' AND SECTION = 'A';

Example 3:  
Q: Find the average marks of students in class 12.  
SQL: SELECT AVG(MARKS) FROM STUDENT WHERE CLASS = '12';

also the sql code should not have """ in the beginning or in the end """  and sql word in the result 
'''
]

# Main header
st.markdown('<h1 class="main-header">🤖 AI-Powered Text-to-SQL Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform your natural language questions into precise SQL queries instantly</p>', unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.markdown("### Database Schema")
    st.markdown("""
    <div class="schema-box" style="color: #003366; font-weight: 600;">
        <strong>Table: STUDENT</strong><br>
        📝 NAME: VARCHAR(25)<br>
        🏫 CLASS: VARCHAR(25)<br>
        📚 SECTION: VARCHAR(25)<br>
        📈 MARKS: INT
    </div>

    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Example Questions")
    examples = [
        "Show all students who scored more than 90",
        "List names and marks of students in class 10",
        "Find the average marks of students in class 12",
        "Count total students in each class",
        "Show top 5 students with highest marks"
    ]
    
    for example in examples:
        st.markdown(f"""
        <div class="example-box">
             <small style="color: #2c3e50; font-weight: 600;">"{example}"</small>
        </div>
        """, unsafe_allow_html=True)

# Main content area
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("### 💬 Ask Your Question")
    question = st.text_input(
        "",
        placeholder="e.g., Show me all students with marks greater than 85...",
        key="input",
        help="Type your question in natural language and I'll convert it to SQL!"
    )
    
    # Center the submit button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        submit = st.button("🚀 Generate SQL Query", use_container_width=True)

# Processing and results
if submit:
    if question.strip():
        with st.spinner('🧠 AI is thinking... Converting your question to SQL...'):
            try:
                response = get_gemini_response(question, prompt)
                print(response)
                
                # Display the generated SQL query
                st.markdown("### 🔍 Generated SQL Query")
                st.markdown(f"""
                <div class="sql-code">
                    <strong>SQL:</strong> {response}
                </div>
                """, unsafe_allow_html=True)
                
                # Execute query and show results
                data = read_sql_query(response, "student.db")
                
                if data:
                    st.markdown("""
                    <div class="result-container">
                        <h3 style="color: #1f77b4; margin-bottom: 1rem;">📋 Query Results</h3>
                    """, unsafe_allow_html=True)
                    
                    # Display results in a nice table format
                    if len(data) > 0:
                        # Create metrics row
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3 style="color: #28a745; margin: 0;">{len(data)}</h3>
                                <p style="margin: 0; color: #666;">Records Found</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3 style="color: #17a2b8; margin: 0;">{len(data[0]) if data else 0}</h3>
                                <p style="margin: 0; color: #666;">Columns</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3 style="color: #ffc107; margin: 0;">✓</h3>
                                <p style="margin: 0; color: #666;">Query Success</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("#### 📊 Data Table")
                        
                        # Display each row with better formatting
                        for i, row in enumerate(data, 1):
                            with st.expander(f"Record {i}: {row}", expanded=i<=5):  # Show first 5 expanded
                                col_data = st.columns(len(row))
                                headers = ["NAME", "CLASS", "SECTION", "MARKS"] if len(row) == 4 else [f"Column {j+1}" for j in range(len(row))]
                                for j, (header, value) in enumerate(zip(headers, row)):
                                    with col_data[j]:
                                        st.metric(header, value)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-container">
                        <h3 style="color: #ffc107;">⚠️ No Results Found</h3>
                        <p>Your query executed successfully but returned no data. Try modifying your question.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f"""
                <div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 1rem; border-radius: 8px;">
                    <h4>❌ Error Occurred</h4>
                    <p>There was an issue processing your request: {str(e)}</p>
                    <small>Please check your question and try again.</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a question before submitting!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by Google Gemini AI | Built with Streamlit</p>
    <p><small>Transform natural language into SQL queries with the power of AI</small></p>
</div>
""", unsafe_allow_html=True)