#! /bin/bash

#Author: Mane Galstyan
#Date: November 20, 2025
#Usage: moveshow showname foldername seasons

show_name=$1
folder_name="$2"
seasons=$3
path=$4
down_path=$5

#Check number of Arguments Passed it Correct
if [ $# -ne 5 ]; then
    echo "Incorrect Num of Argument"
    echo "Usage: moveshow showname foldername seasons show_dir_name download_path"
    exit
elif [ ! -d "$path$folder_name" ]
then 
    echo "Directory doesnt exist"
    exit
fi

count=0

for ((i=1; i<=seasons;i++))
do
    if [[ i -lt 10 ]]
    then
        x=$(echo "$show_name.[sS]0$i*")
    else
        x=$(echo "$show_name.[sS]$i*")
    fi
    file=$(find $down_path -type f -name  $x | wc -l)
    dir=$(find $down_path -type d -name  $x | wc -l)
    count=$(expr $count + $file + $dir)
    if [ $file -gt 0 ] || [ $dir -gt 0 ];
    then
        mv $down_path/$x $path"$folder_name/Season $i/"
    fi
done
echo "Moved $count files for $folder_name !"
exit 0