import requests
from bs4 import BeautifulSoup
from datetime import datetime

def generate_files(athlete_name):
    # Format the athlete name for the URL
    url_name = athlete_name.lower().replace(" ", "-")
    url = f"https://cpb.org.br/atletas/{url_name}/"
    print(url)
    # Send an HTTP request to the URL
    response = requests.get(url)
    
    # Check for a valid response
    if response.status_code != 200:
        print(f'Failed to retrieve page with status code: {response.status_code}')
        exit()
    
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting relevant information
    name = soup.find('h1', class_='Athlete__name').text
    dob_raw = soup.find('time').text.strip()
    dob_formatted = datetime.strptime(dob_raw, "%d/%m/%Y").strftime("+%Y-%m-%dT00:00:00Z/9")
    place_of_birth = soup.find_all('td')[7].text
    
    # Quickstatements for Wikidata
    wikidata_quickstatements = f"""
    CREATE
    LAST|Len|"{name}"
    LAST|Lpt|"{name}"
    LAST|Den|"Brazilian paralympic athlete"
    LAST|Dpt|"Atleta paralímpica brasileira"
    LAST|P31|Q5
    LAST|P21|Q6581072|S854|"{url}"
    LAST|P1532|Q155|S854|"{url}"
    LAST|P27|Q155|S854|"{url}"
    LAST|P569|"{dob_formatted}"|S854|"{url}"
    """
    
    # Wikipedia stub
    wikipedia_stub = f"""
    {{{{Info/Biografia/Wikidata}}}}
    '''{name}''' ({dob_raw}, {place_of_birth}  ) é uma atleta paralímpica brasileira.

    == Ligações externas ==

    {{{{Esboço-atleta}}}}
    {{{{DEFAULTSORT:{name}}}}}
    [[Categoria:Atletas paralímpicos do Brasil]]
    [[Categoria:Naturais de {place_of_birth.split(' – ')[0]}]]
    [[Categoria:Canoístas do Brasil]]
    """
    
    # Writing to files
    with open('wikidata_quickstatements.txt', 'w') as file:
        file.write(wikidata_quickstatements)
    
    with open('wikipedia_stub.txt', 'w') as file:
        file.write(wikipedia_stub)

# Call the function with the athlete's name as argument
generate_files("Adriana Gomes de Azevedo")
