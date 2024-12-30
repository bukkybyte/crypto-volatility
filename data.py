import pandas as pd
import requests


class CryptoCompareAPI():
    
	def __init__(self):
		# Attributes
		self.url = "https://min-api.cryptocompare.com/data/v2/histoday"
      
  
	def getCoinPrice(self, ticker: str, n_records: int):
		"""Get Coin daily params from Crypto Compare 

		Args:
			ticker (str): the id of the coin
			n_records (int): days of coin records

		Returns:
			DataFrame:  A data frame containing coin params and with timestamps
		"""
		params = {
			"fsym" : ticker,
			"tsym" : "USD",
			"limit" : n_records
		}
      
		try:
			responses = requests.get(self.url, params=params)
			result = responses.json()

			if responses.status_code == 200 and result["Response"] == "Error":
				result = result["Message"]

			result = (pd.DataFrame(data=result["Data"]["Data"])[["time", "low", "high", "open", "close"]]).set_index("time")
			# rename index
			result.index.name = "date"
			# Change index to DateTime object
			result.index = pd.to_datetime(result.index, unit='s')
      
		except Exception as e:
			result = str(e)

		return result

        
class SQLRespository():
	def __init__(self, connection):
		self.connection = connection

	def insert_table(self, table_name: str, records: pd.DataFrame, if_exists: str = "replace") -> dict:
		"""Insert DataFrame into SQLite database as table

		Args:
		table_name (str): _description_
		records (pd.DataFrame): _description_
		if_exists (str, optional): _description_. Defaults to "replace".

		Returns:
		dict: record write status and numbers of records
		"""

		n_inserted = records.to_sql(name=table_name, con=self.connection, if_exists=if_exists)

		return {
		"transaction_successful" : True,
		"records_inserted" : n_inserted
		}

	def __wrangle(self, df: pd.DataFrame):
		# Set the index of the data to date and fill Nan rows
		df = df.set_index("date").ffill()
		df.index = pd.to_datetime(df.index)
		return df
     
	def read_table(self, table_name: str):
		"""Read table from SQLite database into a DataFrame

		Args:
			table_name (_type_): SQL tabel name

		Returns:
			pd.DataFrame: _description_
		"""
		query = f"SELECT * FROM {table_name}"
  
		df = self.__wrangle(pd.read_sql(sql=query, con=self.connection))

		return df
	
    

 
    
        