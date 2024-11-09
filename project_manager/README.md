<p align="center"><img src="static/insa/logo_insaflu_new.png" alt="INSaFLU" width="300"></p>


[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)


# INSaFLU - docker installation
INSaFLU (“INSide the FLU”) is an influenza-oriented bioinformatics free web-based platform for an effective and timely whole-genome-sequencing-based influenza laboratory surveillance.


## Installation

        docker:
        * Install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) in your linux server;
        * Install docker extensions [local-persist](https://github.com/MatchbookLab/local-persist);

			```
			$ curl -fsSL https://raw.githubusercontent.com/MatchbookLab/local-persist/master/scripts/install.sh > install.sh
			$ chmod a+x install.sh
			
			### centos version
			$ sudo ./install.sh
			
			### ubuntu
			$ sudo ./install.sh --upstart
			```

:warning: If you're uncomfortable running a script you downloaded off the internet with sudo, you can extract any of the steps out of the install.sh script and run them manually.
