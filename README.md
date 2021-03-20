# CovidBOT

YET this is working repo.

Creating simple CovidBOT that wil grab for me covid statisics (infected, deaths, tests done) from Polish goverment website, store it and send it to friend's group chat.
Right now it is just working code, it needs refractoring and adding featurues. 

### Handled all of the data scrapping. It uses two pages (one is backup page). It scraps data from direct url to iframe from webpage, if that fails than it scraps the data from main webpage.
### It creates string that represents all of the data needed.

Right now I need to handle the Facebook message system. Unfortunetly Facebook doesn't provide any API for private messeaging. 
After that I want to create a database and API that will send all the data in json format.
