#!/bin/bash

# List of Python files to run
PYTHON_FILES=(
    "bistThreshold1DHist.py"
    "currentDraw1DHist.py"
    "erxPhaseWidth1DHist.py"
    "erxPhaseWidth2DHist.py"
    "etxDelayWidth1DHist.py"
    "etxDelayWidth2DHist.py"
    "pllCapbankWidth1DHist.py"
    "pllCapbankWidth2DHist.py"
    "summaryPlots.py"
)

# Loop through each file in the list
for PYTHON_FILE in "${PYTHON_FILES[@]}"; do
    # Check if the file exists and is a Python file
    if [ -f "$PYTHON_FILE" ] && [ "${PYTHON_FILE##*.}" = "py" ]; then
	echo "Starting file: $PYTHON_FILE"
	# Run the Python file
        python "$PYTHON_FILE"
        
        # Print the name of the Python file
        echo "Executed file: $PYTHON_FILE"
    else
        echo "Error: $PYTHON_FILE does not exist or is not a Python file."
    fi
done
