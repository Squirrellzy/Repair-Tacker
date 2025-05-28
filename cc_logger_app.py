import streamlit as st
import pandas as pd
from datetime import datetime
import os
from github import Github

# Constants
EXCEL_FILE = "cc_comments_log.xlsx"
GITHUB_REPO = "Squirrellzy/Repair-Tacker"
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # You can set this in your Streamlit secrets
USERNAME = "maint"
PASSWORD = "mars"

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
    cc_number = st.selectbox("Select Collection Conveyor", [f"CC-{i}" for i in range(1, 78)], key="cc_selector")# Conveyor Selection
    cc_number = st.selectbox("Select Collection Conveyor", [f"CC-{i}" for i in range(1, 78)], key="cc_selector")

    # Comment boxes for each subsection
    comment_1 = st.text_area("A side 1 Comment", key="comment_1")
    comment_2 = st.text_area("2 Comment", key="comment_2")
    comment_3 = st.text_area("3 Comment", key="comment_3")
    comment_4 = st.text_area("B side 4 Comment", key="comment_4")

    # Submit
    if st.button("Submit Comment"):
        entries = []
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if comment_1.strip():
            entries.append([date, f"{cc_number}-A side 1", comment_1.strip()])
        if comment_2.strip():
            entries.append([date, f"{cc_number}-2", comment_2.strip()])
        if comment_3.strip():
            entries.append([date, f"{cc_number}-3", comment_3.strip()])
        if comment_4.strip():
            entries.append([date, f"{cc_number}-B side 4", comment_4.strip()])

        if entries:
            new_entries_df = pd.DataFrame(entries, columns=["Date", "CC_Subsection", "Description"])
            df_existing = pd.read_excel(EXCEL_FILE)
            df_combined = pd.concat([df_existing, new_entries_df], ignore_index=True)
            df_combined.to_excel(EXCEL_FILE, index=False)
            st.success("Comment(s) logged successfully!")

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
            st.info("No comments entered.")

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
