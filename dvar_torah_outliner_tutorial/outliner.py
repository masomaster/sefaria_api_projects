import requests

def get_commentary_text(ref):
  	
    # Our standard GET request, and JSON parsing
    url = f"https://www.sefaria.org/api/v3/texts/{ref}"
    response = requests.get(url)
    data = response.json()

    # Checking to make sure we have a primary version for the commentary 
    # (otherwise, the versions field would be empty). 
    if "versions" in data and len(data['versions']) > 0:
      
      # Retrieve the general name of the commentary book (i.e. "Rashi on Genesis")
      title = data['title']
      
      # Retrieve the text of the commentary
      text = data['versions'][0]['text']

      # Return the title, and the text
      return title, text
    

url = "https://www.sefaria.org/api/calendars"

# Make a GET request to the URL
response = requests.get(url)

# Parse the response as JSON
data = response.json()  

# Get calendar lists
calendar_list = data['calendar_items']

for item in calendar_list:
        if item['title']['en'] == 'Parashat Hashavua':
            parasha_ref = item['ref'] 
            parasha_name = item['displayValue']['en']

parasha_ref = parasha_ref.split("-")[0]


### Get Hebrew text ###

url = f"https://www.sefaria.org/api/v3/texts/{parasha_ref}"

# Make GET request
response = requests.get(url)

# Parse response as JSON 
data = response.json() 

he_vtitle = data['versions'][0]['versionTitle'] 
he_pasuk = data['versions'][0]['text']


### Get English text ###

# Change version to English
url = f"https://www.sefaria.org/api/v3/texts/{parasha_ref}?version=english"

# Make the GET request
response = requests.get(url)

# Parse the response as JSON
data = response.json()

# Retrieve the version title, and text for the English verse.
en_vtitle = data['versions'][0]['versionTitle']
en_pasuk = data['versions'][0]['text']


### Get commentaries ###

url = f"https://www.sefaria.org/api/related/{parasha_ref}"

# Make the GET request
response = requests.get(url)

# Parse the response as JSON
data = response.json()

commentaries = []

for linked_text in data['links']:
    if linked_text['type'] == 'commentary':
        commentaries.append(linked_text['ref'])

com1_title, com1_text = get_commentary_text(commentaries[0])
com2_title, com2_text = get_commentary_text(commentaries[1])
com3_title, com3_text = get_commentary_text(commentaries[2])

print(f"My Outline for Parashat {parasha_name}")
print(f"Hebrew: {he_pasuk} (edition: {he_vtitle})")
print(f"English: {en_pasuk} (edition: {en_vtitle})")
print("\nThree Commentaries:")
print(f"A) {com1_title}: {com1_text}\n")
print(f"B) {com2_title}: {com2_text}\n")
print(f"C) {com3_title}: {com3_text}")