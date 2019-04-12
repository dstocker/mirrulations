import os
import zipfile


def zip_directory(document_id, directory_path):
    zipfile_name = document_id + '.zip'

    if os.path.exists(directory_path):

        with zipfile.ZipFile(
                zipfile_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            root_directory = os.path.basename(directory_path)

            for directory_path, directory_names, file_names \
                    in os.walk(directory_path):
                for file_name in file_names:

                    file_path = os.path.join(directory_path, file_name)
                    parent_path = os.path.relpath(file_path, directory_path)

                    arcname = os.path.join(root_directory, parent_path)

                    # The arcname prevents the archive from
                    # writing the full path to the zipfile
                    zip_file.write(file_path, arcname)

        add_readme(zip_file.filename, document_id)

        return zip_file

    else:
        with zipfile.ZipFile(
                zipfile_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(
                'README.md', 'This file ' + document_id + ' does not exist')
        return zip_file


def add_readme(zip_file, document_id):
    with zipfile.ZipFile(zip_file, 'a', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('README.md', 'This is a README file for ' + document_id)
