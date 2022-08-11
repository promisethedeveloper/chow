# Project proposal

It can be very challenging to find African stores or African restaurants when one is not in an African country. Researchers have submitted that finding African food or African restaurants in the United States can be a challenge for visitors, emigrants, and general lovers of African food and culture.

My website is a database-driven website off an external API. Its goal is to bridge the gap between African stores/restaurants and their customers, by providing the closest location of these services to the Users of my website.

The demography of the users of my website are people who are interested in African cuisines and African items. My website will be designed to accommodate anybody interested in maintaining a connection to their roots by shopping for African items in African stores or by eating cuisines that are African.

I plan on using data from the Yelp Fusion API to get information about the stores and restaurants.

My data schema design will have a users, businesses, and favorites table. The relationship between the users and businesses tables will be a many-to-many relationship. The favorites table will be the join table that will create the many-to-many relationships.
My users' table will store the first name, last name, email address, and password of a user. The password will be hashed using bcrypt to make sure that the user’s password is never compromised. My businesses table will store the yelp API id of a store/restaurant.

The user flow of my website will be a User inputting name of the store/restaurant and location. A page of stores/restaurants that match the inputs is returned to them, they can select a particular store, get the address of the store, and a google map that can take them to the store’s address is shown to them. Users can also add stores/restaurants to their favorites and retrieve them whenever they want.

The features that make my website CRUD, is the ability to add a particular store/restaurant to the database, view stores/restaurants, and delete stores/restaurants. Users can also edit their information on the website.

## API

The link to my API [yelp](https://www.yelp.com/developers/documentation/v3/get_started)

![This is an image](/static/images/database-ddl.png)

## Promise-chow

[Promise-chow](https://promise-chow.herokuapp.com/) is a website that returns the locations of African stores and African restaurants to Users. It provides google maps for easy naviagation to locations of their choice. Users are able to add stores/restaurants to a list of favorites and access them at any time.

Users will have to sign up to be able to make searches on the website. After searches are made, Users can select a particular location to go to and add the location to their list of favorites if they wish. Locations added to favorites can also be removed at any time.

The technologies used for the building of the website are HTML, CSS, JavaScript, Flask, Flask-SQLAlchemy and PostgreSQL.

## Installation

1. Clone the repository
   ```
   $ git clone https://github.com/promisethedeveloper/first_capstone.git
   ```
2. Create a python virtual environment and activate it (it is a good practice but it is not required)
   ```
   $ cd first_capstone
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```
3. Install the requirements
   ```
   $ pip install -r requirements.txt
   ```
4. Run the app
   ```
   $ flask run
   ```

## Running the test

    ```
    $ python -m unittest
    ```
