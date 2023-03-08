import requests
import json
import re
import csv 
import logging
import datetime


today = datetime.datetime.now().date()

auth = ('5ffcf3c5a6c441c8b2516d5e3a375595','59b2cfe4716d4752a5a2b3272faf84fd')
log_file = 'Ticket_Manager/Log_Files/Happy_Fox({}).log'.format(today)
logging.basicConfig(filename=log_file, level=logging.INFO)

#Checks if "Saatchi" is anywhere in the email
def saatchi_exception(email):
    if re.search(r"saatchi", email):
        return 'Saatchi and Saatchi Consumer RB Full Access'
    else:
        return False

#Exctracts the agency name from the user email and checks it against the 'ATL_Agency_Key' file
def agency_list(email):
    agency = re.search(r"@([\w-]*)\.", email)
    with open ("Ticket_Manager/ATL_Agency_Key.csv") as agency_list:
        reader = csv.reader(agency_list, delimiter=',')
        for row in reader:
            if agency[1].lower() == row[0]:
                return row[2]
            if saatchi_exception(email) != False:
                return saatchi_exception(email)
        return "Pub Com Consumer"

#checks if the user is in the pre-approved atl list. Returns the group they are assigned to if on the list
def pre_approved(email):
    with open ('Ticket_Manager/ATL_Pre-approved_User_List.csv') as user_list:
        reader = csv.reader(user_list, delimiter=',')
        for row in reader:
            if email.lower() == row[2].lower():
                return " On XL's with User Group {}".format(row[3])
    return "User not on Pre-approved list"

#For ATL tickets only / updates the ticket
def update_atl(tic_id, group, approval):
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/staff_pvtnote/'.format(tic_id)
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': group + " " + approval})
    ticket = requests.post(url, auth=auth,data=payload, headers=headers)
    if ticket.ok:
        logging.info("Ticket #{}: Updated with: {} {}".format(tic_id, group, approval))
        return 
    if not ticket.ok:
        logging.error("Ticket #{}: Update failed with status code: {}".format(tic_id, ticket.status_code))
        raise Exception("Update failed with status code: {}".format(ticket.status_code))

def update_stel(name, tic_id):
    con_man = ['ewa oksinska', 'ewa celjowska', 'nela ziolek', 'paulina gastol', 'klaudia lipko', 'patryk debek', 'justyna grzesiowska', 'sebastian oleksiak']
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/staff_pvtnote/'.format(tic_id)
    headers = {'Content-Type': 'application/json'}
    if name.lower() in con_man:  
        payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'Content Manager'})
    else:
        payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'General User'})
    ticket = requests.post(url, auth=auth,data=payload, headers=headers)
    if ticket.ok:
        logging.info("Ticket #{}: Updated user type".format(tic_id))
        return 
    if not ticket.ok:
        logging.error("Ticket #{}: Update failed with status code: {}".format(tic_id, ticket.status_code))
        raise Exception("Update failed with status code: {}".format(ticket.status_code))

def update_mon(email, tic_id):
    agency = re.search(r"@([\w-]*)\.", email)
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/staff_pvtnote/'.format(tic_id)
    headers = {'Content-Type': 'application/json'}
    if agency[1] == 'prodigious':
        payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'Content Manager'})
    else:
        payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'Local User'})
    ticket = requests.post(url, auth=auth,data=payload, headers=headers)
    if ticket.ok:
        logging.info("Ticket #{}: Updated User Type".format(tic_id))
        return 
    if not ticket.ok:
        logging.error("Ticket #{}: Update failed with status code: {}".format(tic_id, ticket.status_code))
        raise Exception("Update failed with status code: {}".format(ticket.status_code))

def update_nivea(email, tic_id):
    agency = re.search(r"@([\w-]*)\.", email)
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/staff_pvtnote/'.format(tic_id)
    headers = {'Content-Type': 'application/json'}
    if agency[1] == 'Beiersdorf':
         payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'Annotator'})
    else:
        payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'Viewer'})
    ticket = requests.post(url, auth=auth,data=payload, headers=headers)
    if ticket.ok:
        logging.info("Ticket #{}: Updated User Type".format(tic_id))
        return 
    if not ticket.ok:
        logging.error("Ticket #{}: Update failed with status code: {}".format(tic_id, ticket.status_code))
        raise Exception("Update failed with status code: {}".format(ticket.status_code))

