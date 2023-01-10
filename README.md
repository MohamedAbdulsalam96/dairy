# Dairy Management System
## _Manage entrire operations for your dairy in erpnext starting from Milk Collection, Van Routes, Fat Adjustment, even Milk Marketing and last Mile deliveries._

![image](https://erp.dexciss.com/files/dex_new_logo_black.png)(https://erp.dexciss.com)


"Dairy" is an ERPNext app to connect WhatsApp business API with ERPNext. You can send, receive and even reply to WhatsApp messages without every leaving ERPNext platform.

- Minimal configuration
- 100% open-source within ERPNext
- ✨Quick and Easy Setup ✨

## Features

- Receive WhatsApp messages form your customers directly into ERPNext.
- User Notifications function to trigger messages based on events in ERPNext doctypes.
- Reply to WhatsApp messages directly from ERPNext.
- Buy meta credits to send messages directly from ERPNext.
- Easy setup for whatsapp for business.




> WhatsApp has been a great means of communicating with your customers directly and quickly. With this integration, we aim to streamline those patchy communication between you and your customer. Their messages can be directly seen in ERPNext, so you will never miss to reply an important enquiry. Also, every communication is captured in ERPNext, so you will never loose trace of what happened. You can also use this to send automated canned messages to your prospects and your clients or promote a product or start a sale or scheme.

## Installation

Using bench, install ERPNext as mentioned on the official frappe documentation.
Once ERPNext is installed, add dsc app to your bench by running
```sh
$ bench get-app https://github.com/asoral/whatsapp-client --branch version-14
$ bench setup requirements
$ bench --site <site-name> install-app whatsapp-client
```
>Note: use the correct branch as your ERPNext installed version asks for.

## Functionality
 
* Milk Entry
![image](https://user-images.githubusercontent.com/11851156/211487262-b7f9a46a-ec3b-429f-affa-79f495408d42.png)


* Buy credits by simply clicking on the purchase credit button on whatsapp settings page and use them all up!
![image](https://github.com/asoral/Whatsapp-Client/blob/38faaef3acec51e2be9850f9f9c92a13893a1a76/wp_settings.jpg)

* Send and receive whatsapp messages in 'WhatsApp Message' doctype. Pay attention to the status as it keeps getting updated based on the webhook from meta.
![image](https://github.com/asoral/Whatsapp-Client/blob/6a60648e3b965a760c418e24ca4f24663e4d39a9/wp_msg.jpg)

* You can also create WhatsApp message Template and use them in Notifications under "WhatsApp B2C" to send automated messages. Please remember you can only use "Approved" message templates to send canned-replies.
![image](https://github.com/asoral/Whatsapp-Client/blob/6a60648e3b965a760c418e24ca4f24663e4d39a9/wp_template.jpg)

### WhatsApp message template approval process is dependent on Meta and will take sometime. It seems to take anywhere between 4 - 72 hours in our experience but may also vary.


## License
GNU/General Public License (see license.txt as being followed by ERPNext repository)
The dsc App code is licensed as GNU General Public License (v3) and the Documentation is licensed as Creative Commons (CC-BY-SA-3.0) and the copyright is owned by Dexciss Technology Pvt Ltd and Dexciss Technology LLC (Dexciss) and Contributors.

By contributing to dsc, you agree that your contributions will be licensed under its GNU General Public License (v3).

**ERPNext App, Hell Yeah!**
