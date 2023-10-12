import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv("Reach_Data_GCPL.csv")
profile = ProfileReport(df,minimal=True,
                       title="Linear TV Ads",
                       dataset={
        "description": "This dataset is about linear tv ad reach with cost and time slot."
    })

profile.to_file("data_profile.html")