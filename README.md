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

---

문의: [your-email@example.com]
