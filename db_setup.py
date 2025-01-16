import sqlite3

#create database
conn = sqlite3.connect('stocks.db')

cursor = conn.cursor()

# create table for stock data
# stock factors such as symbol, price, PE ratio, market cap, last time updated
