# 📦 PackageMapper AI

A web application that automatically scrapes college placement websites 
and analyzes placement package data using AI.

## 🚀 Live Demo
[Click here to view the app](https://packagemapperai-tmpuhn8zsbkpefnbmku2zn.streamlit.app/)

## 🛠️ Built With
- [Streamlit](https://streamlit.io/) - Web framework
- [Groq API](https://console.groq.com/) - AI inference
- [Llama 3.3 70B](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) - Language model
- [Pandas](https://pandas.pydata.org/) - Data processing
- [Requests](https://requests.readthedocs.io/) - Web scraping

## ✨ Features
- Upload CSV file with college names and URLs
- Automatically scrapes each college placement page
- AI extracts highest and average package data
- Displays results in a clean table
- Download two separate CSV files:
  - 🏆 Highest Package CSV — colleges sorted by highest package
  - 📊 Average Package CSV — colleges sorted by average package

## 📁 Project Structure

package-mapper-ai/
├── App.py
└── requirements.txt


## 📂 Input File Format
Your CSV file must have exactly these two columns:

| College Name | URL |
|---|---|
| IIT Bombay | https://www.iitb.ac.in/placements |
| IIT Delhi | https://home.iitd.ac.in/placements.php |
| NIT Trichy | https://www.nitt.edu/placements |

## 📤 Output Files
The app generates two downloadable CSV files:

**1. highest_package_colleges.csv**
| College Name | URL | Highest Package (LPA) |
|---|---|---|
| IIT Bombay | https://... | 2.4 |
| IIT Delhi | https://... | 2.0 |

**2. average_package_colleges.csv**
| College Name | URL | Average Package (LPA) |
|---|---|---|
| IIT Bombay | https://... | 20.5 |
| IIT Delhi | https://... | 18.0 |

## ⚙️ How to Run Locally
1. Clone the repository
2. bash
git clone https://github.com/08theabhi/Package_Mapper_AI
cd Package_Mapper_AI


2. Install dependencies
bash
pip install -r requirements.txt


3. Add your Groq API key in `App.py`
python
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"


4. Run the app
bash
streamlit run App.py


## 🔑 API Key Setup
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to **API Keys** → **Create API Key**
4. Copy and paste the key into `App.py`

## 🧠 How It Works

Upload CSV (College Name + URL)
        ↓
App scrapes each college URL
        ↓
Groq AI reads scraped text
        ↓
AI extracts Highest & Average Package
        ↓
Results shown in table
        ↓
Download 2 CSV files


## ⚠️ How to Convert Excel to CSV
Since the app accepts CSV files:
1. Open your Excel file
2. Click **File → Save As**
3. Choose **CSV UTF-8 (.csv)** format
4. Upload the CSV file to the app

## ⚠️ Notes
- Some college URLs may block scraping and return 0 for package data
- Make sure your CSV columns are named exactly:
  - `College Name`
  - `URL`

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
