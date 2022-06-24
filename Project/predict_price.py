import pymongo
import warnings
import numpy as np
import pandas as pd
import math

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM

scaler = MinMaxScaler(feature_range=(0,1))

warnings.filterwarnings('ignore')

# connect to the mongoclient
client = pymongo.MongoClient('mongodb+srv://fong10:043821657@cluster0.ljiy5.mongodb.net/?retryWrites=true&w=majority')

# get the database
database = client['Crypto_Price']


def find_stock(stock_name):
    if stock_name == 'BTC' or stock_name == 'btc':
        col = database["btc"]
    if stock_name == 'ETH' or stock_name == 'eth':
        col = database["eth"]
    if stock_name == 'BNB' or stock_name == 'bnb':
        col = database["bnb"]
    if stock_name == 'ADA' or stock_name == 'ada':
        col = database["ada"]
    if stock_name == 'XRP' or stock_name == 'xrp':
        col = database["xrp"]
    if stock_name == 'DOGE' or stock_name == 'doge':
        col = database["doge"]
    cursor = col.find({})
    dataset = pd.DataFrame.from_dict(cursor)
    return dataset

def find_model(df):
    data = df.filter(['Price'])
    dataset = data.values
    training_data_len = math.ceil(len(dataset)*0.8)

    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data[0:training_data_len,:]

    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i,0])
        y_train.append(train_data[i,0])

    x_train,y_train = np.array(x_train),np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    
    #Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train,y_train,batch_size=40,epochs=3)

    return model

def find_last_60_mins(df): 
    #get the last 60 minutes price values and convert to an array
    last_60_mins = df[-60:].values
    # Scale the data to be values between 0 and 1
    last_60_mins_scaled = scaler.transform(last_60_mins)
    # Create an empty list
    X_test = []
    # Append the past 60 minutes
    X_test.append(last_60_mins_scaled)
    # Convert the X_test data set to a numpy array
    X_test = np.array(X_test)
    # Reshape the data
    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1], 1))
    # print(new_df)
    return X_test

def predict_price(name):

    df = find_stock(name)
    model = find_model(df)

    df = df.filter(['Price'])
    X_test = find_last_60_mins(df)
    count = 0
    next_5_min = []
        
    for i in range (0,5):
        # Get the predicted 
        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
            
        add_to_df = pd.DataFrame({"Price" : pred_price.tolist()[0]})

        df = df.append(add_to_df,ignore_index=True)

        next_5_min.append(pred_price)
        X_test = find_last_60_mins(df)
        # count+=1
        # print("predict price =",pred_price[0][0])
    
    return pred_price[0][0]

# print(predict_price('btc'))
# predict_price('AAPL','close')
# print(predict_price('AAPL','close'))
