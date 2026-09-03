def customer_profile_key(pk):
    return f"customer_profile_key_userID:{pk}"

def technician_profile_key(pk):
    return f"technician_profile_key_userID:{pk}"

def technicianlist_key(page_no):
    return f"technician_list_key_pageNo:{page_no}"

def repairrequest_list_key(userid, page_no):
    return f"repairrequest_list_on_userid:{userid}_pageno:{page_no}"