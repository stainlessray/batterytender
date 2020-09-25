# This test script is intended for beta use. It utilizes the battery tender
# API this project was forked from. First follow the instructions for installing the API
# before running this script.

# To use this script after the API is installed, first you'll need to input your
# mqtt credentials (if secured with basic auth) AND
# your Deltran battery credentials. Read all the comments for details.

# This script is provided in good faith without warranty. It seeks to make
# responsible use of the services provided to Deltran customers to 
# integrate automotive data in their home automation solutions
# Use at your own risk. 

# The only license is that which is established by the author of the API. 
# This is provided in accordance with that license as the fork is intended for PR if successful.

import os
import batterytender
import paho.mqtt.client as mqtt  
import time  


# mqtt broker config
mqtt_sub_topic = 'battender/#' # Do not edit this
broker_address = '192.168.X.XXX'  # provide your broker host address as string (usually formatted as seen)
broker_port = 1883                # provide your broker port as int (default 1883)

# mqtt basic auth config 
# to use these you  need to uncomment the line below
# It is commented and the line begins with '**'
# Find the "Client configuration" section.
mqtt_username = 'username'
mqtt_password = 'password'

#battery tender account config
email = 'email@email.com'
tend_password = 'password_for_deltran'

# set the delay between api calls in seconds
# Anything shorter than ten minutes here is unuseful
# and could evoke a reaction. Servers cost money
delay_time = 1000


def on_message(client, userdata, msg):
    print('>> Message received-> ' + msg.topic + ' ' + str(msg.payload))  
    if msg.topic == 'battender/cmd':
        print('    Command channel received a message')

def on_connect(client, userdata, flags, rc):
    os.system('clear')  
    print('>> Connected with result code {0}'.format(str(rc)))  
    client.publish('battender/status','online', 0, True)

def on_publish(client, userdata, mid):
    os.system('clear')
    print('Message published ')

def on_disconnect(client, userdata, rc):
    print('>> disconnecting')
    client.publish('battender/status','offline', 0, True)
    client.loop_stop()

def on_log(client, userdata, level, buf):
    print('log: ',buf)


# MQTT client configuration
client = mqtt.Client('batterytender') 
client.on_connect = on_connect  
client.on_message = on_message  
client.on_publish = on_publish  
client.on_disconnect = on_disconnect 
client.will_set('battender/status', 'offline', 0, True)
client.on_log = on_log
client.connect(broker_address, broker_port) # (broker, port, keepalive-time) # 'keep alive' should not be necessary with the client loop.
# ** uncomment the line below to use basic auth with mqtt. Be sure to include those credentials above
# client.username_pw_set(username=mqtt_username, password=mqtt_password)  # use for basic authentication



def main():
    try:
        while True:
            bt = batterytender.BatteryTender(email, tend_password)
            client.loop_start()
            client.subscribe(mqtt_sub_topic)
            client.subscribe('battender/cmd/')
            for monitor in bt.monitors:
                for history in monitor.history:
  
                    pubstring = round(history['voltage'],2)
                    mqtt_pub_topic = 'battender/{}/state'.format(monitor.device_id)
                    client.publish(mqtt_pub_topic, str(pubstring))
                    print('Monitor id: {}'.format(monitor.device_id))
                    print('        Date: {}'.format(history['date']))   
                    print('        Voltage: {}'.format(history['voltage']))
                    time.sleep(delay_time)          # !! I think backing this indent up to the first 'for' ststement may make it produce updates for all monitors in a single loop.
                                                    # This needs multiple devices for testing
    except KeyboardInterrupt:
        os.system('clear')
        print('    exiting....')
        choice ='0'
        while choice =='0':     
            print(' 1 exit the program ')
            print(' 2 return to the program ')     
            choice = input ('Select a task: ')    
            if choice == '1':
                exit()
            elif choice == '2':
                main()
            else:
                print('Please choose an available option ')
                choice = '0'
main()
