#!/bin/bash

URL_ROOT=https://young-caverns-47466.herokuapp.com

http POST $URL_ROOT/folders/ name="Operational"
http POST https://young-caverns-47466.herokuapp.com/documents/ title="My First Doc" content="here we gooooooooo" folder=1
