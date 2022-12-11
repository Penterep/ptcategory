import json
import pandas as pd


class JsonExporter:
    def __init__(self, urls: list[str]) -> None:
        self.urls = urls
        self.export_with_parameters = False
        self.export_with_averages = False
        
        
    def export_to_file(self, df :pd.DataFrame, file_name: str) -> None:
        res = {}
        df.insert(0, "URL", self.urls)
        groups = df.groupby("cluster")
        for scalar, group in groups:
            group_res = res[scalar] = {}
            group_res["Count"] = len(group)
            group.drop("cluster", axis=1, inplace=True)
            
            if self.export_with_averages:
                group_res["Average"] = group.mean(numeric_only=True).to_dict()
                group_res["Min"] = group.min(numeric_only=True).to_dict()
                group_res["Max"] = group.max(numeric_only=True).to_dict()
            
            if self.export_with_parameters:
                group_res["Items"] = group.to_dict(orient="records")
            else:
                group_res["Items"] = group["URL"].to_list()
            
        with open(file_name, "w") as f:
            json.dump(res, f, indent=4)
            
