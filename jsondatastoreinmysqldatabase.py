import requests
#function
def get(company_name,intervel):
    #requesting for api on www.alphavantage.com
    response=requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+company_name+"&interval="+intervel+"min&apikey=S5EH3VNQ0WZ5KR74")
    print(response.status_code)
    import json
    # Load the JSON data
    data= response.json()
    #connect to mysql
    import mysql.connector

    conect=mysql.connector.connect(host="localhost",user="root",database="")

    cursor=conect.cursor()
    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS stockcompany")
    # Switch to the newly created database
    cursor.execute(f"USE stockcompany")
    #create table of company 
    company_name=data['Meta Data']['2. Symbol']

    # Create a table to store the data
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {company_name} (
        timestamp DATETIME ,
        open_price DECIMAL(10, 4),
        high_price DECIMAL(10, 4),
        low_price DECIMAL(10, 4),
        close_price DECIMAL(10, 4),
        volume INT
    )
    """
    cursor.execute(create_table_query)

    #Iterate through the data and insert it into the table
    for timestamp, values in data[f"Time Series ({str(intervel)}min)"].items():
        open_price = values["1. open"]
        high_price = values["2. high"]
        low_price = values["3. low"]
        close_price = values["4. close"]
        volume = values["5. volume"]

        insert_query = f"""
        INSERT INTO {company_name} (timestamp, open_price, high_price, low_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (timestamp, open_price, high_price, low_price, close_price, volume))

    # Commit the changes to the database
    conect.commit()

    # Close the cursor and connection
    cursor.close()
    conect.close()
# asking for company name and time interval for data
name=str(input("Enter company symbol name:")).upper()
time_intervel=str(input("Enter time intervel for data: "))
get(name,time_intervel)
print(f"data :\n {data}")
