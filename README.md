# Data Exploration App

A Streamlit application for interactive data exploration, enabling users to upload CSV or Excel datasets and explore them using text and numeric filters. The app allows the creation of visualizations and charts to gain insights from the data. Filtered datasets and generated visualizations are fully downloadable directly from the application. Uploaded datasets can be stored in a PostgreSQL database for easy access to previous uploads, and the application also functions seamlessly without a database. Additionally, the app supports downloading datasets directly from Kaggle.

--- 
## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Design Notes / How It Works](#design-notes--how-it-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Future Work / Roadmap](#future-work--roadmap)
---

## Features

- **Dataset Upload & Management**  
  - Upload CSV or Excel files directly into the app or via a Kaggle dataset identifier.  
  - Automatically store uploaded datasets in PostgreSQL when SQL mode is enabled for reuse across sessions.  
  - Select previously uploaded files from a dropdown to avoid re-uploading. Mistakenly uploaded files can be deleted from the database to clear clutter.  

- **Flexible Filtering**  
  - Filter datasets by **text keywords** across string columns and by **numeric ranges**, including open-ended conditions such as greater than or less than.  
  - Automatically detect column types so that only string columns are available for text searches and only numeric columns are available for range filters.  
  - Identify numeric ID columns and treat them as strings to enable accurate text filtering of identifiers.  

- **Interactive Graph Generation**  
  - Choose from multiple chart types: bar, line, scatter, pie, and heatmap.  
  - Customize graphs with options for binning, stacking, and color-coding categories.  
  - Add and customize multiple graphs simultaneously.  
  - Graphs update automatically when dynamic inputs change, enabling real-time data exploration.  

- **Data & Chart Export**  
  - Download filtered datasets in CSV format directly from the app.  
  - Download generated visualizations as PNG images for offline use or reporting.  

- **Error Handling & User Feedback**  
  - Display clear error messages via custom modal dialogs for SQL connection failures or invalid Kaggle dataset identifiers.  
  - Notify users if SQL mode is disabled due to a connection failure.  
  - Prompt users to check and correct invalid Kaggle dataset identifiers.  

- **Optimized Performance**  
  - Utilize caching to accelerate data loading, filtering, and visualization, ensuring smooth interaction even with larger datasets.

---

