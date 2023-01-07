from App.energies.ProcessSQL import ProcessSQL
import json
import pandas as pd
import re

class ProcessSQLElecMet(ProcessSQL):
    def __init__(self,data_json_str=""):
        super().__init__(table_name="elec_met_energy_tbs",data_json_str=data_json_str)

    def process_data(self):
        #Pre-processing
        # Extract the records from the JSON object
        data_json_str=self.data_json_str
        data_json=json.loads(data_json_str)
        records=data_json["records"]
        try:
            dict_rec=records[0]
        except IndexError:
            print("Aucun enregistrements trouvés à cette date !")
            exit(0)
        features=list(dict_rec["fields"].keys())
        # Construct a list of dictionaries, each containing the feature-value pairs for a record
        records=[{feature:value for feature,value in \
                  zip(features,list(dict_rec["fields"].values()))} for dict_rec in records]
        records={i:dict_i for i,dict_i in enumerate(records)}
        # Convert the list of dictionaries to a pandas DataFrame
        df=pd.read_json(json.dumps(records),orient="index")
        df =df[["libelle_metropole", "consommation", "date", "heures"]]
        pattern = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}")
        mask=df["date"].astype(str).apply(lambda x:bool(pattern.fullmatch(x)))
        df=df.loc[mask]
        df["date"] = pd.to_datetime(df["date"]).dt.strftime('%d/%m/%Y')
        return df

    def get_mask(self,df,df_inserver):
        return df.index==df.index
    #the data represent don't have primary key because the electricty
    #consumption is at metropolis level, so one metropolis can have multiple
    #rows in the data frame corresponding to each place/city of the metropolis
    #but the api doesn't identify clearly each city from the metropolis








