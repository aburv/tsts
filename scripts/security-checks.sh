#!/usr/bin/env bash

set +e

ALPINE_VERSION=3.4
ISSUES_REPORT_FILE=server_hawkeye_report.json

docker create -v /target --name target-code alpine:${ALPINE_VERSION} /bin/true;
docker cp ./ target-code:/target;

apk update
apk add curl

docker run --volumes-from target-code --name hawkeye hawkeyesec/scanner-cli:latest scan -f high /target --json ${ISSUES_REPORT_FILE}
hawkeye_return=$?

mkdir -p /tmp/artifacts/;

docker cp hawkeye:/target/${ISSUES_REPORT_FILE} /tmp/artifacts/${ISSUES_REPORT_FILE}

if [ ${hawkeye_return} == 0 ]
then
    echo "Security checks passed"
else
    echo "Security checks failed. Report is available on artifacts tab."
fi

exit ${hawkeye_return}