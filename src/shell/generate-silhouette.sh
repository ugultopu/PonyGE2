#!/bin/bash
# Run this script from one level above PonyGE2 project. For that,
# symlink this script to one level above PonyGE2 projects.

# Create output directories named after current date and time
directory="results/$(date '+%Y_%m_%d-%H_%M_%S')"
mkdir -p "PonyGE2/$directory"

# Run PonyGE2 script
cd PonyGE2/src
python3 ponyge.py --parameters ai_birds.txt --file_path "$directory" &> "../$directory/output.txt"
