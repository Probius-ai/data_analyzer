import os
import json
from collections import defaultdict

# 분석할 폴더와 객체명을 입력받아 segmentation 정보까지 요약

def summarize_segmentation_by_object(json_dir, object_name=None):
    """
    폴더 내 모든 json 파일에서 객체별 segmentation 정보를 요약.
    object_name이 주어지면 해당 객체만 추출.
    """
    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]
    result = defaultdict(list)
    for json_path in json_files:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            continue
        categories = data.get('categories', [])
        cat_id_to_name = {cat.get('class_id'): cat.get('class_name') for cat in categories if cat.get('class_id') is not None and cat.get('class_name')}
        for ann in data.get('annotations', []):
            cat_id = ann.get('category_id')
            class_name = cat_id_to_name.get(cat_id) or cat_id_to_name.get(str(cat_id))
            if object_name and class_name != object_name:
                continue
            seg = ann.get('segmentation')
            bbox = ann.get('bbox')
            area = ann.get('area')
            result[class_name].append({
                'json_file': os.path.basename(json_path),
                'id': ann.get('id'),
                'segmentation': seg,
                'bbox': bbox,
                'area': area
            })
    return result

if __name__ == "__main__":
    print("분석할 json 폴더 경로를 입력하세요:")
    json_dir = input().strip()
    print("관심있는 객체 이름을 입력하세요 (엔터시 전체):")
    obj_name = input().strip()
    obj_name = obj_name if obj_name else None
    summary = summarize_segmentation_by_object(json_dir, obj_name)
    for obj, items in summary.items():
        print(f"\n[객체: {obj}] 총 {len(items)}개")
        for i, item in enumerate(items[:3]):  # 예시 3개만 출력
            print(f"  {i+1}. 파일: {item['json_file']}, id: {item['id']}, bbox: {item['bbox']}, area: {item['area']}")
            print(f"     segmentation: {item['segmentation']}")
        if len(items) > 3:
            print(f"  ... (총 {len(items)}개)")
    # segmentation 정보 전체를 json으로 저장할 수도 있음
    save = input("\n결과를 json 파일로 저장할까요? (y/n): ").strip().lower()
    if save == 'y':
        save_path = os.path.join(json_dir, f"segmentation_summary_{obj_name or 'all'}.json")
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"저장 완료: {save_path}")
