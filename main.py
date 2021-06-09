from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

home_url = 'https://karnatik.com/'
composers_wanted = {
    "Muttuswaamee Dikshitar": "Dikshitar",
    "Shyaamaa Shaastree": "Syama Sastri", 
    "Tyaagaraaja" : "Tyagayya"
    }
composers = []

#Parse the Karnatik.com homepage and find the link to the page for composers
def parse_karnatik():
    source = requests.get(home_url).text
    soup = bs(source, 'lxml')
    
    url = ""

    links = soup.find_all('li')
    
    for link in links:
        if link.a.text == 'by Composer':
            url = home_url + link.a["href"]
            break
    
    get_composers(url)

    df = pd.DataFrame(composers)
    print(df.shape)

    df.to_csv('composers.csv', index = False)

#Parse composer page links and find the link to the composer home pages
def get_composers(url):
    source = requests.get(url).text
    soup = bs(source, 'lxml')
    links = soup.find_all('a')

    for link in links:
        if link.text in composers_wanted:    
            name = composers_wanted[link.text]
            get_compositions(home_url + link["href"], name)

#Parse each composer's page link and find the compositions 
def get_compositions(url, name):
    source = requests.get(url).text
    soup = bs(source, 'lxml')
    links = soup.find('ol')

    count = 0

    for link in links.find_all('li'):
        title = link.a.text.split('-')[0].strip()
        raagam = link.a.text.split('-')[1].strip()
        count = count + 1
        get_lyrics(home_url + link.a["href"], name, title, raagam, count)

#Parse the composition page for lyric and meaning
#Write everything to csv
def get_lyrics(url, name, title, raagam, count):
    lyric = ""
    meaning = ""

    source = requests.get(url).text
    soup = bs(source, 'lxml')

    tds = soup.find('td', width='420', valign='top')

    if tds is None:
        pass
    else:
        paragraphs = tds.find_all('p')

        lyricfound = False

        for para in paragraphs:
            if "Meaning" in para.text:
                meaning = para.text.strip().removeprefix("Meaning:")
                lyricfound = False
                break

            if lyricfound:
                lyric = lyric + para.text.strip() + "\n"

            if "Language" in para.text:
                lyricfound = True

        df_row = {'composer': name, 
                  'composition': title, 
                  'raagam': raagam, 
                  'lyric': lyric, 
                  'meaning': meaning}
        
        print("Composer: " + name + ", Count: " + str(count))

        composers.append(df_row)

if __name__ == "__main__":
    parse_karnatik()
else:
    print("Well, you are importing this, aren't you?")