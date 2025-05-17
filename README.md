# 이미지 데이터셋 구조 탐색 및 선택 복사 도구

이 프로젝트는 사용자가 이미지 데이터셋 폴더 구조를 쉽게 파악하고, 원하는 이미지만 선택하여 복사할 수 있도록 도와주는 Python 기반 도구입니다.

## 주요 기능
- 폴더 트리 구조로 이미지 데이터셋 구조 탐색
- 이미지 파일 목록 자동 탐색
- 원하는 이미지만 선택하여 복사

## 사용 방법
1. 가상환경 활성화 (최초 1회만)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. 프로그램 실행
   ```bash
   python main.py
   ```
3. 안내에 따라 데이터셋 폴더 경로, 복사할 이미지, 복사 위치를 입력

## 필요 패키지
- Python 3.x
- Pillow

## 예시
```
이미지 데이터셋 구조를 탐색할 폴더 경로를 입력하세요:
/path/to/dataset
[데이터셋 폴더 구조]
|-- class1
|   |-- img1.jpg
|   |-- img2.jpg
|-- class2
|   |-- img3.jpg

복사할 이미지의 상대 경로를 쉼표(,)로 구분하여 입력하세요:
class1/img1.jpg, class2/img3.jpg
복사할 대상 폴더 경로를 입력하세요:
/path/to/output
작업이 완료되었습니다.
```

## 추가 도구 및 활용법

### 1. JSON 어노테이션 객체별 요약 및 복사
- `analyze_json.py`: 폴더 내 json 파일을 분석해 이미지별 객체 종류와 개수를 요약, 원하는 객체가 포함된 json만 복사 가능
- `summarize_segmentation.py`: 폴더 내 json 파일에서 객체별 segmentation, bbox, area 등 상세 정보 요약 및 저장
- `filter_object_json.py`: 폴더 내 json 파일에서 원하는 객체만 남기고 나머지 annotation을 삭제, 결과를 only_폴더에 저장(원본은 보존)

### 예시: 객체별 json 파일만 복사
```bash
python filter_object_json.py
# → json 폴더 경로 입력
# → 남길 객체 이름 입력
# → only_폴더에 결과 저장
```

### 예시: segmentation 정보 요약 및 저장
```bash
python summarize_segmentation.py
# → json 폴더 경로 입력
# → 객체 이름 입력(엔터시 전체)
# → 요약 결과 및 저장 여부 선택
```

### 예시: json 어노테이션 분석 및 요약
```bash
python analyze_json.py
# → json 폴더 경로 입력
# → 객체별 개수, 파일명 요약 및 복사 기능 제공
```

---

문의: [your-email@example.com]
