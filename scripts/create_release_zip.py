import os
import zipfile

zip_path = r"C:\c\git\densha-de-go-yamanote-english\Densha_de_GO_English_Patch_v1.0.zip"
src_folder = r"C:\c\git\densha-de-go-yamanote-english\atmosphere"

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, r"C:\c\git\densha-de-go-yamanote-english")
            z.write(full_path, rel_path)

print(f"Created release zip: {zip_path}, Size: {os.path.getsize(zip_path)} bytes")
