#!/bin/env bash

# Author  : Prashantha TP
# Date    : March 20,2022 Sunday
# License : MIT License
# About   : Script to generate changelog



[[ -z "$1" ]] && echo "Release tag not given.Exiting without generating changelog"&&exit 1;
curr_release="$1"

curr_dir=$(dirname ${BASH_SOURCE[0]})
changelog_file="${curr_dir}/../CHANGELOG.md"

echo "Changelog : ${changelog_file}"

overwrite_file(){
    echo "$@" > "${changelog_file}"

}
append_file(){
    echo "$@" >> "${changelog_file}"
}
add_newlines(){
    printf "\n%.0s" {1..$1} >> "${changelog_file}"
}

get_date(){
    echo "$(date +%d/%m/%Y)"
}

prefixes=("Feat" "Fix" "Util" "Tests" "Chore" "Pack" "Dev" )
last_tag=$(git describe --tags --abbrev=0)
echo "Last tag : $last_tag"
prev_log=""

[[ -f "${changelog_file}" ]]&&prev_log=$(cat "${changelog_file}" | sed -E "s/# Changelog//g")

overwrite_file "# Changelog"
add_newlines 1
append_file  "## ${curr_release} ( $(get_date) )"
add_newlines 1

for prefix in ${prefixes[@]};do
    append_file  "### ${prefix}" 
    add_newlines 1
    append_file "$(git log --oneline ${last_tag}..HEAD | sed -E "s/\*//g" | grep $prefix)"
    add_newlines 1
done

append_file  "${prev_log}"

