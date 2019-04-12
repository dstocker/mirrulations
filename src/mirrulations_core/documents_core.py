import re


def get_doc_attributes(document_id):
    """
    Get the organization(s), the docket_id and the document_id from a file name
    :return: orgs: The organizations(s),
             docket_id: the docket_id,
             document_id: the document_id
    """
    if '_' in document_id:
        split_name = re.split('[-_]', document_id)
        org = split_name[0] + '_' + split_name[1]
        docket_id = org + '_' + split_name[2]
        document_id = docket_id + '-' + split_name[3]
        return org, docket_id, document_id
    else:
        split_name = re.split('[-]', document_id)
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
    hyphened_string = ''
    for x in range(len(list)):
        if x == 0:
            if len(list) == 1:
                hyphened_string = list[x]
            else:
                hyphened_string = list[x] + '-'
        elif x == len(list) - 1:
            hyphened_string = hyphened_string + list[x]
        else:
            hyphened_string = hyphened_string + list[x] + '-'

    return hyphened_string


def remove_job_from_progress(redis_server, json_data):
    """
    :param redis_server:
    :param json_data:
    :return:
    """
    key = redis_server.get_keys_from_progress(json_data['job_id'])
    redis_server.remove_job_from_progress(key)
