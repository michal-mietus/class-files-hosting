# class-files-hosting
Website files hosting for students.

[Page Link](http://iel4.herokuapp.com/)

## Introduce
This project was created to store all necessary files for school lessons.
Application is connected with Dropbox API and allow users to store there their files. 
Also it groups them depending on file type, for example images or pdf files.

### Features
* user login and registration system
* uploading files to the Dropbox hosting
* sorting files into sections, for example school subject
* sorting files depending on their extension

### Technologies
* Python 3.6.7
* Django 2.1.7
* Psycopg2 2.7.7
* Dropbox 9.3.0

### Launch

Clone repository
```
$ git clone https://github.com/michal-mietus/class-files-hosting.git
$ cd class-files-hosting/
```

Create PostgreSQL database.

Change DATABASES variable in `class_files_site/settings.py file`.

You have also to create [dropbox account](https://www.dropbox.com/).

Then in Dropbox create app and put inside `class_files/api_token.py`variable `TOKEN` with your app Token as string.

Now you can run your hosting application.
