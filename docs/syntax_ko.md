알겠습니다. 코드 언어를 무조건 POML로 고정하겠습니다. 아래는 번역된 내용입니다.

# POML 문법 개요

POML(Plain Object Markup Language)은 간단하고 사람이 읽기 쉬운 데이터 직렬화 형식입니다. 이 형식은 읽고 쓰기 쉽도록 설계되어 구성 파일 및 데이터 교환에 적합합니다.

## 기본 문법

### 키-값 쌍
- 키-값 쌍을 정의하는 기본 문법:
  ```poml
  key: value
  ```

- 값은 문자열, 숫자, 불리언 또는 null일 수 있습니다:
  ```poml
  name: John Doe
  age: 30
  married: true
  children: null
  ```

### 주석
- `#`를 사용하여 주석을 작성합니다. 같은 줄에 `#` 뒤에 있는 모든 내용은 주석입니다:
  ```poml
  # 이것은 주석입니다
  name: John Doe  # 인라인 주석
  ```

## 데이터 타입

### 문자열
- 문자열은 따옴표 없이, 작은따옴표로, 또는 큰따옴표로 감쌀 수 있습니다:
  ```poml
  name: John Doe
  single_quote: '작은따옴표 문자열'
  double_quote: "큰따옴표 문자열"
  ```

### 숫자
- 숫자는 정수 또는 부동 소수점 값이 될 수 있습니다:
  ```poml
  integer: 42
  float: 3.14
  ```

### 불리언
- 불리언 값은 `true` 또는 `false`입니다:
  ```poml
  is_active: true
  is_admin: false
  ```

### Null
- Null 값은 `null`로 표시됩니다:
  ```poml
  value: null
  ```

## 컬렉션

### 리스트
- 리스트는 대시 `-`와 그 뒤에 오는 공백으로 정의됩니다:
  ```poml
  fruits:
    - Apple
    - Banana
    - Cherry
  ```

- 리스트는 딕셔너리를 포함할 수 있습니다:
  ```poml
  users:
    - name: John Doe
      age: 30
    - name: Jane Doe
      age: 28
  ```

### 딕셔너리
- 딕셔너리는 키-값 쌍의 컬렉션입니다:
  ```poml
  person:
    name: John Doe
    age: 30
    address:
      street: 123 Main St
      city: Anytown
      postalCode: 12345
  ```

## 여러 줄 문자열

### 리터럴 블록
- 줄 바꿈을 유지하는 리터럴 블록은 `|`로 표시합니다:
  ```poml
  bio: |
    John Doe는 소프트웨어 엔지니어입니다.
    그는 Anytown에 살고 있습니다.
  ```

### 접힌 블록
- 줄 바꿈이 공백으로 대체되는 접힌 블록은 `>`로 표시합니다:
  ```poml
  description: >
    John은 코딩에 열정을 가지고 있으며
    새로운 기술을 배우는 것을 좋아합니다.
  ```

## 앵커와 별칭

### 앵커
- `&` 다음에 앵커 이름을 써서 앵커를 정의합니다:
  ```poml
  address: &addr
    street: 123 Main St
    city: Anytown
    postalCode: 12345
  ```

### 별칭
- `*` 다음에 앵커 이름을 써서 앵커를 참조합니다:
  ```poml
  friends:
    - name: Jane Smith
      address: *addr
    - name: Jim Brown
      address: *addr
  ```

## 태그된 값

### 날짜
- `@date` 다음에 `YYYY-MM-DD` 형식의 날짜를 사용합니다:
  ```poml
  meeting_date: @date 2023-12-01
  ```

### 날짜와 시간
- `@datetime` 다음에 `YYYY-MM-DDTHH:MM:SS` 형식의 날짜와 시간을 사용합니다:
  ```poml
  meeting_time: @datetime 2023-12-01T10:00:00
  ```

### 명령어 출력
- `@cmd` 다음에 쉘 명령어를 사용합니다:
  ```poml
  git_commit: @cmd git rev-parse HEAD
  ```

### 사용자 정의 데이터
- `@custom` 다음에 JSON 유사 문자열을 사용합니다:
  ```poml
  user_data: @custom {"type": "premium", "expiry": "2024-12-01"}
  ```

## 특수 문자
- 특수 문자가 포함된 문자열은 따옴표로 감싸야 합니다:
  ```poml
  special_chars: "특수 문자: \"따옴표\", \\슬래시\\, 등등."
  ```

## 요약
POML은 다양한 응용 프로그램에 적합한 유연하고 읽기 쉬운 형식입니다. 구성 파일 및 데이터 교환을 포함한 여러 용도로 사용될 수 있으며, 기본 데이터 타입, 컬렉션, 여러 줄 문자열, 앵커와 별칭, 태그된 값 등의 문법을 지원하여 개발자에게 다재다능한 선택지를 제공합니다.