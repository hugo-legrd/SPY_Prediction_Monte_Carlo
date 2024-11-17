# Importing Packages
import yfinance as yf
import numpy as np
from random import random
import matplotlib.pyplot as plt
from scipy.stats import norm


#Defining the ticker 
ticker = yf.Ticker('SPY')

#Obtain historical data
start_date = '2013-11-14'
end_data = '2023-11-14'
hist = ticker.history(start=start_date, end=end_data)
print(hist.head())

#Pulling Closing Price Data
hist = hist[['Close']]
print(hist)

#Plotting Price Data
"""hist['Close'].plot(title="SPY Stock Price", ylabel="Closing Price [$]", figsize=[10, 6])
plt.grid()"""

#Create Day, Count, Price and Change Lists
days = [i for i in range(1, len(hist['Close'])+1)]
price_orig = hist['Close'].tolist()
#Change percent in day-to-day of SPy for the last 10 years
change = hist['Close'].pct_change().tolist()
change = change[1:]  #Removing the first term since it is NaN

#Statistics for Use in Model
mean = np.mean(change)
std_dev = np.std(change)
print('\nMean percent change: '+ str(round(mean*100, 2)) + '%')
print('Standard Deviation of percent change: ' + str(round(std_dev*100, 2)) + '%')

#Simulation Number and Prediction Period
simulations = 100
days_to_sim = 1*252 #Trading day in 1 year

#Initializing Figure for simulation
fig = plt.figure(figsize=[10,6])
plt.plot(days, price_orig)
plt.title("Monte Carlo Stock Prices [" + str(simulations) + "] simulations")
plt.xlabel("Trading Days After " + start_date)
plt.ylabel("Closing Price ($)")
plt.xlim([2000, len(days)+days_to_sim])
plt.grid()

#Initializing Lists for Analysis
close_end = []
above_close = []


for i in range(simulations) : 
    #List that tracks the days after 14/11/2023 for plotting purposes
    num_days = [days[-1]]
    #List that tracks the closing price of SPY after 14/11/2023 for a single simulation.
    close_price = [hist.iloc[-1, 0]]
     
    # For Loop for Number of Days to Predict
    for j in range(days_to_sim) : 
        num_days.append(num_days[-1]+1)
        #take a randomized probability, our mean and standard deviation (calculated earlier), 
        #and generates a percent change equivalent to the randomized probability in a normal distribution
        perc_change = norm.ppf(random(), loc=mean, scale=std_dev)
        #use the randomized percent change to calculate the next closing price based on the previous closing price
        close_price.append(close_price[-1]*(1+perc_change))

        if close_price[-1] > price_orig[-1] : 
            #Give 1 is the closing price after the year of simulation is above the end-of-date closing price, 0 if not
            above_close.append(1)
        else : 
            above_close.append(0)

        close_end.append(close_price[-1])
        plt.plot(num_days, close_price)


# Average Closing Price and Probability of Increasing After 1 Year
average_closing_price = sum(close_end)/len(close_end)
average_perc_change = (average_closing_price - price_orig[-1]) / price_orig[-1]
probability_increase = sum(above_close)/len(above_close)



print('\nPredicted closing price after ' + str(simulations) + ' simulations: $' + str(round(average_closing_price, 2)))
print('Predicted percent increase after 1 year: '+ str(round(average_perc_change*100, 2)) + '%')
print('Probability of stock price increasing after 1 year: ' + str(round(probability_increase*100, 2)) + '%')

plt.show()