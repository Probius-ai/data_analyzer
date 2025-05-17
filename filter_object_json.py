import os
import json
import shutil

def filter_json_by_object(json_dir, object_name):
    """
    폴더 내 모든 json 파일에서 annotation 중 object_name과 일치하지 않는 객체를 제거하고,
    'only_' 접두사가 붙은 새 폴더에 저장합니다.
    원본 json 파일은 변경하지 않습니다.
    """
    output_dir = os.path.join(os.path.dirname(json_dir), f"only_{os.path.basename(json_dir)}")
    os.makedirs(output_dir, exist_ok=True)
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    for fname in json_files:
        src_path = os.path.join(json_dir, fname)
        with open(src_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            # 비정상 json은 그대로 복사
            shutil.copy2(src_path, os.path.join(output_dir, fname))
            continue
        # category_id -> class_name 매핑
        categories = data.get('categories', [])
        cat_id_to_name = {cat.get('class_id'): cat.get('class_name') for cat in categories if cat.get('class_id') is not None and cat.get('class_name')}
        # annotation 필터링
        filtered_annotations = []
        for ann in data.get('annotations', []):
            cat_id = ann.get('category_id')
            class_name = cat_id_to_name.get(cat_id) or cat_id_to_name.get(str(cat_id))
            if class_name == object_name:
                filtered_annotations.append(ann)
        # annotation만 변경, 나머지는 그대로
        data['annotations'] = filtered_annotations
        # 저장
        with open(os.path.join(output_dir, fname), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"완료: '{output_dir}' 폴더에 '{object_name}' 객체만 남긴 json 파일이 저장되었습니다.")

if __name__ == "__main__":
    print("json 폴더 경로를 입력하세요:")
    json_dir = input().strip()
    print("남길 객체 이름을 입력하세요:")
    obj_name = input().strip()
    filter_json_by_object(json_dir, obj_name)
