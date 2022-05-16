# onion-notes

## Requirements
``
python3, 
tor
``

## Install required dependencies

```pip install pynacl cepa flask```

## Tor Configuration

First, you need to locate the torrc file. By default it is generally located in /etc/tor folder on Linux. If running Tor via commandline, the file location will also be displayed there when tor is being started.

Once you have located the file, uncomment the following lines by removing the "#" character:

``#ControlPort 9051``
``#CookieAuthentication 1``
