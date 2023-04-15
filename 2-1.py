import numpy as np
import pandas as pd
import googlemaps
# The below two are corresponding cell 14
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# This is to call the csv file
# 'euc-kr' is for encoding the korean and it is the same as 'UTF-8'
# crime_analysis_police = pd.read_csv('G:\\My Drive\\Jongki-study\\05_Manual\\17_Python\\DataScience\\data\\02. crime_in_Seoul.csv', thousands=',', encoding='euc-kr')
crime_analysis_police = pd.read_csv('C:\\Users\\pig69\\Desktop\\17_Python\\DataScience\\data\\02. crime_in_Seoul.csv', thousands=',', encoding='euc-kr')
print(crime_analysis_police.head())

# You need to get API key for Google maps
# https://developers.google.com/maps
# pip install googlemaps

# API is a credential
gmaps_key = "KEY IS HERE" # API is a confidential
gmaps = googlemaps.Client(key=gmaps_key)
print(gmaps.geocode('서울중부경찰서', language='ko'))

# This work is to generate a proper name: BEFORE '중부서' AFTER '서울중부경찰서'
station_name = []
# 'append()' is to add an element to the end of the list.
for name in crime_analysis_police['관서명']:
    # '[:-1]' means start from the beginning and cut it before the last word
    station_name.append('서울' + str(name[:-1]) + '경찰서')

print(station_name)

# This is to call the address from Googlemaps
# Bracket [] means the empty box to designate the value or name
station_address = []
station_lat = []
station_lng = []
for name in station_name:
    # 'tmp' here is used to call all the addressess from Google maps using 'geocode'
    # 'tmp' is an arbitary, so you can name it
    tmp = gmaps.geocode(name, language='ko')
    # 'get' function is to get the exact thing. Here we want "formatted_address" from 'tmp'
    station_address.append(tmp[0].get("formatted_address"))
    
    # This is to get the geo info 
    tmp_loc = tmp[0].get("geometry")
    station_lat.append(tmp_loc['location']['lat'])
    station_lng.append(tmp_loc['location']['lng'])
    # This is to print out all the address and it reapts up to all 
    print(name + '-->' + tmp[0].get("formatted_address"))

# print(station_address)
# print(station_lat)
# print(station_lng)

# This is to designate the 'gu_name' 
gu_name = []
for name in station_address:
    tmp = name.split()
    tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
    gu_name.append(tmp_gu)
    # print(gu_name)

crime_analysis_police['구별'] = gu_name
print(crime_analysis_police.head())

# This is for the exception 
# crime_analysis_police[crime_analysis_police['관서명']=='금천서', ['구별']] =='금천구'
# print(crime_analysis_police[crime_analysis_police['관서명']=='금천서'])

# This is to create the CSV file we worked on and it will have ',' seperated (a, b, c)
crime_analysis_police.to_csv('C:\\Users\\pig69\\Desktop\\17_Python\\DataScience\\data\\02. crime_in_Seoul_gu_name-JL.csv', sep=',', encoding='utf-8')

# There are two 강남구 in the data set
print(crime_analysis_police.sort_values(by='구별', ascending=True))

#  This is call the data set from a directory
# The raw data set has unnecessary column, so 'index_col=0' re-orders the data set
crime_analysis_police_raw = pd.read_csv('C:\\Users\\pig69\\Desktop\\17_Python\\DataScience\\data\\02. crime_in_Seoul_include_gu_name.csv', encoding='utf-8', index_col=0)
print(crime_analysis_police_raw.head())

# This is to re-organize data set based on '구별' and make the data summed if they have the same index
crime_analysis = pd.pivot_table(crime_analysis_police_raw, index='구별', aggfunc=np.sum)
print(crime_analysis.head())

# This is to examine the rate (number of arrested / number of occurances)
crime_analysis['Rape arrest rate'] = crime_analysis['강간 검거'] / crime_analysis['강간 발생'] * 100
crime_analysis['Robbery arrest rate'] = crime_analysis['강도 검거'] / crime_analysis['강도 발생'] * 100
crime_analysis['Murder arrest rate'] = crime_analysis['살인 검거'] / crime_analysis['살인 발생'] * 100
crime_analysis['Burglary arrest rate'] = crime_analysis['절도 검거'] / crime_analysis['절도 발생'] * 100
crime_analysis['Assault arrest rate'] = crime_analysis['폭력 검거'] / crime_analysis['폭력 발생'] * 100

