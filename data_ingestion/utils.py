import pandas as pd
from typing import Tuple

def read_csv_file(uploaded_file) -> pd.DataFrame:
    """
    Read and validate the uploaded CSV file.
    Args:
        uploaded_file: Streamlit uploaded file object
    Returns:
        pd.DataFrame: Parsed DataFrame
    """
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            raise ValueError("The uploaded file is empty")
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {str(e)}")

def format_dataframe_snippet(df: pd.DataFrame, max_rows: int = 15) -> str:
    """
    Format a portion of the DataFrame into a readable string.
    Args:
        df (pd.DataFrame): Input DataFrame
        max_rows (int): Maximum number of rows to include
    Returns:
        str: Formatted string representation of the DataFrame
    """
    column_info = "\n".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()])
    sample_data = df.head(max_rows).to_string(index=False)
    return f"DataFrame Info:\n{column_info}\n\nSample Data:\n{sample_data}"

def validate_csv_size(uploaded_file) -> Tuple[bool, str]:
    """
    Validate if the uploaded CSV file is within reasonable size limits.
    Args:
        uploaded_file: Streamlit uploaded file object
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    MAX_SIZE = 10 * 1024 * 1024
    if uploaded_file.size > MAX_SIZE:
        return False, "File is too large. Please upload a file smaller than 10MB."
    return True, "File size is acceptable." 