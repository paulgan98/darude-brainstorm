library(dplyr)
library(date)
library(lubridate)
library(ggplot2)


#### Dummy data creation
createData <- function(n){
  listOfStates <- c("WA", "OR", "CA", "NV", "AZ", "IL", "TX", "NY", "MA", "GA", "FL", "MI", "PA", "AL", "VA")
  state <- sample(listOfStates, size = n, replace = TRUE)
  date <- sample(seq(as.Date('2000/01/01'), Sys.Date(), by = "day"), n)
  R <- round(runif(n, 0, 255))
  G <- round(runif(n, 0, 255))
  B <- round(runif(n, 0, 255))
  testdata <- data.frame(date, state, R, G, B)
  testdata <- testdata[order(date),] 
}

colorData <- createData(1000)

#### Data commands
colorData$year <- format(colorData$date, '%Y')
colorData$month <- format(colorData$date, '%m')
colorData$week <- week(ymd(colorData$date))

meanYear <- colorData %>% group_by(year) %>% summarize(meanR = mean(R), meanG = mean(G), meanB = mean(B))
meanYearMonth <- colorData %>% group_by(year, month) %>% 
  summarize(meanR = mean(R), meanG = mean(G), meanB = mean(B))
meanState <- colorData %>% group_by(state) %>% summarize(meanR = mean(R), meanG = mean(G), meanB = mean(B))
meanStateYear <- colorData %>% group_by(state, year) %>% 
  summarize(meanR = mean(R), meanG = mean(G), meanB = mean(B))

colorData %>% ggplot() + geom_line(aes(date, R, colour = "R")) + 
  geom_line(aes(date, G, colour = "G")) +
  geom_line(aes(date, B, colour = "B")) +
  scale_color_manual(values = c("Blue","Green", "Red"))

#### I made a change to my code