del crime_analysis['강간 검거'] 
del crime_analysis['강도 검거']
del crime_analysis['살인 검거']
del crime_analysis['절도 검거']
del crime_analysis['폭력 검거'] 

print(crime_analysis.head())

# This is to make a list to adjust the maximum value as 100 
con_list = ['Rape arrest rate', 'Robbery arrest rate', 'Murder arrest rate', 'Burglary arrest rate', 'Assault arrest rate']
# This 'for' loop is to lower a value over 100 to 100 in 'con_list'
for column in con_list:
    # This is to look for a data overs 100 and set it as 100 
    crime_analysis.loc[crime_analysis[column] > 100, column] = 100

crime_analysis.head()

# This is to rename the all korean titles
crime_analysis.rename(columns={'강간 발생':'Rape', '강도 발생':'Robbery', '살인 발생':'Murder', '절도 발생':'Burglary', '폭력 발생':'Assault'}, inplace=True)
print(crime_analysis.head())

# This work is to normalize the data to understand the data holistically
# "pip install scikit-learn"
from sklearn import preprocessing

col = ['Rape', 'Robbery', 'Murder', 'Burglary', 'Assault']

x = crime_analysis[col].values
min_max_scaler = preprocessing.MinMaxScaler()

x_scaled = min_max_scaler.fit_transform(x.astype(float))
crime_analysis_normalize = pd.DataFrame(x_scaled, columns = col, index = crime_analysis.index)

col2 = ['Rape arrest rate', 'Robbery arrest rate', 'Murder arrest rate', 'Burglary arrest rate', 'Assault arrest rate']
crime_analysis_normalize[col2] = crime_analysis[col2]
print(crime_analysis_normalize)

# This is to merge the CCTV data to 'crime_analysis_normalize'
result_CCTV = pd.read_csv('C:\\Users\\pig69\\Desktop\\17_Python\\DataScience\\data\\01. CCTV_result.csv', encoding='UTF-8', index_col='구별')
crime_analysis_normalize[['Population', 'CCTV']] = result_CCTV[['인구수', '소계']]
print(crime_analysis_normalize)

# This is to make a list and sum them to build a column 'criminal'
col = ['Rape', 'Robbery', 'Murder', 'Burglary', 'Assault']
crime_analysis_normalize['Criminal'] = np.sum(crime_analysis_normalize[col], axis=1)
print(crime_analysis_normalize.head())

col = ['Rape arrest rate', 'Robbery arrest rate', 'Murder arrest rate', 'Burglary arrest rate', 'Assault arrest rate']
crime_analysis_normalize['Arrest'] = np.sum(crime_analysis_normalize[col], axis=1)
print(crime_analysis_normalize.head())

# This command is to plot a graph without hitting (it is not really necessary)
%matplotlib inline

#### This code is to set up the font and validate the KOREAN
import platform
path = 'c:/Windows/Fonts/malgun.ttf'
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')

# This is to plot 'crime_analysis_normalize' based on 'pairplot' function with variables such as 'Robbery', 'Murder', 'Assault'
# If you change 'kind=' function, you can have a different shape of graph
sns.pairplot(crime_analysis_normalize, vars=['Robbery', 'Murder', 'Assault'], kind='reg')
plt.show()

# This is to plot 2 by 2 data set with a correlation
sns.pairplot(crime_analysis_normalize, x_vars=['Population', 'CCTV'], y_vars=['Murder', 'Assault'], kind='reg')
plt.show()

# This is to plot 2 by 2 data set with a correlation
sns.pairplot(crime_analysis_normalize, x_vars=['Population', 'CCTV'], y_vars=['Murder arrest rate', 'Assault arrest rate'], kind='reg')
plt.show()

# The previous result shows the (-) correlation and it looks vague
# This is to calculate the ratio of the crime to the arrest
tmp_max = crime_analysis_normalize['Arrest'].max()
crime_analysis_normalize['Arrest'] = crime_analysis_normalize['Arrest'] / tmp_max * 100
crime_analysis_normalize_sort = crime_analysis_normalize.sort_values(by='Arrest', ascending=False)
crime_analysis_normalize_sort

