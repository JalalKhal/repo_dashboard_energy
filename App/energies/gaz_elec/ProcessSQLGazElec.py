from App.energies.ProcessSQL import ProcessSQL
import json
import pandas as pd

class ProcessSQLGazElec(ProcessSQL):
    def __init__(self,data_json_str=""):
        super().__init__(table_name="gaz_elec_energy_tbs",data_json_str=data_json_str)

    def process_data(self):
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
        df=pd.read_json(json.dumps(records),orient="index")
        return df

    def get_mask(self,df,df_inserver):
        return ~(df["annee"].isin(df_inserver["annee"])) | ~df["libelle_region"].isin(df_inserver["libelle_region"]) \
            | ~df["filiere"].isin(df_inserver["filiere"]) | ~df["operateur"].isin(df_inserver["operateur"])
        #test if duplicates exists








