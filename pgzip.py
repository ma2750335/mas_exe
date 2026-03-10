import os
import zipfile

def zip_directory(output_filename, exclude_dirs=None, exclude_files=None, exclude_exts=None):
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []
    if exclude_exts is None:
        exclude_exts = []

    base_dir = os.getcwd()

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # 過濾資料夾
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                # 檢查是否排除檔名
                if file in exclude_files:
                    continue
                # 檢查是否排除副檔名
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    # 排除的資料夾、檔案和副檔名
    exclude_dirs = ['__pycache__', '.git']
    exclude_files = ['readme.md']
    exclude_exts = ['.zip', '.gitignore']

    zip_directory('project.zip', exclude_dirs, exclude_files, exclude_exts)
