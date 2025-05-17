import os
import json
import shutil
from collections import defaultdict

# 폴더 내 모든 JSON 파일을 분석하는 함수
def analyze_json_folder(json_dir, save_summary=True):
    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]
    if not json_files:
        print("해당 폴더에 json 파일이 없습니다.")
        return
    all_summaries = []
    for json_path in json_files:
        print(f"\n===== {os.path.basename(json_path)} =====")
        summary = analyze_json(json_path, print_result=True)
        all_summaries.append(summary)
    if save_summary:
        save_path = os.path.join(json_dir, "_analysis_summary.json")
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(all_summaries, f, ensure_ascii=False, indent=2)
        print(f"\n요약 결과가 {save_path} 에 저장되었습니다.")

# 단일 JSON 파일 분석 함수 (기존 코드)
def analyze_json(json_path, print_result=False):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 이미지 파일명
    image_info = data.get('images', [{}])[0]
    image_file = image_info.get('file_name', 'Unknown')

    # category_id -> class_name 매핑
    categories = data.get('categories', [])
    cat_id_to_name = {}
    for cat in categories:
        # Superb AI Suite 형식: class_id, class_name
        cat_id = cat.get('class_id')
        cat_name = cat.get('class_name')
        if cat_id is not None and cat_name:
            cat_id_to_name[cat_id] = cat_name

    # 객체별로 이름 모으기
    objects_by_name = defaultdict(list)
    for ann in data.get('annotations', []):
        cat_id = ann.get('category_id')
        # category_id가 int일 수도, str일 수도 있음
        class_name = cat_id_to_name.get(cat_id) or cat_id_to_name.get(str(cat_id))
        if class_name:
            objects_by_name[class_name].append(ann)
        else:
            objects_by_name['Unknown'].append(ann)

    summary = {
        "json_file": os.path.basename(json_path),
        "image_file": image_file,
        "object_counts": {name: len(objs) for name, objs in objects_by_name.items()},
        "objects": {
            name: [
                {"id": obj.get('id'), "bbox": obj.get('bbox'), "area": obj.get('area')} for obj in objs
            ] for name, objs in objects_by_name.items()
        }
    }

    if print_result:
        # 메타데이터 출력
        print(f"이미지 파일: {image_file}")
        print("객체별 포함 개수:")
        for name, objs in objects_by_name.items():
            print(f"- {name}: {len(objs)}개")
        print("\n상세 객체 정보:")
        for name, objs in objects_by_name.items():
            print(f"[{name}]")
            for obj in objs:
                print(f"  id: {obj.get('id')}, bbox: {obj.get('bbox')}, area: {obj.get('area')}")
            print()

    return summary

def summarize_folder(json_dir):
    """
    폴더 내 모든 json 파일을 요약해 객체별 개수와 파일명을 한눈에 보기 쉽게 출력
    """
    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]
    summary_by_object = defaultdict(list)
    for json_path in json_files:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(f"[경고] {os.path.basename(json_path)}: dict 타입이 아님 (list 등). 건너뜀.")
            continue
        image_info = data.get('images', [{}])[0]
        image_file = image_info.get('file_name', 'Unknown')
        categories = data.get('categories', [])
        cat_id_to_name = {cat.get('class_id'): cat.get('class_name') for cat in categories if cat.get('class_id') is not None and cat.get('class_name')}
        for ann in data.get('annotations', []):
            cat_id = ann.get('category_id')
            class_name = cat_id_to_name.get(cat_id) or cat_id_to_name.get(str(cat_id))
            if class_name:
                summary_by_object[class_name].append(os.path.basename(json_path))
            else:
                summary_by_object['Unknown'].append(os.path.basename(json_path))
    print("\n[객체별 json 파일 개수 및 파일명]")
    for obj, files in summary_by_object.items():
        print(f"- {obj}: {len(files)}개")
        print(f"  예시: {', '.join(files[:5])}{' ...' if len(files) > 5 else ''}")
    return summary_by_object

def copy_jsons_by_object(json_dir, object_name, dest_dir):
    """
    원하는 객체이름이 포함된 json 파일을 새로운 폴더에 복사
    """
    os.makedirs(dest_dir, exist_ok=True)
    summary = summarize_folder(json_dir)
    files_to_copy = summary.get(object_name, [])
    if not files_to_copy:
        print(f"'{object_name}' 객체가 포함된 json 파일이 없습니다.")
        return
    for fname in files_to_copy:
        src = os.path.join(json_dir, fname)
        dst = os.path.join(dest_dir, fname)
        shutil.copy2(src, dst)
    print(f"총 {len(files_to_copy)}개의 json 파일이 '{dest_dir}' 폴더에 복사되었습니다.")

if __name__ == "__main__":
    print("분석/요약할 json 파일이 들어있는 폴더 경로를 입력하세요:")
    json_dir = input().strip()
    if not os.path.isdir(json_dir):
        print("유효한 폴더 경로가 아닙니다.")
    else:
        summary = summarize_folder(json_dir)
        print("\n특정 객체이름의 json 파일만 복사하려면 객체이름을 입력하세요 (엔터시 건너뜀):")
        obj_name = input().strip()
        if obj_name:
            print("복사할 대상 폴더 경로를 입력하세요:")
            dest_dir = input().strip()
            copy_jsons_by_object(json_dir, obj_name, dest_dir)
