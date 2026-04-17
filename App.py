import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from groq import Groq
import io

st.set_page_config(page_title="College Placement Analyzer", layout="wide")

client = Groq(api_key="gsk_xxxxxxxxxxxxxxxxxxxx")  # your Groq key here

def scrape_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract all visible text
        text = soup.get_text(separator=" ", strip=True)
        # Limit to 3000 chars to fit in Groq context
        return text[:3000]
    except Exception as e:
        return f"Error scraping: {str(e)}"

def extract_packages_with_ai(college_name, scraped_text):
    try:
        prompt = f"""
        You are a data extractor. From the following placement page text of {college_name},
        extract ONLY:
        1. Highest Package (in LPA - Lakhs Per Annum)
        2. Average Package (in LPA - Lakhs Per Annum)

        Return ONLY in this exact format, nothing else:
        HIGHEST: <number>
        AVERAGE: <number>

        If you cannot find the data, return:
        HIGHEST: 0
        AVERAGE: 0

        Text:
        {scraped_text}
        """
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()

        highest = 0.0
        average = 0.0

        for line in result.split("\n"):
            if "HIGHEST:" in line:
                try:
                    highest = float(line.split(":")[1].strip())
                except:
                    highest = 0.0
            if "AVERAGE:" in line:
                try:
                    average = float(line.split(":")[1].strip())
                except:
                    average = 0.0

        return highest, average

    except Exception as e:
        return 0.0, 0.0

# ---- UI ----
st.title("🎓 College Placement Analyzer")
st.write("Upload an Excel file with College Name and URL columns to analyze placement data.")

uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 Uploaded Data:")
    st.dataframe(df)

    # Check columns
    if "College Name" not in df.columns or "URL" not in df.columns:
        st.error("❌ Excel must have exactly 'College Name' and 'URL' columns.")
    else:
        if st.button("🔍 Analyze Placements"):
            results = []
            progress = st.progress(0)
            status = st.empty()

            for i, row in df.iterrows():
                college = row["College Name"]
                url = row["URL"]

                status.write(f"⏳ Scraping: **{college}**")

                # Step 1 - Scrape
                scraped_text = scrape_page(url)

                # Step 2 - Extract with AI
                highest, average = extract_packages_with_ai(college, scraped_text)

                results.append({
                    "College Name": college,
                    "URL": url,
                    "Highest Package (LPA)": highest,
                    "Average Package (LPA)": average
                })

                progress.progress((i + 1) / len(df))

            status.write("✅ Analysis Complete!")

            results_df = pd.DataFrame(results)

            # CSV 1 - Sorted by Highest Package
            highest_df = results_df[["College Name", "URL", "Highest Package (LPA)"]]\
                .sort_values("Highest Package (LPA)", ascending=False)\
                .reset_index(drop=True)

            # CSV 2 - Sorted by Average Package
            average_df = results_df[["College Name", "URL", "Average Package (LPA)"]]\
                .sort_values("Average Package (LPA)", ascending=False)\
                .reset_index(drop=True)

            # Show results
            st.subheader("🏆 Highest Package - All Colleges")
            st.dataframe(highest_df)

            st.subheader("📊 Average Package - All Colleges")
            st.dataframe(average_df)

            # Download buttons
            col1, col2 = st.columns(2)

            with col1:
                csv1 = highest_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Highest Package CSV",
                    data=csv1,
                    file_name="highest_package_colleges.csv",
                    mime="text/csv"
                )

            with col2:
                csv2 = average_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Average Package CSV",
                    data=csv2,
                    file_name="average_package_colleges.csv",
                    mime="text/csv"
                )
