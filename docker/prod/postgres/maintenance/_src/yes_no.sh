#!/usr/bin/env bash

yes_no(){
  # shellcheck disable=SC2034
  declare desc="Prompt for confirmation. \${1}: confirmation message"

  # The first argument passed to the function is stored in the local variable arg1
  local arg1="${1}"

  # Read user input after displaying the prompt message (arg1) followed by (y/[n])?
  # The default response is 'n' if the user presses enter without typing anything
  read -r -p "${arg1} (y/[n])? " response

  # Check if the response matches 'y' or 'Y'
  if [[ "${response}" =~ ^[Yy]$ ]]
  then
    # If the response is 'y' or 'Y', exit with status 0 (success)
    exit 0
  else
    # Otherwise, exit with status 1 (failure)
    exit 1
  fi
}
