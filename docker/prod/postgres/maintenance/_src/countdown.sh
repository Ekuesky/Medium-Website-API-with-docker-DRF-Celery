#!/usr/bin/env bash

# Function to perform a countdown
countdown(){

  # Declares a variable `desc` that describes the function. This is for documentation purposes.
  # shellcheck disable=SC2034
  declare desc="A simple countdown."

  # `seconds` is the first argument passed to the function, representing the number of seconds to count down.
  local seconds="${1}"

  # Calculate the end time in seconds since the epoch (Unix timestamp)
  # by adding the current time (`date +%s`) and the number of seconds.
  local d=$(($(date +%s) + "${seconds}"))

  # Loop until the current time is less than or equal to the end time
  while [ "$d" -ge "$(date +%s)" ]; do
    # Calculate the remaining time in seconds and format it as HH:MM:SS
    # `date -u --date @seconds` interprets the seconds as a Unix timestamp and formats it.
    echo -ne "$(date -u --date @$(($d - $(date +%s))) +%H:%M:%S)\r"

    # Sleep for 0.1 seconds before the next iteration to update the countdown display
    sleep 0.1
  done

}

