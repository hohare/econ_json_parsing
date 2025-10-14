#!/bin/bash

# Run makeCSVECOND.py
echo "Running makeCSVECOND.py..."
python3 makeCSVECOND.py

# Check if the first script ran successfully
if [ $? -eq 0 ]; then
    echo "makeCSVECOND.py ran successfully."
else
    echo "Error: makeCSVECOND.py failed."
    exit 1
fi

# Run makeCSVECONT.py
echo "Running makeCSVECONT.py..."
python3 makeCSVECONT.py

# Check if the second script ran successfully
if [ $? -eq 0 ]; then
    echo "makeCSVECONT.py ran successfully."
else
    echo "Error: makeCSVECONT.py failed."
    exit 1
fi

echo "Both scripts ran successfully."
