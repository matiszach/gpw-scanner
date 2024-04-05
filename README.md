# gpw-scanner
A program that generates a weekly summary of stock market and sends it via email

# Installation
First, clone the repository to your local machine using the following command:
```
git clone https://github.com/matiszach/gpw-scanner.git
```
Then, set up a .env file in the repository's root directory and fill it with proper program parameters. If you just need the data locally and do not want to send it via email, simply set SEND to "No" and skip the rest of the variables.
```
MIN_VOLUME = <integer representing minimum weekly trading volume of shown stocks (in thousands of PLN)>
SEND = <Yes/No>
SENDER = <sender's email address>
RECIPIENT = <recipient's email address>
PASSWORD = <sender's email app password>
```
You can create the app password for your gmail account [here](https://myaccount.google.com/apppasswords).

The last step is to install all the requiered libraries using the following command:
```
pip3 install -r requirements.txt
```

# Usage

To run the program simply run the following command:
```
python3 main.py
```
The program will scrape the [gpw website](https://www.gpw.pl/) for the stock data which should take about 15-20 seconds.
Then it will send the stock summary from the sender's email to recipient's email in .png and .csv formats.

# Strategies

Currently implemented stock trading strategies (more to be added soon)

## [inside bars](https://priceaction.com/price-action-university/strategies/inside-bar/)

