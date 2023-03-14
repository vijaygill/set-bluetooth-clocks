# set-bluetooth-clocks
Python based utility to discover and update times of bluetooth clocks - uses python package [bluetooth-clocks](https://github.com/koenvervloesem/bluetooth-clocks.git).

I have a bunch of Xiaomi LYWSD02 clocks which also act as temperature sensors for my Home Assistant setup.

The clocks keep losing track of time. So I wrote this little utility to update time.

It is at a very initial stage and can be improved a lot, though it does the job I wanted it to do.

So if you feel it is useful and you want to imrove it, please feel free to raise a PR!

The utility goes through a loop every 15 minutes (hard-coded) and does following
* Discovers all the bluetooth clocks and builds a list of clocks that allow reading (and possibly writing also. The API does not provide can_write() method).
* Iterates through the list
  * Gets the current time of each clock.
  * If the gap between current time and the obtained time is more than 30 seconds (currently hard-coded), it tries to update the time.
  
I have a few raspberry pi's also running in my house. So I run the utility on all of those to ensure that the clocks are not missed. I have noticed that not every clock get discovered in a run of a loop.

To do:
* Remove hard-coded values and turn those into command-line parameters / environment variables.
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
