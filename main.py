from google_api.google_email_delete import get_label_id, search_emails, delete_emails

def main():
    """
    Step 1: specify labels
    """
    label_parent_name = 'SPAM'
    label_child_names = None
    # label_child_names = ['SOCIAL']

    label_ids = []

    parent_label_id = get_label_id(label_name=label_parent_name)
    if parent_label_id:
        label_ids.append(parent_label_id)

    if label_child_names:
        for labe_child_name in label_child_names:
            if labe_child_name:
                child_label_id = get_label_id(label_name=f'{label_parent_name}_{labe_child_name}')
                if child_label_id:
                    label_ids.append(child_label_id)

    """
    Step 2: search emails for the label
    """
    query_string = None
    # query_string = 'Subject: You got files '
    email_results = []

    # search emails by query string. use this when deleting emails by email subject.
    if query_string:
        email_results = search_emails(query_string=query_string, label_ids=None)
        
    # search emails within a label. use this when deleting emails for the label.
    if not query_string and label_ids:
        for label_id in label_ids:
            email_results = search_emails(query_string=None, label_ids=label_id)
    
    """
    Step 3: delete emails
    """
    delete_emails(email_results)
    
if __name__ == '__main__':
    main()
    