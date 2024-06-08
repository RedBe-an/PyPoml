import re
import subprocess
from datetime import datetime, date
from typing import Any, Dict, List, NoReturn, Tuple, Union

class PomlParseError(Exception):
    pass

class Poml:
    def __init__(self):
        self.anchors = {}

    def parse(self, poml_string: str) -> Union[Dict[str, Any], List[Any]]:
        """Parse the provided Poml string into a Python dictionary or list."""
        self.anchors = {}
        lines = poml_string.splitlines()
        data, _ = self._parse_lines(lines)
        return data

    def _parse_lines(self, lines: List[str], indent_level: int = 0) -> Tuple[Union[Dict[str, Any], List[Any]], List[str]]:
        """
        Recursively parse lines into a Python dictionary or list.
        Handles indentation and maintains current parse context.
        """
        result: Union[Dict[str, Any], List[Any]] = {}
        current_indent = None
        current_key = None
        array_mode = False
        current_array = []
        
        while lines:
            line = lines.pop(0).rstrip()
            if not line or line.lstrip().startswith('#'):
                continue
            
            indent = len(line) - len(line.lstrip())
            if current_indent is None:
                current_indent = indent
            if indent < current_indent:
                lines.insert(0, line)
                break
            elif indent > current_indent:
                if current_key:
                    value, remaining_lines = self._parse_lines([line] + lines, indent_level + 1)
                    if array_mode:
                        current_array[-1][current_key] = value
                    else:
                        result[current_key] = value
                    lines = remaining_lines
                continue
            
            line = line.lstrip()
            
            if line.startswith('- '):
                array_mode = True
                line = line[2:]
            
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                if key.startswith('&'):
                    anchor = key[1:]
                    key = anchor
                    self.anchors[anchor] = {}
                if key.startswith('*'):
                    alias = key[1:]
                    if alias not in self.anchors:
                        raise PomlParseError(f"Undefined alias: {alias}")
                    if array_mode:
                        current_array.append(self.anchors[alias])
                    else:
                        result[key] = self.anchors[alias]
                else:
                    if value:
                        if array_mode:
                            current_array.append({key: self._parse_value(value, lines)})
                        else:
                            result[key] = self._parse_value(value, lines)
                    else:
                        current_key = key
                        if array_mode:
                            current_array.append({current_key: None})
                        else:
                            result[current_key] = None
            else:
                if array_mode:
                    current_array.append(self._parse_value(line, lines))
                else:
                    raise PomlParseError(f"Invalid line: {line}")
        
        if array_mode:
            return current_array, lines
        return result, lines

    def _parse_value(self, value: str, lines: List[str]) -> Any:
        """
        Parse a single value, converting it to the appropriate Python type.
        Handles strings, numbers, booleans, and null.
        """
        if value.startswith('|') or value.startswith('>'):
            return self._parse_multiline_string(value, lines)
        if value.startswith('@'):
            return self._parse_tagged_value(value, lines)
        if value in ("true", "false"):
            return value == "true"
        if value == "null":
            return None
        if re.match(r'^-?\d+$', value):
            return int(value)
        if re.match(r'^-?\d+\.\d+$', value):
            return float(value)
        return self._unescape_string(value.strip('"').strip("'"))

    def _parse_multiline_string(self, indicator: str, lines: List[str]) -> str:
        """
        Parse a multiline string starting with | or >.
        """
        multiline_value = []
        while lines:
            line = lines.pop(0)
            indent = len(line) - len(line.lstrip())
            if indent <= 0:
                lines.insert(0, line)
                break
            multiline_value.append(line.strip())
        if indicator == '|':
            return "\n".join(multiline_value)
        elif indicator == '>':
            return " ".join(multiline_value)

    def _parse_tagged_value(self, value: str, lines: List[str]) -> Any:
        """
        Parse a tagged value, such as date, datetime, command output, or custom data.
        """
        tag, content = value.split(' ', 1)
        if tag == '@date':
            return datetime.strptime(content, '%Y-%m-%d').date()
        elif tag == '@datetime':
            return datetime.strptime(content, '%Y-%m-%dT%H:%M:%S')
        elif tag == '@cmd':
            return self._execute_command(content)
        elif tag == '@custom':
            return self._parse_custom_data(content)
        else:
            raise PomlParseError(f"Unknown tag: {tag}")

    def _execute_command(self, command: str) -> str:
        """
        Execute a command and return its output.
        """
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise PomlParseError(f"Command failed: {command}")
        return result.stdout.strip()

    def _parse_custom_data(self, content: str) -> Any:
        """
        Parse custom data provided as a JSON-like string.
        """
        try:
            return eval(content)  # Using eval to simplify; in real usage, prefer json.loads
        except Exception as e:
            raise PomlParseError(f"Invalid custom data: {content}")

    def _unescape_string(self, value: str) -> str:
        """
        Unescape special characters in a string.
        """
        return value.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')

    def dump(self, data: Union[Dict[str, Any], List[Any]], indent: int = 0) -> str:
        """Convert a Python dictionary or list into a Poml string."""
        if isinstance(data, dict):
            return self._dump_dict(data, indent)
        if isinstance(data, list):
            return self._dump_list(data, indent)
        return str(data)

    def _dump_dict(self, data: Dict[str, Any], indent: int) -> str:
        """
        Convert a Python dictionary into a Poml string.
        Handles nested dictionaries and lists.
        """
        result = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                result.append(f"{'  ' * indent}{key}:")
                result.append(self.dump(value, indent + 1))
            else:
                result.append(f"{'  ' * indent}{key}: {self._dump_value(value)}")
        return "\n".join(result)

    def _dump_list(self, data: List[Any], indent: int) -> str:
        """
        Convert a Python list into a Poml string.
        Handles nested dictionaries and lists.
        """
        result = []
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, (dict, list)):
                        result.append(f"{'  ' * indent}- {key}:")
                        result.append(self.dump(value, indent + 2))
                    else:
                        result.append(f"{'  ' * indent}- {key}: {self._dump_value(value)}")
            else:
                result.append(f"{'  ' * indent}- {self._dump_value(item)}")
        return "\n".join(result)

    def _dump_value(self, value: Any) -> str:
        """
        Convert a Python value into a Poml-compatible string.
        Handles escaping of special characters and custom types.
        """
        if isinstance(value, str):
            if any(char in value for char in '":{}[],&*#?|-<>=!%@\\'):
                return f'"{value}"'
            return value
        if isinstance(value, datetime):
            return f"@datetime {value.isoformat()}"
        if isinstance(value, date):
            return f"@date {value.isoformat()}"
        if isinstance(value, bool):
            return "true" if value else "false"
        if value is None:
            return "null"
        if isinstance(value, dict) or isinstance(value, list):
            return self.dump(value)
        return str(value)

    def read_from_file(self, file_path: str) -> Union[Dict[str, Any], List[Any]]:
        """Read POML data from a file and parse it into a Python dictionary or list."""
        with open(file_path, 'r', encoding='utf-8') as file:
            poml_string = file.read()
        return self.parse(poml_string)

    def write_to_file(self, data: Union[Dict[str, Any], List[Any]], file_path: str) -> None:
        """Write Python dictionary or list as POML data to a file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.dump(data))

    def validate(self, data: Union[Dict[str, Any], List[Any]]) -> bool:
        """
        Validate the POML data.
        For simplicity, this method just checks if all keys are strings
        and all values are of valid types.
        """
        def is_valid(value: Any) -> bool:
            if isinstance(value, (str, int, float, bool, type(None), datetime, date)):
                return True
            if isinstance(value, list):
                return all(is_valid(item) for item in value)
            if isinstance(value, dict):
                return all(isinstance(k, str) and is_valid(v) for k, v in value.items())
            return False

        if isinstance(data, dict):
            return all(isinstance(k, str) and is_valid(v) for k, v in data.items())
        if isinstance(data, list):
            return all(is_valid(item) for item in data)
        return False

    def fill_defaults(self, data: Union[Dict[str, Any], List[Any]], defaults: Union[Dict[str, Any], List[Any]]) -> Union[Dict[str, Any], List[Any]]:
        """
        Fill missing values in the POML data with defaults.
        This method merges the provided defaults into the data.
        """
        if isinstance(data, dict) and isinstance(defaults, dict):
            for key, value in defaults.items():
                if key not in data:
                    data[key] = value
                elif isinstance(value, dict):
                    data[key] = self.fill_defaults(data.get(key, {}), value)
                elif isinstance(value, list):
                    data[key] = self.fill_defaults(data.get(key, []), value)
        elif isinstance(data, list) and isinstance(defaults, list):
            for i in range(len(defaults)):
                if i >= len(data):
                    data.append(defaults[i])
                elif isinstance(defaults[i], dict):
                    data[i] = self.fill_defaults(data[i], defaults[i])
                elif isinstance(defaults[i], list):
                    data[i] = self.fill_defaults(data[i], defaults[i])
        return data

    def merge(self, base: Union[Dict[str, Any], List[Any]], updates: Union[Dict[str, Any], List[Any]]) -> Union[Dict[str, Any], List[Any]]:
        """
        Merge two POML data structures.
        Updates the base data with values from the updates data.
        """
        if isinstance(base, dict) and isinstance(updates, dict):
            for key, value in updates.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    base[key] = self.merge(base[key], value)
                elif key in base and isinstance(base[key], list) and isinstance(value, list):
                    base[key] = self.merge(base[key], value)
                else:
                    base[key] = value
        elif isinstance(base, list) and isinstance(updates, list):
            for i in range(len(updates)):
                if i < len(base) and isinstance(base[i], dict) and isinstance(updates[i], dict):
                    base[i] = self.merge(base[i], updates[i])
                elif i < len(base) and isinstance(base[i], list) and isinstance(updates[i], list):
                    base[i] = self.merge(base[i], updates[i])
                else:
                    if i < len(base):
                        base[i] = updates[i]
                    else:
                        base.append(updates[i])
        return base
    
    def dump_to_file(self, data, filepath) -> NoReturn:
        """Dump a Python dictionary or list into a Poml file."""
        poml_string = self.dump(data)
        with open(filepath, 'w') as file:
            file.write(poml_string)

# Example usage:
poml = Poml()

poml_string = """
# Example of Poml with various features
person:
  name: John Doe
  age: 30
  married: true
  address: &addr
    street: 123 Main St
    city: Anytown
    postalCode: 12345
