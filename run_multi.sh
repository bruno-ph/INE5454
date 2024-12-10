#!/bin/bash
cat workable_countries.txt | xargs -n 1 -P 10 -I {} bash -c "python3 src/get_regional_list.py '{}'"