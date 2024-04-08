import pandas as pd
import os
from glob import glob

def merge_csv_with_timestamps(output_csv_dir, timestamps_csv_dir, merged_csv_dir):
    # List all CSV files in the output CSV directory
    output_csv_files = glob(os.path.join(output_csv_dir, '*.csv'))
    
    for output_csv_path in output_csv_files:
        # Derive the base file name without extension to match with timestamp file
        base_file_name = os.path.basename(output_csv_path)
             
        # Construct the expected timestamp CSV file path
        timestamps_csv_path = os.path.join(timestamps_csv_dir, base_file_name)
        
        # Check if the corresponding timestamps CSV exists
        if not os.path.exists(timestamps_csv_path):
            print(f"No matching timestamp file found for {base_file_name}. Skipping...")
            continue
        
        # Load the CSV files
        output_df = pd.read_csv(output_csv_path)
        timestamps_df = pd.read_csv(timestamps_csv_path)

        # Merge the two dataframes on the Frame and Frame_Number columns
        merged_df = pd.merge(output_df, timestamps_df, left_on='Frame', right_on='Frame_Number', how='left')

        # Including all relevant columns and renaming
        #final_df = merged_df[['Datetime', 'Frame', 'Track', 'Class', 'BBox', 'Time', 'Date', 'Red_Light']].copy()
        final_df = merged_df[['Datetime', 'Frame', 'Track', 'Class', 'Class_ID','xmin', 'ymin','xmax','ymax', 'Time', 'Date', 'Red_Light']].copy()
        final_df.rename(columns={'Frame': 'FrameNumber', 'Red_Light': 'Color'}, inplace=True)
        
        # Handle 'Color' column
        final_df['Color'].fillna('Not Red', inplace=True)
        final_df['Color'] = final_df['Color'].apply(lambda x: 'Red' if x == True else 'Not Red')

        # Construct path for saving the merged CSV
        merged_csv_path = os.path.join(merged_csv_dir, base_file_name)
        
        # Save the merged dataframe
        final_df.to_csv(merged_csv_path, index=False)
        print(f"Merged CSV saved to {merged_csv_path}")

# Directories containing the CSV files
#output_csv_dir = 'C:/Users/marya1/Box/MnDOT DNRTOR Project/Meenakshi/detect_objects'
#timestamps_csv_dir = 'C:/Users/marya1/Box/MnDOT DNRTOR Project/Meenakshi/detect_red'
#merged_csv_dir = 'C:/Users/marya1/Box/MnDOT DNRTOR Project/Meenakshi/final_csv'


output_csv_dir = '/home/marya1/Documents/MnDoTNRToR/inference/detect_objects/processing'
timestamps_csv_dir = '/home/marya1/Documents/MnDoTNRToR/inference/detect_red'
merged_csv_dir = '/home/marya1/Documents/MnDoTNRToR/inference/final_csv'

# Call the function with the directories
merge_csv_with_timestamps(output_csv_dir, timestamps_csv_dir, merged_csv_dir)