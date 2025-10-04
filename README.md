# M4A to MP4 Converter for YouTube Upload

This Python script converts M4A audio files to MP4 video files with a blank video component, making them suitable for YouTube upload.

## Features

- ✅ Convert single M4A files to MP4
- ✅ Batch convert multiple M4A files in a directory
- ✅ Customizable background color and video resolution
- ✅ Automatic audio duration detection
- ✅ Cross-platform support (Windows, macOS, Linux)

## Prerequisites

### 1. Python 3.6+
Make sure you have Python 3.6 or higher installed.

### 2. FFmpeg
This script requires FFmpeg to be installed on your system.

#### Installation Instructions:

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
- Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Or use Chocolatey: `choco install ffmpeg`

**CentOS/RHEL:**
```bash
sudo yum install ffmpeg
# or for newer versions:
sudo dnf install ffmpeg
```

## Usage

### Basic Usage

Convert a single M4A file:
```bash
python m4a_to_mp4_converter.py input.m4a
```

Convert with custom output filename:
```bash
python m4a_to_mp4_converter.py input.m4a -o output.mp4
```

### Batch Conversion

Convert all M4A files in a directory:
```bash
python m4a_to_mp4_converter.py -d /path/to/m4a/files
```

Convert with custom output directory:
```bash
python m4a_to_mp4_converter.py -d /path/to/m4a/files -o /path/to/output
```

### Customization Options

**Change background color:**
```bash
python m4a_to_mp4_converter.py input.m4a --color white
```

**Change video resolution:**
```bash
python m4a_to_mp4_converter.py input.m4a --resolution 1280x720
```

**List available colors:**
```bash
python m4a_to_mp4_converter.py --list-colors
```

### Command Line Options

```
positional arguments:
  input                 Input M4A file or directory for batch conversion

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output MP4 file or directory
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing M4A files for batch conversion
  --color COLOR         Background color for the video (default: black)
  --resolution RESOLUTION
                        Video resolution (default: 1920x1080)
  --list-colors         List available color names and exit
```

## Examples

### Example 1: Basic Conversion
```bash
# Convert my_audio.m4a to my_audio.mp4 with black background
python m4a_to_mp4_converter.py my_audio.m4a
```

### Example 2: Custom Settings
```bash
# Convert with white background and 720p resolution
python m4a_to_mp4_converter.py my_audio.m4a --color white --resolution 1280x720
```

### Example 3: Batch Processing
```bash
# Convert all M4A files in the current directory
python m4a_to_mp4_converter.py -d .
```

### Example 4: Batch with Custom Output
```bash
# Convert all M4A files and save to a specific directory
python m4a_to_mp4_converter.py -d ./audio_files -o ./video_files
```

## Output

The script will:
1. Check if FFmpeg is available
2. Analyze the input audio file to determine duration
3. Create a video with the specified background color and resolution
4. Combine the blank video with the original audio
5. Output an MP4 file ready for YouTube upload

## Supported Colors

The script supports standard color names:
- black (default)
- white
- red
- green
- blue
- yellow
- cyan
- magenta
- gray/grey

## Troubleshooting

### FFmpeg Not Found
If you get an error about FFmpeg not being found:
1. Make sure FFmpeg is installed
2. Check that FFmpeg is in your system PATH
2. On Windows, you may need to restart your command prompt after installing FFmpeg

### Permission Errors
If you get permission errors:
- Make sure you have write permissions to the output directory
- Try running with administrator/sudo privileges if necessary

### Large Files
For very large audio files, the conversion may take some time. The script will show progress information.

## Technical Details

The script uses FFmpeg's `color` filter to generate a solid color video that matches the duration of the input audio file. The video is then combined with the original audio to create the final MP4 file.

**FFmpeg command used:**
```bash
ffmpeg -f lavfi -i "color=c=black:size=1920x1080:duration=120" -i input.m4a -c:v libx264 -c:a aac -shortest output.mp4
```

This creates a high-quality MP4 file that YouTube will accept for upload.

