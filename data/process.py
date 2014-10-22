import pandas as pd
import re as re
from datetime import datetime
import csv

lostAnimals = pd.read_csv('LostAnimals-OpenRefine.csv')

def collapse_colors(item):
  valid_colors = ["black", "white", "brown", "grey"]
  colors = []
  item = str(item).lower()
  
  count = 0

  for valid_color in valid_colors:
    if valid_color in item and count < 2:
      colors.append(valid_color)
      #count += 1

  if len(colors) == 0:
    colors.append("other")

  return "/".join(colors).title()

def is_dog(item):
  item = str(item).lower()
  if item == "nan":
    return False
  else:
    return True

def extract_sex(item):
  item = str(item).lower()
  if item == "nan":
    return "x"
  return item[0]

def filter_df_by_top_n_items(df, column_name, n):
  filtered_df = df.copy()
  df_filter = filtered_df[column_name].value_counts().head(n)
  df_filter = list(df_filter.keys())
  df_filter = { column_name: df_filter }
  row_mask = filtered_df.isin(df_filter).any(1)
  filtered_df = filtered_df[row_mask]
  return filtered_df

lostAnimals.rename(columns={ "Name": "pet_name" }, inplace=True)
lostAnimals.rename(columns={ "CKC Class": "dog_breed_type" }, inplace=True)
lostAnimals['Color'] = lostAnimals['Color'].map(lambda x : collapse_colors(x))
lostAnimals['is_dog'] = lostAnimals['dog_breed_type'].map(lambda x : is_dog(x))
lostAnimals['sex_simple'] = lostAnimals['Sex'].map(lambda x : extract_sex(x))
lostAnimals['date_created'] = pd.to_datetime(lostAnimals['DateCreated'])

lostAnimals[(lostAnimals.is_dog)][(lostAnimals.pet_name != 'Unknown') & (lostAnimals.pet_name != '?')]['pet_name'].value_counts().head(10).to_csv('name.csv')
lostAnimals['Color'].value_counts().head(25).to_csv('color.csv')
lostAnimals[(lostAnimals.is_dog == True)]['Purebred'].value_counts().head(25).to_csv('breed.csv')
lostAnimals.to_csv('all.csv')

all_dogs = lostAnimals[(lostAnimals.is_dog) & (lostAnimals.pet_name != 'Unknown') & (lostAnimals.sex_simple != 'x')]
top_dogs = filter_df_by_top_n_items(all_dogs, 'pet_name', 10)

top_dogs_by_sex = top_dogs.groupby(['pet_name', 'sex_simple']).size().reset_index()
top_dogs_by_sex.columns = ["name", "sex", "count"]
top_dogs_by_sex.to_csv("name_and_sex.csv", index=False)

top_dogs_by_breed = top_dogs.groupby(['pet_name', 'dog_breed_type']).size().reset_index()
top_dogs_by_breed.columns = ["name", "dog_breed_type", "count"]
top_dogs_by_breed.to_csv("name_and_breed.csv", index=False)

lost_by_date = lostAnimals[lostAnimals['date_created'] > '2011-01-01'].set_index('date_created').resample('M', how='sum')
lost_by_date.to_csv("lost_by_date.csv")