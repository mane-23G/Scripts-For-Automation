#!/usr/bin/env python3
import subprocess
from pathlib import Path
import re
from collections import defaultdict

paths = ["/var/lib/deluge/Downloads/","/content/Shows2/Downloads/","/content/Shows3/Downloads/","/content/Shows4/Downloads/","/content/Shows5/Downloads"]
show_paths = ["/content/Shows/","/content/Shows2/Shows/","/content/Shows3/Shows/","/content/Shows4/Shows/","/content/Shows5/Movies"]
paths = ["/Users/mane/scratch/fake/Shows1/Downloads/","/Users/mane/scratch/fake/Shows2/Downloads/"]
show_paths = ["/Users/mane/scratch/fake/Shows1/Shows/","/Users/mane/scratch/fake/Shows2/Shows/"]


for i,path in enumerate(paths):
    #creates the path of the dir to be traversed
    target_dir = Path(path)

    #the path that files/dir will be moved to 
    show_dir = show_paths[i]

    #map to the show names and num of seasons
    simplified = defaultdict(int)

    #map to the show name to files/dirs and season folder
    sorting = defaultdict(list)

    #pattern to find number of season regardless of '.' or ' ' and Season or S
    pattern = r'[sS](eason\ )?[0-9]{1,3}'

    #the file is individual files
    pattern_alt = r'[sS](eason\ )?[0-9]{1,3}-'
    
    #pattern to find if year is included in title
    pattern_year = r'\(?[0-9]{4}\)?'
    
    #pattern to find resoultion 
    pattern_res = r'[\[(]?[0-9]{4}p'

    #iterate through the items in the Downloads folder
    for entry in target_dir.iterdir():

        #turn entry name to string and search for the season pattern 
        name = str(entry.name)

        #search for all the patterns
        season = re.search(pattern,name)
        season_pack = re.search(pattern_alt,name)
        year = re.search(pattern_year,name)
        res = re.search(pattern_res,name)
        pos = len(name)

        #if file name is for multiple seasons make no season folder
        if season_pack:
            season = season_pack.group()
            pos = name.find(season)
            season = 0
        #if file is individual get number of seasons
        elif season:
            season = season.group()
            pos = name.find(season)
            pattern_season = r'[0-9]{1,3}'
            season = re.search(pattern_season,season).group()
        #its a movie or doesnt have season in title
        else:
            season = 0

        #search entry name for year i.e. 2014 1990  and find pos if it exists
        if year:
            year = year.group()
            year_pos = name.find(year)
            pos = pos if year_pos > pos else year_pos
        
        #search for res in the file name like 1080p
        if res:
            res = res.group()
            res_pos = name.find(res)
            pos = pos if res_pos > pos else res_pos
        
        #file name doesnt fit 
        if pos == 0:
            print(f"File {name} does not match naming conventions")
            continue

        #split the name and then rejoin it for the title (folder name) and strip it of anything but spaces and alphanumerics 
        title = name[0:pos].split('.')
        if len(title) == 1:
            title = name[0:pos].split(' ')
        title = ' '.join(title)
        title = re.sub(r'[^a-zA-Z0-9\ ]','',title).strip()
        
        #add show and number of seasons and entry name and corresponding season
        season = int(season)
        simplified[title] = max(simplified[title],season)
        sorting[title].append([name,str(season)])

    #for each show loop through the sorting dict and create show folder and mv the file to the corresponding folder
    for key,value in simplified.items():
        print(f"{key} is being processed ...")
        subprocess.call(['./makedirs.sh',key,str(value),show_dir])
        for entry,season in sorting[key]:
            #loc = /path/to/entry/entry_name
            loc = path + entry

            #dest = /path/to/show/Season n/
            dest = show_dir + key + '/Season ' + season + '/'
            if season == '0':
                dest = show_dir + key + '/'

            # print(f"loc is {loc} and dest is {dest}")
            subprocess.call(['mv',loc,dest])  
        # print("\n")