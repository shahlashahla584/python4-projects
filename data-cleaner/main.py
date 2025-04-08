import streamlit as st 
import pandas as pd 
import os
from io import BytesIO

st.set_page_config(page_title="📁File Converter and Cleaner", layout="wide")
   
# Title
st.title("***📂File Converter by Shahla Ahmed***")
st.write("Transform your files between CSV and Excel Formats 🚀")

# Upload files
upload_files = st.file_uploader("Upload your files (accept CSV & Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = file.name.split(".")[-1]
        if file_ext == "csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File type: {file_ext}")
            continue
        
        # Details
        st.write("🔎 Preview head of Dataframe")
        st.dataframe(df.head())
        
        # Data Cleaning
        st.subheader("Data Cleaning")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!!")
            
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been filled successfully")
                    
        st.subheader("Select Columns")
        columns = st.multiselect(f"Select Columns for {file.name}", options=list(df.columns), default=list(df.columns))
        df = df[columns]
        
        # Data visualization
        st.subheader("Data Chart 📊")
        if st.checkbox(f"Show Chart 📊 for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        
        # Conversion
        st.subheader("Conversion")
        conversion_type = st.radio(f"Convert 🔄 {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            output = BytesIO()
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            if conversion_type == "CSV":
                df.to_csv(output, index=False)
                file_name = file.name.replace(file_ext, "csv")
            else:
                df.to_excel(output, index=False)
                file_name = file.name.replace(file_ext, "xlsx")
            
            output.seek(0)
            st.download_button(
                label=f"📥 Download {file_name}",
                data=output,
                file_name=file_name,
                mime=mime_type
            )
            
st.success("All files processed successfully!! 🎉")