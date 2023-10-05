## Notes on Assignment

* make sure not to use Amazon Linux 2023
* dont need to inclyude credentials/keys
* Need to access metadata about the instance
* in userData, use curl to get metadata about the instance
* set up S3 bucket website
* from python, launch web browser and display the webpage of the S3 bucket
* in python copy the monitoring.sh script and scp to the instance and then the instance must execute the script (through remote command execution) with ssh
* bucket will be configured for static website hosting

### bucket must have 2 items:
* image of setu logo
* index.html file that displays the image

### Core Fuctionality (60%)
## Additional functionality (10%)
examples of additional functionality:
* interact with other AWS services
* pass params as cmd line args
* install db on instance
* access error logs by querying the a webserver
* use boto3 to monitor system performance




