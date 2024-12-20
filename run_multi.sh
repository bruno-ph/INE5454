#!/bin/bash
cat intermediate_data/workable_countries.txt | xargs -n 1 -P 10 -I {} bash -c "python3 intermediate_data/get_regional_list.py '{}'"