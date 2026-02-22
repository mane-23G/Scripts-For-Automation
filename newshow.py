#!/usr/bin/env python3
import subprocess
from pathlib import Path
import re
from collections import defaultdict

# path_to_dir = "/var/lib/deluge/Downloads/"
paths = ["/var/lib/deluge/Downloads/","/content/Shows2/Downloads/","/content/Shows3/Downloads/","/content/Shows4/Downloads/"]
show_paths = ["/content/Shows/","/content/Shows2/Shows/","/content/Shows3/Shows/","/content/Shows4/Shows/"]
paths = ["/Users/mane/scratch/fake/Shows1/Downloads/","/Users/mane/scratch/fake/Shows2/Downloads/"]
show_paths = ["/Users/mane/scratch/fake/Shows1/Shows/","/Users/mane/scratch/fake/Shows2/Shows/"]

movies = ["/content/Shows5/Downloads/"]
movie_path = ["/content/Shows5/Movies/"]

# paths = ["/home/mmane/scratch/fake/Shows1/Downloads/","/home/mmane/scratch/fake/Shows2/Downloads/"]
# show_paths = ["/home/mmane/scratch/fake/Shows1/Shows/","/home/mmane/scratch/fake/Shows2/Shows/"]

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
    pattern = r'[sS](eason\ )?[0-9]{1,3}-'

    #pattern to find if year is included in title
    pattern_year = r'\([0-9]{4}\)'

    #iterate through the items in the Downloads folder
    for entry in target_dir.iterdir():
        #turn entry name to string and search for the season pattern 
        name = str(entry.name)
        season = re.search(pattern,name)

        #the file is serires pack where it would be s01-s07
        #set season to 0 to have dir of show name created only
        if season:
            season = season.group()
            pos = name.find(season)
            season = 0
        else:
            #the file is individual files
            pattern_alt = r'[sS](eason\ )?[0-9]{1,3}'
            season = re.search(pattern_alt,name)
            
            if not season:
                print(f"Show {name} does not match naming conventions.")
                continue
            
            #isolate season number from entry and find position of season in name string
            season = season.group() 
            pos = name.find(season)
            pattern_season = r'[0-9]{1,3}'
            season = re.search(pattern_season,season).group()

        #search entry name for year i.e. 2014 1990  and find pos if it exists
        year = re.search(pattern_year,name[0:pos])
        if year:
            year = year.group()
            pos = name.find(year)

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

            subprocess.call(['mv',loc,dest])

# iterate move downlad and dest paths
# move all files in download to dest
for i,m in enumerate(movies):
    #creates the path of the dir to be traversed
    target_dir = Path(m)
    mov_dir = movie_path[i]
    
    #moves entry to dest folder
    for entry in target_dir.iterdir():
        name = m + str(entry.name)
        subprocess.call(['mv',name,mov_dir])

