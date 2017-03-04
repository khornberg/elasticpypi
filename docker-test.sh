if [[ $@ == *"help"* ]]; then
    echo "run this from inside your elasticpypi repo dir."
    echo "options:"
    echo "  build  - Builds the Dockerfile before running tests."
    echo "  test   - Runs tests inside a Docker container"
    echo "  debug  - Runs bash in an interactive Docker container "
    echo "           with `pwd` mounted at /code"
fi


if [[ $@ == *"build"* ]]; then
    sudo docker build -t elasticpypi-test .
fi

if [[ $@ == *"test"* ]]; then
    sudo docker run -it \
        -v $(pwd):/code \
        -e AWS_DEFAULT_REGION=artic-1 \
        -e SERVICE=serverless-service-name \
        -e STAGE=/dev \
        -e BUCKET=your-bucket-name \
        -e TABLE=elasticpypi \
        -e USERNAME=elasticpypi \
        -e PASSWORD=something-secretive \
        -e OVERWRITE=false \
        elasticpypi-test
fi

if [[ $@ == *"debug"* ]]; then
    sudo docker run -it \
        -v $(pwd):/code \
        -e AWS_DEFAULT_REGION=artic-1 \
        -e SERVICE=serverless-service-name \
        -e STAGE=/dev \
        -e BUCKET=your-bucket-name \
        -e TABLE=elasticpypi \
        -e USERNAME=elasticpypi \
        -e PASSWORD=something-secretive \
        -e OVERWRITE=false \
        elasticpypi-test \
        /bin/bash
fi