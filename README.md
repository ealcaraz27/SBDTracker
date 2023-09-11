# SBDTracker
Python Script to check the availability of the SBD Belt in the size 2XL and send an email using Google's SMTP to notify you

## Requirements
This program only works when sending emails from a Google Account (gmail)
- Beautiful Soup
`pip install beautifulsoup4`
- Requests
`pip install requests`
- smtplib
  - Configure the `config.json` file with the following:
    - `sender_email` Email address for sending (gmail)
    - `receiver_email` Email address to receive notifications
    - `app_pass` Can be generated through gmail
        - Refer to [Documentation](https://support.google.com/mail/answer/185833?hl=en)
