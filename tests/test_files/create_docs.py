import os
import json
PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    "../test_files/mirrulations_files/Big_Archive/")

for i in range(1000):
    doc_number = '0000' + str(i)
    doc_number = doc_number[-4:]
    with open(PATH + 'doc.FMCSA-' + doc_number + '-2350-21654.json', 'w+') as outfile:
        data = {
        "allowLateComment": False,
        "attachments": [
            {
                "attachmentOrderNumber": 1,
                "fileFormats": [
                    "https://api.data.gov/regulations/v3/download?documentId=FMCSA-1997-2350-21654&attachmentNumber=1&contentType=tiff",
                    "https://api.data.gov/regulations/v3/download?documentId=FMCSA-1997-2350-21654&attachmentNumber=1&contentType=pdf"
                ],
                "postingRestriction": "No_restrictions",
                "title": "David S. Schorlemer - Comments"
            }
        ],
        "commentDueDate": "2000-12-15T23:59:59-05:00",
        "commentOnDoc": {
            "documentId": "FMCSA-1997-2350-0001",
            "documentType": "RULES",
            "title": "Advanced Notice of Proposed Rulemaking - Hours of Service of Drivers"
        },
        "openForComment": False,
        "postMarkDate": "2000-10-17T00:00:00-04:00",
        "postedDate": "2000-10-17T00:00:00-04:00",
        "receivedDate": "2000-10-17T00:00:00-04:00",
        "status": "Posted",
        "docketTitle": {
            "label": "Docket Title",
            "value": "Notice of Proposed Rulemaking (NPRM) - Hours of Service of Drivers"
        },
        "pageCount": {
            "label": "Page Count",
            "value": "1"
        },
        "docketType": {
            "label": "Docket Type",
            "value": "Rulemaking"
        },
        "documentType": {
            "label": "Document Type",
            "value": "Public Submission"
        },
        "docSubType": {
            "label": "Document SubType",
            "value": "Comment(s)"
        },
        "attachmentCount": {
            "label": "Attachment Count",
            "value": "1"
        },
        "agencyName": {
            "label": "Agency Name",
            "value": "Federal Motor Carrier Safety Administration"
        },
        "rin": {
            "label": "RIN",
            "value": "2126-AA23"
        },
        "title": {
            "label": "Document Title",
            "value": "David S. Schorlemer - Comments"
        },
        "trackingNumber": {
            "label": "Comment tracking Number",
            "value": "8034ce3b"
        },
        "docketId": {
            "label": "Docket ID",
            "value": "FMCSA-1997-2350"
        },
        "comment": {
            "label": "Comment",
            "value": "See attached file(s)"
        },
        "documentId": {
            "label": "Document ID",
            "value": "FMCSA-1997-2350-21654"
        },
        "numItemsRecieved": {
            "label": "Number of Comments Received",
            "value": "1"
        },
        "agencyAcronym": {
            "label": "Agency",
            "value": "FMCSA"
        }
        }
        json.dump(data, outfile)