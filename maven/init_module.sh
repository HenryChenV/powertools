#!/bin/sh

THIS_FILE=$0
MODULE_NAME=$1


help() {
    echo 
    echo "Usage ./${THIS_FILE} <module-name>"
    echo
}


gen_project() {
mvn archetype:generate \
    -DgroupId=cn.chenhenry.java \
    -DartifactId=${MODULE_NAME} \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DinteractiveMode=false
}


main() {
    if [ x"" = x"${MODULE_NAME}" ]; then
        help
        exit 1
    fi

    gen_project
}


main
