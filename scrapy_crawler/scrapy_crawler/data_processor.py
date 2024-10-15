import pandas as pd

def process_data(data):
    
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset='url', keep='first')
    return df
