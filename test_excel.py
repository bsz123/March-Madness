import pandas as pd

try:
    # Try reading with minimal formatting
    df = pd.read_excel("NCAA-data/fg-percent.xlsx", engine='openpyxl', style_compression=True)
    print("Successfully read the file!")
    print(df.head())
except Exception as e:
    print(f"Error reading with style_compression: {str(e)}")
    
    try:
        # Try reading with data_only option
        df = pd.read_excel("NCAA-data/fg-percent.xlsx", engine='openpyxl', 
                         engine_kwargs={'options': {'data_only': True}})
        print("\nSuccessfully read the file with data_only!")
        print(df.head())
    except Exception as e:
        print(f"\nError reading with data_only: {str(e)}")

