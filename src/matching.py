import re

filename = 'harmonize/landing/27-29.03.23/DCIM/DJI_202303271339_009_12deabril/DJI_20230327134300_0004_V.JPG'
pattern = r'harmonize/landing/(\d+)-(\d{2}\.\d{2}\.\d{2})/DCIM/DJI_(\d{8})(\d{4})_\d{3}_(.*)/DJI_(\d{8})(\d{6})_'#(\d+)_(.*).JPG'

match = re.match(pattern, filename)

if not match:
    # Debugging information
    print("No match found.")
    print(f"Input: {filename}")
    print("Groups:")
    for group in match.groups():
        print(group)
else:
    for group in match.groups():
        print(group)
    print("Match found!")
