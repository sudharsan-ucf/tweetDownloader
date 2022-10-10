# Repository to download tweets using Twitter API v2

Create a file named `twitterKeys.json` following a pattern similar to `twitterKeys.sample.json`.
Run `python downloadTweets.py` to download tweets.

The tweets will be saved as a list of json strings to a file with name `RealTimeOutput/%Y-%M-%D.txt`

The code may fail and does not handle all errors. In such cases, restarting might be a easy solution. Run the script `loopCountry.sh` to continually restart the downloads. A better way would be to setup the downloader as a service using `systemctl` for example.