def update_mond(email, tic_id):
    agency = re.search(r"@([\w-]*)\.", email)
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/staff_pvtnote/'.format(tic_id)
    headers = {'Content-Type': 'application/json'}
    if agency[1] == 'mdlz':
         payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'MDLZ/Agency'})
    else:
        payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': 'POP Studios'})
    ticket = requests.post(url, auth=auth,data=payload, headers=headers)
    if ticket.ok:
        logging.info("Ticket #{}: Updated User Type".format(tic_id))
        return 
    if not ticket.ok:
        logging.error("Ticket #{}: Update failed with status code: {}".format(tic_id, ticket.status_code))
        raise Exception("Update failed with status code: {}".format(ticket.status_code))

def up_raz(email, tic_id):
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/staff_pvtnote/'.format(tic_id)
    headers = {'Content-Type': 'application/json'}
    message = """Hi Lindsay and Ryan,

The following user has accessed Razorfish DrivePlus for the first time, if you can please confirm if approved and let us know what role to assign.

Email address: {}

If approved, please confirm how their system role should be assigned: 
 • Project Manager • Client Services • Creative • Production • BA • PQA • QA • Gen 7 • Review Only""".format(email)
    payload = json.dumps({'staff': 9, 'assignee': 9, 'status': 9, 'plaintext': message})
    ticket = requests.post(url, auth=auth,data=payload, headers=headers)
    if ticket.ok:
        logging.info("Ticket #{}: Updated Request Email Template".format(tic_id))
        return 
    if not ticket.ok:
        logging.error("Ticket #{}: Update failed with status code: {}".format(tic_id, ticket.status_code))
        raise Exception("Update failed with status code: {}".format(ticket.status_code))

def info_up(client, product, ttype, tic_id):
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/update_custom_fields/'.format(tic_id)
    headers = {'Content-Type': 'application/json'}
    if product == 183:
        func = 255
    if product == 27:
        func = 275
    payload = json.dumps({'staff': 9, 't-cf-34': client, 't-cf-10': product, 't-cf-25': 108, 't-cf-40': func, 't-cf-26': ttype})
    ticket = requests.post(url, auth=auth,data=payload, headers=headers)
    if ticket.ok:
        logging.info("Ticket #{}: Ticket Fields Updated".format(tic_id))
        return 

#checks if a user is in the contact list. returns the id of the user
def contact_checker(email):
    con_url = 'https://support.productioncloud.io/api/1.1/json/user/{}/'.format(email)
    response = requests.get(con_url, auth=auth)
    if response.ok:
        return response.json()['id']
    else:
        return False

#adds a new user to the contact list
def add_user(name, email):
    url = 'https://support.productioncloud.io/api/1.1/json/users/'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'email': email, 'name': name})
    response = requests.post(url, auth=auth, data=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        return False

#Given the subject line of the ticket, this checks the 'Ticket_Type' file for the the Site, Request Type, and Site Key
def ticket_type(subject):
    with open ('Ticket_Manager/Ticket_Type.csv') as type_list:
        reader = csv.reader(type_list, delimiter=",")
        for row in reader:
            if subject == row[0]:
                return (row[1], row[2], row[3])
        return ('0', '0', '0')

#Returns the First name, Last Name, and Email of user
def user_injest(message, product, client, tic_type):
    if product == 27:
        user_firstname = re.search(r"\* FirstName : ([\w -]*)", message)
        user_lastname = re.search(r"\* LastName : ([\w -]*)", message)
        user_email = re.search(r"\* Email : ([\w\.-]*@[\w\.-]*)", message)
        return (user_firstname[1] + " " + user_lastname[1], user_email[1])
    if product == 183 and tic_type == 110:
        user_firstname = re.search(r"FirstName:\n\n\[([\w -]*)\]", message, re.M)
        user_lastname = re.search(r"LastName:\n\n\[([\w -]*)\]", message, re.M)
        user_email = re.search(r"email:\n\n\[([\w\.-]*@[\w\.]*)\]", message, re.M)
        return (user_firstname[1] + " " + user_lastname[1], user_email[1])
    if product == 27 and tic_type == 110 and client == 161:
        user_email = re.search(r"Email:\n\n([\w\.-]*@[\w\.]*)", message, re.M)
        user_name = re.search(r"Name:\n([\w\. -]*)", message, re.M)
        return (user_name[1], user_email[1])
    else:
        return False
