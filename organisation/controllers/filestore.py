from pathlib import Path, PurePath
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class MediaFileStorage(FileSystemStorage):

    # This method is actually defined in Storage
    def get_full_file_path(self, organisation, name):
        return PurePath(settings.MEDIA_ROOT, str(organisation.id), name)

    # This method is actually defined in Storage
    def get_media_root_file_path(self, file_path):
        return PurePath(file_path).relative_to(PurePath(settings.MEDIA_ROOT))

    def get_directory_path(self, organisation):
        return PurePath(settings.MEDIA_ROOT, str(organisation.id))

    def move_file(self, organisation, file_path):
        file_path_parts = list(file_path.parts)
        new_path = PurePath(settings.MEDIA_ROOT, str(organisation.id), file_path_parts[-1])
        Path(file_path).rename(new_path.mkdir(parents=True, exist_ok=True))
        return new_path

    def store_file(organisation, uploaded_file):
        directory_path = PurePath(settings.MEDIA_ROOT, str(organisation.id))
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        path = PurePath(directory_path, uploaded_file.name)
        with open(path, 'wb+') as destination:
            for chunk in iter(lambda: uploaded_file.file.read(10000), b''):
                destination.write(chunk)
        return str(path.relative_to(PurePath(settings.MEDIA_ROOT)))
