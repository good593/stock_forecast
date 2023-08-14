import os 
import random 
import numpy as np 
import torch 
from tqdm import tqdm
import math

import pandas as pd 

def reset_seeds(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)    # 파이썬 환경변수 시드 고정
    np.random.seed(seed)
    torch.manual_seed(seed) # cpu 연산 무작위 고정
    torch.cuda.manual_seed(seed) # gpu 연산 무작위 고정
    torch.backends.cudnn.deterministic = True  # cuda 라이브러리에서 Deterministic(결정론적)으로 예측하기 (예측에 대한 불확실성 제거 )

def load_corps(corps_path:str) -> pd.DataFrame:
    df_dtype = {
        'stock_code': 'object'
    }

    df = pd.read_csv(corps_path, dtype=df_dtype)
    print(df.shape)
    return df 

def load_stock(stock_code_list:list, stock_path:str) -> dict:
    stock_df_dict = {}
    for stock_code in tqdm(stock_code_list):
        save_path = stock_path.format(stock_code=stock_code)
        df_dtype = {
            'stock_code':'object'
        }
        stock_df = pd.read_csv(save_path, index_col='Date', dtype=df_dtype, parse_dates=['Date'])
        stock_df_dict[stock_code] = stock_df
    
    print(len(stock_df_dict.keys()))
    return stock_df_dict



