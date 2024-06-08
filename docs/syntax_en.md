# POML Syntax Overview

POML (Plain Object Markup Language) is a simple and human-readable data serialization format. It is designed to be easy to read and write, making it suitable for configuration files and data exchange.

## Basic Syntax

### Key-Value Pairs
- Basic syntax for defining key-value pairs:
  ```
  key: value
  ```

- Values can be strings, numbers, booleans, or null:
  ```
  name: John Doe
  age: 30
  married: true
  children: null
  ```

### Comments
- Use `#` for comments. Everything following `#` on the same line is a comment:
  ```
  # This is a comment
  name: John Doe  # Inline comment
  ```

## Data Types

### Strings
- Strings can be unquoted, single-quoted, or double-quoted:
  ```
  name: John Doe
  single_quote: 'Single quoted string'
  double_quote: "Double quoted string"
  ```

### Numbers
- Numbers can be integers or floating-point values:
  ```
  integer: 42
  float: 3.14
  ```

### Booleans
- Boolean values are `true` or `false`:
  ```
  is_active: true
  is_admin: false
  ```

### Null
- Null value is represented by `null`:
  ```
  value: null
  ```

## Collections

### Lists
- Lists are defined with a dash `-` followed by a space:
  ```
  fruits:
    - Apple
    - Banana
    - Cherry
  ```

- Lists can contain dictionaries:
  ```
  users:
    - name: John Doe
      age: 30
    - name: Jane Doe
      age: 28
  ```

### Dictionaries
- Dictionaries are collections of key-value pairs:
  ```
  person:
    name: John Doe
    age: 30
    address:
      street: 123 Main St
      city: Anytown
      postalCode: 12345
  ```

## Multiline Strings

### Literal Block
- Use `|` to denote a literal block where newlines are preserved:
  ```
  bio: |
    John Doe is a software engineer.
    He lives in Anytown.
  ```

### Folded Block
- Use `>` to denote a folded block where newlines are replaced by spaces:
  ```
  description: >
    John is passionate about coding
    and loves to learn new technologies.
  ```

## Anchors and Aliases

### Anchors
- Define anchors with `&` followed by the anchor name:
  ```
  address: &addr
    street: 123 Main St
    city: Anytown
    postalCode: 12345
  ```

### Aliases
- Reference anchors with `*` followed by the anchor name:
  ```
  friends:
    - name: Jane Smith
      address: *addr
    - name: Jim Brown
      address: *addr
  ```

## Tagged Values

### Date
- Use `@date` followed by a date in `YYYY-MM-DD` format:
  ```
  meeting_date: @date 2023-12-01
  ```

### Datetime
- Use `@datetime` followed by a datetime in `YYYY-MM-DDTHH:MM:SS` format:
  ```
  meeting_time: @datetime 2023-12-01T10:00:00
  ```

### Command Output
- Use `@cmd` followed by a shell command:
  ```
  git_commit: @cmd git rev-parse HEAD
  ```

### Custom Data
- Use `@custom` followed by a JSON-like string:
  ```
  user_data: @custom {"type": "premium", "expiry": "2024-12-01"}
  ```

## Special Characters
- Strings containing special characters should be quoted:
  ```
  special_chars: "Special characters: \"quotes\", \\slashes\\, and more."
  ```

## Summary
POML is a flexible and easy-to-read format suitable for various applications, including configuration files and data exchange. Its syntax includes support for basic data types, collections, multiline strings, anchors and aliases, and tagged values, making it a versatile choice for developers.