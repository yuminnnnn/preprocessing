import re
import os
from typing import List


# 1. 파일 로드 및 전처리
def load_data(filepath: str) -> List[str]:
  
    if not os.path.exists(filepath):
        print(f"오류: 파일을 찾을 수 없습니다: {filepath}")
        return []

    print(f"파일 로드 시작: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()


# 2. 반복되는 | 가 있는 행 제거
def should_skip_row(row: str) -> bool:
   
    if re.match(r'^\|[\s:-]+\|[\s:-]+\|', row.strip()):
        return False
    
    return '||' in row

def filter_data(raw_data: List[str]) -> List[str]:
    
    valid_rows = []

    print("행 필터링 (|| 포함 행 제거)")
    for row in raw_data:
        if row.strip().startswith('|') and re.match(r'^\|[\s:-]+\|[\s:-]+\|', row.strip()):
             valid_rows.append(row)
             continue
        
        if should_skip_row(row):
            print(f"제외된 행 (|| 포함): {row.strip()}")
            continue

        if should_skip_row(row):
            print(f"제외된 행: {row.strip()}")
            continue
        
        valid_rows.append(row)
        
    return valid_rows


# 숫자 포맷팅 (3자리 -> *.**, 4자리 -> **.**)
def format_number_as_decimal(match: re.Match) -> str:
    
    number_str = match.group(0)
    length = len(number_str)

    if length == 3:
        return f"{number_str[:-2]}.{number_str[-2:]}"
    elif length == 4:
        return f"{number_str[:-2]}.{number_str[-2:]}"
    else:
        return number_str

def format_cell_content(cell: str) -> str:
 
    number_pattern = r'\b\d{3,4}\b'
    
    formatted_cell = re.sub(number_pattern, format_number_as_decimal, cell)
    
    return formatted_cell

def process_data(filtered_data: List[str]) -> List[str]:
    
    processed_data = []
    print("데이터 후처리 (3,4자리 숫자 소수점 변환)")
    
    for row in filtered_data:
        if re.match(r'^\|[\s:-]+\|[\s:-]+\|', row.strip()):
            processed_data.append(row.strip())
            continue

        cells = [cell.strip() for cell in row.strip().split('|')]
        
        content_cells = [cell for cell in cells if cell]
        
        if not content_cells:
            processed_data.append(row.strip())
            continue

        formatted_cells = []
        for cell in content_cells:
            formatted_cells.append(format_cell_content(cell))
        
        processed_row = f"| {' | '.join(formatted_cells)} |"
        processed_data.append(processed_row)

    return processed_data


# 4. 메인 실행
if __name__ == "__main__":

    INPUT_FILE = "안양대_2021.md"
    
    raw_data = load_data(INPUT_FILE)
    
    if not raw_data:
        print("처리할 데이터가 없습니다. 프로그램을 종료합니다.")
    else:
        filtered_data = filter_data(raw_data)
        final_processed_data = process_data(filtered_data)
        
        print("최종 처리 결과 (클린 데이터)")
        
        for line in final_processed_data:
            print(line)

        with open('[f]안양대_2021.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(final_processed_data))
        print("\n처리된 데이터가 'output_processed_data.md' 파일로 저장되었습니다.")