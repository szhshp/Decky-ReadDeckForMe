#!/bin/bash
# Define the project name and output directory
projectname="decky-rifm"
output_dir="out"
temp_dir="${projectname}" 

# Ensure the script is run from the root of the project, not from the /scripts directory
set -e

# Clean up previous build
rm -rf out
rm -rf tmp

# Run the build process
pnpm run build

# Create necessary directories
mkdir -p $output_dir/{dist,bin}

# Copy built files
cp -r dist/* $output_dir/dist
cp -r bin/* $output_dir/bin

# Copy essential files
cp plugin.json $output_dir/
cp main.py $output_dir/ 2>/dev/null || :
cp README.md $output_dir/ 2>/dev/null || :
cp LICENSE $output_dir/ 2>/dev/null || cp LICENSE.md $output_dir/ 2>/dev/null || :

# Create a temporary directory with the project name
mkdir -p $temp_dir

# Move the contents of the output directory to the temporary directory
mv $output_dir/* $temp_dir/

# Create a zip file of the temporary directory
zip -r "${projectname}.zip" $temp_dir

# Move the zip file to the output directory
mv "${projectname}.zip" $output_dir/

# Clean up the temporary directory
rm -rf $temp_dir