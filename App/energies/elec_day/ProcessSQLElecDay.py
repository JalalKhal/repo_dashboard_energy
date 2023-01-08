from App.energies.ProcessSQL import ProcessSQL
import json
import pandas as pd

class ProcessSQLElecDay(ProcessSQL):
    def __init__(self,data_json_str=""):
        # Call the superclass's constructor to initialize the table name and the data_json_str attribute
        super().__init__(table_name="elec_day_energy_tbs",data_json_str=data_json_str)

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
        # Add new columns with the month, day, quarter, and year
        df["jour"]=pd.to_datetime(df["jour"])
        df["month"]=df["jour"].dt.month
        df["day"]=df["jour"].dt.day
        df["quarter"]=df["jour"].dt.quarter
        df["year"]=df["jour"].dt.year
        return df

    def get_mask(self,df,df_inserver):
        # Return a mask that selects rows that are either in df but not in df_inserver
        # based on the "categorie" column, or rows that are in df but not in df_inserver
        # based on the "jour" column
        return ~(df["categorie"].isin(df_inserver["categorie"])) | ~df["jour"].isin(df_inserver["jour"])
        #test if duplicates exists




