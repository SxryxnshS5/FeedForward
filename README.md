# FeedForward

_FeedForward is a food sharing website with the aim to reduce food waste and fight hunger._
_The goal is hoped to be achieved through the main functionality of creating and collecting food adverts._

_Created by Team 14._
_Members: Alex Lines, Emmanouel Constantinou, Rebecca Picken, Suryansh Singh, Toby Dook, Tariq Bagaar_

_Repository URL: https://github.com/newcastleuniversity-computing/CSC2033_Team14_23-24_

**Main Functionality:**
- The user can create an account using their personal details
- The user can log in to their account, provided that they have created one.
- Adverts can be created by each user, containing details about their contents, expiry date and location.
- Users can only delete their own adverts if they wish.
- All the available adverts are presented in a list form, so that users can view and collect whichever they wish.
- The available adverts are also listed on a map, with a drop pin indicating each one.
- Users can message advertisers if questions regarding the adverts arise.
- Users can view their account details and personal information in the account page.
- Admins can view all the collected adverts as well as all the active users.
- Admins can also delete any advert or any user they wish.
- Admins can view all deleted adverts, whether it was deleted by them or their creator.
- New admin accounts can only be created by current admins.


## Running the program

### Dependencies:
All the dependencies can be installed using the **requirements.txt** file.
  
