from pathlib import Path
import frappe, hashlib, json
from datetime import datetime

# Path("encodings").mkdir(exist_ok=True)
FILESPATH = Path(frappe.utils.get_bench_path()).joinpath('sites').joinpath(frappe.utils.get_site_base_path()).joinpath('public/files/ckeditor5')

@frappe.whitelist(allow_guest=True)
def get_url():
    return frappe.utils.get_url()


@frappe.whitelist(allow_guest=True)
def ckeditor_image_upload():
    try:
        files = frappe.local.request.files
        print(files, len(files))
        if len(files):
            filedata = files.getlist('upload')[0]
            # print(filedata.filename,filedata.content_type, filedata.content_length, filedata.headers)
            # save file
            filename = hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()[:15]+'-'+filedata.filename
            filenamepath = FILESPATH.joinpath(filename)
            with open(filenamepath, "wb") as binary_file:
                # Write bytes to file
                binary_file.write(filedata.read())
            frappe.local.response.http_status_code = 201
            frappe.local.response.status_code = 201
            frappe.local.response.type = "json"
            frappe.local.response.url = frappe.utils.get_url()+'/files/ckeditor5/'+filename
            frappe.local.response.uploaded = True
    except Exception as e:
        print(e)

@frappe.whitelist(allow_guest=True)
def get_doc(doctype, name):
    if not frappe.db.exists(doctype, {'name':name}):
        return {'code': 404, 'text': "Wiki not found" }
    return {'code': 201, 'data':frappe.get_doc(doctype, name)}


@frappe.whitelist(allow_guest=True)
def get_roles():
    return ['Wiki Editor'] #frappe.get_roles(frappe.session.user)


def response(message, status_code, data=None, json=None, error=None):
    """This method generates a response for an API call with appropriate data and status code.

    Args:
        message (str): Message to be shown depending upon API result. Eg: Success/Error/Forbidden/Bad Request.
        status_code (int): Status code of API response.
        data (Any, optional): Any data to be passed as response (Dict, List, etc). Defaults to None.
    """

    #if not status_code in [200, 201]:
    #    frappe.enqueue(frappe.log_error, message=message + "\n" + str(error), title="API Response Error", queue='long')


    frappe.local.response["message"] = message
    frappe.local.response["http_status_code"] = status_code
    frappe.local.response["status_code"] = status_code
    if data:
        frappe.local.response["data"] = data
    if json:
        frappe.local.response["json"] = data
    elif error:
        frappe.local.response["error"] = error
    return