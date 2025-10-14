import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

from slack_sdk import WebClient

def send_slack(message):
    client = WebClient(token="")

    result = client.chat_postMessage(
            channel = "cms-econ-asic", 
            text = message,
            username = "Bot User")

    return result

def send_slack_image(image_path):
    client = WebClient(token="")

    with open(image_path, "rb") as file_content:
        result = client.files_upload(
        channels="cms-econ-asic",
        file=file_content,
        filename="image.png",
        title="PNG Image"
        )



# Define the path to the directory containing the CSV files
path = 'plots/summary/csv-results/*.csv'

# Read all CSV files
files = glob.glob(path)

# Determine the parent directory to save the figures
parent_directory = 'plots/summary/'

# Get today's date
today = datetime.now().strftime('%Y-%m-%d')

# Initialize data containers
quality_counts = defaultdict(int)
barcode_counts = defaultdict(int)
chip_quality_counts = defaultdict(int)

# Process each file
for file in files:
    data = pd.read_csv(file)
    
    # Count quality occurrences
    for quality, count in data['quality'].value_counts().items():
        quality_counts[quality] += count
    
    # Count chips with quality > 0 for each barcode
    for barcode, subdata in data.groupby('barcode'):
        total_chips_in_barcode = len(subdata)
        barcode_counts[barcode] += (subdata['quality'] > 0).sum()
        barcode_counts[f"{barcode}_total"] = total_chips_in_barcode  # Store total chips per barcode
    
    # Count chips with quality > 0 for each chip number
    for chip, subdata in data.groupby('chip'):
        chip_quality_counts[chip] += (subdata['quality'] > 0).sum()

# Total chips for percentages
total_chips = sum(quality_counts.values())

# Quality labels
quality_labels = {0: 'bad', 1: 'pass', 2: 'medium = 1.08 V', 3: 'high = 1.03 V', 4:'top = 0.99 V'}

# Plot 1: Number of chips as a function of quality
plt.figure(figsize=(10, 6))
qualities_sorted = sorted(quality_counts.keys())
values = [quality_counts[q] for q in qualities_sorted]
labels = [quality_labels[q] for q in qualities_sorted]

# Create bar chart
bars = plt.bar(labels, values, color='skyblue')

# Add text annotations for counts and percentages
for bar, count in zip(bars, values):
    percentage = count / total_chips * 100
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 5,
        f"{count} ({percentage:.1f}%)",
        ha='center',
        va='bottom'
    )

plt.xlabel('Quality Levels')
plt.ylabel('Number of Chips')
plt.title(f'Inventory Plot: Number of Chips by Quality ({today})')
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(parent_directory, "chips_by_quality.png"))
send_slack_image(os.path.join(parent_directory, "chips_by_quality.png"))

#plt.show()

# Plot 2: Number of chips with quality > 0 as a function of the barcode
plt.figure(figsize=(12, 6))

# Sort barcodes by numeric order
sorted_barcodes = sorted([b for b in barcode_counts.keys() if "_total" not in b])
sorted_values = [barcode_counts[barcode] for barcode in sorted_barcodes]
sorted_totals = [barcode_counts[f"{barcode}_total"] for barcode in sorted_barcodes]

# Create bar chart
bars = plt.bar(sorted_barcodes, sorted_values, color='orange')

# Add text annotations for counts and percentages
for bar, count, total in zip(bars, sorted_values, sorted_totals):
    percentage = count / total * 100
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        f"{count} ({percentage:.1f}%)",
        ha='center',
        va='bottom'
    )

plt.xlabel('Barcode')
plt.ylabel('Number of Chips with Quality > 0')
plt.title(f'Inventory Plot: Number of Chips with Quality > 0 by Barcode ({today})')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 90)  # Fix y-axis to 90
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(parent_directory, "chips_by_barcode.png"))
send_slack_image(os.path.join(parent_directory, "chips_by_barcode.png"))


#plt.show()

qualities_to_plot = {
    2: 'medium = 1.08 V',
    3: 'high = 1.03 V',
    4: 'top = 0.99 V'
}

for quality, label in qualities_to_plot.items():
    plt.figure(figsize=(12, 6))
    filtered_barcode_counts = defaultdict(int)

    # Filter barcodes for the current quality
    for file in files:
        data = pd.read_csv(file)
        for barcode, subdata in data.groupby('barcode'):
            filtered_barcode_counts[barcode] += (subdata['quality'] == quality).sum()
            filtered_barcode_counts[f"{barcode}_total"] = len(subdata)  # Total chips per barcode

    sorted_barcodes = sorted([b for b in filtered_barcode_counts.keys() if "_total" not in b])
    sorted_values = [filtered_barcode_counts[barcode] for barcode in sorted_barcodes]
    sorted_totals = [filtered_barcode_counts[f"{barcode}_total"] for barcode in sorted_barcodes]

    # Create bar chart
    bars = plt.bar(sorted_barcodes, sorted_values, color='blue')

    # Add text annotations for counts and percentages
    for bar, count, total in zip(bars, sorted_values, sorted_totals):
        percentage = count / total * 100 if total > 0 else 0
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{count} ({percentage:.1f}%)",
            ha='center',
            va='bottom'
        )

    plt.xlabel('Barcode')
    plt.ylabel(f'Number of Chips with Quality = {label}')
    plt.title(f'Inventory Plot: Number of Chips with Quality = {label} by Barcode ({today})')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 90)  # Fix y-axis to 90
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(parent_directory, f"chips_by_barcode_{label.replace(' ', '_')}.png"))
    send_slack_image(os.path.join(parent_directory, f"chips_by_barcode_{label.replace(' ', '_')}.png"))

    #plt.show()

# Plot 3: Number of chips with quality > 0 as a function of the chip number
plt.figure(figsize=(12, 6))
sorted_chip_numbers = sorted(chip_quality_counts.keys())
sorted_chip_values = [chip_quality_counts[chip] for chip in sorted_chip_numbers]

plt.bar(sorted_chip_numbers, sorted_chip_values, color='green')
plt.xlabel('Chip Number')
plt.ylabel('Number of Chips with Quality > 0')
plt.title(f'Inventory Plot: Number of Chips with Quality > 0 by Chip Number ({today})')
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(parent_directory, "chips_by_chip_number.png"))
send_slack_image(os.path.join(parent_directory, "chips_by_chip_number.png"))

#plt.show()
