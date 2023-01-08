from App.energies.ProcessSQL import ProcessSQL
import json
import pandas as pd

class ProcessSQLGaz(ProcessSQL):
    def __init__(self,data_json_str=""):
        super().__init__(table_name="gaz_energy_tbs",data_json_str=data_json_str)

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
        # Drop the mois column and select certain columns
        df=df.drop("mois",axis=1)
        columns=["date","code_insee_region","region","secteur_d_activite","operateur","conso_journaliere_mwh_pcs_0degc"]+ \
                ["00_00_00"]+["0"+str(i+1)+"_00" for i in range(4)]+["05_00_00","06_00_00"]+ ["0"+str(i+1)+"_00" for i in range(6,9)]+["10_00"]+ \
                ["11_00_00","12_00_00"]+[str(i+1)+"_00" for i in range(12,18)]+["19_00_00"]+[str(i+1)+"_00" for i in range(19,23)]
        df=df[columns]
        df.columns=[col[:5] for col in df.columns]
        # Rename some columns
        df=df.rename(columns={"regio":"region","opera":"operateur","code_":"code",})
        # Define a mapping from regions to region groups
        groups_region={"Île-de-France":0,"Grand Est":0,"Hauts-de-France":0,"Bourgogne-Franche-Comté":1,"Auvergne-Rhône-Alpes":1, \
                       "Provence-Alpes-Côte d'Azur":1,"Occitanie":2,"Nouvelle-Aquitaine":2,"Centre-Val de Loire":2, \
                       "Normandie":3,"Bretagne":3,"Pays de la Loire":3}
        map_groups={0:"Nord-est",1:"Sud-est",2:"Sud-ouest",3:"Nord-ouest"}
        # Add a column with the region group label
        df["region_groups"]=[map_groups[groups_region[region]] for region in df["region"]]
        df["02_00"]=df[["01_00","03_00"]].mean(axis=1) #inconsistent data for 2 am

        # Add new columns with the month, day, quarter, and year
        df["month"]=df["date"].dt.month
        df["day"]=df["date"].dt.day
        df["quarter"]=df["date"].dt.quarter
        df["year"]=df["date"].dt.year
        # Rearrange the columns
        df=df[list(df.columns[:1])+["region_groups"]+list(df.columns[-1:-5:-1])+list(df.columns[1:30])]
        return df

    def get_mask(self,df,df_inserver):
        return ~(df["date"].isin(df_inserver["date"])) | ~df["code"].isin(df_inserver["code"])
        #test if duplicates exists








