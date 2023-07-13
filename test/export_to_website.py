import os
import json
import subprocess
import re

DOHERTY_THRESHOLD = 400 # ms

# ======================================================================
# return an emoji from a given string
def strToEmoji(string):
    if string == "Passed": return "✔️"
    elif string == "Failed": return "❌"
    elif string == "Skipped": return "⏭️"
    elif string == "Inconclusive": return "❔"
    else: return "❔"

# ======================================================================
# return an emoji from a given string
def durationToEmoji(duration_string, regex_pattern):
    # Extract the integer duration from the string
    match = re.match(regex_pattern, duration_string)
    
    integer_duration = 0;
    if match:
        integer_duration = int(match.group(1))
    
    if integer_duration > 0 and integer_duration < DOHERTY_THRESHOLD: return "⚡"
    elif integer_duration >= DOHERTY_THRESHOLD: return "🐌"
    else: return "❔"

# ======================================================================
# count how must performance tests are fast
def countFast(dictionary, regex_pattern):
    count = 0
    for element in dictionary['entries']:
        match = re.match(regex_pattern, element['value'])
        integer_duration = 0;
        if match:
            integer_duration = int(match.group(1))
        if integer_duration > 0 and integer_duration < DOHERTY_THRESHOLD: count += 1
    return count

# ======================================================================
# count how must performance tests are slow
def countSlow(dictionary, regex_pattern):
    count = 0
    for element in dictionary['entries']:
        match = re.match(regex_pattern, element['value'])
        integer_duration = 0;
        if match:
            integer_duration = int(match.group(1))
        if integer_duration > DOHERTY_THRESHOLD: count += 1
    return count

# ======================================================================
# return the count of test matching the result filter
def count(dictionary, myfilter):
    count = 0
    for element in dictionary['entries']:
        if element['value'] in myfilter:
            count += 1
    return count

# ======================================================================
# push to the repo
def PushToRepo():
    subprocess.run('cd C:/Users/Gif\Dropbox/rpgpowerforge/rpgforge.docs && git add . && git commit -m "maj doc" && git push', shell=True)

def getDictFromJsonFilesList(filenameList, directory):
    result_dict = {}
    for filename in filenameList:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Merge the data into the result dictionary, avoiding duplicated keys
            result_dict.update(data)
    return result_dict
    
# ======================================================================
# UpdateFunctionalTests
def UpdateFunctionalTests(dictionary):
    # Output the MD file
    md_filepath = 'C:/Users/Gif/Dropbox/rpgpowerforge/rpgforge.docs/src/functional_tests.md'

    # Open the file in write mode
    with open(md_filepath, 'w', encoding='utf-8') as file:
        # write general info
        file.write("# Functional tests\n\n")
        file.write("This section covers the **Functional tests** results of **RPG Power Forge**.\n\n")
        file.write("These tests make sure each functionnality run properly. With our specification for each feature, we can determine is a test is passed ✔️ or failed ❌.\n\n")
        file.write("*In development, tests are added regularly*\n\n")
        
        # write metadata
        file.write("## Context\n\n")
        file.write("Item|Value\n")
        file.write("---|---\n")
        for element in dictionary['entries']:
            if element['value'] not in "Passed,Failed":
                file.write(f"{element['key']}| {element['value']}\n")
        
        # write the summary of tests
        file.write("\n## Summary\n\n")
        file.write("Total Tests|Passed ✔️|Failed ❌\n")
        file.write("---|---|---\n")
        passed = count(dictionary, 'Passed')
        failed = count(dictionary, 'Failed')
        total = passed + failed
        file.write(f"{total}|{passed}|{failed}\n")
        
        # write test detail results
        file.write("\n## Details\n\n")
        file.write("Test Name|Result\n")
        file.write("---|---\n")
        for element in dictionary['entries']:
            if element['value'] in "Passed,Failed":
                testName = element['key'].replace("_Functionnal_"," : ")
                file.write(f"{testName}| {strToEmoji(element['value'])}\n")

        print("UpdateFunctionalTests : Data written to the file successfully.")

# ======================================================================
# UpdateFunctionalTests
def UpdatePerformanceTests(dictionary):
    # Output the MD file
    md_filepath = 'C:/Users/Gif/Dropbox/rpgpowerforge/rpgforge.docs/src/performance_tests.md'
    
    # local regex pattern
    regex_pattern = r'^(\d+) ms$'
    
    # Open the file in write mode
    with open(md_filepath, 'w', encoding='utf-8') as file:
        # write general info
        file.write("# Performance tests\n\n")
        file.write("This section covers the **Performance tests** results of **RPG Power Forge**.\n\n")
        file.write("These tests measure how efficient a feature is. With a given threshold (Doherty Threshold, more info [here](https://lawsofux.com/doherty-threshold/)), we can determine if the feature is fast enough ⚡ or too slow 🐌.\n\n")
        file.write("*In development, tests are added regularly*\n\n")
        
        # write metadata
        file.write("## Context\n\n")
        file.write("Item|Value\n")
        file.write("---|---\n")
        for element in dictionary['entries']:
            if not re.match(regex_pattern, element['value']):
                file.write(f"{element['key']}| {element['value']}\n")
        
        # write the summary of tests
        file.write("\n## Summary\n\n")
        file.write("Total Tests|Fast ⚡|Slow 🐌\n")
        file.write("---|---|---\n")
        fast = countFast(dictionary, regex_pattern)
        slow = countSlow(dictionary, regex_pattern)
        total = fast + slow
        file.write(f"{total}|{fast}|{slow}\n")
        
        # write test detail results
        file.write("\n## Details\n\n")
        file.write("Test Name|Duration|Result\n")
        file.write("---|---|---\n")
        for element in dictionary['entries']:
            if re.match(regex_pattern, element['value']):
                testName = element['key'].replace("_Performance_"," : ")
                file.write(f"{testName}|{element['value']}|{durationToEmoji(element['value'], regex_pattern)}\n")

        print("UpdatePerformanceTests : Data written to the file successfully.")

# ==============================================================================================
# Get a list of all filenames in the directory
resultDir = 'C:/Users/Gif/Dropbox/rpgpowerforge/test_engine/Sample_project/Assets/Project/Tests/Results'
directory  = os.listdir(resultDir)

# Split filenames into two arrays based on suffixes
functional_files = []
performance_files = []

for filename in directory:
    if filename.endswith('_Functionnal.json'):
        functional_files.append(filename)
    elif filename.endswith('_Performance.json'):
        performance_files.append(filename)

UpdateFunctionalTests(getDictFromJsonFilesList(functional_files, resultDir))
UpdatePerformanceTests(getDictFromJsonFilesList(performance_files, resultDir))
PushToRepo()

