from App.energies.ProcessSQL import ProcessSQL
import json
import pandas as pd

class ProcessSQLGazIndustriel(ProcessSQL):
    def __init__(self,data_json_str=""):
        super().__init__(table_name="gaz_industriel_energy_tbs",data_json_str=data_json_str)

    def g(self,i):
        if -1<i and i<10:
            return "0"+str(i)
        return str(i)

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
        df=pd.read_json(json.dumps(records),orient="index")
        columns=["date","operateur","secteur_d_activite","consommation_journaliere_mwh_pcs"]+ \
                [self.g(i)+"_00" for i in range(24)]
        df=df[columns]
        # Rename some of the columns
        df=df.rename(columns={"consommation_journaliere_mwh_pcs":"conso","secteur_d_activite":"secteur"})
        # Add new columns with the month, day, quarter, and year
        df["month"]=df["date"].dt.month
        df["day"]=df["date"].dt.day
        df["quarter"]=df["date"].dt.quarter
        df["year"]=df["date"].dt.year
        for column_int in df.columns[3:]:
            df[column_int]=pd.to_numeric(df[column_int], errors='coerce')#transform non numeric value to NaN
        df=df.dropna()
        return df

    def get_mask(self,df,df_inserver):
        return ~(df["date"].isin(df_inserver["date"])) | ~df["operateur"].isin(df_inserver["operateur"])
        #test if duplicates exists








