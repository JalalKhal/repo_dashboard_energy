from App.energies.ProcessSQL import ProcessSQL
import json
import pandas as pd
import re

class ProcessSQLElecMet(ProcessSQL):
    def __init__(self,data_json_str=""):
        # Call the superclass's constructor to initialize the table name and the data_json_str attribute
        super().__init__(table_name="elec_met_energy_tbs",data_json_str=data_json_str)

    def process_data(self):
        # Extract the records from the JSON object stored in the data_json_str attribute
        data_json_str=self.data_json_str
        data_json=json.loads(data_json_str)
        records=data_json["records"]
        try:
            dict_rec=records[0]
        except IndexError:
            print("Aucun enregistrements trouvés à cette date !")
            exit(0)
        # Get the list of features (keys) from the first record
        features=list(dict_rec["fields"].keys())
        # Construct a list of dictionaries, each containing the feature-value pairs for a record
        records=[{feature:value for feature,value in \
                  zip(features,list(dict_rec["fields"].values()))} for dict_rec in records]
        # Assign a unique integer index to each record
        records={i:dict_i for i,dict_i in enumerate(records)}
        # Convert the list of dictionaries to a pandas DataFrame
        df=pd.read_json(json.dumps(records),orient="index")
        # Keep only the columns we are interested in
        df =df[["libelle_metropole", "consommation", "date", "heures"]]
        # Use a regular expression to filter out rows with invalid dates
        pattern = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}")
        mask=df["date"].astype(str).apply(lambda x:bool(pattern.fullmatch(x)))
        df=df.loc[mask]
        # Convert the dates to a different format
        df["date"] = pd.to_datetime(df["date"]).dt.strftime('%d/%m/%Y')
        return df

    def get_mask(self,df,df_inserver):
        # Return a mask that selects all rows in the dataframe
        return df.index==df.index
    #the data represent don't have primary key because the electricty
    #consumption is at metropolis level, so one metropolis can have multiple
    #rows in the data frame corresponding to each place/city of the metropolis
    #but the api doesn't identify clearly each city from the metropolis
