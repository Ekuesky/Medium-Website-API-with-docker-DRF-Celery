#!/usr/bin/env bash

#!/usr/bin/env bash

# Function to print a newline
message_newline(){
  echo
}

# Function to print a debug message
message_debug(){
  # shellcheck disable=SC2145
  echo -e "DEBUG: ${@}"
}

# Function to print a welcome message in bold
message_welcome(){
  # shellcheck disable=SC2145
  echo -e "\e[1m${@}\e[0m"
}

# Function to print a warning message in yellow
message_warning(){
  # shellcheck disable=SC2145
  echo -e "\e[33mWARNING\e[0m: ${@}"
}

# Function to print an error message in red
message_error(){
  # shellcheck disable=SC2145
  echo -e "\e[31mERROR\e[0m: ${@}"
}

# Function to print an informational message in white
message_info(){
  # shellcheck disable=SC2145
  echo -e "\e[37mINFO\e[0m: ${@}"
}

# Function to print a suggestion message in yellow
message_suggestion(){
  # shellcheck disable=SC2145
  echo -e "\e[33mSUGGESTION\e[0m: ${@}"
}

# Function to print a success message in green
message_success(){
  # shellcheck disable=SC2145
  echo -e "\e[32mSUCCESS\e[0m: ${@}"
}

