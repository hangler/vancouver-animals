import pandas as pd
import re as re
from datetime import datetime

lostAnimals = pd.read_csv('LostAnimals-2014-09-30.csv')

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
  valid_colors = ["black", "white", "brown", "grey", "red", "tan", "gold"]
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

def collapse_breeds(item):
  valid_breeds = ["lab", "shih", "shep", "chihuahua", "collie", "pitbull", "husky", "pomeranian", "rott", "retriever" ]
  breeds = []
  item = str(item).lower()

  if " x" in item:
    breeds.append("cross")
  else:
    for valid_breed in valid_breeds:
      if valid_breed in item:
        breeds.append(valid_breed)
  
  if len(breeds) == 0:
    breeds.append("other")
  elif len(breeds) > 1:
    breeds = []

  return "/".join(breeds).title()

def is_breed(item, regex):

  item = str(item).strip(".")
  result = regex.search(item)

  return False if result is None else True



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
lostAnimals['is_cat'] = lostAnimals['Breed'].map(lambda x : is_breed(x, cat_regex))
lostAnimals['is_dog'] = lostAnimals['Breed'].map(lambda x : is_breed(x, dog_regex))
lostAnimals['is_other'] = lostAnimals['Breed'].map(lambda x : is_breed(x, other_regex))
lostAnimals['is_unknown'] = lostAnimals['Breed'].map(lambda x : is_breed(x, unknown_regex))
lostAnimals['pet_name'] = lostAnimals['Name']

print lostAnimals[(lostAnimals.is_other < 1) & (lostAnimals.is_dog < 1) & (lostAnimals.is_cat < 1)]['Breed'].value_counts()

lostAnimals[(lostAnimals.is_dog)][lostAnimals.pet_name != 'Unknown']['Name'].value_counts().head(10).to_csv('name.csv')
lostAnimals['Color'].value_counts().head(25).to_csv('color.csv')
lostAnimals[(lostAnimals.is_other == True) & (lostAnimals.is_unknown == True)]['Breed'].value_counts().to_csv('breed.csv')
lostAnimals.to_csv('all.csv')