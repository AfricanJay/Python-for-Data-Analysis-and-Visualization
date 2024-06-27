#Import packages

import warnings

import numpy as np
import pandas as pd
from plotnine import *
from skimpy import skim

%matplotlib inline
warnings.filterwarnings("ignore")

#Import World-Management Survey Data

wms  = pd.read_csv("https://osf.io/uzpce/download")
wms.head()
skim(wms)

#Creating a continuous variable out of ordered variables

wms["avg_score"] = wms.filter(regex="lean|perf|talent").mean(axis=1)
wms["avg_score"].describe()

wms["sum_aa"] = wms.filter(regex="aa_").sum(axis=1)
wms["sum_aa"].describe()

wms["country"].value_counts()
wms["country"].value_counts(normalize = True)

import pycountry_convert as pc

wms["continent"] = (
    wms["country"]
    .apply(lambda x: np.where(x == "Northern Ireland", "Ireland", x))
    .apply(lambda x: np.where(x == "Republic of Ireland", "Ireland", x))
    .apply(pc.country_name_to_country_alpha2) # converts country name to country code
    .apply(pc.country_alpha2_to_continent_code) # country code to continent code
    .apply(pc.convert_continent_code_to_continent_name)# continent code to name
)
wms["continent"].value_counts(dropna=False)

wms["ownership"].value_counts(dropna=False)
wms["owner"] = np.where(
    wms["ownership"].isnull(),
    np.nan,
    np.where(
        wms["ownership"] == "Government",
        "govt",
        np.where(
            wms["ownership"].str.contains("family", regex=False),
            "family",
            np.where(wms["ownership"] == "Other", "other", "private"),
        ),
    ),
)
wms["owner"].value_counts(dropna=False)
