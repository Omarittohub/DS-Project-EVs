# Charger les bibliothèques nécessaires
library(readr)

# Lire le fichier CSV
grouped_by_year <- read_csv("C:/Users/omari/Desktop/Work/DATASC/AvancementBorneEV/grouped_by_year_for_R_AllYears.csv")

# Effectuer une régression linéaire avec l'année comme variable indépendante et cumulative_total comme variable dépendante
linear_model <- lm(cumulative_total ~ year, data = grouped_by_year)

# Résumé de la régression linéaire
summary(linear_model)

# Générer des graphiques diagnostiques
par(mfrow = c(2, 2))  # Organiser les graphiques en une grille 2x2

# Graphiques diagnostiques pour le modèle de régression linéaire
plot(linear_model)

par(mfrow = c(1, 1)) 
plot(grouped_by_year$year, grouped_by_year$cumulative_total, 
     main = "Total Cumulé par rapport aux années", 
     xlab = "Année", ylab = "Total Cumulé", pch = 19, col = "blue")
abline(linear_model, col = "red", lwd = 2)


# Charger les bibliothèques nécessaires
library(readr)

# Lire le fichier CSV
grouped_by_year <- read_csv("C:/Users/omari/Desktop/Work/DATASC/AvancementBorneEV/grouped_by_year_for_R_AllYears.csv")

# Ajuster un modèle de régression exponentielle
# Transformer cumulative_total en échelle logarithmique
grouped_by_year$log_cumulative_total <- log(grouped_by_year$cumulative_total)

exp_model <- lm(log_cumulative_total ~ year, data = grouped_by_year)

# Résumé du modèle exponentiel
summary(exp_model)

# Ajuster un modèle de régression polynomial (degré 2 ou 3 selon les données)
poly_model <- lm(cumulative_total ~ poly(year, 2), data = grouped_by_year)

# Résumé du modèle polynomial
summary(poly_model)

# Tracer les données originales avec les modèles de régression
plot(grouped_by_year$year, grouped_by_year$cumulative_total, 
     main = "Total Cumulé par rapport aux Années avec les Modèles de Régression", 
     xlab = "Année", ylab = "Total Cumulé", pch = 19, col = "blue")

# Ajouter le modèle exponentiel
curve(exp(predict(exp_model, newdata = data.frame(year = x))), 
      add = TRUE, col = "red", lwd = 2)

# Ajouter le modèle polynomial
lines(grouped_by_year$year, predict(poly_model), col = "green", lwd = 2)

# Ajouter une légende
legend("topleft", legend = c("Exponentiel", "Polynomial"), 
       col = c("red", "green"), lwd = 2)











# Load necessary libraries
library(readr)

# Read the CSV file
grouped_by_year <- read_csv("C:/Users/omari/Desktop/Work/DATASC/AvancementBorneEV/grouped_by_year_for_R_AllYears.csv")

# Filter the data to include only years >= 1990
grouped_by_year_filtered <- grouped_by_year[grouped_by_year$year >= 2000, ]
grouped_by_year_filtered <- grouped_by_year_filtered[grouped_by_year_filtered$year < 2025, ]

# Fit an Exponential Regression Model
# Transform cumulative_total to log scale
grouped_by_year_filtered$log_cumulative_total <- log(grouped_by_year_filtered$cumulative_total)

exp_model <- lm(log_cumulative_total ~ year, data = grouped_by_year_filtered)

# Exponential Model Summary
summary(exp_model)

# Fit a Polynomial Regression Model (degree 2)
poly_model <- lm(cumulative_total ~ poly(year, 2), data = grouped_by_year_filtered)

# Polynomial Model Summary
summary(poly_model)

# Plot the Original Data with Regression Models (1990 onwards)
plot(grouped_by_year_filtered$year, grouped_by_year_filtered$cumulative_total, 
     main = "Cumulative Total vs Year (1990+) with Regression Models", 
     xlab = "Year", ylab = "Cumulative Total", pch = 19, col = "blue")

