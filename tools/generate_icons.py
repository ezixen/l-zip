from PIL import Image
from pathlib import Path

root = Path('d:/Dev/L-ZIP')
source = root / 'images' / 'L-ZIP-logo.png'
if not source.exists():
    raise SystemExit(f'Missing source image: {source}')

img = Image.open(source).convert('RGBA')

# Create ICO for Windows
ico_path = root / 'images' / 'L-ZIP-logo.ico'
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
img.save(ico_path, sizes=icon_sizes)

# Browser extension icons
ext_dir = root / 'browser-extension'
ext_dir.mkdir(exist_ok=True)
img.resize((128, 128), Image.LANCZOS).save(ext_dir / 'icon-128.png')
img.resize((48, 48), Image.LANCZOS).save(ext_dir / 'icon-48.png')

# VS Code extension icon
vscode_dir = root / 'vscode-extension'
vscode_dir.mkdir(exist_ok=True)
img.resize((128, 128), Image.LANCZOS).save(vscode_dir / 'icon.png')

print('Created:')
print(f'  {ico_path}')
print(f'  {ext_dir / "icon-128.png"}')
print(f'  {ext_dir / "icon-48.png"}')
print(f'  {vscode_dir / "icon.png"}')
