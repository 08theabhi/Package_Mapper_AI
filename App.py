 # your Groq key here  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
import streamlit as st
import pandas as pd
import requests
import io
from html.parser import HTMLParser

# ---- HTML Parser ----
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {"script", "style", "head", "meta"}
        self.current_skip = False

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.current_skip = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.current_skip = False

    def handle_data(self, data):
        if not self.current_skip:
            self.text.append(data.strip())

    def get_text(self):
        return " ".join(t for t in self.text if t)

st.set_page_config(page_title="PackageMapper AI", layout="wide")

GROQ_API_KEY = "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"  # your Groq key here

def scrape_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        parser = TextExtractor()
        parser.feed(response.text)
        text = parser.get_text()
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
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        result = response.json()["choices"][0]["message"]["content"].strip()

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
st.title("📦 PackageMapper AI")

# Explain conversion step
st.info("""
📌 **How to upload your Excel file:**
1. Open your Excel file
2. Click **File → Save As**
3. Choose **CSV UTF-8 (.csv)** format
4. Upload the CSV file below
""")

st.write("Upload a CSV file with **College Name** and **URL** columns.")

uploaded_file = st.file_uploader("📂 Upload File", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("📋 Uploaded Data:")
        st.dataframe(df)

        if "College Name" not in df.columns or "URL" not in df.columns:
            st.error("❌ File must have exactly 'College Name' and 'URL' columns.")
        else:
            if st.button("🔍 Analyze Placements"):
                results = []
                progress = st.progress(0)
                status = st.empty()

                for i, row in df.iterrows():
                    college = row["College Name"]
                    url = row["URL"]
                    status.write(f"⏳ Scraping: **{college}**")
                    scraped_text = scrape_page(url)
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

                highest_df = results_df[["College Name", "URL", "Highest Package (LPA)"]]\
                    .sort_values("Highest Package (LPA)", ascending=False)\
                    .reset_index(drop=True)

                average_df = results_df[["College Name", "URL", "Average Package (LPA)"]]\
                    .sort_values("Average Package (LPA)", ascending=False)\
                    .reset_index(drop=True)

                st.subheader("🏆 Highest Package - All Colleges")
                st.dataframe(highest_df)

                st.subheader("📊 Average Package - All Colleges")
                st.dataframe(average_df)

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
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
