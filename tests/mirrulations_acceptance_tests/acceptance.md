To run dummy_server to have a single job on the server
and have the client get work and return data:

To run server:
'python tests/mirrulations_acceptance_tests/dummy_server.py'

To run client:
'mirrulations_client'

add api key
add localhost 0.0.0.0:8080

This should then run, terminate the server, but the client
is left running. Ideally this will be changed to have the
client close out too, but this framework can be used to help
load data into a client or server and test the communication
one or more clients and the server to find issues we are having
with the Mirrulations system.
