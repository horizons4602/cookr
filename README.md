# cookr

Guide for setting up this project locally for development:

1) Get your own free API Keys from
 - Spoonacular (need just API key) https://spoonacular.com/food-api/docs#Search-Recipes-Complex
 - Edamam (need API key and app ID) https://developer.edamam.com/edamam-docs-recipe-api
 - Just follow the guides for getting free developer keys, they're pretty obvious to get

2) Create API keys as environment variables
  - In linux, this is just >$ export MY_ENV_VARIABLE="YOUR_KEY_HERE"
  - In windows, idk, you'll have to lookup "how to add environment variables in windows" and add the same variables as below

  Create the following environment variables:
  - EDAMAM_API_KEY
  - EDAMAM_APP_ID
  - APIKEY_SPOONACULAR

3) Run the project using the following commands (these should work on windows powershell, but idk):
  - $ flask --app cookr init-db (this isn't a part of the command, just saying that this command shouldn't be run every time, just once. It wipes the whole database you've built locally)
  - $ python3 -m venv .venv
  - $ . .venv/bin/activate
  - $ flask --app cookr run --debug
  - $ http://127.0.0.1:5000/saved (this is a link to the register account page, links to other pages might be hard to find atm since its in mid development)

4) Before making changes, checkout development and then create your own branch 'git checkout -b YOUR_BRANCH_NAME_HERE". Now feel free to add whatever it is you're working on. Only 2 rules should be followed:
- Don't push code to your branch which has errors. Anyone who pulls your branch should be able to run it.
- Don't edit code outside of your task within your branch. If you see an error somewhere else and want to fix it, commit your current changes, then create a new branch stemming off development for specifically fixing that error. The purpose of this is just to prevent merge conflicts, which can be a difficult to resolve quickly if you change a bunch of unrelated stuff in your branch.