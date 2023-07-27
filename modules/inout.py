import json

#read from
def input_json(file):
    with open(file, 'r') as openfile:
 
    # Reading from json file
        json_object = json.load(openfile)
        return json_object
        
#read to
def output_json(file, json_object):
    with open("parse.json", "w") as outfile:
        trimmed_string = json_object.strip('"\n ')

        # Removing unwanted substrings
        cleaned_string = trimmed_string.replace("\\n", "").replace("Here is the output:\n```", "").replace("```", "").replace("\\\"", "\"")

        # Using json.loads to parse the string into JSON
        clean_data = json.loads(cleaned_string)
        # Reading from json file
        json.dump(clean_data, outfile)