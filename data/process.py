import pandas as pd
import re as re
from datetime import datetime
import csv

def dog_breed_dict_from_csv(file_name):
  dog_breed_dict = {}
  with open(file_name, mode='r') as infile:
    reader = csv.reader(infile)
    next(reader, None)  # skip the headers
    for rows in reader:
      breed = rows[0].lower()
      breed_type = rows[1].lower()
      if "(" in breed:
        start = breed.index("(")
        end = breed.index(")")
        pre_parenthetical_content = breed[0:start-1]
        parenthetical_content = breed[start+1:end]
        dog_breed_dict[parenthetical_content] = breed_type
        dog_breed_dict[parenthetical_content + " " + pre_parenthetical_content] = breed_type
      dog_breed_dict[breed] = breed_type
  # Manual additions
  dog_breed_dict["germ. shepherd"] = "herding dogs"
  dog_breed_dict["german shepherd"] = "herding dogs"
  dog_breed_dict["chihuahua"] = "toy dogs"
  dog_breed_dict["pitbull"] = "non-sporting dogs"
  dog_breed_dict["pit bull"] = "non-sporting dogs"
  dog_breed_dict["retriever"] = "sporting dogs"
  dog_breed_dict["dachshund"] = "hounds"
  dog_breed_dict["terrier"] = "terriers"
  dog_breed_dict["border collie"] = "herding dogs"
  dog_breed_dict["collie"] = "herding dogs"
  dog_breed_dict["jack russell terrier"] = "terriers"
  dog_breed_dict["shepherd"] = "herding dogs"
  dog_breed_dict["husky"] = "working dogs"
  return dog_breed_dict

lostAnimals = pd.read_csv('LostAnimals-2014-09-30.csv')
dog_breed_dict = dog_breed_dict_from_csv("breed_index.csv")
#print dog_breed_dict


cats = [
          r"[mn]aine? ?coon",
          r"\Along ?hair(ed)?\Z",
          r"\Ashort ?hair(ed)?\Z",
          r"\bcats?\b",
          r"\bd[lms]h\b",
          r"ab+ys+inian",
          r"american curl",
          r"american short",
          r"bal[ae]nese",
          r"blue lynx ragdoll",
          r"calico",
          r"domestic (short|medium|long) hair",
          r"dsc",
          r"fluffy dc",
          r"kitten",
          r"manx",
          r"med(ium)? ?hair",
          r"norwegian",
          r"persian",
          r"russian",
          r"sdc",
          r"siames+e",
          r"sphynx",
          r"tabby",
          r"tomcat",
          r"tor(toise|i) ?shell",
          r"tuxedo",
         ]

dogs = [
          r"[ck]orso",
          r"[hou]+nd",
          r"[mpy]ork(ie)?",
          r"\Ajr\Z",
          r"\Asilky\Z",
          r"\br[op]tt?",
          r"air[e]?dale",
          r"akita",
          r"alsati[ao]?n",
          r"aussie",
          r"australian cattle",
          r"b[ae]senji",
          r"basset+",
          r"beagle",
          r"benji",
          r"ber[mn]ese ?^[8]",
          r"bernard",
          r"bi[cs]*hon",
          r"black & tan",
          r"blue he[ae]+ler",
          r"bo(rder|uvier|xer)",
          r"brittany",
          r"bull",
          r"chi?huahua",
          r"chow",
          r"co(cker|llie|rg[iy]?)",
          r"coyote",
          r"dach",
          r"dalmati[ao]n",
          r"dingo",
          r"dob(y|erman|ie)",
          r"dog",
          r"duck ?toller",
          r"eskimo",
          r"fox",
          r"german",
          r"gold(en)? ret",
          r"great dane",
          r"great pyr",
          r"griff[io]?n",
          r"gsd",
          r"havanese",
          r"heeler",
          r"huske?(ie|y)",
          r"jack",
          r"japanese breed",
          r"jin(do)?",
          r"jrt",
          r"kel[pt]ie",
          r"King Charles Cavalier",
          r"kuvasz",
          r"l[ha]+s[ao]?",
          r"la(b|ndseer)",
          r"leonberger",
          r"mailese",
          r"mal([ai]?mute|t[ei]?)",
          r"malanois",
          r"mastif+",
          r"min",
          r"mongrel",
          r"multi breed",
          r"munster",
          r"mutt",
          r"n\.?s\.?[dt]+\.?",
          r"newf",
          r"oodle",
          r"pap*il+i?on",
          r"pek[ei]?",
          r"pin\b",
          r"pit\b",
          r"po(m|o)",
          r"pointer",
          r"presa can[ae]+rio",
          r"pug",
          r"puli",
          r"pup",
          r"puppy",
          r"pyr[ae]?n[es]*",
          r"r(a|ei)?ner",
          r"retr x",
          r"retr?[ie]*ver",
          r"rhodesian",
          r"ri(ch|dge)back",
          r"s[ch]*n?a?u[hsz]*er",
          r"s[chk]*ipperke",
          r"samoy",
          r"sc?har[\s-]?pei",
          r"scooby doo",
          r"scottie",
          r"setter",
          r"sh[e]+p",
          r"sh[ei]b[au]?",
          r"shelti[e]?",
          r"shih?",
          r"small [dg]og",
          r"small breed",
          r"span",
          r"staff",
          r"terr",
          r"unknown breed",
          r"vi[szl]+a",
          r"westie",
          r"whippet",
          r"wolf",

         ]

