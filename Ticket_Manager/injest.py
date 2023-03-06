import requests
import happyfox
from tqdm import tqdm
import datetime
import logging

today = datetime.datetime.now().date()

auth = ('5ffcf3c5a6c441c8b2516d5e3a375595','59b2cfe4716d4752a5a2b3272faf84fd')
url = 'https://support.productioncloud.io/api/1.1/json/tickets/?q=status:"New"'
json_data = requests.get(url,auth=auth).json()
ticket_count = json_data['page_info']['count']
log_file = 'Ticket_Manager/Log_Files/Happy_Fox({}).log'.format(today)
print(log_file)
open(log_file,"a+")
logging.basicConfig(filename=log_file, level=logging.INFO)

for x in tqdm(range(ticket_count)):
    subject_line = json_data['data'][x]['subject']
    ticket_id = json_data['data'][x]['id']
    ticket_message = json_data['data'][x]['first_message']
    ticket = happyfox.ticket_type(subject_line)
    tic_type = int(ticket[0])
    if tic_type == '0':
        continue
    client = int(ticket[1])
    if client =='0':
        continue
    product = int(ticket[2])
    if product == '0':
        continue
    happyfox.info_up(client, product, tic_type, ticket_id)
    if happyfox.user_injest(ticket_message, product, client, tic_type) != False:
        name,email = happyfox.user_injest(ticket_message, product, client, tic_type)
        logging.info("Ticket #{}: Assigned to {} <{}>".format(ticket_id, name, email))
        if happyfox.contact_checker(email) == False:
            happyfox.add_user(name, email)
        if product == 27 and tic_type == 110:
            if client == 158:
                agency = happyfox.agency_list(email)
                pre_app = happyfox.pre_approved(email)
                happyfox.update_atl(ticket_id, agency, pre_app)
            if client == 222:
                happyfox.update_stel(name, ticket_id)
            if client == 208:
                happyfox.update_mon(email, ticket_id)
        if product == 183 and tic_type == 110:
            if client == 197:
                happyfox.update_nivea(email, ticket_id)
            if client == 208:
                happyfox.update_mond(email, ticket_id)
            if client == 206:
                happyfox.up_raz(email, ticket_id)
    else:
        continue
