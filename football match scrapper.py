import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_man_utd_fixtures():
    url = "https://www.bbc.com/sport/football/teams/manchester-united/scores-fixtures"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    matches = []
    # BBC structures fixtures inside divs with class 'sp-c-fixture'
    fixtures = soup.find_all('div', class_='sp-c-fixture')
    
    for fixture in fixtures:
        # Extract date
        date_div = fixture.find_previous('h3', class_='gel-minion')
        date = date_div.text.strip() if date_div else "Unknown Date"
        
        # Extract teams
        teams = fixture.find_all('span', class_='sp-c-fixture__team-name')
        if len(teams) == 2:
            home_team = teams[0].text.strip()
            away_team = teams[1].text.strip()
        else:
            continue
        
        # Extract time or result
        time_div = fixture.find('time')
        match_time = time_div['datetime'] if time_div and 'datetime' in time_div.attrs else "TBD"

        matches.append({
            'date': date,
            'home_team': home_team,
            'away_team': away_team,
            'match_time': match_time
        })
    
    # Filter for Manchester United matches only
    mu_matches = [m for m in matches if 'Manchester United' in (m['home_team'], m['away_team'])]
    
    df = pd.DataFrame(mu_matches)
    return df

if __name__ == "__main__":
    df_fixtures = scrape_man_utd_fixtures()
    print(df_fixtures)
