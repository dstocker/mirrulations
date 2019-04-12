import os.path
import re

HOME_REGULATION_PATH = '/regulations-data/'


def search_for_document_in_directory(document_id,
                                     directory_path=HOME_REGULATION_PATH):
    """
    Called by the server to check to see if
    a document exists in the directory structure
    :param document_id: the document id being searched
    :param directory_path: The directory path being searched in
    :return: Return the full path if the document exists,
             else return an empty string
    """

    organisations, dock_id, doc_id = get_doc_attributes(document_id)

    full_path = directory_path + organisations + '/' + dock_id + '/' + doc_id
    doc_json = 'doc.' + doc_id + '.json'

    if os.path.isfile(full_path + '/' + doc_json):
        return full_path
    else:
        return ''


def get_doc_attributes(document_id):
    """
    Get the organization(s), the docket_id and the document_id from a file name
    :return: orgs: The organizations(s),
             docket_id: the docket_id,
             document_id: the document_id
    """
    if "_" in document_id:
        split_name = re.split("[-_]", document_id)
        org = split_name[0] + "_" + split_name[1]
        docket_id = org + "_" + split_name[2]
        document_id = docket_id + "-" + split_name[3]
        return org, docket_id, document_id
    else:
        split_name = re.split("[-]", document_id)
        length = len(split_name)
        count = 0
        for x in range(length):
            if split_name[x].isdigit():
                break
            else:
                count += 1
        org_list = split_name[:count]
        org_list.sort()
        org = add_hyphens(org_list)
        docket_id = add_hyphens(split_name[:len(split_name) - 1])
        document_id = add_hyphens(split_name[:len(split_name)])
        return org, docket_id, document_id


def add_hyphens(list):
    """
    Adds hyphens between the list of strings passed
    :param list: the list to be hyphenated
    :return: A string of the list with hyphens in-between
    """
    hyphened_string = ""
    for x in range(len(list)):
        if x == 0:
            if len(list) == 1:
                hyphened_string = list[x]
            else:
                hyphened_string = list[x] + "-"
        elif x == len(list) - 1:
            hyphened_string = hyphened_string + list[x]
        else:
            hyphened_string = hyphened_string + list[x] + "-"

    return hyphened_string
