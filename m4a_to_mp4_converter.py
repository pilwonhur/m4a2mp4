#!/usr/bin/env python3
"""
M4A to MP4 Converter for YouTube Upload
Converts M4A audio files to MP4 video files with a blank video component.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import json

def check_ffmpeg():
    """Check if ffmpeg is installed and available."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_audio_duration(audio_file):
    """Get the duration of the audio file in seconds."""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', 
            '-show_format', audio_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return None

def convert_m4a_to_mp4(input_file, output_file=None, background_color='black', resolution='1920x1080'):
    """
    Convert M4A audio file to MP4 video file with blank video component.
    
    Args:
        input_file (str): Path to input M4A file
        output_file (str): Path to output MP4 file (optional)
        background_color (str): Background color for the video (default: black)
        resolution (str): Video resolution (default: 1920x1080)
    """
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return False
    
    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.with_suffix('.mp4')
    
    # Get audio duration
    duration = get_audio_duration(input_file)
    if duration is None:
        print("Error: Could not determine audio duration.")
        return False
    
    print(f"Converting '{input_file}' to '{output_file}'...")
    print(f"Audio duration: {duration:.2f} seconds")
    print(f"Video resolution: {resolution}")
    print(f"Background color: {background_color}")
    
    # FFmpeg command to create MP4 with blank video and original audio
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',  # Use libavfilter virtual input
        '-i', f'color=c={background_color}:size={resolution}:duration={duration}',  # Generate solid color video
        '-i', input_file,  # Input audio file
        '-c:v', 'libx264',  # Video codec
        '-c:a', 'aac',  # Audio codec
        '-shortest',  # End when shortest input ends
        '-y',  # Overwrite output file
        output_file
    ]
    
    try:
        # Run the conversion
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Successfully converted to '{output_file}'")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during conversion: {e}")
        print(f"FFmpeg stderr: {e.stderr}")
        return False

def batch_convert(input_directory, output_directory=None, background_color='black', resolution='1920x1080'):
    """
    Convert all M4A files in a directory to MP4.
    
    Args:
        input_directory (str): Directory containing M4A files
        output_directory (str): Directory to save MP4 files (optional)
        background_color (str): Background color for the video
        resolution (str): Video resolution
    """
    
    if not os.path.exists(input_directory):
        print(f"Error: Input directory '{input_directory}' does not exist.")
        return
    
    # Set output directory
    if output_directory is None:
        output_directory = input_directory
    else:
        os.makedirs(output_directory, exist_ok=True)
    
    # Find all M4A files
    m4a_files = list(Path(input_directory).glob('*.m4a'))
    
    if not m4a_files:
        print(f"No M4A files found in '{input_directory}'")
        return
    
    print(f"Found {len(m4a_files)} M4A files to convert...")
    
    successful = 0
    failed = 0
    
    for m4a_file in m4a_files:
        output_file = Path(output_directory) / f"{m4a_file.stem}.mp4"
        
        print(f"\n--- Converting: {m4a_file.name} ---")
        if convert_m4a_to_mp4(str(m4a_file), str(output_file), background_color, resolution):
            successful += 1
        else:
            failed += 1
    
    print(f"\n📊 Conversion Summary:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Output directory: {output_directory}")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert M4A audio files to MP4 video files with blank video component for YouTube upload.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python m4a_to_mp4_converter.py input.m4a
  python m4a_to_mp4_converter.py input.m4a -o output.mp4
  python m4a_to_mp4_converter.py -d /path/to/m4a/files
  python m4a_to_mp4_converter.py -d /path/to/m4a/files -o /path/to/output
  python m4a_to_mp4_converter.py input.m4a --color white --resolution 1280x720
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input M4A file or directory for batch conversion')
    parser.add_argument('-o', '--output', help='Output MP4 file or directory')
    parser.add_argument('-d', '--directory', help='Directory containing M4A files for batch conversion')
    parser.add_argument('--color', default='black', 
                       help='Background color for the video (default: black)')
    parser.add_argument('--resolution', default='1920x1080',
                       help='Video resolution (default: 1920x1080)')
    parser.add_argument('--list-colors', action='store_true',
                       help='List available color names and exit')
    
    args = parser.parse_args()
    
    # List available colors
    if args.list_colors:
        print("Available color names:")
        colors = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'gray', 'grey']
        for color in colors:
            print(f"  - {color}")
        return
    
    # Check if ffmpeg is available
    if not check_ffmpeg():
        print("❌ Error: FFmpeg is not installed or not available in PATH.")
        print("Please install FFmpeg: https://ffmpeg.org/download.html")
        print("On macOS: brew install ffmpeg")
        print("On Ubuntu/Debian: sudo apt install ffmpeg")
        print("On Windows: Download from https://ffmpeg.org/download.html")
        sys.exit(1)
    
    # Handle batch conversion
    if args.directory:
        batch_convert(args.directory, args.output, args.color, args.resolution)
        return
    
    # Handle single file conversion
    if not args.input:
        parser.print_help()
        return
    
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' does not exist.")
        sys.exit(1)
    
    # Convert single file
    success = convert_m4a_to_mp4(args.input, args.output, args.color, args.resolution)
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()

