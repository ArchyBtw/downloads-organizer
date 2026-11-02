from pathlib import Path

downloads_dir = Path.home() / 'sandbox'
perevod = {
    'documents': ['txt', 'pdf'],
    'images': ['png', 'jpg'],
    'archive': ['zip', 'rar', '7z'],
    'programs': ['exe', 'bin'],
    'torrents': ['torrent']
}

skip = ['без расширения', 'скрытые файлы', 'part', 'crdownload', 'tmp']

groups = {}

for i, n in perevod.items():
    for b in n:
       groups[b] = i

def get_extension(file):
    if '.' in file:
        if file[0] == '.':
            return 'скрытые файлы'
        elif file[-1] == '.':
            return 'без расширения'
        else:
            ext = file.split('.')[-1].lower()
            return ext
    else:
        return 'без расширения'

def new_name(name, zanat):
    if name not in zanat:
        return name

    base_stem = Path(name).stem
    suffix = Path(name).suffix
    counter = 1
    
    if base_stem.endswith(')') and ' (' in base_stem:
        parts = base_stem.rsplit(' (', 1)
        if parts[1][:-1].isdigit():
            base_stem = parts[0]
            counter = int(parts[1][:-1]) + 1

    candidate = f"{base_stem} ({counter}){suffix}"
    while candidate in zanat:
        counter += 1
        candidate = f"{base_stem} ({counter}){suffix}"
        
    return candidate

files = {}
for item in downloads_dir.iterdir():
    if item.is_file():
        las = get_extension(item.name)
        if las not in skip:
           files[item.name] = las

files = dict(sorted(files.items()))

for i, n in files.items():
    print('перевод ' + i + ' в ' + groups.get(n, 'other'))

while True:
    if len(files) == 0:
        print('Переносить нечего')
        break
    vopros = input('Переводить файлы?\n[да/нет]: ')
    if vopros.lower() == 'да':
        count = 0
        for i, n in files.items():
            spisok = []
            try:
                catalog = downloads_dir / groups.get(n, 'other')
                catalog.mkdir(exist_ok=True)
                for b in catalog.iterdir():
                    spisok.append(b.name)
                print(f'{downloads_dir / i} => {catalog / new_name(i, spisok)}' )
                (downloads_dir / i).rename(catalog / new_name(i, spisok))
                count += 1
            except FileNotFoundError:
                print(f'Файл {i} не перемещен, не удалось найти.')
            except PermissionError:
                print(f'Файл {i} не перемещен, недостаточно прав')
            except OSError as error:
                print(f'Файл {i} не перемещен, ошибка: {error}')
        print(f'Успешно переведено {count} файлов!')
        break
    elif vopros.lower() == 'нет':
        print('Не переведен')
        break
    else:
        print('Пожалуйста выберите да/нет!')

