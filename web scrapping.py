import requests
from bs4 import BeautifulSoup
import csv

date = input("Please Enter the date in the following format MM/DD/YYYY : ")
page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")


def main (page):

    src = page.content
    soup = BeautifulSoup(src , "lxml" )
    matches_details = []

    championships = soup.find_all("div" , {"class" : "matchCard"})

    def get_match_info(championships):
        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all("div" , {"class" : "item finish liItem"})
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            # name of teams
            team_A = all_matches[i].find("div" , {'class' : 'teamA'}).text.strip()
            team_B = all_matches[i].find("div" , {'class' : 'teamB'}).text.strip()

            # results
            match_score = all_matches[i].find('div' , {'class' : 'MResult'}).find_all('span' , {'class' : 'score'})
            score = f"{match_score[0].text.strip()} - {match_score[1].text.strip()}"

            # time of the match 
            match_time = all_matches[i].find('div' , {'class' : 'MResult'}).find('span' , {'class' : 'time'}).text.strip()

            # add match info to matches_details
            matches_details.append({'نوع البطولة' : championship_title , 
                                    'الفريق الأول' : team_A,
                                    'الفريق الثاني' : team_B,
                                    'ميعاد المباراة' : match_time,
                                    'نتيجة المباراة' : score})
            
    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = matches_details[0].keys()

    with open('C:/Users/UAS/Documents/yalla_kora/matches-details.csv' , 'w') as output_file:
        dict_writer = csv.DictWriter(output_file , keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")
    
    
main(page)