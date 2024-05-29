# Testing Documentation

This document provides an overview of the testing methodologies used for the website to ensure the functionality of 
various components. During the development of the code, both black-box and white-box testing were used, the former due to 
simplicity and effectiveness while writing the code, and the latter to achieve some level of automation.


## Manual Testing

The code was tested manually quite often, especially whenever a new feature was implemented.
This approach was particularly valuable for testing the website's user interface and overall functionality from an end-user 
perspective. By simulating user interactions with the website without needing to understand its internal code, manual testing 
allowed for the validation of user flows, navigation, and feature usability. This method provided a holistic view of the website's
performance, ensuring that it met user requirements and functioned intuitively. Additionally, it assisted with early
detection of usability issues and allowed for iterative improvements to enhance the overall user experience. This is an
overview of how key parts of the system were manually tested.

### Front-End 

Manual testing was particularly helpful for testing the Graphical User Interface of the website. Since it focuses
on testing how software functions from a user's perspective, it allowed us to interact with the website just like a regular user would. 
This meant we could check if buttons, forms, and menus worked as expected without having necessarily had implemented the full features yet.
By clicking around and trying different actions, we could ensure that the website looked and behaved correctly for users, helping us catch any glitches 
or usability issues early on. The front end was also manually tested whenever adjustments to templates were made, such as adding tables or making 
them dynamic with the back end code. This approach ensured that the website provided a smooth and intuitive experience for visitors, improving overall user satisfaction.


### Back-end
Manual testing played a crucial role in ensuring the reliability and functionality of the website, especially during the implementation 
of key features facilitated by various view functions. It helped with quickly establishing whether a feature was correctly implemented or not.

### User Actions

We navigated to the signup page and attempted to register with valid and invalid input data, such as email addresses, passwords, and personal information.
We verified that appropriate error messages were displayed for invalid inputs. Similarly, we logged in using different user credentials, ensuring that the 
login process worked seamlessly and that users were redirected to their accounts upon successful authentication. We accessed the change details page to update
user information such as email addresses, names, and contact details. We tested different scenarios, including valid updates, invalid inputs, and changes made 
by both regular users and administrators. 

### Advert Actions

We accessed the create advert page to add new food donation adverts. We filled out the form with various food items, expiration dates, and addresses,
checking for proper validation and submission. Additionally, we visited the advert details page to ensure that adverts were displayed accurately,
including their descriptions and contact information. We simulated the process of collecting adverts by navigating to the collect confirmation page. 
We confirmed that users could collect adverts successfully, triggering the appropriate database updates and confirming 
the collection via the confirmation message.

### Admin Actions
We thoroughly examined the admin account overview page to ensure that it provided comprehensive details, including collected and current adverts,
current users, and deleted adverts. We verified that only admins could access this page and that the information displayed was accurate and up-to-date.
We accessed the user account overview page for different user accounts, both regular users and administrators. We confirmed 
that admins could view detailed information about individual users, including their adverts and order history. Additionally, we verified that unauthorized 
access attempts were appropriately restricted.We tested the delete user functionality by accessing the delete user page with different user accounts. 
We confirmed that only administrators could delete user accounts and that the process resulted in the user's role being changed to 'off.' We also checked 
for proper error handling in cases where the user did not exist or the admin attempted to delete their own account.

### Messages

We navigated to the messages page to check if all conversations with other users were displayed correctly. We verified that the most 
recent message for each conversation was visible and that the timestamp showed how long ago the message was sent. 
We used the message form to send messages to other users and confirmed that the messages were delivered successfully. 
We checked that the sent messages appeared in the conversation history and that they were displayed with the correct timestamp.

## Automated Testing
Automated testing plays a crucial role in our project, ensuring our software works smoothly. We focused on automating 
database testing due to the significance of it in the system. Without a functional dataabse, the system would simply not work.
This is the reason why we initially ensured that the database was fully functional to our needs, using automated tests.
Later we also tried to automate tests on some key parts of the system, related with user actions, such as advert creating 
as well as admin actions, for instance deleting a user. This is a brief overview of the approach of the automated tests.

### Database
The provided database test file includes unit tests for various database functions such as creating users, adverts, and messages. 
The tests are written using the unittest framework. In automating the testing of database operations, we initiated by preparing the 
test environment. This involved ensuring that the database was empty at the beginning of each test to prevent interference from any 
residual data that might have been left behind by failed tests. 
Each test method focused on validating a specific aspect of the database operations:
- Testing the connection to the database.
- Verifying the creation and deletion of users, adverts, messages, and collections.
- Checking the functionality to mark advertisements as unavailable when they expire.
- Testing the retrieval of available adverts, conversations, and message history.
The test cases covered various scenarios, including creating and deleting database records, handling valid and invalid data inputs,
and ensuring the correct behavior of database queries and operations. The setup method ensured that the database was properly 
initialized before each test, while the teardown method cleaned up any test data after each test, ensuring the test environment remained consistent.

### Admin

In automating the testing of admin views, the unittest and flask testing frameworks were used. We began by setting up the Flask application instance for testing,
configuring it to use an SQLite in-memory database. This setup ensured that tests could be run in isolation without affecting the production database.
Each test method focused on a specific aspect of the admin views:
- Testing access control for different user roles, including admins and regular users.
- Verifying functionality related to creating and managing admin accounts.
- Checking the behavior of the account overview page for both existing and nonexistent users.
- Ensuring that admin users can delete other users' accounts successfully.
The tests were structured to cover various scenarios, such as accessing pages without logging in, attempting actions with different user roles, 
handling valid and invalid data inputs, and managing user accounts. This approach provided comprehensive coverage of the admin views' behavior 
under different conditions. The use of setup and teardown methods ensured that the test environment was properly initialized 
before each test and cleaned up afterward, maintaining consistency and avoiding interference between tests. 

