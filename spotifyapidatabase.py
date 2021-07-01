import os
import requests
import spotipy
import pandas as pd
import sqlalchemy
from sqlalchemy import  create_engine

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
           'John':'0k17h0D3J5VfsdmQ1iZtE9'}

print('Here are the artists: ')
for m in musicians.keys():
  print(m)
user = input('Please enter an artist name: ')
artist_id = musicians[user]

def gettingrequest():
  r = requests.get(BASE_URL + 'artists/' + artist_id, headers=headers)
  return r

def createdb():
  info = r.json()
  print('artist name: ' + info['name'] + '. Genres: ', info['genres'])

  store = {'name' : info['name'],
        'popularity' : info['popularity']}

  col_names = ['name', 'popularity']
  df = pd.DataFrame(columns=col_names)
  df.loc[len(df.index)] = [store['name'], store['popularity']]

  engine = create_engine('mysql://root:codio@localhost/spotifyapi')
  df.to_sql('popularity_table', con=engine, if_exists='replace', index=False)
  
def savedb():
  os.system("mysqldump -u root -pcodio spotifyapi > music.sql")
  
def loaddb():
  os.system("mysql -u root -pcodiospotifyapi < music.sql")
  


r = gettingrequest()

if r.status_code != 200:
  print('invalid id')
else:
  createdb()
  
savedb()
loaddb()
  








