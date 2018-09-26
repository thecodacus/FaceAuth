# FaceAuth
FaceAuth  Is a Face authentication Web demo to add face login system to your django web application.
using django, opencv.js ,dlib and tensorflow/tenserflow serving, check the [demo](http://anirbankar.ai)

# Screen Shots
Login Screen Open           |  Login Screen Recognizing
:-------------------------:|:-------------------------:
![Login Screen Open](screenshots/1.png?raw=true) |  ![Login Screen Recognizing](screenshots/2.png?raw=true)

Training Screen Open            |  Training Screen Training
:-------------------------:|:-------------------------:
![Training Screen Open](screenshots/3.png?raw=true) |  ![Training Screen Training](screenshots/4.png?raw=true)


# Prerequisites

This code is comes with a two docker repositories and will require them to deploy it.
check the docker installation [instruction](https://docs.docker.com/install/)



# Deployment
clone the repository and run the following command to start it up
```shell
$ git clone https://github.com/thecodacus/FaceAuth.git
$ cd FaceAuth
$ docker-compose -f docker-compose.yml -f docker-compose.production.yml up
```

# Authors
* **Anirban Kar** - *live work* - [anirbankar.ai](http://anirbankar.ai)

# License
Copyright 2018 Anirban Kar All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
