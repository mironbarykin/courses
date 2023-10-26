# Short Description
My project allows users to listen to and create podcasts and episodes for them. Add to the queue, like and leave comments on episodes. Subscribe to podcasts. Use the search. View podcasts and episodes information as Image, Description, Name, Comments and Author. Authors are also able to check likes and subscribers of episode or podcast which they created.
# How to run
1. Clone or Download (and unzip) the repository on your local machine.
2. Navigate in the repository folder and run the following commands to make and apply migrations ``` python manage.py makemigrations podcaster``` ```python manage.py migrate```
## Dependencies
My project uses only two libraries (Which are probably already pre-installed): Django and Datetime.
# Distinctiveness and Complexity
I belive that my project utterly satisfies the distinctiveness and complexity requirements which *CS50’s Web Programming with Python and JavaScript* final project requires. Because my project is sufficiently distinct from all other projects in the course as well is not a social network and not a e-commerce site. My application uses Django (with four models) on the back-end and JavaScript on the front-end. The application is mobile-responsive.
My applications using media/audio files, which uploaded by user and represented to other users with an audio player, which have not been done in this course before. As well as loader animation on JavaScript and CSS.
# File Structure
```
Capstone
│   db.sqlite3
│   manage.py
│   README.md           (The file containing all required information about the project.)
│
└───capstone
│   │   asgi.py
│   │   settings.py     (The django generated file containing settings for the project. Media and Static roots added.)
│   │   urls.py         (The django generated file containing all urls paths for the project. Podcaster app urls included as well as MEDIA and STATIC urls.)
│   │   wsgi.py
│
└───media               (The directory containing all user-uploaded files.)
│   │
│   └───episodes        (The directory especially containing all episodes audio files uploaded by the users or by django admin panel.)
│
└───podcaster           (The application directory.)
    │   admin.py        (The django generated file containing admin panel settings. User, Podcast, Episode and comment models registered.)
    │   apps.py         
    │   models.py       (The django generated file containing all models. User, Podcast, Episode and Comment models created and described.)
    │   tests.py
    │   urls.py         (The django generated file containing all url paths for this exact application. Paths for Index, Login, Logout, Register, Create, Episode, Podcast, Queue and Subscriptions pages created.)
    │   views.py        (The django generated file containing all view functions to response on URL requests. Functions for Index, Login, Logout, Register, Create, Episode, Podcast, Queue and Subscriptions pages created)
    │
    └───migrations      (The django generated directory containing all migrations.)
    │   │
    │
    └───services        (The directory containing required (actions, posting and search) services.)
    │   │   actions.py  (The file containing one 'action' function which make provided action on Episode or Podcast wich id also provided as an arguent. The user making the request is also should be provided as an argument. Returns None.)
    │   │   posting.py  (The file containing three functions for posting episodes, podcasts and comments. 'posting_episode' function posting the episode with providing request as an argument if successfull returns None. 'posting_podcast' function posting the podcast with providing request as an argument if succesfull returns None. 'posting_comment' function posting the comment with providing request and episode id as an arguments if successful returns None.)
    │   │   search.py   (The file containing one 'process' function which applies special search process with provided question as an argument. After getting all suitable episodes and podcasts, which names contains requested question. Whether amount of all suitable episodes and podcast are more than one the 'index' and all suitable podcasts and episodes are returned or if only one suitable podcast or episode founded the episode or podcast page with id returned.)
    │
    └───static          (The directory containing all static files as pictures, styles and js scripts.)
    │   │   script.js   (The file containing event listener for window is fully loaded. When completed hide the loader and removing it from the html body.)
    │   │   style.css   (The file containging styles for loader, and its animation, body-content, form-group, sticky-top and episode-like-count.)
    │   │   plus.png                (The plus picture.)
    │   │   tick.png                (The tick picture.)
    │   │   like_inactive.png       (The black heart picture.)
    │   │   like_active.png         (The read heart picture.)
    │   
    └───templates       (The directory containing all html templates files.)
        │
        └───podcaster   (The directory containing all html files for this specific application.)
        │   _episode.html           (The file containing html for episode page. Including: episode name, episode podcast and date, as well as form for comment placement and viewing, description, image and player, actions like adding to queue and like, for author also number of likes.)
        │   _podcast.html           (The file containing html for podcast page. Including: podcast name, episodes of the podcast, date when podcast was founded and name of the author of this podcast, as well as description, image and subscribe action, for author also number of subscribers.)
        │   _queue.html             (The file containing html for queue page. Including: all quened episodes with episodes' podcast, date, description and button to visit the page.)
        │   _subscriptions.html     (The file containing html for subscriptions page. Including: all subscribed podcasts with podcasts' author, date, description and button to visit the page.)
        │   login.html              (The file containing html for login page. Including: for for the login and link for registration. The form have username and password fields.)
        │   layout.html             (The file containing html for all pages as layout. Including: navigation block (as sticky-top) with linkg to Home(Index) page, Log-Out, Queue, Subscriptions and Create for logged in users and log-in for others. As well as search field for all of them.)
        │   index.html              (The file containing html for main (index) page. Including: all or specific podcasts and episodes with podcasts' author, date, description and button to visit the page for podcast and episodes' podcast, date, description and button to visit the page for episodes.)
        │   register.html           (The file containing html for registration page. Including: form for registration with username, email, password and password confirmation, age and country fields and link to the Log-In page.)
        │   create.html             (The file containing html for create page. Including two forms for episode (when user also created a podcast) or podcast (when user not author of a podcast) posting. The podcast for have a Name, Description and Image fields. The episode form have a Name, Description, Image and Audio fields. )
```
# Models of the Project
**User**

Model of a user contains: 
* username
* password
* email
* age
* country

Model of users is related to:
*    podcasts ('author' PODCAST)
*    subscriptions ('subscribers' PODCAST)
*    queue ('queuned_users' EPISODE)
*    liked_on ('liked_by' EPISODE)
*    comments ('author' COMMENT)

Model of user have functions:
*    is_author respond with 'True' when user has podcasts and 'False' when hasn't    


**Podcast**

Model of a podcast contains: 
*    name (of this podcast)
*    description (of this podcast) 
*    image (url of podcast's image) 
*    date (when podcast was created)
*    author (who was created this podcast)
*    subscribers (who subscribed on this podcast)

Model of podcast is related to:
*    episodes ('podcast' EPISODE)


**Episode**

Model of an episode contains: 
*    podcast (in which episode was published) 
*    name (of this episode)
*    description (of this episode) 
*    image (url of episode's image) 
*    audio (file of episode)
*    timetags (might be none, tage like "00:00 TAG_DESCRIPTION")
*    date (when episode was published)
*    liked_by (who liked this episode)
*    queuned_users (who is put this episode to queue)

Model of an episode is related to:
*    comments ('episode' COMMENT)


**Comment**

Model of a comment contains: 
*    author (of the comment)
*    episode (where comment was published)
*    date (when comment was published)
*    content (what is the comment content)
