# Media Server

## M3U Filter Script

This Python script filters an M3U playlist and keeps only TV channels from specific countries (default: DE, UK, AT).

Features
	•	Reads an existing .m3u playlist file
	•	Filters channels based on their tvg-name attribute
	•	Writes a new .m3u file containing only the selected countries
	•	Displays a summary of processed, kept, and removed channels

Usage
	1.	Make sure Python 3 is installed.
	2.	Place your .m3u file in the same directory as the script.
	3.	(Optional) Edit the following variables inside the script if needed:

input_file = "tv_channels_678cb8d5ba_plus.m3u"
output_file = "filtered_channels_DE_UK_AT.m3u"
countries_to_keep = ["DE", "UK", "AT"]


	4.	Run the script:

python3 m3u_filter.py


	5.	The filtered file will be saved as specified in output_file.

Example Output

M3U Channel Filter
==================================================
Input file: tv_channels_678cb8d5ba_plus.m3u
Output file: filtered_channels_DE_UK_AT.m3u
Keeping channels from: DE, UK, AT
==================================================
Processing M3U file...
Keeping: DE:ZDF
Keeping: UK:BBC One
...
Filtering complete!
Total channels processed: 120
Channels kept: 35
Channels removed: 85
Filtered file saved as: filtered_channels_DE_UK_AT.m3u


⸻

Do you also want me to add a section on installing dependencies (in case someone runs it in a fresh environment), or keep it minimal since it only uses the standard library?
