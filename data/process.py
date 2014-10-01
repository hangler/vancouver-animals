import pandas as pd
from datetime import datetime

lostAnimals = pd.read_csv('LostAnimals-2014-09-30.csv')

# Some cursory data cleaning...

def collapse_colors(item):
  valid_colors = ["black", "brown", "grey", "white"]
  colors = []
  item = str(item).lower()
  
  for valid_color in valid_colors:
    if valid_color in item:
      colors.append(valid_color)

  if len(colors) == 0:
    colors.append("other")

  return "/".join(colors).title()


x_collapse_colors = {
  "Apricot": "Orange",
  "Beige": "Tan",
  "Black": "Black",
  "Black & Brown": "Black & Brown",
  "Black & Tan": "Black & Tan",
  "Black & Tan & White": "Tri Colour",
  "Black & White": "Black & White",
  "Black/White": "Black & White",
  "Blonde": "Yellow",
  "Brindle": "Brindle",
  "Brown": "Brown",
  "Brown & Black": "Black & Brown",
  "Brown & White": "Brown & White",
  "Chocolate": "Brown",
  "Cream": "White",
  "Gold": "Yellow",
  "Golden": "Yellow",
  "Grey": "Grey",
  "Red": "Red",
  "Tan": "Tan",
  "Tan & White": "Tan & White",
  "Tan & Black": "Black & Tan",
  "Tri": "Other",
  "Tri Colour": "Other",
  "White": "White",
  "White & Black": "Black & White",
  "White & Brown": "Brown & White",
  "White & Grey": "Grey & White",
  "White & Tan": "Tan & White",
}

lostAnimals.replace("?", "Unknown", inplace=True)
lostAnimals['Color'] = lostAnimals['Color'].map(lambda x : collapse_colors(x))

lostAnimals['Name'].value_counts().head(25).to_csv('name.csv')
lostAnimals['Color'].value_counts().head(25).to_csv('color.csv')
lostAnimals['Breed'].value_counts().head(25).to_csv('breed.csv')