#!/bin/bash
(./cookie | play -t wav -) &
pidof python2 > /var/run/cookie
