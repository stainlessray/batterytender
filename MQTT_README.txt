 The script integrates an mqtt client using paho mqtt. 
          `pip install _paho-mqtt`_
 You need the battery tender library installed also, that instruction is in the README
 for the original repo AND my fork
 Once running you can listen to mqtt topic "battender/#" to see all relevant messages. 

 The API provides an ID for each monitor on your account. 
 The second field of the mqtt topic will contain the ID of the monitor being reported.
 
 You can create an mqtt sensor in Home Assistant to receive updates using **"battender/#"** which isn't ideal. 

 _Finding your monitor ID in the mqtt message is recommended._ The mqtt message format looks like this :
        **battender/{}/state**
 
        where '{}' will contain the ID of each device on your account.
        Your mqtt sensor should be listening to each device you have independantly instead. 
        (I have plans to include all Battery Tender devices in single json formatted message in the future)
 
 First you'll need to edit a couple lines in the script:

1. * You'll need to edit the credentials portion for your Battery Tender account in the script. The comments inside will provide guidance.
2.  * If you are using mqtt with a a username and password you need to also edit the username  and password fields in the script -- AND another line needs to be uncommented. (details provided in script comments)
3. * If you already have the Battery Tender Library installed, just put this script in the same directory, and run it with this command : 
        `python ./batend_feature_tests.py` 

