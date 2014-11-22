#GoBus

**Gobus** aims to help citiziens and tourists to enjoy local transports to reach a destination in Bari city (Puglia, Italy).
It deals with an Android application which keeps the user up, guiding him to a final destination via notifications shown on a smartwatch. 

So the user provides a destination via the application and then is continuosly warned about the next bus line and its departure time to reach the destination. 

It has been developed during an hackathon in Bari and it works with the Bari city open data, even if it could be potentially works with any city whose provides data about local transport. 
This repo collect the server side of the project, whose online [here](http://fast-fire-771.appspot.com).

##The workflow
The workflow is pretty simple:

1. Register user destination, retrieving stops nearby and lines whose will get there;
2. Use this information to extract lines and departure times whose are equale to those selected in the first step. 

##Test it out

###First step:

Make an HTTP POST call to
		
		http://fast-fire-771.appspot.com/init

passing:

1. **destination**: the final destination
2. **user_id**: an unique token to identify the request

###Second step:
Make an HTTP POST call to

		http://fast-fire-771.appspot.com/stops

passing: 

1. **latitude**: the current user latitude
2. **longitude**: the current user longitude
3. **user_id**: the user_id value provided in the first call

##Technologies

GoBus server side runs on Google Cloud Platform and use the webapp2 framework and enjoys some Google wrappers to persist data in the Google datastore.
So, it's written in Python. 
Download the GAE software if you want to test locally.

Since the server side has been implemented in few hours, please forgive any lack/bug. 

			

 