# Project proposal

It can be very challenging to find African stores or African restaurants when one is not in an African country. Researchers have submitted that finding African food or African restaurants in the United States can be a challenge for visitors, emigrants, and general lovers of African food and culture.

My website is a database-driven website off an external API. The goal of my website is to bridge the gap between African stores/restaurants and their customers by providing the closest location of these services to the Users of my website.

The demography of the users of my website are people who are interested in African cuisines and African items. My website will be designed to accommodate anybody interested in maintaining a connection to their roots by shopping for African items in African stores or by eating cuisines that are African.

I plan on using data from the Yelp Fusion API to get information about the stores and restaurants.

My data schema design will have a users, businesses, and favorites table. The relationship between the users and businesses tables will be a many-to-many relationship. The favorites table will be the join table that will create the many-to-many relationships.
My users' table will store the first name, last name, email address, and password of a user. The password will be hashed using bycrpt to make sure that the user’s password is never compromised. My businesses table will store the yelp API id of a store/restaurant.

The user flow of my website will be a User inputting name of the store/restaurant and location. A page of stores/restaurants that match is returned to them, they can select a particular store, get the address of the store, and a google map that can take them to the store’s address is shown to them. Users can also add stores/restaurants to their favorites and retrieve them whenever they want.

The features that make my website CRUD, is the ability to add a particular store/restaurant to the database, view stores/restaurants, and delete stores/restaurants. Users can also edit their information on the website.

## API

The link to my API [yelp](https://www.yelp.com/developers/documentation/v3/get_started)

![This is an image](/static/images/database-ddl.png)
