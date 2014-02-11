quoter
======

This quote machine will be a site that can do these stories:

1. Admin should be able to define a quote
2. The defined quote should generate a unique url
3. Only the admin should be able to manage quotes
4. Admin should be able to diable quotes, edit
5. Admin should be able to see how many times and locations the quotes where viewed from
6. A User should be able to follow a quote url to view a quote
7. A user should be able to follow a print url to view a print friendly quote


Technologies
------------

1. [Django](https://www.djangoproject.com/)
2. [Postgres](http://www.postgresql.org/) to work with [Heroku](https://www.heroku.com/), but [MongoDB](http://www.mongodb.org/) is better.
3. [AngularJs](http://angularjs.org/) -> for admin screen
4. [Heroku](https://www.heroku.com/) to host for free, but means I have to get the database model right first time


TODO: Change Screen
-----------------

1. Put watch on totals to do the grand totals
2. Post JSON model directly to django
3. Have Django amend the data in the database.
4. Have a list screen to pick/delete quotes. 
5. Put log-in framework in place