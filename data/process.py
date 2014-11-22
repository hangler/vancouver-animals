import pandas as pd
import re as re
from datetime import datetime
import csv

lostAnimals = pd.read_csv('LostAnimals-OpenRefine.csv')

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

lostAnimals.rename(columns={ "Name": "name" }, inplace=True)
lostAnimals.rename(columns={ "ckc_class": "dog_breed_type" }, inplace=True)
lostAnimals.rename(columns={ "State": "state" }, inplace=True)
lostAnimals['is_dog'] = lostAnimals['dog_breed_type'].map(lambda x : is_dog(x))
lostAnimals['sex_simple'] = lostAnimals['Sex'].map(lambda x : extract_sex(x))
lostAnimals['date_created'] = pd.to_datetime(lostAnimals['DateCreated'])

names = lostAnimals[(lostAnimals.is_dog) & (lostAnimals.name != 'Unknown') & (lostAnimals.name != '?') & (lostAnimals.sex_simple != 'x')]['name'].value_counts().head(10)
names.to_csv('name.csv')

lostAnimals['Color'].value_counts().head(25).to_csv('color.csv')
lostAnimals[(lostAnimals.is_dog == True)]['Purebred'].value_counts().head(25).to_csv('breed.csv')
lostAnimals.to_csv('all.csv')

all_dogs = lostAnimals[(lostAnimals.is_dog) & (lostAnimals.name != 'Unknown') & (lostAnimals.name != '?') & (lostAnimals.sex_simple != 'x')]
female_dogs = all_dogs[(all_dogs.sex_simple == 'f')]
male_dogs = all_dogs[(all_dogs.sex_simple == 'm')]
top_dogs = filter_df_by_top_n_items(all_dogs, 'name', 10)

top_dogs_by_sex = top_dogs.groupby(['name', 'sex_simple']).size().reset_index()
top_dogs_by_sex.columns = ["name", "sex", "count"]
top_dogs_by_sex.to_csv("name_and_sex.csv", index=False)
top_dogs_by_sex_pivot = top_dogs_by_sex.pivot(index="name", columns="sex", values="count")

top_dogs_by_breed = top_dogs.groupby(['name', 'dog_breed_type']).size().reset_index()
top_dogs_by_breed.columns = ["name", "dog_breed_type", "count"]
top_dogs_by_breed.to_csv("name_and_breed.csv", index=False)
top_dogs_by_breed_pivot = top_dogs_by_breed.pivot(index="name", columns="dog_breed_type", values="count")

top_dogs_by_state = top_dogs.groupby(['name', 'state']).size().reset_index()
top_dogs_by_state.columns = ["name", "state", "count"]
top_dogs_by_state.to_csv("name_and_state.csv", index=False)
top_dogs_by_state_pivot = top_dogs_by_state.pivot(index="name", columns="state", values="count")

top_dogs_by_color = top_dogs[['name', 'color_has_multi', 'color_has_black', 'color_has_white', 'color_has_grey', 'color_has_brown', 'color_has_tan', 'color_has_red', 'color_has_orange', 'color_has_gold', 'color_has_blue']]
top_dogs_by_color = top_dogs_by_color.groupby('name', as_index=False).sum().set_index("name")
top_dogs_by_color.to_csv("name_and_color.csv", index=False)

top_dogs_by_sex_pivot.join(top_dogs_by_breed_pivot).join(top_dogs_by_state_pivot).join(top_dogs_by_color).fillna(0).to_csv("name_stats.csv")

lost_by_date = lostAnimals[lostAnimals['date_created'] > '2011-01-01'].set_index('date_created').resample('M', how='sum')
lost_by_date.to_csv("lost_by_date.csv")