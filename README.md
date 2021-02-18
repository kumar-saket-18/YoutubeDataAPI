# YoutubeDataAPI
An API to fetch latest videos from YouTube for a given tag/search query

-> open terminal

-> clone this project using : git clone git@github.com:kumar-saket-18/YoutubeDataAPI.gittxt

-> sudo pip install pipenv

-> pipenv install django

-> pipenv shell

-> pip install -r requirements.txt

MySQL COnnection : 
    -> sudo mysql -u root
    -> CREATE USER 'youtube_search_project'@'%';
    -> ALTER USER ''youtube_search_project'@'%' IDENTIFIED BY 'qwerty123';   (### for security reasons user,password,db_name should always be read from env but here                                                                                we have directly put these values in settings.py which is not ideal.) 
    -> flush privileges
    -> GRANT ALL PRIVILEGES ON *.* TO 'youtube_search_project'@'%' WITH GRANT OPTION;
    -> create database my_project;

-> python manage.py migrate  (migrate all the pre-defined and our migrations)

-> python manage.py runserver

-> http://127.0.0.1:8000/     (hit this url, will redirect to youtube api showing the latest 10 youtube videos of a pre-defined search query.)
