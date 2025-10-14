import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Define the directories and files
base_dir = 'plots'
directories = [
'summary', 'bistThreshold', 'currentDraw1D', 'eRxPhaseWidth1DHist',
'eRxPhaseWidth2DHist', 'eTxDelayWidth1DHist', 'eTxPhaseWidth2DHist',
'pllCapbank1D', 'pllCapbank2D'
]

# Create a PDF file
with PdfPages('plots_summary.pdf') as pdf:
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        if os.path.exists(dir_path):
            for file_name in os.listdir(dir_path):
                if file_name.endswith('.png'):
                    file_path = os.path.join(dir_path, file_name)
                    # Create a new figure
                    fig, ax = plt.subplots()
                    img = plt.imread(file_path)
                    ax.imshow(img)
                    ax.axis('off')
                    ax.set_title(f'{directory}/{file_name}')
                    # Save the figure to the PDF
                    pdf.savefig(fig)
                    plt.close(fig)

print("PDF created successfully!")