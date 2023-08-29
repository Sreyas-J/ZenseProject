# Sync,Clip,Edit

**Problem Statement:**
Existing solutions lack a user-friendly platform that integrates video calling, real-time document editing, collaborative coding, and secure recordings. There is a need for an organized solution with these features that is easy-to-use.

**Project Goals:**
The project aims to develop a platform, that integrates video calling, real-time document editing, collaborative coding, and secure recordings. The aim is to empower teams, educators, and professionals to work together effectively and provide an enriched learning experience.

**Key Features:**
- Collaborate on documents, coding tasks and video calls which also has the option to record.
- Manage groups and join video calls.
- Real-time document editing with code block support and execution.
- Secure recordings for playback and reference.

**Administrative Control:**
To ensure efficient group management, the platform offers administrators the option to hold exclusive settings. This functionality fosters a focused and organized collaborative environment, enhancing overall productivity and teamwork.
## Implementation

**Frontend**
The project's frontend is developed using HTML, CSS, and JavaScript. HTML structures the content, CSS manages styling, and JS handles API calls and WebSocket communication.

**Backend**
Runs on Django, the backend handles server-side logic, database interactions, and routing.

**Video Calls and Recording**
The Agora API facilitates real-time video calls, while integration with AWS S3 enables video call recording. To ensure security, the AWS S3 bucket isn't publicly accessible. Users within a group can access recorded videos via dynamically generated AWS temporary URLs, preserving privacy. AWS interactions are managed using the Boto3 Python library.

**Live Code Editing**
Utilizing Quill JS for the text editor and WebSockets on the frontend, with Django Channels on the backend, the project enables real-time editing and code output display. Document content is stored in a Quill-compatible format in the database, which can be parsed as JSON data.

## Installation

**Clone the project**

https://github.com/Sreyas-J/ZenseProject.git

**Install required packages**

pip install -r requirements.txt

cd ZenseProject

**Database Migrations**

  python3 manage.py makemigrations

  python3 manage.py migrate 

**Start the server**

  python3 manage.py runserver
## Code Documentation

**ZenseProject**

**asgi.py:-**

This file defines the URLs and routes and specifies how to interpret them.

**settings.py:-**

In this file, settings have been edited to enable static and media folders, as well as to activate Django channels.

**urls.py:-**

The primary URLs file that defines the paths for different URL routes.

**liveEdit**

**consumers.py:-**

Manages real-time communication logic to facilitate the live editor functionality. This involves retrieving data for existing documents, updating the database, and transmitting updated content to other users. It ensures that the processed data aligns with the Quill editor's understanding, maintaining proper JSON parsing.

**models.py:-**

Defines the database tables required for the live editing feature, specifically the document model.

**routing.py:-**

Handles consumer routing, creating the route for the live editing consumer.

**urls.py:-**

Defines the URL route to view a specific document.

**views.py:-**

Facilitates interaction between the frontend and the database, encompassing the view for the live editor page.

**templates/:-**

Contains the HTML file for the live editor web page (doc.html).

**videoCall**

**models.py:-**

Creates the necessary database tables for the video calling app.

**urls.py:-**

Includes the remaining URLs for the website.

**views.py:-**

**Token:** Returns a JSONResponse with essential information to join a video call.

**record, update_record:** Interacts with room.js via JSON to update the database and communicate with the Agora API for video recording.

**get_presigned_url:** Generates a temporary URL to access videos from AWS S3, compensating for the lack of public access to the S3 bucket.

**view_recording:** Displays a certain video recording page by using the temporarily generated URL.

**view_notifications:** Displays notifications, distinguishing between seen and unseen notifications on the frontend.

**send_notification:** Creates and sends notifications to all members of a given group.

The other views are straightforward.

**templates/:-**

Contains necessary HTML files for the videoCall app.

**media/icon/**

Stores group icons uploaded by users.

**static**

**images/:-**

Contains images used on the website (e.g., microphone, video, leave icons).

**js/:-**

Includes JS files used for the website. Room.js communicates with the Agora API using Django-run endpoints. AgoraRTC_N-4.18.2.js is provided by Agora to enable video calling features.

**styles/:-**

Holds a CSS file responsible for most of the styling in room.html and lobby.html.

**.env**

This file stores environment variables for the Boto3 library and Agora API.
## Challenges
**Learning Agora API and Debugging Issues:** Integrating the Agora API for video calls and recordings posed a challenge, especially while debugging issues that arose during the implementation of the API.

**Implementing Django Channels:** Django Channels is different from conventional Django settings,this introduced a learning curve. Adapting to its asynchronous nature and understanding its intricacies demanded dedicated effort and study.

**Processing Quill Editor Data:** The real-time collaborative code editing feature utilizing the Quill editor presented a challenge in terms of processing data before sharing it with other members and saving it in the database. As Quill interprets data in a specific format, converting and ensuring compatibility between JSON and Quill's format demanded creative handling to ensure functionality.
## Future Scope

**Expanded Language Support**: Enhancement of the live editor by adding support for a wider range of programming languages. This will enable users to collaborate on coding tasks in their preferred language.

**Present Screen Option:** Implement a feature to share screens during a video call, enabling demonstrations and visual explanations.

**Integrated Chat Functionality:** Introduce a comprehensive chat feature that operates both within and outside video calls. This will facilitate real-time communication, discussion, and coordination among users.

**Group Folders:** Extend group functionality by introducing support for folders and diverse file types. This enhancement will enhance collaboration on larger-scale projects, promoting better organization and streamlined coordination.

**AI-Generated Recording Summaries:** Implement an AI-powered feature that automatically generates summaries of recorded video calls. This will enable users to quickly review key points and discussions without needing to watch the entire recording.

**Download and share:** Provide the option to download and share documents and recordings. 
