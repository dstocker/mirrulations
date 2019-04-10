# Mirrulations

![](https://healthchecks.io/badge/1f6c74dc-b07d-44fd-a752-0a61ea/Hqd-_HXp/mirrulation.svg)

Software to create and maintain a mirror of regulations.gov

#### Regulations.gov
------
The data on [Regulations.gov](https://www.regulations.gov) consists of Congressional laws that have been passed and implemented as regulations by federal agencies. The site is available to the public such that anyone can read and provide feedback for these regulations to make their opinions known.


#### The Problem
------

The way that Regulations.gov is currently set up, users may search for and comment on regulations on the main site, however finding older regulations through the site's API has become a more difficult and limited process where users must apply for an API key to be granted time-limited access to larger sets of data.


The reason users must apply for an API key is because Regulations.gov has taken steps toward conserving their system resources by limiting how many times per hour a user can query the API. This came about after late-show host, John Oliver, called attention to the [fight for net neutrality](https://www.cbsnews.com/news/john-oliver-fans-flood-fcc-website-in-fight-for-net-neutrality/) in 2017 where a flood of viewers crashed the FCC's website with their comments. In an effort to reduce the overall traffic, API access is now limited to one account per organization as well and requires an approval process to validate API keys.

#### The Objective
------

The objective of the Mirrulations project is to make the data on Regulations.gov more easily accessible to the public by acting as a mirror to the site. Since it is federal data, it must be available (with exceptions) to the public under the [Freedom of Information Act](https://foia.state.gov/Learn/FOIA.aspx). By making the data readily available in one place, analysts can more easily study it.

#### The Solution
------
The Mirrulations project endeavors to create a mirror of the regulatory data on Regulations.gov to make it more accessible to the general public. Our goal is to collect all of the data from the site and store it in a database/cloud for users to search for at their leisure. The only problem with that is that there are currently over 9.6 million regulations documents (and counting!) to be downloaded.

With the API limiting that is in place, it would take us months to download all of the data by ourselves so we are creating a volunteer computing system that allows other people to contribute to the expedition of the downloading process. Through this project users can apply for an API key and volunteer their computer's CPU for downloading data and sending it to our server. If you choose to volunteer, the instructions below will help you to help us get up and running.


## Getting Started

If you are interested in becoming a developer, see `docs/developers.md`.

To run Mirrulations, you need Python 3.7.2 or greater ([MacOSX](https://docs.python-guide.org/starting/install3/osx/) or [Windows](https://docs.python-guide.org/starting/install3/win/)) on your machine to run this, as well as [redis](https://redis.io/) if you are running a server

You will also need a valid API key from Regulations.gov to participate. To apply for a key, you must simply [contact the Regulations Help Desk](regulations@erulemakinghelpdesk.com) and provide your name, email address, organization, and intended use of the API. If you are not with any organizations, just say so in your message. They will email you with a key once they've verified you and activated the key.

To download the actual project, you will need to go to our [GitHub page](https://github.com/MoravianCollege/mirrulations) and [clone](https://help.github.com/articles/cloning-a-repository/) the project to your computer.

If you are running a server, please run a redis server before continuing.

From your terminal, in the project directory, set up a virtual environment by

	python3 -m venv .env
	source .env/bin/activate
    pip install -e .

Lastly, run `mirrulations_client` to get it running as a client, or `mirrulations_server` to get it running as a server.

If you do not have a `config.json` previously made, you will be prompted to make one.
(You can also force an overwrite of `config.json` with the tag `--config` at the end of your command.)
A terminal prompt will show up, asking for the API key from earlier as well as, if ran as a client, a server IP and a port.
You can use the IP 10.76.100.34 and port 8080.
The API key itself is the one you received earlier.

### Disclaimers
--------
"Regulations.gov and the Federal government cannot verify and are not responsible for the accuracy or authenticity of the data or analyses derived from the data after the data has been retrieved from Regulations.gov."

In other words, "once the data has been downloaded from Regulations.gov, the U.S. Government cannot verify and is not responsible for the quality, accuracy, reliability, or timeliness of any analyses conducted using the downloaded data."

This product uses the Regulations.gov Data API but is neither endorsed nor certified by Regulations.gov.

--------
This project is currently being developed by a student research team at Moravian College in association with Careset under Fred Trotter.
