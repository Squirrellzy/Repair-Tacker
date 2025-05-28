import streamlit as st
import pandas as pd
from datetime import datetime
import os
from github import Github

# Constants
EXCEL_FILE = "cc_comments_log.xlsx"
GITHUB_REPO = "your-username/your-repo-name"
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # You can set this in your Streamlit secrets
USERNAME = "maint"
PASSWORD = "MaRS"

# Login
st.title("Login")
username_input = st.text_input("Username")
password_input = st.text_input("Password", type="password")

if username_input == USERNAME and password_input == PASSWORD:
    st.success("Login successful!")

    # Initialize Excel file if not present
    if not os.path.exists(EXCEL_FILE):
        df_init = pd.DataFrame(columns=["Date", "CC_Subsection", "Description"])
        df_init.to_excel(EXCEL_FILE, index=False)

    # UI Title
    st.title("Collection Conveyor Comment Logger")

    # Conveyor Selection
    cc_number = st.selectbox("Select Collection Conveyor", [f"CC-{i}" for i in range(1, 78)])
    subsection = st.selectbox("Select Subsection", ["A side 1", "2", "3", "B side 4"])

    # Comment Input
    comment = st.text_area("Enter Comment")

    # Submit
    if st.button("Submit Comment"):
        if comment.strip():
            # Prepare new entry
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cc_subsection = f"{cc_number}-{subsection}"
            new_entry = pd.DataFrame([[date, cc_subsection, comment.strip()]], columns=["Date", "CC_Subsection", "Description"])

            # Append to Excel
            df_existing = pd.read_excel(EXCEL_FILE)
            df_combined = pd.concat([df_existing, new_entry], ignore_index=True)
            df_combined.to_excel(EXCEL_FILE, index=False)

            st.success("Comment logged successfully!")

            # Push to GitHub
            try:
                g = Github(GITHUB_TOKEN)
                repo = g.get_repo(GITHUB_REPO)
                with open(EXCEL_FILE, "rb") as f:
                    content = f.read()
                file = repo.get_contents(EXCEL_FILE)
                repo.update_file(EXCEL_FILE, "Update log", content, file.sha)
                st.success("Excel file updated on GitHub!")
            except Exception as e:
                st.warning(f"Failed to push to GitHub: {e}")
        else:
            st.error("Please enter a comment before submitting.")

    # Download Button
    st.markdown("---")
    st.header("Download Log")
    with open(EXCEL_FILE, "rb") as f:
        st.download_button(
            label="Download Excel Log",
            data=f,
            file_name=EXCEL_FILE,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("Please enter valid credentials.")
