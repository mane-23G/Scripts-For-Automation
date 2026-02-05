#! /bin/bash
#Author: Mane Galstyan
#Date: November 20, 2025
#Usage: newshow title num_seasons

seasons=$2
i=1
path=$3
title=$1
#Check number of Arguments Passed it Correct
if [ $# -ne 3 ]; then
	echo "Incorrect Num of Argument"
    echo "Usage: newshows title num_seasons show_dir"
    exit
#Check is directory for show exists 
elif [ -d "$path$title" ]
then 
    echo "Directory already exists"
    s=$(ls "$path$title" | wc -l)
    #If requested num of season dir is less than existing num of seasons exit
    if [ $s -ge $seasons ]
    then
        echo "No need for more seasons"
        exit
    #If requested num of season dir is greater than existing num of seasons update i to start from prexisting + 1
    else 
        i=$(($i+$s))
    fi
#If directory for show doesnt exist create one
else 
    echo "Directory doesnt exist yet"
    mkdir "$path$title"
    echo "Directory Created"
fi

#Create Seaons from i to requested amount
echo "Creating Seasons .."
for ((i; i<=seasons;i++))
do
    echo -n "$i .. "
    mkdir "$path$title/Season $i"
done
echo "Done!"

exit 0