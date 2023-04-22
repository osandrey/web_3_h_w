from threading import Thread
import concurrent.futures
from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    # Створюємо папку для архіву
    target_folder.mkdir(exist_ok=True, parents=True)
    # Створюємо папку куди розпакуємо архів
    # Беремо суфікс у файла і удаляємо replace(filename.suffix, '')
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))

    # Створюємо папку для архіву з іменем файлу
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Це не архів {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Помилка видалення папки {folder}')

def worcker(cort):
    func, files, folder, dir, ext = cort
    if ext:
        for file in files:
            func(file, folder / dir / ext)
    else:
        for file in files:
            func(file, folder / dir)



def main(folder: Path):
    parser.scan(folder)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        thread_list = []
        result = executor.submit(worcker, (handle_media, parser.JPEG_IMAGES, folder, 'images', 'JPEG'))
        thread_list.append(result)
        thread_list.append(executor.submit(worcker, (handle_media, parser.JPG_IMAGES, folder, 'images', 'JPG')))
        thread_list.append(
            executor.submit(worcker, (handle_media, parser.PNG_IMAGES, folder, 'images', 'PNG')))
        thread_list.append(
            executor.submit(worcker, (handle_media, parser.SVG_IMAGES, folder, 'images', 'SVG')))
        thread_list.append(
            executor.submit(worcker, (handle_media, parser.MP3_AUDIO, folder, 'audio', 'MP3')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.OGG_AUDIO, folder, 'audio', 'OGG')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.WAV_AUDIO, folder, 'audio', 'WAV')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.AMR_AUDIO, folder, 'audio', 'AMR')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.DOC_DOCUMENTS, folder, 'documents', 'DOC')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.DOCX_DOCUMENTS, folder, 'documents', 'DOCX')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.TXT_DOCUMENTS, folder, 'documents', 'TXT')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.PDF_DOCUMENTS, folder, 'documents', 'PDF')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.XLSX_DOCUMENTS, folder, 'documents', 'XLSX')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.PPTX_DOCUMENTS, folder, 'documents', 'PPTX')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.AVI_VIDEO, folder, 'video', 'AVI')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.MP4_VIDEO, folder, 'video', 'MP4')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.MOV_VIDEO, folder, 'video', 'MOV')))
        thread_list.append(executor.submit(worcker, (handle_media, parser.MKV_VIDEO, folder, 'video', 'MKV')))
        thread_list.append(executor.submit(worcker, (handle_other, parser.MY_OTHER, folder, 'UFO-obj', '')))
        thread_list.append(executor.submit(worcker, (handle_archive, parser.ARCHIVES, folder, 'archives', '')))
        [el.result() for el in thread_list]

        # for el in thread_list:
        #     el.result()
    # Виконуємо реверс списку для того щоб видалити всі папки
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def path_function():
    try:
        folder = sys.argv[1]
    except IndexError:
        print('Enter valid path to the folder')
    else:
        folder_for_scan = Path(folder)
        print(f'Start in folder {folder_for_scan.resolve()}')
        argument = folder_for_scan.resolve()

        # thread = Thread(target=main, args=(argument,))
        # thread.start()
        main(folder_for_scan.resolve())


if __name__ == '__main__':
    path_function()





