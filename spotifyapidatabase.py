import os
import requests
import spotipy
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

CLIENT_ID = '73a956d832824facb9e966d05f16d603'
CLIENT_SECRET = '576392b285274a69b51832ed5c5fa253'

AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
})

print(auth_response.status_code)

auth_response_data = auth_response.json()


access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

BASE_URL = 'https://api.spotify.com/v1/'

musicians = {'Sia': '5WUlDfRSoLAfcVSX1WnrxN',
             'Billie': '6qqNVTkY8uBg9cP3Jd7DAH',
             'Sark': '01DTVE3KmoPogPZaOvMqO8',
             'Pink Floyd': '0k17h0D3J5VfsdmQ1iZtE9'}


def gettingrequest():
    col_names = ['name', 'popularity']
    df = pd.DataFrame(columns=col_names)
    for name in musicians:
        res = requests.get(BASE_URL + 'artists/' + musicians[name],
                           headers=headers)
        r = res.json()
        store = {'name': r['name'],
                 'popularity': r['popularity']}
        df.loc[len(df.index)] = [store['name'], store['popularity']]

    return df


def createdb():
    df = gettingrequest()
    engine = create_engine('mysql://root:codio@localhost/spotifyapi')
    df.to_sql('popularity_table', con=engine, if_exists='replace', index=False)


def savedb():
    os.system("mysqldump -u root -pcodio spotifyapi > music.sql")


def loaddb():
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' +
              'spotifyapi' + ';"')
    os.system("mysql -u root -pcodio spotifyapi < music.sql")


def gettingdataset():
    engine = create_engine('mysql://root:codio@localhost/spotifyapi')
    loaddb()
    df = pd.read_sql_table('popularity_table', con=engine)
    return df


def barchart(dataframe, barvalue):
    colors = ['red', 'orange', 'yellow', 'green']
    plt.bar(dataframe, barvalue, color=colors)
    plt.title('Artiste and How Popular They Are')
    plt.xlabel('Artiste')
    plt.ylabel('Popularity')
    plt.show()


if __name__ == '__main__':
    createdb()
    savedb()
    barchart(gettingdataset().name, gettingdataset().popularity)
