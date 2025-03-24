# Python SQLite App

## Overview
This project is a Python application that utilizes SQLite to manage and analyze NCAA basketball data. It loads data from Excel files, merges the datasets, and provides visualizations using Streamlit.

1. Setup the SQLite database and tables:
   - The `db_setup.py` script creates the database and tables, and inserts data from the Excel files.

## Project Structure
```
python-sqlite-app
├── src
│   ├── main.py          # Main entry point of the application
│   ├── db
│   │   └── setup_db.py  # Responsible for setting up the SQLite database
│   └── utils
│       └── data_loader.py # Utility functions for loading and transforming data
├── requirements.txt     # Lists the dependencies required for the project
└── README.md            # Documentation for the project
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-sqlite-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Prepare the SQLite database:
   - Run the `setup_db.py` script to create the database and tables, and to insert data from the Excel files.

## Usage
- To run the application, execute the `main.py` script:
  ```
  streamlit run src/main.py
  ```

- Follow the prompts in the Streamlit interface to select data for visualization.

## Dependencies
- pandas
- Streamlit
- Plotly
- SQLite

## Contributing
Feel free to submit issues or pull requests for improvements or additional features.