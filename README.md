# set-bluetooth-clocks
Python based utility to discover and update times of bluetooth clocks - uses python package [bluetooth-clocks](https://github.com/koenvervloesem/bluetooth-clocks.git).

I have a bunch of Xiaomi LYWSD02 clocks which also act as temperature sensors for my Home Assistant setup.

The clocks keep losing track of time. So I wrote this little utility to update time.

It is at a very initial stage and can be improved a lot, though it does the job I wanted it to do.

So if you feel it is useful and you want to imrove it, please feel free to raise a PR!

The utility goes through a loop every 15 minutes and does following
* Discovers all the bluetooth clocks and builds a list of clocks that allow reading (and possibly writing also. The API does not provide can_write() method).
* Iterates through the list
  * Gets the current time of each clock.
  * If the gap between current time and the obtained time is more than 30 seconds (currently hard-coded), it tries to update the time.
