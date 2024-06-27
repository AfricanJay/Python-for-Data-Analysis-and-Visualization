#Created  by Jennifer Onyeama

#Multiple regression
#Model choice with multiple regressors
#Prediction with multiple regressors:
#useful graphs for predictions
#Confidence Interval
#Prediction Interval
#- Robustness tests/External validity
#Time/Location/Type


import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from plotnine import *
from skimpy import skim
from stargazer.stargazer import Stargazer

%matplotlib inline
warnings.filterwarnings("ignore")

#using European data observations

hotels_europe_price = pd.read_csv("https://osf.io/p6tyr/download")
hotels_europe_features = pd.read_csv("https://osf.io/utwjs/download")

#Join them by hotel_id

europe = hotels_europe_price.merge(hotels_europe_features, on = "hotel_id")
europe.head()

del hotels_europe_price
del hotels_europe_features

#mulitple linear regression

vienna = (
    europe.loc[lambda x: x["accommodation_type"] == "Hotel"]
    .loc[lambda x: (x["year"] == 2017) & (x["month"] == 11) & (x["weekend"] == 0)]
    .loc[lambda x: x["city_actual"] == "Vienna"]
    .loc[lambda x: (x["stars"] >= 3) & (x["stars"] <= 4)]
    .loc[lambda x: x["stars"].notnull()]
    .loc[lambda x: x["price"]<=600]
)

 #calculate log price

vienna["lnprice"] = np.log(vienna["price"])

#Summary statistics on price and log of price

(
    vienna.filter(["price", "lnprice", "distance", "stars", "rating"])
    .describe(percentiles=[0.5, 0.95])
    .T
)
skim(vienna.filter(["price", "lnprice", "distance", "stars", "rating"]))

#check the scatter plots - with the visual inspection 

(
    ggplot(vienna, aes(x="distance", y="lnprice"))
    + geom_point(color="red", size=2)
    + geom_smooth(method="loess", color = "blue")
    + labs(x="Distance to city center (miles)", y="Log of price (US dollars)")
    + theme_bw()
)


#stars vs price

(
    ggplot(vienna, aes(x="stars", y="lnprice"))
    + geom_point(color="red", size=2)
    + geom_smooth(method="lm", color="blue")
    + labs(x="Star of the Hotel", y="Log of price (US dollars)")
    + theme_bw()
)

(
    ggplot(vienna, aes(x="rating", y="lnprice"))
    + geom_point(color="red", size=2)
    + geom_smooth(method="loess", color = "blue")
    + labs(x = "Ratings of the hotel",y = "Log of price (US dollars)")
    + theme_bw()
)

#Running regressions

#Baseline A: use only rating with heteroscedastic SE

reg0 = smf.ols("lnprice ~ rating", data=vienna).fit(cov_type ="HC3")
print(reg0.summary())

#Baseline B: use only distance with heteroscedastic SE

reg1 = smf.ols("lnprice ~ distance", data=vienna).fit(cov_type ="HC3")
print(reg1.summary())

#Multiple regression with both rating and distance

reg2 = smf.ols("lnprice ~ distance + rating", data=vienna).fit(cov_type ="HC3")
print(reg2.summary())


vienna["star3"] = np.where(vienna["stars"] == 3,1,0)
vienna["star35"] = np.where(vienna["stars"] == 3.5,1,0)
vienna["star4"] = np.where(vienna["stars"] == 4,1,0)

reg3 = smf.ols("lnprice ~ distance + rating + star3 + star35", data=vienna).fit(cov_type ="HC3")
reg3.summary()

#Compare results

table = Stargazer([reg0, reg1, reg2,reg3])


import copy
def lspline(series, knots):
    def knot_ceil(vector, knot):
        vector_copy = copy.deepcopy(vector)
        vector_copy[vector_copy > knot] = knot
        return vector_copy

    if type(knots) != list:
        knots = [knots]
    design_matrix = None
    vector = series.values

    for i in range(len(knots)):
        # print(i)
        # print(vector)
        if i == 0:
            column = knot_ceil(vector, knots[i])
        else:
            column = knot_ceil(vector, knots[i] - knots[i - 1])
        # print(column)
        if i == 0:
            design_matrix = column
        else:
            design_matrix = np.column_stack((design_matrix, column))
        # print(design_matrix)
        vector = vector - column
    design_matrix = np.column_stack((design_matrix, vector))
    # print(design_matrix)
    return design_matri

table


#result analysis using regression 4

#Save the predicted and residual values

vienna["lnprice_hat"] = reg4.fittedvalues
vienna["lnprice_resid"] = reg4.resid

corr_term = np.exp(vienna["lnprice_resid"].mean() / 2)
vienna["price_hat"] = np.exp(vienna["lnprice_hat"]) * corr_term

#List of 5 best deals

vienna.sort_values(by="lnprice_resid").head(5).filter(
    [
        "hotel_id",
        "price",
        "price_hat",
        "lnprice",
        "lnprice_hat",
        "lnprice_resid",
        "distance",
        "stars",
        "rating",
    ]
)

#y - yhat graph (regression line must be the same as the 45 degree line!)
(
    ggplot(vienna, aes(x="lnprice_hat", y="lnprice"))
    + geom_point()
    + geom_smooth(method="lm", formula="y~x", se=False)
    + labs(x="ln(predicted price, US dollars) ", y="ln(price, US dollars)")
    + geom_segment(
        aes(x=4.8, y=4.1, xend=4.68, yend=4.1),
        arrow=arrow(),
        color="red",
    )
    + annotate("text", x=4.95, y=4.1, label="Best deal", size=8, color="red")
    + geom_abline(intercept=0, slope=1, size=0.5, color="red", linetype="dashed")
    + coord_cartesian(xlim=(4, 5.5), ylim=(4, 5.5))
    + theme_bw()
)

residual - yhat graph: it needs to be flat
(
    ggplot(vienna, aes(x="lnprice_hat", y="lnprice_resid"))
    + geom_point(color="red", size=2)
    + geom_smooth(method="lm", colour="blue", se=False, formula="y~x")
    + labs(x="ln(Predicted hotel price, US dollars)", y="Residuals")
    + theme_bw()
)

