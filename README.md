# class-files-hosting
Website files hosting for students.

## Introduce
Class files hosting is web application, which allows students to store their files from lessons as images or documents like pdf files.

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
