import json
from pathlib import Path

def key_cleaning(raw_key: str) -> str:
    cleaned = raw_key.replace('.', '').strip().lower()
    cleaned = cleaned.replace('-', '_')
    cleaned = cleaned.replace(' ', '_')
    return cleaned

def parse_dynamic_ipconfig(filepath: Path) -> dict:
    content = filepath.read_text(encoding="utf-16").splitlines()

    file_res = {"file_name": filepath.name, "adapters": []}
    curr_adapter = {"adapter_name": ""}
    last_key = None

    for line in content:
        line_striped = line.strip()
        
        if not line_striped: 
            continue

        # Detecting adapter name by checking if the line ends with a colon and does not start with whitespace
        if not line.startswith((' ', '\t')) and line_striped.endswith(':'):
            if len(curr_adapter) > 1:
                file_res["adapters"].append(curr_adapter)

            adapter_name = line_striped[:-1].strip()
            curr_adapter = {"adapter_name": adapter_name}
            last_key = None
            continue

        # Detecting key-value pairs: looking for lines that contain a colon with spaces around it
        if curr_adapter is not None:
            # Parsing only single line key-value pairs
            if ':' in line and line[line.index(':') + 1] == ' ' and line[line.index(':') - 1] == ' ':
                key_part, val_part = line.split(':', 1)
                clean_key = key_cleaning(key_part)
                clean_val = val_part.strip()
                curr_adapter[clean_key] = clean_val
                last_key = clean_key
            # Multi-line values, it adds them to a list
            elif last_key:
                existing = curr_adapter[last_key]

                if type(existing) == str:
                    curr_adapter[last_key] = [existing, line_striped]
                else:
                    curr_adapter[last_key].append(line_striped)

    if len(curr_adapter) > 1:
        file_res["adapters"].append(curr_adapter)

    return file_res

def main():
    all_results = []

    for path in sorted(Path(".").glob("*.txt")):
        parsed_data = parse_dynamic_ipconfig(path)
        all_results.append(parsed_data)

    json_output = json.dumps(all_results, indent=2, ensure_ascii=False)
    print(json_output)

    with open("out.json", "w", encoding="utf-8") as f:
        f.write(json_output)

if __name__ == "__main__":
    main()
