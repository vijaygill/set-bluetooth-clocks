#!/usr/local/bin/python

import os
import asyncio
import bluetooth_clocks
import bluetooth_clocks.scanners

from datetime import datetime, timedelta

import logging
import colorlog

import argparse

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

async def discover_clocks(args, clocks):
    def on_clock_found(clock):
        try:
            logger.info("Found clock: {0} ({1})".format(clock.name, clock.address))
            if clock.name.startswith('LYWSD02'):
                clocks.append(clock)
                logger.info("Added clock to the list: {0} ({1})".format(clock.name, clock.address))
            else:
                logger.info("Not adding clock to the list: {0} ({1})".format(clock.name, clock.address))
        except Exception as e:
            logger.error("Error: ".format(e))
            pass
    scan_duration = args.scan_duration

    await bluetooth_clocks.scanners.discover_clocks(on_clock_found, scan_duration)

async def update_time(args, clock):
    logger.info("Working on : {0} ({1})".format(clock.address, clock.name))
    attempts_gettime = args.attempts_gettime
    attempts_settime = args.attempts_settime
    diff_max = args.diff_tolerance
    needs_update = False
    for attempt in range(1, attempts_gettime + 1):
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
        for attempt in range(1, attempts_settime + 1):
            try:
                now = datetime.now().timestamp()
                await clock.set_time(now, False)
                logger.info("Clock updated with current time.")
                break
            except Exception as e:
                logger.error("Error while setting time in attempt {0} of {1}: {2}".format(attempt, attempts_settime, e))
                pass


async def update_times(args, clocks):
    for clock in clocks:
        await update_time(args, clock)

async def main(args):
    sleep_time_sec = args.loop_interval
    while True:
        try:
            clocks = []
            logger.info("Main loop started.")
            await discover_clocks(args, clocks)
            await update_times(args,clocks)
            next_run_time = datetime.now() + timedelta(seconds = sleep_time_sec)
            logger.info("Main loop finished. Next run will be around: {0} ({1} seconds)".format(next_run_time.strftime("%Y-%m-%d %H:%M:%S"), sleep_time_sec))
            await asyncio.sleep(sleep_time_sec)
        except Exception as e:
            logger.error("Error in mail: {0}".format(e))
            pass

LOOP_INTERVAL_DEFAULT = 60 * 60 * 2 # 2 hours
SCAN_DURATION_DEFAULT = 30
DIFF_TOLERANCE_DEFAULT = 30
ATTEMPTS_GETTIME_DEFAULT = 10
ATTEMPTS_SETTIME_DEFAULT = 15

if __name__ ==  '__main__':
    parser = argparse.ArgumentParser(description = "Utility to update date-time on all visible bluetooth clocks", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--loop-interval", default = os.getenv("LOOP_INTERVAL", LOOP_INTERVAL_DEFAULT), help="Time between runs of main loop, in seconds.", type = int)
    parser.add_argument("--scan-duration", default = os.getenv("SCAN_DURATION", SCAN_DURATION_DEFAULT), help="Scan duration per clock to listen and wait, in seconds.", type = int)
    parser.add_argument("--diff-tolerance", default = os.getenv("DIFF_TOLERANCE", DIFF_TOLERANCE_DEFAULT), help="Maximum difference allowed in current time and clock time before update is performed, in seconds.", type = int)
    parser.add_argument("--attempts-gettime", default = os.getenv("ATTEMPTS_GETTIME", ATTEMPTS_GETTIME_DEFAULT), help="Number of times attempts should be made to read time from clock.", type = int)
    parser.add_argument("--attempts-settime", default = os.getenv("ATTEMPTS_SETTIME", ATTEMPTS_SETTIME_DEFAULT), help="Number of times attempts should be     made to set time on the clock.", type = int)

    args = parser.parse_args()

    logger.info(' '.join(f'{k}={v}' for k, v in vars(args).items()))

    print("Set BlueTooth clocks application.")
    asyncio.run(main(args))