### Database:      
The device running the program should be hosting a mySQL server. mySQL should be downloaded and installed on the 
device and the server should be running constantly. ( For more information: https://dev.mysql.com/doc/refman/8.4/en/installing.html)

An .env file is required for the database to be created. The reason it is not contained in the files of this project is 
because it should contain the user and password of the mySQL host, the values of which are different on each device.
To create the file, double-click on the project directory and select New -> File and name it '.env'. Then add the following
contents, replacing the 'user' and 'password' placeholders with the appropriate mySQL server username and password.
        
        SECRET_KEY = a3f0b27e5d8c49e7bf6a38d9c4e216dc
        SQLALCHEMY_DATABASE_URI = mysql+mysqlconnector://user:password@localhost:3306/2033foodsharing
        SQLALCHEMY_ECHO = True
        SQLALCHEMY_TRACK_MODIFICATIONS = False

The database must be built using the Python Console and the following commands:

        from app import db
        from models import init_db
        init_db()

If the above commands are executed successfully, the database will be built and should contain one user with the 'admin' role.

If the above steps are followed successfully, the program can be executed by running the Flask Server (using PyCharm, 
edit configurations -> Add new run configuration -> Flask Server -> Debug Mode ON -> Apply).

## Website Guide

The interface of the website is considered to be straight-forward and clear to use. However, if there is any uncertainty
or issue on how to use the website, this guide can be helpful.

### Account Related Actions
1. **Sign Up**

    To create a new account on the website, follow these steps:
    
          1. Navigate to the Sign-Up Page (can be done by clicking on the 'Sign Up' button at the top of the website)
          2. Fill Out the Form:
          3. Enter your email, first name, last name, password, date of birth, address, and phone number.
          4. When finished, click the 'Submit' button at the bottom of the form.
    
    If the sign-up is successful, you will be redirected to the **Login** page.

2. **Log In**

    To access your account, you need to log in:

       1. Navigate to the Login Page (can be done by clicking on the 'Login' button at the top of the website)
       2. Enter your registered email and password.
       3. Click the 'Log In' button.
    
    If the login is successful, you will be redirected to the **Account** page.

3. **Account Page (Account Information)**

    To view you account details, you need to be logged in.

        1. Click on the 'Account' button at the top of the website.

    The **Account** page provides all the personal information you signed up with, as well as all the adverts you have created
    and collected.

4. **Change Account Details**

   To update your account information:

        1. Navigate to the Account Page (#3)
        2. Click on the 'Change Details' button underneath the Personal Information table.
        3. You will be redirected to a Change Details Form.
        4. You need to fill out the whole form, including the modified and unmodified details.
        5. Click the 'Submit' button.

   Your account details will be updated, and you will be redirected the **Account** page.

5. **Log Out**

    To log out of your account:
    
        1. Click the 'Logout' button at the top of the screen
    
    You will be logged out, and you will be redirected to the **Login** page, along with a message confirming that you have been logged out.

6. **Delete Account**

    If you wish to delete your account:
    
        1. Navigate to the Account Page (#3)
        2. Click on the 'Delete Account' button.
        3. You will be asked if you wish to delete your account, in which you will have the options to click 'Yes' or 'No'.
        4. Click 'OK' to delete you account.
        5. Your account will be deactivated.
        6. You will be logged out and redirected to the main page with a message confirming that your account has been deleted.

### Advert Related Actions

7. **Create an advert**

    To create an advert follow these steps:
    
        1. Navigate to the Create Advert page by clicking the 'Create Advert' button at the navigation bar.
        2. Fill out the advert form with the appropriate details
        3. For the exact location of the advert, use the map to drop a pin on where it is located
        4. Click on the 'Submit' button once finished

    The advert will be created, and you will be redirected to the **Advert Details** page, where the details of it will be displayed.

8. **Listed Adverts**
    
    To view the available adverts:

        1. Click on the 'Listed Adverts' button at the top of the website.
    
    You will be directed to the **Listed Adverts** page, where all the available adverts are displayed

9. **Advert Details**
    
    To view the details of an advert:

        1. Find the advert you want the details for, by going to the Listed Adverts page (#8)
        2. Click on the id of the advert.
   
    You will be directed to the **Advert Details** page, where the information regarding the specific advert will be displayed.

10. **Delete an advert**

    To delete an advert:

        1. Navigate to the Advert Details page. You can do so in two ways: either by navigating to your Account page (#3), 
        finding the advert you wish to delete in the "Advert Donation History" table, and clicking on its id, or by navigating
        to the Listed Adverts page (#8), finding the advert and clicking its id.
        2. Click the 'Delete' button at the bottom of the page.
        3. You will be asked if you wish to delete the advert, click 'OK'
   
    The advert will be deleted, and you will be redirected to the **Account** page.

11. **Collect an advert**

    To collect an advert:

        1. Navigate to the Listed Adverts page (#8)
        2. Find the advert you want to collect and click on its id.
        3. You will be redirected to the Advert Details page, where its details can be displayed
        4. Click on the 'Collect' button

    A confirmation of your collection will be displayed.
    Keep in mind you can collect adverts created by other users and not yourself.

12. **Advert Map**

    You can view a map containing all the adverts, represented by a drop pin.
    To view the map:

        1. Navigate to the Advert Map page by clicking on the 'Advert Map' button on the navigation bar.
    
    The drop pins are clickable, so if you wish to see the details of any advert, just click on the pin and then the adverts name.

13. **Messages**

    You can message the creator of an advert, if the information provided is insufficient, and you wish to know more.
    You can do so by:

        1. Assuming you are at the Advert Details page (#9), scroll down and click on the 'Message Advertiser' button
        2. You will be directed to the message page with the recipient being the creator of the specific advertiser.
        3. Fill in the message bar.
        4. Click the 'Submit' button.

    Your message will be sent to the advertiser, and you can respond to them in the same way when you get an answer from them.
    You can view all your messages by clicking on the **Messages** button, on the navigation bar at the top of the website.
    Be aware that if you have no messages, the **Messages** page will be empty.

### Admin Related Actions

14. **Log in (Admin)**

    To log in to an admin account, you can use the same steps as a user would **(#2)**.
    When you successfully log in, you will be redirected to the **Admin Account** page.

15. **Admin Account Page (Account and Website Information)**
    
    To view account information, you can follow the same steps as a user would **(#3)**.
    When you are successfully to the **Account Page**, your personal information will be displayed at the beginning of the website.
    Underneath the personal information, you will find Website information. 
    These include:

        1. Advert Collection History - History of every collected advert
        2. Current Adverts - All available adverts
        3. Deleted Adverts - All deleted adverts, by users or other admins.
        4. Users - All active users and their main details. (for all details for a specific user refer to #)
        5. Admins - All active admins and their main details. (for all details for a specific admin refer to #)
    
16. **Change Account Details (Admin)**

    To change account details, you can use the same steps as a user would **(#4)**
    When you successfully change your details, you will be redirected to the **Admin Account page**.

17. **Create new Admin**

    To create a new admin account:

        1. Navigate to Admin Account page (#15).
        2. Click on the 'Add New Admin' button at the bottom of the page.
        3. You will be redirected to an Admin Sign up page, where you need to fill the form with the details of the new admin.
        4. Click submit once the form is filled.
    
    If you successfully created a new admin account, you will be redirected to the **Admin Account** page, where you can see the new admin
    in the **Admins** table.

18. **User Details**

    To see all the details of a specific user:

        1. Navigate to the Admin Account page (#15).
        2. Find the 'Users' table, and search for the specific user.
        3. Click on their id.

    You will be redirected to the **Account Overview** page, where you can see their personal information, the adverts they have created
    and their orders (collected adverts).

19. **Delete a User**

    To delete a user:

        1. Navigate to the Account Overview page (#18).
        2. Click on the 'Delete User' button.
        3. A confirmation message will appear asking you if you are sure youwish to delete the account.
        4. Click 'OK'.

    You will be redirected to the **Admin Account** page with a confirmation message saying the account was successfully deleted.

20. **Advert Details (Admin)**

    You can view listed adverts **(#8)** and their specific details **(#9)** in the same way a user would.
    As an admin, you can also view listed, collected and deleted adverts through the **Admin Account** page **(#15)**
    Through the **Admin Account** page, you can view specific details of any advert by:

        1. Finding the specific advert you want details about in any of the advert tables (Advert Collection History, 
        Current Adverts, Deleted Adverts).
        2. Click on its id.

    You will be redirected to the **Advert Details** page, containing the information of the specific advert.

21. **Delete an advert**

    To delete any advert created by any user:

        1. Navigate to the Advert Details page of the advert you wish to delete (#20).
        2. click the 'Delete' button at the bottom of the page.
        3. A confirmation message will ask you if you are sure you want to delete the avdert.
        4. Clcik 'OK'.

    You will be redirected to the **Admin Account** page, where you can see the deleted advert in the **Deleted Adverts** table.

22. **Delete Admin Account**

    To delete an admin account:

        1. Navigate to the Admin Account Page (#15).
        2. Click on the 'Delete Account' button.
        3. You will be asked if you are sure you want to delete the account.
        4. Click 'OK'

    Your account will be deleted, you will be logged out, and you will be redirected to the main page.

    

 