others = [
            r"\Aduck\Z",
            r"\Arat\Z",
            r"african grey",
            r"alexandrian",
            r"bearded dragon",
            r"bird",
            r"budg(ie|y)",
            r"bunny",
            r"cockat([ie]+l|oo)",
            r"dove",
            r"eared dwarf",
            r"ferret",
            r"finch",
            r"green cheek",
            r"guinea",
            r"hen",
            r"monkey",
            r"parakeet",
            r"parro(le)?t",
            r"peacock",
            r"pigeon",
            r"python",
            r"rabbit",
            r"ringneck",
            r"snake",
            r"sun conure",
            r"turtle",
           ]

unknowns = [
            r"(un|not )sure",
            r"\A\?+\Z",
            r"\Ablack\Z",
            r"\Agold\Z",
            r"\Amed(ium)? size\Z",
            r"\Ared\Z",
            r"\Arust\Z",
            r"\Asmall\Z",
            r"\Aunknown\Z",
            r"\Awhite\Z",
            r"black & brindle",
            r"black w torn left ear",
            r"black w white on neck",
            r"black with brown spots",
            r"Blk/Brown & Blk/White",
            r"did not say",
            r"did not specify breed",
            r"full sized",
            r"heinz 57",
            r"lion head",
            r"long fluffy fir",
            r"long fluffy fur",
            r"med-large \?",
            r"medium long hair",
            r"medium size, short hair",
            r"not given",
            r"not really sure",
            r"rust & tan",
            r"small scruffy",
            r"small scruffy\?",
            r"small short haired curly tail",
            r"small with half cropped tail",
            r"very small"
           ]

cat_regex = re.compile("|".join(cats), re.IGNORECASE)
dog_regex = re.compile("|".join(dogs), re.IGNORECASE)
other_regex = re.compile("|".join(others), re.IGNORECASE)
unknown_regex = re.compile("|".join(unknowns), re.IGNORECASE)

# Some cursory data cleaning...

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

def dog_breed_type(breed):
  breed = str(breed).lower()
  breed_type = ""
  if " x" in breed or " mix" in breed:
    #print "CROSS: " + breed
    breed_type = "cross"
  elif breed in dog_breed_dict:
    #print "FOUND: " + breed + " --> " + dog_breed_dict[breed]
    breed_type = dog_breed_dict[breed]
  else:
    found = False
    for key in dog_breed_dict.keys():
      if breed in key:
        breed_type = dog_breed_dict[key]
        found = True
        break
      if key in breed:
        breed_type = dog_breed_dict[key]
        found = True
        break
    if not found:
      #print "MISS:  " + breed
      breed_type = "unknown"
  return breed_type

def extract_sex(item):
  item = str(item).lower()
  if item == "nan":
    return "x"
  return item[0]

def is_animal_type(item, regex):

  item = str(item).strip(".")
  result = regex.search(item)

  return False if result is None else True

def filter_df_by_top_n_items(df, column_name, n):
  filtered_df = df.copy()
  df_filter = filtered_df[column_name].value_counts().head(n)
  df_filter = list(df_filter.keys())
  df_filter = { column_name: df_filter }
  row_mask = filtered_df.isin(df_filter).any(1)
  filtered_df = filtered_df[row_mask]
  return filtered_df


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
lostAnimals.rename(columns={ "Name": "pet_name" }, inplace=True)
lostAnimals['Color'] = lostAnimals['Color'].map(lambda x : collapse_colors(x))
lostAnimals['is_cat'] = lostAnimals['Breed'].map(lambda x : is_animal_type(x, cat_regex))
lostAnimals['is_dog'] = lostAnimals['Breed'].map(lambda x : is_animal_type(x, dog_regex))
lostAnimals['is_other'] = lostAnimals['Breed'].map(lambda x : is_animal_type(x, other_regex))
lostAnimals['is_unknown'] = lostAnimals['Breed'].map(lambda x : is_animal_type(x, unknown_regex))
lostAnimals['sex_simple'] = lostAnimals['Sex'].map(lambda x : extract_sex(x))
lostAnimals['dog_breed_type'] = lostAnimals[lostAnimals.is_dog == True]['Breed'].map(lambda x : dog_breed_type(x))
lostAnimals['date_created'] = pd.to_datetime(lostAnimals['DateCreated'])

lostAnimals[(lostAnimals.is_dog)][lostAnimals.pet_name != 'Unknown']['pet_name'].value_counts().head(10).to_csv('name.csv')
lostAnimals['Color'].value_counts().head(25).to_csv('color.csv')
lostAnimals[(lostAnimals.is_dog == True)]['Breed'].value_counts().head(25).to_csv('breed.csv')
lostAnimals.to_csv('all.csv')

# Now do some group by magic
# http://pandas.pydata.org/pandas-docs/stable/indexing.html
#byname = lostAnimals[(lostAnimals.is_dog == True)].groupby(['Name', 'sex_simple'])
#print byname.describe()

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