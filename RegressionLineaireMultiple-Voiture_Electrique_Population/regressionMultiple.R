library(readr)
final_result <- read_csv("C:/Users/omari/Desktop/Work/DATASC/RegressionLineaireMultiple-Voiture_Electrique_Population/final_result.csv")


model <- lm(Total_Electric_Cars ~ ., data = final_result)

full_model <- lm(Total_Electric_Cars ~ ., data = final_result)
null_model <- lm(Total_Electric_Cars ~ 1, data = final_result)
step_aic <- step(null_model, 
                 scope = list(lower = null_model, upper = full_model), 
                 direction = "both", 
                 trace = FALSE)  # trace = TRUE shows the steps
summary(step_aic)

if (!require("olsrr")) {
  install.packages("olsrr")
}

library(olsrr)

# Full model: including all predictors
full_model <- lm(Total_Electric_Cars ~ ., data = final_result)

# Stepwise selection based on BIC (both forward and backward)
bic_model <- ols_step_both_p(full_model, criterion = "bic")

# Print results
print(bic_model)

# Summary of the final model
summary(bic_model$model)


# Residuals vs Fitted Plot
plot(model$fitted.values, resid(model),
     main = "Residuals vs Fitted Values",
     xlab = "Fitted Values",
     ylab = "Residuals",
     pch = 19, col = "blue")
abline(h = 0, col = "red", lwd = 2)


# Observed vs Predicted
plot(final_result$Total_Electric_Cars, model$fitted.values,
     main = "Observed vs Predicted",
     xlab = "Observed Values",
     ylab = "Predicted Values",
     pch = 19, col = "darkgreen")
abline(a = 0, b = 1, col = "red", lwd = 2)  # y = x line for perfect predictions

# Fit the linear regression model with only PopulationTotale
model_population <- lm(Total_Electric_Cars ~ PopulationTotale, data = final_result)

# Plot predicted vs actual values
plot(final_result$Total_Electric_Cars, model_population$fitted.values,
     main = "Observed vs Predicted: Population Only",
     xlab = "Observed Total Electric Cars",
     ylab = "Predicted Total Electric Cars",
     pch = 19, col = "blue")
abline(a = 0, b = 1, col = "red", lwd = 2)  # y = x line for perfect predictions




# Fit the linear regression model excluding PopulationTotale
model_others <- lm(Total_Electric_Cars ~ DEC_MED18 + NbrDePtsDeRech   , data = final_result)

# Plot predicted vs actual values
plot(final_result$Total_Electric_Cars, model_others$fitted.values,
     main = "Obsr vs Prediction : sans Population",
     xlab = "Observer Totale VE",
     ylab = "Prediction Totale VE",
     pch = 19, col = "blue")
abline(a = 0, b = 1, col = "red", lwd = 2)  # y = x line for perfect predictions