# Add Exponential Model
curve(exp(predict(exp_model, newdata = data.frame(year = x))), 
      add = TRUE, col = "red", lwd = 2)

# Add Polynomial Model
lines(grouped_by_year_filtered$year, predict(poly_model), col = "green", lwd = 2)

legend("topleft", legend = c("Exponential", "Polynomial"), 
       col = c("red", "green"), lwd = 2)







# Définir l'année future que l'on souhaite prédire
future_year <- 2030

# Créer un data frame pour l'année future
new_data <- data.frame(year = future_year)

# Prédiction avec le modèle exponentiel
exp_prediction <- exp(predict(exp_model, newdata = new_data))
print(paste("Prédiction du modèle exponentiel pour l'année", future_year, ":", exp_prediction))

# Prédiction avec le modèle polynomial
poly_prediction <- predict(poly_model, newdata = new_data)
print(paste("Prédiction du modèle polynomial pour l'année", future_year, ":", poly_prediction))



# Fit a Polynomial Regression Model (degree 3)
poly_model_3 <- lm(cumulative_total ~ poly(year, 3), data = grouped_by_year_filtered)

# Polynomial Model Summary
summary(poly_model_3)

# Fit a Polynomial Regression Model (degree 4)
poly_model_4 <- lm(cumulative_total ~ poly(year, 4), data = grouped_by_year_filtered)

# Polynomial Model Summary
summary(poly_model_4)

# Plot the Original Data with Higher-Degree Polynomial Models
plot(grouped_by_year_filtered$year, grouped_by_year_filtered$cumulative_total, 
     main = "Cumulative Total vs Year with Polynomial Models", 
     xlab = "Year", ylab = "Cumulative Total", pch = 19, col = "blue")

# Add Degree-3 Polynomial Model
lines(grouped_by_year_filtered$year, predict(poly_model_3), col = "green", lwd = 2)

# Add Degree-4 Polynomial Model
lines(grouped_by_year_filtered$year, predict(poly_model_4), col = "purple", lwd = 2)

# Add a legend to distinguish the models
legend("topleft", legend = c("Degree-3 Polynomial", "Degree-4 Polynomial"), 
       col = c("green", "purple"), lwd = 2)



# Définir la plage des degrés de polynôme à ajuster
degree_range <- 2:5  # Pour les degrés 3 et 4, peut être étendu si nécessaire

# Créer le graphique initial
plot(grouped_by_year_filtered$year, grouped_by_year_filtered$cumulative_total, 
     main = "Total Cumulé vs Année avec Modèles Polynômiaux", 
     xlab = "Année", ylab = "Total Cumulé", pch = 19, col = "blue")

for (degree in degree_range) {
  
  # Ajuster le modèle de régression polynomiale pour le degré actuel
  poly_model <- lm(cumulative_total ~ poly(year, degree), data = grouped_by_year_filtered)
  
  # Ajouter la courbe du polynôme au graphique
  lines(grouped_by_year_filtered$year, predict(poly_model), 
        col = rainbow(length(degree_range))[degree - min(degree_range) + 1], lwd = 2)
  
  # Prédiction à l'aide du modèle polynomial
  poly_prediction <- predict(poly_model, newdata = new_data)
  print(paste("Prédiction du Modèle Polynômial de Degré", degree, "pour l'année", future_year, ":", poly_prediction))
  
  model_summary <- summary(poly_model)
  print(paste("R-carré pour le Modèle Polynômial de Degré", degree, ":", model_summary$r.squared))
  print(paste("R-carré ajusté pour le Modèle Polynômial de Degré", degree, ":", model_summary$adj.r.squared))
  print(paste("_____________________________________________________________________"))
}

# Ajouter une légende pour distinguer les modèles
legend("topleft", legend = paste("Degré", degree_range, "Polynômial"), 
       col = rainbow(length(degree_range)), lwd = 2)
  




