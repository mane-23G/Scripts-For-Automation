#!/usr/bin/env python3
import subprocess
from pathlib import Path
import re
from collections import defaultdict

# path_to_dir = "/var/lib/deluge/Downloads/"
paths = ["/var/lib/deluge/Downloads/","/content/Shows2/Downloads/","/content/Shows3/Downloads/","/content/Shows4/Downloads/"]
show_paths = ["/content/Shows/","/content/Shows2/Shows/","/content/Shows3/Shows/","/content/Shows4/Shows/"]
# paths = ["/Users/mane/scratch/fake/Shows1/Downloads/","/Users/mane/scratch/fake/Shows2/Downloads/"]
# show_paths = ["/Users/mane/scratch/fake/Shows1/Shows/","/Users/mane/scratch/fake/Shows2/Shows/"]

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
    
    #pattern to match the file name number of seasons portion one for ones with . and one for spaces
    # pattern = r'\.[sS][0-9][0-9]'
    # pattern2 = r'\([0-9]{4}\)'
    # pattern3 = r'[sS]eason\ [0-9]{0,3}'
    pattern = r'[sS](eason\ )?[0-9]{1,3}'
    pattern_year = r'\([0-9]{4}\)'

    #iterate through the items in the Downloads folder
    #1. change the entry(folder item) into str
    #2. find the place where the season number is
    #3. search for the occurence of pattern
    #4. group the result to get the actual string
    #5. get the start position of the name
    #6. from the beg of string to the end split the title with '.' to create folder nmae
    #7. add the show name to the dict with the num of seasons being the max of the value
    for entry in target_dir.iterdir():
        name = str(entry.name)
        season = re.search(pattern,name)
        if not season:
            print(f"Entry {name} doesnt fit naming convention. ")
            continue
        
        season = season.group() 
        pos = name.find(season)
        pattern_season = r'[0-9]{1,3}'
        season = re.search(pattern_season,season).group()

        year = re.search(pattern_year,name[0:pos])
        if year:
            year = year.group()
            pos = name.find(year)

        title = name[0:pos].split('.')
        if len(title) == 1:
            title = name[0:pos].split(' ')
        title = ' '.join(title)
        title = re.sub(r'[^a-zA-Z0-9\ ]','',title).strip()

        season = int(season)
        simplified[title] = max(simplified[title],season)
        sorting[title].append([name,str(season)])
        # sorting_entry[title].append(name)
        # sorting_season[title].append(str(int(season)))

    # remove the / from the download path
    # path = path[:-1]
    # iterate every key,value in the show map
    #1. join together the folder name (with space) with '.'
    #2. print out the show being processed
    #3. call make dirs which essentially just make the season folders and the show folders
    #4. moves the files given the num of seasons to the final dest
    # for key,value in simplified.items():
    #     print(f"{key} is being processed ...")
        # subprocess.call(['./makedirs.sh',key,str(value),show_dir])
        # key - (Normal People) , entry_list - (normal people s01e01, normal people s01e02, ...) season_list - (1,1) 
        # NVM cant pass arrays in bash script *sad face*
        # subprocess.call(['./movestuff.sh',key,entry_list,season_list])
    


    for key,value in simplified.items():
        print(f"{key} is being processed ...")
        subprocess.call(['./makedirs.sh',key,str(value),show_dir])
        for entry,season in sorting[key]:
            loc = path + entry
            dest = show_dir + key + '/Season ' + season + '/'
            # print(f"location: {loc}")
            # print(f"destantion: {dest}")
            subprocess.call(['mv',loc,dest])

# # iterate move downlad and dest paths
# # move all files in download to dest
# for i,m in enumerate(movies):
#     #creates the path of the dir to be traversed
#     target_dir = Path(m)
#     mov_dir = movie_path[i]
    
#     for entry in target_dir.iterdir():
#         name = m + str(entry.name)
#         subprocess.call(['mv',name,mov_dir])




# cd fake/ ; cd Shows1/Downloads ; mkdir 'Invincible (2021) Season 1 S01 (1080p WEB-DL x265 HEVC 10bit EAC3 5.1 SAMPA)'; mkdir 'Invincible (2021) Season 2 S02 (1080p AMZN WEB-DL x265 HEVC 10bit EAC3 5.1 Ghost)'; mkdir 'Invincible (2021) Season 3 S03 (1080p AMZN WEB-DL x265 HEVC 10bit DDP 5.1 Vyndros)'; mkdir 'Normal People Season 1  [2160p x265 10bit S94 Joy]'; mkdir 'Abbott.Elementary.S01.1080p.DSNP.WEBRip.DDP5.1.x264-NTb[rartv]'; mkdir 'Abbott Elementary (2021) Season 2 S02 (1080p AMZN WEB-DL x265 HEVC 10bit EAC3 5.1 Silence)'; mkdir 'Abbott Elementary (2021) S03 (1080p AMZN WEB-DL x265 10bit EAC3 5.1 Silence)'; mkdir 'Abbott Elementary (2021) S04 (1080p AMZN WEB-DL x265 10bit EAC3 5.1 Silence)'; cd ../../Shows2/Downloads ; mkdir 'Tell.Me.Lies.S01.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA'; touch 'Tell.Me.Lies.S02E01.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv'; touch 'Tell.Me.Lies.S02E02.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv'; touch 'Tell.Me.Lies.S02E03.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv'; touch 'Tell.Me.Lies.S02E04.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv'; touch 'Tell.Me.Lies.S02E05.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv'; touch 'Tell.Me.Lies.S03E06.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv'; mkdir "Normal People Season 1 [2160p x265 10bit S94 Joy]"; mkdir "Normal People Season 2 [2160p x265 10bit S94 Joy]"