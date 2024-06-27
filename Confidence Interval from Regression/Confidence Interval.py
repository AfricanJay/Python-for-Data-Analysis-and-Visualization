import Advanced_reg

#Confidence interval for the E(Y|X):
#predict the outcomes with predict command and use the se.fit = T,

pred_CI = reg4.get_prediction().summary_frame(alpha=0.05)
pred_CI.head()

#Add the CI values to vienna dataset

vienna["CI_up"] = pred_CI["mean_ci_lower"]

(
    ggplot(data=vienna)
    + geom_point(aes(x="distance", y="lnprice"), color="blue", size=2)
    + geom_line(aes(x="distance", y="lnprice_hat"), color="red", size=1)
    + geom_line(aes(x="distance", y="CI_up"), color="red", size=0.5, linetype="dashed")
    + geom_line(aes(x="distance", y="CI_low"), color="red", size=0.5, linetype="dashed")
    + labs(x="Distance to city center (miles)", y="Log of price (US dollars)")
    + theme_bw()
)

#predicting any new potential variable

new_hotel_vienna = pd.DataFrame(
    {"distance": 2.5, "star3": 0, "star35": 0, "rating": 3.2}, index=[0]
)

pred_new = reg4.get_prediction(new_hotel_vienna).summary_frame(alpha=0.05)
pred_new

pred_new["pred_price"] = np.exp(pred_new["mean"])*corr_term
pred_new["CI_low"] = np.exp(pred_new["mean_ci_lower"])*corr_term
pred_new["CI_up"] = np.exp(pred_new["mean_ci_upper"])*corr_term

pred_new.filter(["CI_low","pred_price","CI_up"])

#Prediction interval: considers the inherent error 


pred_new["PI_low"] = np.exp(pred_new["obs_ci_lower"])*corr_term
pred_new["PI_up"] = np.exp(pred_new["obs_ci_upper"])*corr_term

pred_new.filter(["PI_low","pred_price","PI_up"])

#comparison of results

#the model itself 

pred_new.filter(["pred_price","CI_low","CI_up","PI_low","PI_up"])
vienna["CI_low"] = pred_CI["mean_ci_upper"]

reg_poly = smf.ols(
    "lnprice ~ distance + np.power(distance, 2)+ np.power(distance, 3) + rating + np.power(rating, 2)+ np.power(rating, 3)+ star3 + star35",
    data=vienna,
).fit(cov_type="HC3")

#Predictions and errors

#for log values

vienna["lnprice_hat_rp"] = reg_poly.fittedvalues

#error for the levels

corr_term_rp = np.exp(vienna["lnprice_resid_rp"].mean() / 2)
vienna["price_hat_rp"] = np.exp(vienna["lnprice_hat_rp"]) * corr_term_rp
vienna["price_resid_rp"] = vienna["price"] - vienna["price_hat_rp"]

#residual vs distance graph

(
    ggplot(vienna, aes(x="distance", y="price_resid_rp"))
    + geom_point(color="red", size=2)
    + geom_smooth(method="lm", colour="blue", se=False, formula="y~x")
    + labs(x="Distance", y="Residuals")
    + theme_bw()
)

#Create a residual vs ratings graph

(
    ggplot(vienna, aes(x="rating", y="price_resid_rp"))
    + geom_point(color="red", size=2)
    + geom_smooth(method="lm", colour="blue", se=False, formula="y~x")
    + labs(x="Ratings of the hotels", y="Residuals")
    + scale_x_continuous(
        expand=(0.01, 0.01), limits=(2, 5), breaks=np.arange(2, 5, 0.5)
    )
    + theme_bw()
)
vienna["lnprice_resid_rp"] = reg_poly.resid
