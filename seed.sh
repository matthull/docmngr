#!/bin/bash

URL_ROOT="https://young-caverns-47466.herokuapp.com"

http POST $URL_ROOT/folders/ name="VA Site"
http POST $URL_ROOT/folders/ name="Team 1" parent_folder=1
http POST $URL_ROOT/folders/ name="Team 2" parent_folder=1
http POST $URL_ROOT/folders/ name="Team 2 Night Shift" parent_folder=6
# Get details on all the folders for VA Site
http GET $URL_ROOT/folders/1/

http POST $URL_ROOT/folders/ name="Corporate HQ"
http POST $URL_ROOT/folders/ name="Exec Suite" parent_folder=2
http POST $URL_ROOT/folders/ name="Mail Room" parent_folder=2
http POST $URL_ROOT/folders/ name="HR" parent_folder=2
# Get details on all the folders for Corporate
http GET $URL_ROOT/folders/2/

http POST $URL_ROOT/topics/ name="Sales"
http POST $URL_ROOT/topics/ name="Technical Support"
http POST $URL_ROOT/topics/ name="Customer Service"
# List all our topics
http GET $URL_ROOT/topics/

http POST $URL_ROOT/documents/ \
  title="Work Instructions for Great Prosperity" \
  content="here we gooooooooo" \
  folder=1

http POST $URL_ROOT/documents/ \
  title="How to Sell You Butt Off" \
  content="It's a wild wild world..." \
  folder=2

http GET $URL_ROOT/folders/1/documents/
http GET $URL_ROOT/folders/2/documents/

# Put "How to sell" doc in sales topic
http POST $URL_ROOT/documents/1/topics/1/
http GET $URL_ROOT/documents/1/
