import json

def fix_json_format(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    json_data = "[" + ",".join([line.strip() for line in lines]) + "]"
    
    try:
        parsed_json = json.loads(json_data)
        with open(output_file, 'w') as out_file:
            json.dump(parsed_json, out_file, indent=4)
        print(f"Successfully fixed JSON and saved to {output_file}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

fix_json_format('letterboxed_solutions.json', 'fixed_solutions.json')
