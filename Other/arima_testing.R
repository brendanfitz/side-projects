library("datasets", lib.loc="C:/Program Files/R/R-3.5.1/library")
# install.packages("forecast")
library("forecast")
# install.packages("readxl")
library("readxl")

data <- read_excel("C:/Users/Brendan Non-Admin/Desktop/in and out sample.xlsx", sheet='Raw Data')

data$`Actual Sales`[0:32]

bankingts <- ts(data$`Actual Sales`[0:32], frequency=12, start=c(2010, 1))

mod <- auto.arima(bankingts)

forecast(mod, 3)
