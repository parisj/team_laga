### team_laga

# Identifizierung Entsieglungspotenzial

## Table of Content
1. Project Description
2. Technologies used
3. Authors

## 1. Project Description
This project focuses on evaluating the potential areas of rads and parkinglots which could be used as green areas or parking lots.
This would lead to an improved air quality, cooler temperatures in the summer and also increasing life quality.


## 2. Technologies used
In this project we used the information of the Roads and the Zones form the kanton [St. Gallen](https://daten.sg.ch/) and displayed
them using the osmnx library in Python. The project consists out of different tools to prepare the available dataset, calculate and plot 
different unsealing configuration. 
    
### The main modules are:
    
-**tools_polygon** (Plot and create Polygons from Geodata, Intersect and Filter)
        
-**tools_osmnx** (easier ploting and visualization)
        
-**tools_street** (Characterise streetdata and propose randomised unsealing solutions)
        
    
### Sources Datasets: 
[begegnungszonen.csv](https://daten.sg.ch/explore/dataset/begegnungszonen%40stadt-stgallen/export/?disjunctive.gebiet&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQ09VTlQiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjZmYwMDAwIn1dLCJ4QXhpcyI6InJlYWxpc2llcnQiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJ5ZWFyIiwic29ydCI6IiIsImNvbmZpZyI6eyJkYXRhc2V0IjoiYmVnZWdudW5nc3pvbmVuQHN0YWR0LXN0Z2FsbGVuIiwib3B0aW9ucyI6eyJkaXNqdW5jdGl2ZS5nZWJpZXQiOnRydWV9fX1dLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlfQ%3D%3D), 
[gemeindestrassenplan.csv](https://daten.sg.ch/explore/dataset/gemeindestrassenplan%40stadt-stgallen/export/?disjunctive.strassenkl&disjunctive.strassenna&disjunctive.strassennr), 
[tempo-30-zonen.csv](https://daten.sg.ch/explore/dataset/tempo-30-zonen%40stadt-stgallen/export/)

## 3. Install
Clone repository 
  
```
git clone https://github.com/parisj/team_laga.git
cd team_laga
pip install -r requirements.txt
```
    
    
## 4.Authors
  - Anton Paris
  - Alexander Bruun
  - Pierluigi Margarito
  - Leart Sejdiu
    
    