friends:
  - name: Jane Smith
    address: *addr
  - name: Jim Brown
    address: *addr
bio: |
  John Doe is a software engineer.
  He lives in Anytown.
description: >
  John is passionate about coding
  and loves to learn new technologies.
notes:
  - "Special characters: \"quotes\", \slashes\\, and more."
  - "Use of single quotes: 'example'"
fruits:
  - Apple
  # Comment within list
  - Banana
  - Cherry
meeting_date: @date 2023-12-01
meeting_time: @datetime 2023-12-01T10:00:00
git_commit: @cmd git rev-parse HEAD
user_data: @custom {"type": "premium", "expiry": "2024-12-01"}
"""

if __name__ == "__main__" :
    # Parse the Poml string into a Python dictionary
    parsed_data = poml.parse(poml_string)
    print("Parsed Data:")
    print(parsed_data)

    # Dump the Python dictionary back into a Poml string
    dumped_string = poml.dump(parsed_data)
    print("\nDumped Poml:")
    print(dumped_string)

    # Validate the parsed data
    is_valid = poml.validate(parsed_data)
    print("\nIs Valid:")
    print(is_valid)

    # Fill missing values with defaults
    defaults = {
        "person": {
            "age": 25,
            "address": {
                "postalCode": "00000"
            }
        },
        "fruits": ["Apple", "Banana", "Cherry", "Date"]
    }
    filled_data = poml.fill_defaults(parsed_data, defaults)
    print("\nFilled Data:")
    print(filled_data)

    # Merge with another dataset
    updates = {
        "person": {
            "name": "John Smith",
            "address": {
                "city": "Newtown"
            }
        },
        "fruits": ["Grape"]
    }
    merged_data = poml.merge(parsed_data, updates)
    print("\nMerged Data:")
    print(merged_data)
