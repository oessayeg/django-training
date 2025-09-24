#/bin/sh

curl -s -i $1 | grep -i 'location' | cut -d ' ' -f 2
