#!/bin/bash
docker run --network=di_bot_default --rm -v C://Users//grish//PycharmProjects//testtest//di_bot//liquibase//:/liquibase/changelog liquibase/liquibase --driver=org.postgresql.Driver --url="jdbc:postgresql://postgres:5432/di_bot" --username=di_bot --password=dipadissdiwd --changelogFile=root.changelog.xml update
