
import pandas as pd

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["amount"] = df["amount"].fillna(0.0)
    df["log_amount"] = (df["amount"]+1).apply(lambda x: pd.np.log(x))
    df["is_fraud"] = df["is_fraud"].astype(int)
    return df