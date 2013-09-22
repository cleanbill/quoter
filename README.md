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
3. [AngularJs](http://angularjs.org/) -> Not used...boo!
4. Hopefully use [Heroku](https://www.heroku.com/) to host for free, but means I have to get the database model right first time


TODO: Edit Screen
-----------------

1. Add a state to describe, lines (desc or not), sub lines (total or not), so when deleting text line doesn't go.
2. Do a ">" for changing state of lines
3. When totals change the grand total should change
4. Do a [JQuery Impromptu](http://trentrichardson.com/Impromptu/index.php) prompt box for client input.
5. Post JSON model directly to django
6. Have Django amend the data in the database.
7. Have a list screen to pick/delete quotes. 