target_col = ['Rape arrest rate', 'Robbery arrest rate', 'Murder arrest rate', 'Burglary arrest rate', 'Assault arrest rate']
crime_analysis_normalize_sort = crime_analysis_normalize.sort_values(by='Arrest', ascending=False)

plt.figure(figsize= (10,10))
sns.heatmap(crime_analysis_normalize_sort[target_col], annot=True, fmt='.2f', linewidths=.5)
plt.title('Crimal arrest ratio (normalized analysis)')
plt.show()

# This is to save the final version as a csv format
crime_analysis_normalize.to_csv('C:\\Users\\pig69\\Desktop\\17_Python\\DataScience\\data\\02. crime_in_Seoul_final-JL.csv', sep=',', encoding='utf-8')

# This to call the json file for the Seoul 
import json
geo_path = 'C:\\Users\\pig69\\Desktop\\17_Python\\DataScience\\data\\02. skorea_municipalities_geo_simple.json'
geo_str = json.load(open(geo_path, encoding='utf-8'))

# This is to plot the mapping graph for 'Murder' by using dimmed color
map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
map.choropleth(geo_data = geo_str, data=crime_analysis_normalize['Murder'], columns = [crime_analysis_normalize.index, crime_analysis_normalize['Murder']], fill_color='PuRd', key_on = 'feature.id')
map

# This is to plot the mapping graph for 'Rape' by using dimmed color# 
map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
map.choropleth(geo_data=geo_str, data=crime_analysis_normalize['Rape'], columns=[crime_analysis_normalize.index, crime_analysis_normalize['Rape']], fill_color = 'YlGnBu', key_on='feature.id')
map

# This is to plot the mapping graph for 'Criminal' by using dimmed color
map = folium.Map(location=[37.5502, 126.982], zoon_start=11, tiles='Stamen Toner')
map.choropleth(geo_data=geo_str, data=crime_analysis_normalize['Criminal'], columns=[crime_analysis_normalize.index, crime_analysis_normalize['Criminal']], fill_color = 'PuRd', key_on='feature.id')
map

# This is to check the 'Murder' rate per 'Population' 
tmp_criminal = crime_analysis_normalize['Murder'] / crime_analysis_normalize['Population'] * 1000000
map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
map.choropleth(geo_data=geo_str, data=tmp_criminal, columns=[crime_analysis_normalize.index, tmp_criminal], fill_color='PuRd', key_on='feature.id')
map

# This is to re-call the raw file to 
crime_analysis_police_raw['lat'] = station_lat
crime_analysis_police_raw['lng'] = station_lng
col = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
tmp = crime_analysis_police_raw[col] / crime_analysis_police_raw[col].max()
crime_analysis_police_raw['Arrest'] = np.sum(tmp, axis=1)
print(crime_analysis_police_raw.head())

# This is to draw (pick) the locations of police stations 
map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
for n in crime_analysis_police_raw.index:
    # The format of the below code is: 'folium.Marker([latitude, longitude]).add_to(designated one)'
    folium.Marker([crime_analysis_police_raw['lat'][n], crime_analysis_police_raw['lng'][n]]).add_to(map)
map

# This is to do mapping with a 'CircleMarker' and the size of circles is based on the size of 'Arrest' 
map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
for n in crime_analysis_police_raw.index:
    folium.CircleMarker([crime_analysis_police_raw['lat'][n], crime_analysis_police_raw['lng'][n]], radius=crime_analysis_police_raw['Arrest'][n]*10, color='#3186cc', fill_color='#3186cc').add_to(map)
map

#  This is to draw two things on the map: Number of 'Criminal' normalized rates as a reded-dimmed color and number of 'Arrest'as size of 'CircleMarker'
map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
map.choropleth(geo_data=geo_str, data=crime_analysis_normalize['Criminal'], columns=[crime_analysis_normalize.index, crime_analysis_normalize['Criminal']], fill_color='PuRd', key_on='feature.id')
for n in crime_analysis_police_raw.index:
    folium.CircleMarker([crime_analysis_police_raw['lat'][n], crime_analysis_police_raw['lng'][n]], radius= crime_analysis_police_raw['Arrest'][n]*10, color='#3186cc', fill_color='#3186cc').add_to(map)
map


