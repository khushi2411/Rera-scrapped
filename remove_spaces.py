import json

def remove_spaces_from_keys(data):
    """
    Recursively remove spaces from all dictionary keys.
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Remove spaces from the key
            new_key = key.replace(" ", "")
            new_dict[new_key] = remove_spaces_from_keys(value)
        return new_dict
    elif isinstance(data, list):
        return [remove_spaces_from_keys(item) for item in data]
    else:
        return data

# Define input and output file names
input_file = "Rera-residential-new-rural.json"
output_file = "Rera-residential-new-rural1.json"

# Load the input JSON
with open(input_file, "r", encoding="utf-8") as infile:
    data = json.load(infile)

# Build new data dictionary with RegistrationNumber as the key and remove the ActionID section
new_data = {}
for orig_key, project in data.items():
    # Remove spaces from all keys in the project
    project_no_spaces = remove_spaces_from_keys(project)
    # Remove the ActionID key if present
    project_no_spaces.pop("ActionID", None)
    # Extract the RegistrationNumber from the Details section
    details = project_no_spaces.get("Details", {})
    reg_no = details.get("RegistrationNumber")
    if reg_no:
        new_data[reg_no] = project_no_spaces
    else:
        # If RegistrationNumber is missing, fall back to the original key.
        new_data[orig_key] = project_no_spaces

# Write the new JSON to the output file
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(new_data, outfile, ensure_ascii=False, indent=4)

print(f"Conversion completed. Output saved to '{output_file}'.")
