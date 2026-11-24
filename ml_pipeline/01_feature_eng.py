import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input kolom wajib: pemasukan, total_hutang, tenor_bulan, pengeluaran_pokok
    """
    data = df.copy()
    data['cicilan_wajib'] = data['total_hutang'] / np.maximum(data['tenor_bulan'], 1)
    data['dti_ratio'] = (data['cicilan_wajib'] / np.maximum(data['pemasukan'], 1)) * 100
    data['eir_ratio'] = (data['pengeluaran_pokok'] / np.maximum(data['pemasukan'], 1)) * 100
    data['disposable_income'] = data['pemasukan'] - (data['pengeluaran_pokok'] + data['cicilan_wajib'])
    return data