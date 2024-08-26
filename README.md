<div align="center">
<a href="http://melissadeleon.com" target="_blank" class="text-decoration: none;">
  <img src="./mybank/static/mybank/images/logo.png" width="100" height="100" alt="MyBank logo" style="vertical-align: middle;"><h1 style="display: inline; font-size: 70px; color: #198754; margin-left: 10px; vertical-align: middle;">MyBank
</h1>
</a>
</div>
<br>
<h3 align="center">
<strong>MyBank:</strong> Redefining the Future of Banking</h3>
<h3 align="center">LIVE. FUTURE. NOW.</h3>
<h3 align="center">MyBank is an innovative online banking platform designed to merge the reliability of traditional banking with cutting-edge technology. The goal is to offer a scalable, user-friendly solution that transforms financial management into a modern, efficient experience.</h3>
 
<p align="center">
  <a href="https://choosealicense.com/licenses/mit/">
    <img src="https://img.shields.io/badge/License-MIT-brightgreen"/ >
  </a>
  <img src="https://img.shields.io/badge/Version-1.0.0-blue"/ >
</p>  

![mybank-heroimage](https://raw.githubusercontent.com/melissadeleonx/bank-app/main/mybankhero.png)

<p align="center">
  <a href="https://twitter.com/melissadeleonx">
    <img src="https://img.shields.io/badge/follow-%40melissadeleonx%203.5k+-1DA1F2?label=XTwitter&logo=twitter&style=for-the-badge&color=blue" alt="Melissa De Leon's Twitter"/>
  </a>
  <a href="https://www.linkedin.com/in/melissadeleonx/">
    <img src="https://img.shields.io/badge/LinkedIn-melissadeleonx-blue?style=for-the-badge&logo=linkedin" alt="Melissa De Leon's LinkedIn"/>
  </a>
</p>

<br>
<br>

## Table of Contents

1. [**MyBank Django Website - CS50W Final Project**](#mybank-django-website---cs50w-final-project)
2. [🔍 Distinctiveness and Complexity](#distinctiveness-and-complexity)
3. [📝 AGILE Workflow](#agile-workflow)
4. [✨ Features](#features)
5. [📚 Documentation](#documentation)
6. [📂 File Structure and Contents](#file-structure-and-contents)
7. [🔐 Auth and Security](#auth)
8. [📬 Postman/API Tests](#postmanapi-tests)
9. [🚀 Building and Running the Project](#building-and-running-the-project)
10. [🛠️ Contribution Guidelines](#contribution-guidelines)
11. [📋 License Information](#license-information)
12. [🔗 Links to GitHub Setup and Issues](#links-to-github-setup-and-issues)
13. [🙏 Acknowledgements](#acknowledgements)
14. [✉️ Contact Information](#contact-information)

# MyBank Django Website - CS50W Final Project

Hello World! I am Melissa De Leon and this is my CS50W Final Project **MyBank**

**MyBank** is an online banking website that aims to provide a user-friendly interface for managing accounts, tracking transactions, and handling financial operations. This is the first iteration of my project, with plans to eventually turn it into a mobile application.

By integrating core banking functionalities with advanced tech features, MyBank delivers a forward-thinking approach to managing finances. 

MyBank, simple, secure, scalable.

As a requirement for the CS50 Web Development course, I built MyBank using the Python Django framework for the backend, and implemented the frontend using JavaScript and the Bootstrap CSS framework. I also integrated basic REST APIs, with plans to enhance these functionalities in the future.

## Distinctiveness and Complexity

When I set out to build this project, my goal was to create something uniquely my own, an application that combines creativity with the rigorous demands of online banking security. MyBank might be smaller in scale compared to major commercial banking systems, but it’s designed to replicate real-world security practices and provide a robust foundation for secure online banking. I drew inspiration from the user-centric designs of popular apps like Duolingo and TikTok, as well as innovative payment systems like WeChat Pay and Alipay. With MyBank, I wanted to create a platform that is both secure and highly user-friendly, blending high standards of security with a seamless user experience.

### Distinctiveness
What sets MyBank apart from my previous projects is its focus on innovative security features. I implemented Two-Factor Authentication (2FA) using Time-based One-Time Passwords (TOTP) and integrated Google OAuth2 for enhanced security and convenience. Developing these features was not just about following best practices but also about ensuring that user accounts are protected with advanced security measures. Given that this is a banking website, protecting user finances is my top priority, and I wanted to make sure that MyBank embodies this ethos fully.

Additionally, MyBank is designed to be mobile-responsive with an emphasis on simplicity and engagement. I aimed to create an intuitive user experience that encourages frequent use and supports effective financial management. This design philosophy ensures that even while maintaining high-security standards, the platform remains accessible and enjoyable to use.

### Complexity

I wasn’t initially familiar with many of the security implementations required for my chosen project, but my curiosity and determination to learn propelled me forward. Over the course of a month, I engaged in in-depth research, countless trials and errors, and a steep learning curve. I am proud to present a minimum viable product that incorporates these advanced security features. For example, Google Oauth2 API requires knowledge of API and Google Cloud Console, I tried 3 or more packages to actuallty get its logic. Implementing 2FA and Cross-Site Scripting (XSS) protection also involved not just selecting the right libraries and packages but also configuring them properly and ensuring they work seamlessly with the rest of the application to deliver a smooth user experience.

Building MyBank was also an exercise in exceeding industry standards. I incorporated secure password hashing, email verification, and comprehensive session management, which I believe sets a high bar for security and user experience in online banking. This project pushed me to understand not just the "how" but also the "why" behind these features, deepening my appreciation for the complexities involved in creating secure digital platforms.

Through this journey, I've learned that combining technical rigor with a user-centered design is challenging but incredibly rewarding. MyBank represents not just a functional online banking application, but also a personal achievement in navigating the complexities of cybersecurity and user experience design.

### Why an online banking system?

While taking both the CS50 Web and Cybersecurity courses, I became very interested in Cybersecurity Architecture, particularly the principles of authentication, authorization, auditing and accountability, as well as Identity and Access Management (IAM). I chose to develop an online banking system to apply these concepts in a real-world scenario, where secure user authentication and scalable architecture are paramount.

MyBank is still a work in progress, but my focus has been on developing robust backend functionalities that embody the core principles of web development and cybersecurity.

## Features
### Advanced Security Measures 
I always wonder how QR codes work and I found out that Python and Django have built-in security features that can implement this so I didn't settle for basic security and utilize these features instead.
- Two-Factor Authentication (2FA): Implemented using TOTP for added security.
- Cross-Site Scripting (XSS) Protection: Ensures data integrity and user safety.
- Email Verification and OAuth2: Enhances security and user convenience.

### User Journey
MyBank’s structure focuses on simplicity and engagement, aiming to provide an intuitive user experience that encourages regular use.  To ensure a smooth and user-friendly steps, I followed Agile Methodology's user story approach:

#### Registration Process
      - Users sign up via UserRegistrationForm or Google OAuth2.
      - Email verification is required unless using Google OAuth2.
      - Completion of 2FA setup is mandatory before accessing the MyBank Dashboard.

#### Log In Process
      - Users log in via UserLogInForm or Gmail.
      - Post-login, 2FA completion is verified with TOTP. If not set up, users are prompted to configure 2FA.
      - Access to the dashboard is conditional on verification and 2FA status.

#### Deposit and Withdraw
      - Users can deposit and withdraw funds. Future enhancements will expand these functionalities.

#### Transaction History
      - Users can view detailed history of their transactions.
      - Users can filter transaction history by date or type.

#### Future Plans
      - Ongoing improvements will include additional features and enhanced security measures.
      - #TODO Error Handling and Performance Optimization
      - #TODO MVP Follow-up: 
      - Address post-MVP issues, like restricting dashboard access. 
      - Research on access code system as an alternative to email.
      - #TODO Security  Enhancements: 
      - Rate limiting to prevent brute-force attacks.
      - Add security questions (old but gold) to align with common practices in online banking.
      - HTTPS across the platform for secure data transmission.
      - Cookie compliance (GDPR etc.)
      - #TODO User Behavior and Alerts:
      - Research more on way to implement user behavior analytics to monitor and understand user interactions.
      - Set up SMS or email alerts for various activities
      - #TODO Core Functionalities:
      - Transfer functionality
      - Make Payment functionality to handle bill payments and other services.
      - Qrcode to make payments in physical stores
      - Account Overview chart
      - Budget Tracker feature
      - #TODO User Experiece:
      - Check on famous apps' marketing/user experience strategy 
      - Professional Email Template
      - Profile Management features
      - Settings and customizations
      - #TODO Tests and Debugging

I once heard that programming is like creating a recipe: the best recipes are functional, user-friendly, and engaging. With MyBank, I aim to craft an experience that is smooth, secure, and delightful.

## AGILE Workflow
Follow **MyBank** progress on the [Github Project page](https://github.com/users/melissadeleonx/projects/3), where you can view tasks in different stages: Backlog, Todo, In Progress, and Done.

## Documentation
**COMING SOON**
- The MyBank website is currently a work in progress. As development continues, comprehensive documentation will be added to provide detailed guidance on all features and functionalities.

## File Structure and Contents
Below is the structure of the project and the contents of each file:
```bash
myproject/
├── 📂mybank/                           # Main application directory
│ ├── 📂migrations/                     # Database migrations directory
│ ├── 📂static/                        # Static files (CSS, JS, images)
│ │   ├── 📂images/                    # Directory for image files
│ │   ├── 📂css/                       # Directory for CSS files
│ │   │   ├── styles.css              # Styles for the website
│ │   ├── 📂js/                        # Directory for JavaScript files
│ │       ├── color-mode.js           # JavaScript for color mode toggle
│ │       ├── morpher.js              # JavaScript for morphing animations
│ │       ├── script.js               # General-purpose JavaScript
│ │       └── scrolls.js              # JavaScript for scrolling effects
│ ├── 📂templates/                    # HTML templates directory
│ │   ├── 📂accounts/                 # Templates for account-related views
│ │   ├── 📂auth/                     # Templates for authentication views
│ │   ├── 📂base/                     # Base templates for common layout
│ │   ├── 📂components/              # Reusable HTML components
│ │   ├── 📂confirmation/            # Templates for confirmation pages
│ │   ├── 📂pages/                   # Templates for main pages
│ │   ├── 📂partials/                # Partial templates for reusable sections
│ │   ├── 📂transactions/            # Templates for transaction-related views
│ │   └── index.html                 # Landing page template
│ ├── init.py                         # Initialization file for the Django app
│ ├── admin.py                        # Admin site configurations
│ ├── apps.py                         # Application-specific configurations
│ ├── forms.py                        # Forms used in the application
│ ├── models.py                       # Database models
│ ├── serializers.py                  # Serializers for API data
│ ├── signals.py                      # Signal handlers for the application
│ ├── tests.py                        # Test cases for the application
│ ├── urls.py                         # URL routing for the application
│ ├── utils.py                        # Utility functions and helpers
│ └── views.py                        # Views and request handlers
├── 📂myproject/                      # Project-level directory
│ ├── init.py                         # Initialization file for the project
│ ├── asgi.py                         # ASGI configuration for asynchronous support
│ ├── settings.py                    # Project settings and configurations
│ ├── urls.py                         # URL routing for the entire project
│ └── wsgi.py                         # WSGI configuration for deployment
├── manage.py                         # Command-line utility for administrative tasks
├── .env                              # Environment variables
├── .gitignore                        # Specifies files to be ignored by Git
├── README.md                         # Project documentation
└── requirements.txt                  # List of project dependencies


```

## Auth and Security
Here are the libraries and tools used to improved the security of the website.

### Standard Library
- `io`: Used for in-memory binary streams.
- `base64`: Used for encoding binary data as ASCII text.

### Third-party Library
- `pyotp`: A Python library for generating and verifying one-time passwords, which is crucial for implementing Two-Factor Authentication (2FA).
- `qrcode`: Used to generate QR codes for easy scanning during 2FA setup.
- `googleapiclient`: Used for interacting with Google APIs, specifically for handling Google OAuth2 authentication.

### Django Core Imports
`settings`, `HttpResponse`, `render`, `redirect`, `get_object_or_404`: Core utilities for handling web requests and responses.
`messages`: Used to display temporary messages to users.
`send_mail`: A Django utility for sending emails.
`reverse`: Generates URLs from view names, useful for dynamic routing.
`timezone`: Provides time-zone-aware datetime objects.
`force_bytes`, `urlsafe_base64_encode`, `urlsafe_base64_decode`: Utilities for encoding and decoding data, typically used in token generation and verification.

### Django Auth Imports
`login`, `logout`, `get_user_model`: Django's built-in authentication functions for handling user sessions.
`login_required`: A decorator to enforce that a view can only be accessed by authenticated users.
`default_token_generator`: Generates tokens for one-time use, commonly used in password reset functionality.
`SetPasswordForm`: A Django form used to handle password reset logic.

### Custom Imports
`UserRegistrationForm`, `UserLoginForm`, `DepositForm`, `WithdrawalForm`, `TOTPVerificationForm`, `PasswordResetRequestForm`: Custom forms defined in your project.
`User`, `UserProfile`, `Account`, `Transaction`: Custom models representing users, profiles, bank accounts, and transactions.
`get_authorization_url`, `get_credentials_from_code`: Custom functions for handling Google OAuth2 authentication.
`verify_user_email`: A utility function for verifying user emails.

## Postman/API Tests

I used the Postman App to test APIs, ensuring they function correctly and meet the RESTful standards. Postman allows for detailed API testing, including request and response validation, status codes, and headers.

##  Building and Running the Project
🚀 To get started with MyBank, follow these steps to build and run the project locally:

1. **Clone the Repository**: or Download it
   ```bash
   git clone https://github.com/melissadeleonx/myproject.git

2. **Go to Project Directory**:
   ```bash
   cd myproject

3. **Create a Virtual Environment(see instructions depending on your Terminal Operating System)
   ```bash
   python -m venv venv

4. **Activate the Virtual Environment (see instructions depending on your Terminal Operating System)
   ```bash
   source venv/Scripts/activate

5. **Installed the Required Dependancies
   ```bash
   pip install -r requirements.txt

6. Set Up the Database
   ```bash
   python manage.py migrate

7. Create a Superuser (Admin Account):
   ```bash
   python manage.py createsuperuser

8. Run the Development server 
   ```bash
   python manage.py runserver

## Contribution Guidelines
Coming Soon

##  License Information
This project is licensed under the [MIT License](./LICENSE.md). See the `LICENSE.md` file for details.
 
##  Links to GitHub Setup and Issues
https://github.com/melissadeleonx/bank-app

https://github.com/melissadeleonx/bank-app/issues

## Acknowledgements
🙏 Thank you so much for the opportunity to learn CS50 family!

Deeply grateful to Professor David Malan, Professor Brian Yu, Harvard Online CS50 Teaching Fellows and all of the CS50 Community ❤️❤️❤️

This project includes code from the following sources:

- **colormode.js**: Adapted from Bootstrap's documentation, licensed under the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/). Original Authors: [The Bootstrap Authors](https://getbootstrap.com/)
- **morpher.js:** Adapted from Ethereum's open-source repository. Licensed under the [MIT License](https://opensource.org/licenses/MIT). Original source: [github.com/ethereum/ethereum-org-website](https://github.com/ethereum/ethereum-org-website).


## Contact Information
If you have any questions, feedback, or inquiries about **MyBank**, feel free to reach out to me through the following channels:

* 👩‍💻 Developer: **Melissa De Leon**
* 📧 Email: primavita19@gmail.com
* 🌐 Website: melissadeleon.com
* 💼 LinkedIn: Melissa De Leon
* 🐦 TwitterX: @melissadeleonx

# bank-app
cs50W Final Project - Bank Web App
