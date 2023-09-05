import requests
import pandas as pd
from urllib import parse

class utils:
  @staticmethod
  def get_dataframe_by_period(dataframe, start_year, start_month, end_year, end_month, country):
    masking = (dataframe['Year'] == (str(start_year) + '년')) & (dataframe['month'] == (str(start_month) + '월'))
    start_idx = dataframe[masking].index.values[0]
    
    masking = (dataframe['Year'] == (str(end_year) + '년')) & (dataframe['month'] == (str(end_month) + '월'))
    end_idx =  dataframe[masking].index.values[0]
    
    # 법무부 제외
    dataframe = dataframe.drop(['법무부_명수', '법무부_전년대비'], axis=1)

    if country == '*':
      results = dataframe.loc[start_idx:end_idx]
      results = dataframe.fillna(0)              
    else:
      results = dataframe.loc[start_idx:end_idx, ['Year', 'month', f'{country}_명수']]
      results[f'{country}_명수'] = results[f'{country}_명수'].fillna(0)
      
    results['date'] = results['Year'] + results['month']
    
    return results
