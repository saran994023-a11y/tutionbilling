How to Run the Code
To run the Tuition Billing System locally, follow these steps:

1. Clone the Repository
First, clone the repository to your local machine:

  git clone <repository-url>
  cd tuition-billing-system
  
2. Install Dependencies
  Ensure you have Python and necessary packages installed.

Install Python:
  Make sure Python 3.x is installed on your machine. You can check by running:

  python --version
Install Required Python Packages: Navigate to the project directory and install the required Python dependencies by running:

pip install -r requirements.txt


3. Set Up the SQLite3 Database

Run the Migrations: To create the necessary database tables, run the following command:
For Django:
  python manage.py makemigrations
  python manage.py migrate
  
The database file will be created automatically when you run the migration commands.
Configure the SQLite Database: Ensure your project directory contains the database file (e.g., db.sqlite3). If it doesn't exist yet, it will be created upon running the migration commands.
If you need to configure any database settings, check the settings.py (if you're using Django) or similar configuration file for the correct path to the database file.
  
4. Start the Development Server
   Once the dependencies are installed and the database is set up, you can start the development server.

For Django: Run the following command to start the local server:
   python manage.py runserver

5. Access the Application
   Once the server is running, open your browser and go to http://localhost:8000 (the default port for Django). You should now see the Tuition Billing System homepage.
   
6. Click "Go to Admin panel" and follow the steps:
   
 i) Master Admin Login
      Login Credentials:
            Username: pradeep
            Password: punchbiz
  Navigate to the login page and enter the above credentials to access the Master Dashboard.
  
 ii) Add Branches
    After logging in as Master Admin, go to the "Add Branch" section in the Master Dashboard.
    Fill out the branch details:
    Branch Name: eg(Erode).
    Username and Password: eg(punchbiz).
  
 iii) Subjects:
    Hold down the Ctrl key (or Cmd on Mac) and left-click to select multiple subjects for the branch from the dropdown list.
    Click the "Add" button to create the branch.
    A confirmation message will appear if the branch is created successfully.
    Add Subjects
    Navigate to the "Add Subject" section in the Master Dashboard.
    Enter the following details:
    Subject Name: Specify the name of the subject (e.g., Mathematics, Science, etc.).
    Fee: Enter the fee amount for the subject.
    Click the "Add" button to save the subject.
    The subject will now be available for selection when creating branches or invoices.
    Tuition Center Login
    Use the branch-specific Username and Password created by the Master Admin.

  
  Navigate to the login page and enter the branch credentials to access the Tuition Center Dashboard.
  
 i) Manage Students
  Log in to the Tuition Center Dashboard.
  Go to the "Manage Students" section:
  
 ii) Add Student:
    Fill in the student details (Name, phone_number, address, etc.).
    Assign the subjects they will enroll in (select multiple using Ctrl + Left Click).
    Click "Add" to save the student details.

 iii) Edit Student:
    Select the student from the list.
    Update their details or change the assigned subjects.
    Click "Update" to save changes.
    
 iv) View Students:
    Browse the student list for details of all enrolled students.
    Generate Invoices
    Navigate to the "Billing" section in the Tuition Center Dashboard.
    Select the Student Name from the dropdown list.
    Choose the subjects to include in the invoice:
    Use Ctrl + Left Click to select multiple subjects.
    Verify the fees and applicable taxes (calculated automatically).
    Click "Generate Invoice".
    A preview of the invoice will appear.
    Click "Download PDF" to save the invoice to your device.

 V) Track Billing Status:
    Go to the "Billing Status" section in the Tuition Center Dashboard.
    View the list of students with their billing details, including:
    Invoice Number
    Total Amount
    Payment Status (Paid/Unpaid)
    Use the search or filter options to locate specific invoices.
    Edit/Remove Branches or Subjects
    
 vi) Edit Branch:
    In the Master Dashboard, go to the "Manage Branches" section.
    Select the branch to edit its details (e.g., add or remove subjects).
    Click "Update" to save changes.
    
 vii) Remove Branch:
  Select the branch from the list and click "Delete".
  
 viii) Edit/Remove Subjects:
    Navigate to the "Manage Subjects" section in the Master Dashboard.
    Edit the subject details or delete them as required.
