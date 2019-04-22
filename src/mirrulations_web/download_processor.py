import mirrulations_web.dir_search as ds
import mirrulations_web.directory_zip as dz
import mirrulations_core.config as config

HOME_REGULATION_PATH = str(
    config.web_read_value('regulations path')) + 'regulations-data/'


def download_zip(document_id, download_path=HOME_REGULATION_PATH):
    zip_path = ds.search_for_document_in_directory(document_id, download_path)
    if zip_path != '':
        zipfile = dz.zip_directory(document_id, zip_path)
        return zipfile.filename
    else:
        return ''
