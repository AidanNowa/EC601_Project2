# EC601_Project2

### How To Run ###
Download the repository and edit the file to add in your Google API Key. Run the Middle_Meet.py file. Through the terminal, you will be prompted with two locations. Inputs can be as general as cities/counties or as specific as individual addresses. Next, you will be asked to input your interests. Input these comma-separated like: "restaurant, bar, movie theater". Your recommendations will then be printed to the terminal.

## Mission Statement ##
Middle Meet aims to facilitate connection between two people from different areas by recommending locations between the two parties. Locations are recommended based on the user's interests and locations. Middle Meet calculates the geographic midpoint between the two locations and uses those coordinates as the center point for their recommendations. 

Currently, only 2 input locations are supported and a search radius of 5km is preset for recommendations. 


## User Stories ##
I want to meet up with my friend but we live in different areas of the city. Instead of one person traveling all the way to see the other, we'd like to find a place in between but since neither of us lives there we do not have any recommendations 

I am meeting someone for the first time and don't want them to know where my apartment is. Instead, I want to meet them at a neutral location in between us and need recommendations.

My friends and I have tried all the restaurants by our apartments and want to find new ones in an area that won't force one of us to travel further than the other.

## Future Improvements Above MVP ##
In the future, I would like to add the following features:
* Website Interface (prototype HTML files included but not functional)
* Allow for user-inputted search radius
* Address validation and autocomplete through Google Maps API
* Checking for valid user inputs to interests as only certain keywords are supported by the API
