import email
import imaplib
from dataclasses import dataclass
from typing import List

from ssm import ParameterStore

imap = imaplib.IMAP4_SSL("imap.gmail.com")

@dataclass
class Email:
    id: int
    title: str
    sender: str

@dataclass
class Parameters:
    lastEmailIdRead: str
    email: str
    password: str

class EmailReader:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.parameter_store = ParameterStore()
        self.email = self.parameter_store.get_parameter(self.parameters.email)
        self.imap = self.login()
        self.latest_email_read = self.get_latest_email_read()


    def login(self) -> imaplib.IMAP4_SSL:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        password = self.parameter_store.get_parameter(self.parameters.password)
        imap.login(self.email, password)

        return imap

    @staticmethod
    def __decode_str(string: str):
        """Decode email header string."""
        decoded_header = email.header.decode_header(string)
        result = []
        for decoded_part, charset in decoded_header:
            if isinstance(decoded_part, bytes):
                if charset:
                    decoded_part = decoded_part.decode(charset)
                else:
                    decoded_part = decoded_part.decode()
            result.append(decoded_part)
        return ''.join(result)

    def read_emails(self) -> List[Email]:
        imap = self.imap
        emails = []

        emails_to_read_ids = [
            str(id_as_int).encode('ascii')
            for id_as_int
            in range(self.latest_email_read+1, self.get_latest_email_receive()+1)
        ]
        print(f"There are {len(emails_to_read_ids)} to be read...")

        for email_id in emails_to_read_ids:
            _, msg_data = imap.fetch(email_id, '(RFC822)')
            imap.store(email_id, '-FLAGS', '\\Seen') # Mark as unread

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = self.__decode_str(msg['from'].split(" <")[0])
                    read_email = Email(
                        id=email_id,
                        title= self.__decode_str(msg['subject']),
                        sender = sender,
                    )
                    print(f"Email ==> {read_email}")
                    emails.append(read_email)
        return emails

    def update_latest_email_read(self, most_recent_email_id: int):
        try:
            print("Updating parameter store ")
            self.parameter_store.update_parameter(
                self.parameters.lastEmailIdRead,
                str(most_recent_email_id)
            )
        except Exception as e:
            raise Exception(e)

    def get_latest_email_read(self) -> int:
        try:
            value = self.parameter_store.get_parameter(
                name=self.parameters.lastEmailIdRead
            )
            # The below if statement will only be executed once (first run after infra is created)
            if value == "ThisWillBeManagedByTheLambda":
                print("Bootstraping the Parameter store with ID value")
                self.update_latest_email_read(self.get_latest_email_receive())
                return self.get_latest_email_receive()
            return int(value)
        except Exception as e:
            print(e)

    def get_latest_email_receive(self) -> int:
        imap = self.imap
        imap.select('INBOX')
        _, email_ids = imap.search(None, 'ALL')
        email_ids = email_ids[0].split()

        latest_email_id = email_ids[-1]
        return int(latest_email_id.decode('ascii'))
