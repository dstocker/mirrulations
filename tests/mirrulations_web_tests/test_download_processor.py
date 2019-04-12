import os
import zipfile
import mirrulations_web.download_processor as dp

REGULATIONS_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '../test_files/regulations-data/')
CMS_PATH = 'CMS/CMS-2019-0006/CMS-2019-0006-10896'


def test_download_zip():
    path = dp.download_zip('CMS-2019-0006-10896', REGULATIONS_PATH)
    archive = zipfile.ZipFile(path, 'r')
    readme_file = bytes.decode(archive.read('README.md'))
    assert readme_file == 'This is a README file for CMS-2019-0006-10896'
    assert os.path.exists(path)
    os.remove(path)
