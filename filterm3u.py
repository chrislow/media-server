#!/usr/bin/env python3
"""
M3U Filter Script
Filters an M3U playlist file to keep only channels from specific countries (DE, UK, AT).
"""

import re
import os


def filter_m3u_by_countries(input_file, output_file, countries=None):
    """
    Filter M3U file to keep only channels from specified countries.

    Args:
        input_file (str): Path to the input M3U file
        output_file (str): Path to the output M3U file
        countries (list): List of country codes to keep (default: ['DE', 'UK', 'AT'])
    """
    if countries is None:
        countries = ["DE", "UK", "AT"]

    # Create regex pattern to match channels from specified countries
    # Pattern looks for channels that start with any of the country codes followed by ':'
    country_pattern = "|".join([f"{country}:" for country in countries])
    pattern = re.compile(f'tvg-name="({country_pattern})', re.IGNORECASE)

    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"Error reading input file: {e}")
        return False

    filtered_lines = []
    keep_next_line = False
    channels_kept = 0
    total_channels = 0

    print("Processing M3U file...")

    for i, line in enumerate(lines):
        line = line.strip()

        # Always keep the header
        if line.startswith("#EXTM3U"):
            filtered_lines.append(line + "\n")
            continue

        # Check if this is a channel info line
        if line.startswith("#EXTINF:"):
            total_channels += 1

            # Check if this channel matches our country criteria
            if pattern.search(line):
                filtered_lines.append(line + "\n")
                keep_next_line = True
                channels_kept += 1

                # Extract channel name for progress indication
                name_match = re.search(r'tvg-name="([^"]*)"', line)
                if name_match:
                    channel_name = name_match.group(1)
                    print(f"Keeping: {channel_name}")
            else:
                keep_next_line = False

        # Keep the URL line if the previous EXTINF line was kept
        elif keep_next_line and line.startswith("http"):
            filtered_lines.append(line + "\n")
            keep_next_line = False

        # Keep other non-URL lines (comments, etc.)
        elif not line.startswith("http") and line.strip():
            # Only keep if it's not associated with a filtered-out channel
            if not keep_next_line:
                continue

    # Write filtered content to output file
    try:
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.writelines(filtered_lines)

        print(f"\nFiltering complete!")
        print(f"Total channels processed: {total_channels}")
        print(f"Channels kept: {channels_kept}")
        print(f"Channels removed: {total_channels - channels_kept}")
        print(f"Filtered file saved as: {output_file}")

        return True

    except Exception as e:
        print(f"Error writing output file: {e}")
        return False


def main():
    """Main function to run the M3U filter."""
    # File paths
    input_file = "tv_channels_678cb8d5ba_plus.m3u"
    output_file = "filtered_channels_DE_UK_AT.m3u"

    # Countries to keep (you can modify this list)
    countries_to_keep = ["DE", "UK", "AT"]

    print("M3U Channel Filter")
    print("=" * 50)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Keeping channels from: {', '.join(countries_to_keep)}")
    print("=" * 50)

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found in current directory.")
        print("Please make sure the M3U file is in the same directory as this script.")
        return

    # Filter the M3U file
    success = filter_m3u_by_countries(input_file, output_file, countries_to_keep)

    if success:
        print(f"\n✅ Success! Filtered M3U file created: {output_file}")
    else:
        print(f"\n❌ Failed to create filtered M3U file.")


if __name__ == "__main__":
    main()
