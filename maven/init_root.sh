#!/bin/sh

THIS_FILE=$0
ROOT_NAME=$1


help() {
    echo 
    echo "Usage ./${THIS_FILE} <root-name>"
    echo
}


gen_project() {
    mvn archetype:generate \
        -DgroupId=com.henry.java \
        -DartifactId=${ROOT_NAME} \
        -DarchetypeGroupId=org.codehaus.mojo.archetypes \
        -DarchetypeArtifactId=pom-root \
        -DinteractiveMode=false
}


main() {
    if [ x"" = x"${ROOT_NAME}" ]; then
        help
        exit 1
    fi

    gen_project
}


main
