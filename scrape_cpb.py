import requests
from bs4 import BeautifulSoup
from datetime import datetime
import click
import webbrowser


@click.command()
@click.argument('athlete_name', required=False)
def generate_files(athlete_name):
    if not athlete_name:
        athlete_name = click.prompt('Please enter the athlete name')
    
    # Format the athlete name for the URL
    url_name = athlete_name.lower().replace(" ", "-")
    url = f"https://cpb.org.br/atletas/{url_name}/"
   # Send an HTTP request to the URL
    response = requests.get(url)
    
    # Check for a valid response
    if response.status_code != 200:
        print(f'Failed to retrieve page with status code: {response.status_code}')
        exit()
    

    webbrowser.open(url)

    # Open a browser with a Google search for the athlete's name
    google_search_url = f"https://www.google.com/search?q={athlete_name}"
    webbrowser.open(google_search_url)
    
    # Open the Wikipedia editing page for the athlete's name
    wikipedia_edit_url = f"https://pt.wikipedia.org/w/index.php?title={athlete_name.replace(' ', '_')}&action=edit&redlink=1"
    webbrowser.open(wikipedia_edit_url)



    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting relevant information
    name = soup.find('h1', class_='Athlete__name').text
    dob_raw = soup.find('time').text.strip()
    # Find the anchor tag with class 'Athlete__social-media--instagram'
    instagram_link = soup.find('a', class_='Athlete__social-media--instagram')['href']

    # Extract handle from the link
    instagram_handle = instagram_link.split('/')[-1]

    print(instagram_handle)
    dob_formatted = datetime.strptime(dob_raw, "%d/%m/%Y").strftime("+%Y-%m-%dT00:00:00Z/11")
    yob =     datetime.strptime(dob_raw, "%d/%m/%Y").strftime("%Y")
    place_of_birth = soup.find_all('td')[7].text
    city_of_birth = place_of_birth.split("–")[0].strip()
    
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
LAST|P569|{dob_formatted}|S854|"{url}"
    """
    if instagram_handle:
        wikidata_quickstatements += f'\nLAST|P2003|"{instagram_handle}"'
    # Wikipedia stub
    wikipedia_stub = f"""
{{{{Info/Biografia/Wikidata}}}}
'''{name}''' ({dob_raw}, [[{city_of_birth}]]  ) é uma [[atleta paralímpica]] [[brasileira]].

== Ligações externas ==

{{{{Esboço-atleta}}}}
{{{{DEFAULTSORT:{name}}}}}
[[Categoria:Atletas paralímpicos do Brasil]]
[[Categoria:Naturais de {city_of_birth}]]
[[Categoria:Nascidos em {yob}]]
[[Categoria:Pessoas com deficiência física do Brasil]]
[[Categoria:!Wikiconcurso Mulheres Brasileiras no Esporte (artigos)]]

{{{{Referências}}}}
{{{{controle de autoridade}}}}
{{{{Portal3|Desporto|Eventos Multiesportivos|Mulheres|Brasil}}}}

    """
    
    # Writing to files
    with open('wikidata_quickstatements.txt', 'w') as file:
        file.write(wikidata_quickstatements)
    
    with open('wikipedia_stub.txt', 'w') as file:
        file.write(wikipedia_stub)

# This part is needed to make it runnable as a script.
if __name__ == '__main__':
    generate_files()