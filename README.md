# ECSE3038_lab4
# Aim of Lab
* This lab is designed to get students more accustomed to the technologies used in designing and implementing a RESTful API server.
# Program Description
# Requirements
*The specifications have shifted slightly from the last lab. The client's budget has recently increase and now they're able to pay for a database service. Based on research it is determined that PostgreSQL is the most suitable database platform for the project. Therefore, the client requested to modify the API server to store all `Tank` related data to be stored in the database. The `Profile` data can be handled the same way as it was originally implemented, where the profile data is saved in a variable on the server.
# Function Description
* GET /data
When this route is requested, the server should respond with an array of zero more tank objects.
* POST /data
The server should be able to handle a POST request that consumes a JSON body, validates it against schema and returns the saved document.
* PATCH /data/:id
The server should allow a user to alter the parts of one of the tanks after it has been posted. The server should allow the requester to make a JSON body with any combination of the four attributes and update them as necessary (The requester should NOT be allowed to edit the `id` attribute). The server should respond with the edited document.
* DELETE /data/:id
The server should allow the requester to delete any previously POSTed object.
# Joke
* Why don’t scientists trust atoms? Because they make up everything :)
