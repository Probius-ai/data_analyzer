import os
import shutil
from PIL import Image

# Helper to print directory tree
def print_tree(root, prefix=""):
    files = os.listdir(root)
    files.sort()
    for i, file in enumerate(files):
        path = os.path.join(root, file)
        is_last = i == len(files) - 1
        print(prefix + ("└── " if is_last else "├── ") + file)
        if os.path.isdir(path):
            print_tree(path, prefix + ("    " if is_last else "│   "))

def list_images(root):
    image_files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                image_files.append(os.path.join(dirpath, f))
    return image_files

def copy_images(image_paths, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    for img in image_paths:
        shutil.copy(img, dest_dir)
    print(f"Copied {len(image_paths)} images to {dest_dir}")

# 이미지 데이터셋 구조를 트리 형태로 출력하는 함수
def print_dataset_structure(root_dir, indent=0):
    for item in os.listdir(root_dir):
        path = os.path.join(root_dir, item)
        print('    ' * indent + '|-- ' + item)
        if os.path.isdir(path):
            print_dataset_structure(path, indent + 1)

# 사용자가 복사할 이미지를 선택하고 복사하는 함수
def copy_selected_images(src_dir, dst_dir, selected_files):
    os.makedirs(dst_dir, exist_ok=True)
    for file_rel_path in selected_files:
        src_path = os.path.join(src_dir, file_rel_path)
        dst_path = os.path.join(dst_dir, os.path.basename(file_rel_path))
        shutil.copy2(src_path, dst_path)
        print(f"Copied: {src_path} -> {dst_path}")

# 메인 실행 함수
def main():
    print("이미지 데이터셋 구조를 탐색할 폴더 경로를 입력하세요:")
    root_dir = input().strip()
    if not os.path.isdir(root_dir):
        print("유효한 폴더 경로가 아닙니다.")
        return
    print("\n[데이터셋 폴더 구조]")
    print_dataset_structure(root_dir)

    print("\n복사할 이미지의 상대 경로를 쉼표(,)로 구분하여 입력하세요:")
    selected = input().strip()
    selected_files = [s.strip() for s in selected.split(',') if s.strip()]
    if not selected_files:
        print("선택된 파일이 없습니다.")
        return
    print("복사할 대상 폴더 경로를 입력하세요:")
    dst_dir = input().strip()
    copy_selected_images(root_dir, dst_dir, selected_files)
    print("\n작업이 완료되었습니다.")

if __name__ == "__main__":
    main()
