import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from ai_assistant.llm_api import LLMAPI
from data_ingestion.utils import read_csv_file, format_dataframe_snippet, validate_csv_size

st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="💰",
    layout="wide"
)

if 'df' not in st.session_state:
    st.session_state.df = None
if 'api' not in st.session_state:
    try:
        st.session_state.api = LLMAPI()
    except ValueError as e:
        st.error(str(e))
        st.stop()

st.title("AI Financial Assistant 💰")
st.markdown("""
Upload your financial data in CSV format and ask questions about it. 
The AI will analyze your data and provide insights!
""")

uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file is not None:
    is_valid, message = validate_csv_size(uploaded_file)
    if not is_valid:
        st.error(message)
        st.stop()
    try:
        st.session_state.df = read_csv_file(uploaded_file)
        st.subheader("Data Preview")
        st.dataframe(st.session_state.df.head())
        with st.expander("DataFrame Information"):
            st.write(st.session_state.df.info())
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.stop()

user_question = st.text_input("Ask a question about your financial data:", 
                            placeholder="e.g., What were the top 5 expenses last month?")

if user_question and st.session_state.df is not None:
    if st.button("Get Answer"):
        try:
            with st.spinner("Analyzing your data..."):
                data_snippet = format_dataframe_snippet(st.session_state.df)
                response = st.session_state.api.get_response(data_snippet, user_question)
                st.subheader("AI Analysis")
                st.write(response)
                st.download_button(
                    label="Download Analysis",
                    data=response,
                    file_name="financial_analysis.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error getting AI response: {str(e)}")
elif user_question and st.session_state.df is None:
    st.warning("Please upload a CSV file first!") 