## Tech Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io/) for interactive dashboards and input components  
- **Data Processing**: [pandas](https://pandas.pydata.org/) for in-memory analysis and filtering  
- **Database / DB Access**: [PostgreSQL](https://www.postgresql.org/) for persistent dataset storage, accessed via [psycopg2](https://www.psycopg.org/) for executing general queries and [SQLAlchemy](https://www.sqlalchemy.org/) for queries that require creating/selecting a pandas dataframe table using SQL.

- **Application Graphs**: Interactive graphs generated using [Streamlit](https://streamlit.io/) native charting APIs and [Plotly Express](https://plotly.com/python/plotly-express/) for more advanced visualizations. 
- **Configuration**: `.env` for credentials, `config.yaml` for feature toggles  
- **Notebook Analysis**: Used [Jupyter](https://jupyter.org/) notebooks with [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/) for exploratory data analysis & visualization, correlation heatmaps, and pair plots.  
  

---
## Design Notes / How It Works

- **Configuration Layer**  
  - Runtime settings are loaded from `.env` and `config.yaml` through a central `Settings` utility.  
  - Separates sensitive credentials (`.env`) from non-sensitive configuration (`config.yaml`) for cleaner and safer app configuration management.
  - SQL mode can be toggled on or off at startup, enabling the same app to run with or without PostgreSQL.  

- **Session State Management**  
  - A custom utility (`st_helpers`) manages widget creation and key tracking, ensuring consistent mapping between Streamlit components and their saved values.  
  - This utility organizes session state into structured sections (datasets, filters, graphs) so that all user inputs and configurations persist reliably across reruns.  
  - Filters are reapplied automatically on rerun by restoring saved values from session state, and graph configurations (columns, bins, stacking, colors) are stored in structured state objects so multiple independent charts can persist and update in real time.

- **Database Layer**  
  - A dedicated `DBConnection` class handles PostgreSQL connectivity via SQLAlchemy.  
  - On startup, it verifies the target database exists (creating it if necessary) and initializes SQLAlchemy engines/sessions.  
  - Provides a thin abstraction for executing queries and returning results as pandas DataFrames, simplifying integration with the filtering layer.  

- **Caching & Performance**  
  - `st.cache_data` is used for expensive but deterministic operations like reading large datasets.  
  - `st.cache_resource` is applied to long-lived objects such as database connections.  
  - Caching dramatically reduces startup latency and filtering delays for larger datasets.  

- **File Upload & Streamlit Limitations**  
  - The native `st.file_uploader` widget cannot be programmatically cleared due to Streamlit limitations, which normally requires the user to press the built-in ❌ button to reset.  
  - To work around this, the uploader is instantiated with a dynamic key, which is incremented to create a new uploader on rerun, ensuring a seamless experience when switching uploads.  

- **Exception Handling & Workflow**  
  - Risky operations (database connections, Kaggle fetches) are wrapped in try/except blocks to prevent crashes and allow graceful recovery.  
  - Exceptions are displayed in custom modal dialogs, providing informative feedback while keeping the UI clean.  
  - App configurations are updated automatically after failures (e.g., disabling SQL mode) so that errors do not disrupt the app’s continued operation.

---

## Project Structure
```
project/
├── notebooks/                    # Jupyter notebooks for data exploration
│   └── data_visualization.ipynb  # Explores manufacturing_defects.csv specifically
├── src/                          # Main application source code
│   └── app.py                    # Entry point for the Streamlit app  
├── project_utils/                # Helpers for data parsing and loading
│   ├── datahelpers.py            # Data summarization, analysis helpers  
│   └── read_data.py              # CSV/Excel reading and Kaggle downloading  
├── util_app/                     # Application-specific utilities
│   ├── db/                       # Database connection and SQL helpers
│   │   ├── db_connection.py      # DBConnection class (connect, query execution, close)
│   │   └── sql_helpers.py        # SQL query constructors
│   ├── filters/                  # Filtering logic
│   │   ├── filters.py            # Build streamlit search UI + filter application
│   │   └── pd_filters.py         # Pandas-based filter methods
│   ├── ui/                       # Streamlit UI components
│   │   ├── dataframes.py         # Display dataframe analysis and filtering
│   │   ├── dialogs.py            # Custom st.dialogs 
│   │   ├── file_upload.py        # File upload handling
│   │   ├── graphs.py             # Graph creation and plotting
│   │   ├── sections.py           # Section builders for app layout
│   │   └── st_helpers.py         # Streamlit input & session_state helpers
│   └── utils/                    # Supporting utilities
│       ├── id_generator.py       # Unique ID generator
│       └── settings.py           # Loads .env + config.yaml and manages settings
├── test_data/                    # Sample/test datasets  
├── .env                          # Environment variables (ignored in git)  
├── .env.example                  # Example environment file  
├── .gitignore                    # Ignore files for storage & security(e.g. test_data/ files and .env)
├── config.yaml                   # Feature toggles (e.g. SQL enable)  
├── requirements.txt              # Python dependencies
```
---

## Installation

1. Clone this repository:  
   ```bash
   git clone https://github.com/CLiang531/data-exploration-app.git
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
   on Anaconda, do:
   ```bash
   conda create -n venv
   conda activate venv
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Set up PostgreSQL and configure `.env` using `.env.example` as a reference. To copy the example file, run 
   ```bash 
   cp .env.example .env
   ```
---

## Usage

To the run the app after installation:
1. Edit `config.yaml` to enable or disable SQL for filtering. If enabled, verify that SQL credentials in `.env` are accurate. 
2. In the project directory, run
   ```bash
   cd src
   python -m streamlit run app.py
   ```
   Alternatively, run
   ```bash
   cd src
   streamlit run app.py
   ```
4. If the app does not pop up on its own, navigate to `localhost:8501` on your browswer

**Note:** If SQL is enabled, uploaded datasets will be remembered across runs. Otherwise, filtering and exploration are done in-memory with pandas and will not save.

---

## Future Work / Roadmap

- [ ] **SQL Filtering Support**
  - Add SQL-based filtering for larger datasets 
- [ ] **Authentication & User Accounts**  
  - Allow users to log in and save their datasets/graphs across sessions using [Firebase](https://firebase.google.com/).  
- [ ] **Containerization and Cloud Deployment**  
  - Containerize the app with [Docker](https://www.docker.com/) and support deployment on [AWS](https://aws.amazon.com/)/[Azure](https://azure.microsoft.com/)/[GCP](https://cloud.google.com/).
- [ ] **LLM-powered Q&A**
   - Integrate [OpenAI GPT](https://openai.com/) LLM to enable natural language queries directly on datasets so that users can ask specific questions that aren't supported through current search and analysis options.
- [ ] **Support Comparisons Across Datasets**
   - Allow users to compare multiple datasets side by side; current implementation only allows analysis of one file.


