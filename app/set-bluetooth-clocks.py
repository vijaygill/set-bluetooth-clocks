#!/usr/local/bin/python

import asyncio
import bluetooth_clocks
import bluetooth_clocks.scanners

from datetime import datetime

import logging
import colorlog

logger = logging.getLogger(__name__)
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(asctime)s - %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'white',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
        }))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

async def discover_clocks(clocks):
    def on_clock_found(clock):
        try:
            is_readable = clock.is_readable()
            info = "Found clock: {0} ({1}) - is_readable: {2}".format(clock.name, clock.address, is_readable)
            logger.info(info)
            if is_readable:
                clocks.append(clock)
        except Exception as e:
            logger.error("Error: ".format(e))
            pass

    await bluetooth_clocks.scanners.discover_clocks(on_clock_found, 60)

async def update_time(clock):
    logger.info("Working on : {0} ({1})".format(clock.address, clock.name))
    attempts_gettime = 5
    attempts_settime = 15
    diff_max = 30
    needs_update = False
    for attempt in range(attempts_gettime):
        try:
            timestamp = await clock.get_time()
            time = datetime.fromtimestamp(timestamp)
            logger.info("Current time: {0}".format(time))
            now = datetime.now()
            diff = (now - time).total_seconds()
            diff = abs(diff)
            if (diff <= diff_max):
                logger.info("Difference ({0}) is less than limit ({1}). Not updating time now.".format(diff, diff_max))
            else:
                logger.warning("Difference ({0}) is greater than limit ({1}). Updating time now to {2}.".format(diff, diff_max, now))
                needs_update = True

            break
        except Exception as e:
            logger.error("Error while getting time in attempt {0} of {1}: {2}".format(attempt, attempts_gettime, e))
            pass
    if needs_update:
        for attempt in range(attempts_settime):
            try:
                now = datetime.now().timestamp()
                await clock.set_time(now, False)
                logger.info("Clock updated with current time.")
                break
            except Exception as e:
                logger.error("Error while setting time in attempt {0} of {1}: {2}".format(attempt, attempts_settime, e))
                pass


async def update_times(clocks):
    for clock in clocks:
        await update_time(clock)

async def main():
    sleep_time_sec = 60 * 15
    while True:
        try:
            clocks = []
            logger.info("Main loop started.")
            await discover_clocks(clocks)
            await update_times(clocks)
            logger.info("Main loop finished.")
            await asyncio.sleep(sleep_time_sec)
        except Exception as e:
            logger.error("Error in mail: {0}".format(e))
            pass


if __name__ ==  '__main__':
    print("Set BlueTooth clocks application.")
    asyncio.run(main())

