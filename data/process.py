import pandas as pd
from datetime import datetime

lostAnimals = pd.read_csv('LostAnimals-2014-09-30.csv')

# Some cursory data cleaning...
lostAnimals.replace("?", "Unknown", inplace=True)
lostAnimals.replace("White & Brown", "Brown & White", inplace=True)
lostAnimals.replace("Black/White", "Black & White", inplace=True)
lostAnimals.replace("Tri", "Tri Colour", inplace=True)
lostAnimals.replace("Tan & Black", "Black & Tan", inplace=True)
lostAnimals.replace("Brown & Black", "Black & Brown", inplace=True)
lostAnimals.replace("White & Black", "Black & White", inplace=True)
lostAnimals.replace("White & Tan", "Tan & White", inplace=True)
lostAnimals.replace("Black & Tan & White", "Tri Colour", inplace=True)
lostAnimals.replace("White & Grey", "Grey & White", inplace=True)

lostAnimals['Name'].value_counts().head(25).to_csv('name.csv')
lostAnimals['Color'].value_counts().head(25).to_csv('color.csv')
lostAnimals['Breed'].value_counts().head(25).to_csv('breed.csv')