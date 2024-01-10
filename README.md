

# Group One Project 2
Group one is coding a trading algorithm that will focus on using one metric, delta divergence, to enter and exit short-term futures trades. The algo will exclusively trade NASDAQ mini (NQ) futures, and our group will spend most of our time fine-tuning this strategy to determine the ideal parameters with which to control this algorithm. We define success as beating the S&P 500 and beating the simpler trading strategy of buying and holding the NASDAQ mini future over the period of time that we used to test it.

### Objectives
* API Integration: Enable users to access real-time market data, financial news, and additional information through APIs, enhancing the software's functionality and relevance.
* Algorithmic Training: We will code a trading algorithm that will trade using real NQ future data on a platform (we have not yet chosen our platform, but we will likely use either tradovate or tradingview. Cost and API access will be the two main factors that will influence our decision). 
Machine Learning: We will use machine learning to backtest and educate our algo to execute trades in order to achieve the highest probability of success.

### Financial metrics for trading Algorithm
* Delta divergence is a momentum indicator particularly common in the context of order flow analysis. It measures the cumulative delta (difference between buying and selling volume) and the movement of the price of an asset. We hypothesize that an increase in the absolute value of delta divergence indicates a higher probability of predicting which direction the asset will move. An increased positive delta divergence indicates that there are significantly more buyers than sellers, but the price does not reflect the heightened presence of buyers. Therefore, the price is likely to increase, or ‘catch up’ to the buyers. When the delta divergence is negative, this indicates that there are significantly more sellers than buyers, but the price either increases or does not drop as expected. Therefore, we would take this negative divergence as a bearish indicator that the price will drop, or ‘catch up’ to the heightened presence of sellers.
* Others to be determined, starting with MACD.

### Tasks to complete:
* Research which platform to use
* API access to chosen platform
* Use ML to teach algo
* Backtest algo and make adjustments based on backtesting results
* Repeat steps until satisfactory result. We define success as beating the S&P 500 as well as beating the simpler trading strategy of buying and holding the NASDAQ mini future over the period of time that we used to test it.

### Group Members
* Elliot Watt
* Gino Petrosian
* Jenny Trieu
* Jorge Miguel Garcia
* David Taylor
