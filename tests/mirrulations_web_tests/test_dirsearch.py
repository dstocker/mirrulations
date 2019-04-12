import os
from mirrulations_web import dir_search as ds

PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "../../tests/test_files/regulations-data/")


def test_search_document_in_directory_good_document():
    full_path = ds.search_for_document_in_directory("CMS-2019-0006-10896",
                                                    PATH)
    assert full_path == PATH + "CMS/CMS-2019-0006/CMS-2019-0006-10896"


def test_search_document_in_directory_good_document_special_case():
    full_path = ds.search_for_document_in_directory(
        "AHRQ_FRDOC_0001-0036", PATH)
    assert full_path == \
        PATH + "AHRQ_FRDOC/AHRQ_FRDOC_0001/AHRQ_FRDOC_0001-0036"


def test_search_document_in_directory_good_document_orgs_out_of_order():
    full_path = ds.search_for_document_in_directory(
        "USC-RULES-CV-2018-0003-1139", PATH)
    assert full_path == PATH \
        + "CV-RULES-USC/USC-RULES-CV-2018-0003/USC-RULES-CV-2018-0003-1139"


def test_search_document_in_directory_bad_document():
    full_path = ds.search_for_document_in_directory(
        "CMS-2019-0006-10898", PATH)
    assert full_path == ""


def test_search_document_in_directory_bad_document_special_case():
    full_path = ds.search_for_document_in_directory(
        "AHRQ_FRDOC_0001-0037", PATH)
    assert full_path == ""


def test_search_document_in_directory_bad_document_orgs_out_of_order():
    full_path = ds.search_for_document_in_directory(
        "USC-RULES-CV-2018-0003-1130", PATH)
    assert full_path == ""


def test_search_document_in_directory_default_parameter():
    full_path = ds.search_for_document_in_directory(
        "USC-RULES-CV-2018-0003-1130")
    assert full_path == ""
