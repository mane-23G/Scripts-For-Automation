#! /bin/bash
#Testing
#Author: Mane Galstyan
#Date: November 20, 2025
#Usage: moveshow showname foldername seasons

#Check number of Arguments Passed it Correct
if [ $# -ne 3 ]; then
    echo "Incorrect Num of Argument"
    echo "Usage: moveshow showname foldername seasons"
    exit
# elif [ ! -d /media/shows/"$1" ]
elif [ ! -d /Users/mane/script/"$2" ]
then 
    echo "Directory doesnt exist"
    exit
fi

seasons=$3

for ((i=1; i<=seasons;i++))
do
    if [[ i -lt 10 ]]
    then
        x=$(echo "$1.S0$i*")
    else
        x=$(echo "$1.S$i*")
    fi
    count=$(find /Users/mane/script/shows/ -type f -name  $x | wc -l)
    if [[ count -gt 0 ]]
    then
        mv /Users/mane/script/shows/$x /Users/mane/script/"$2"/Season\ $i
    fi
done
echo "Moved $1 files!"
exit 0
