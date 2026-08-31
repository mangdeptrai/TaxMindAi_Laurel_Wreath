import pandas as pd
from taxtwin.models import Company
def load_company(file_path):
    df = pd.read_csv(file_path)
    return [Company(**row) for _, row in df.iterrows()]