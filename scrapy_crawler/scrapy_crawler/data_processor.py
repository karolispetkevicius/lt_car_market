import pandas as pd

def process_data(data):
    
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset='url', keep='first')
    df['brand'] = df['brand'].str.replace('+',' ')
    df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce')
    df['mileage'] = df['mileage'].apply(lambda x: None if pd.isna(x) else int(x))
    df['price']= df['price'].apply(lambda x: None if pd.isna(x) else x)
    df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['year'] = df['year'].apply(lambda x: None if pd.isna(x) else x)
    return df
