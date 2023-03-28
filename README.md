# set-bluetooth-clocks
Python based utility to discover and update times of bluetooth clocks - uses python package [bluetooth-clocks](https://github.com/koenvervloesem/bluetooth-clocks.git).

I have a bunch of Xiaomi LYWSD02 clocks which also act as temperature sensors for my Home Assistant setup.

The clocks keep losing track of time. So I wrote this little utility to update time.

If you feel it is useful and you want to imrove it, please feel free to raise a PR!

The utility goes through a loop periodically (controller via command-line parameter or environment variable) and does following
* Discovers all the bluetooth clocks and builds a list of clocks.
* Iterates through the list
  * Gets the current time of each clock.
  * If the gap between current time and the obtained time is more than 30 seconds (currently hard-coded), it tries to update the time.
  
I have a few raspberry pi's also running in my house. So I run the utility on all of those to ensure that the clocks are not missed. I have noticed that not every clock get discovered in a run of a loop.

To do:
* ~~Remove hard-coded values and turn those into command-line parameters / environment variables.~~
* Refactor the code to allow things run in parallel to reduce time taken per loop.


Log of a typical run of loop:
```
2023-03-14 18:57:57,688 - Main loop started.
2023-03-14 18:57:59,098 - Found clock: ATC_721501 (A4:C1:38:72:15:01) - is_readable: False
2023-03-14 18:58:00,050 - Found clock: ATC_192B8E (A4:C1:38:19:2B:8E) - is_readable: False
2023-03-14 18:58:10,127 - Found clock: LYWSD02 (E7:2E:01:40:10:8E) - is_readable: True
2023-03-14 18:58:19,167 - Found clock: ATC_944307 (A4:C1:38:94:43:07) - is_readable: False
2023-03-14 18:58:57,760 - Working on : E7:2E:01:40:10:8E (LYWSD02)
2023-03-14 18:59:09,578 - Current time: 2023-03-14 18:59:02
2023-03-14 18:59:09,580 - Difference (7.580225) is less than limit (30). Not updating time now.
2023-03-14 18:59:09,581 - Main loop finished.
```
## Command-line parameters
```
usage: set-bluetooth-clocks.py [-h] [--loop-interval LOOP_INTERVAL] [--scan-duration SCAN_DURATION] [--diff-tolerance DIFF_TOLERANCE]
                               [--attempts-gettime ATTEMPTS_GETTIME] [--attempts-settime ATTEMPTS_SETTIME]

Utility to update date-time on all visible bluetooth clocks

options:
  -h, --help            show this help message and exit
  --loop-interval LOOP_INTERVAL
                        Time between runs of main loop, in seconds. (default: 14400)
  --scan-duration SCAN_DURATION
                        Scan duration per clock to listen and wait, in seconds. (default: 120)
  --diff-tolerance DIFF_TOLERANCE
                        Maximum difference allowed in current time and clock time before update is performed, in seconds. (default: 30)
  --attempts-gettime ATTEMPTS_GETTIME
                        Number of times attempts should be made to read time from clock. (default: 10)
  --attempts-settime ATTEMPTS_SETTIME
                        Number of times attempts should be made to set time on the clock. (default: 15)
```


## Docker-compose file
The environment variables in the docker-compose file follow the command-line parameters. See help on command-line parameters.

```
services:
  set-bluetooth-clocks:
      build:
          dockerfile : Dockerfile
          context: .
      container_name: set-bluetooth-clocks
      restart: unless-stopped
      volumes:
          - /etc/localtime:/etc/localtime:ro
          - /etc/timezone:/etc/timezone:ro
          - /tmp/docker/set-bluetooth-clocks/tmp:/tmp
          - /run/dbus:/run/dbus:ro
          - /var/lib/bluetooth:/var/lib/bluetooth:ro
      environment:
        #- LOOP_INTERVAL=7200
        - SCAN_DURATION=60
        #- DIFF_TOLERANCE=30
        #- ATTEMPTS_GETTIME=10
        #- ATTEMPTS_SETTIME=15
      security_opt:
          - seccomp:unconfined
```
