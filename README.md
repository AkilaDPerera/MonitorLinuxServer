# Monitor Linux/Ubuntu Server (04/2020)
This is a python2 script which can be used to monitor Linux/Ubuntu/Unix server CPU, Memory and Disk utilization and issue warning as emails in the case of exceeding utilization thresholds defined. Simple and easy to understand script to a person who has basic python coding skills. Feel free to contribute for greater features. 

## Instructions

You can find a function name analyze_server in the server_health_monitor.py file. Write a suiltable main method and call this function inside with the suitable parameters. Script will report the current CPU, RAM and Disk utilization values to a ServerHealth.log file in the sepecified location in the parameter. 

### Example main method
```
def main():
    # Consider: 
    #   CPU Idle percentage threshold as 20%
    #   Memory availability percentage threshold as 20%
    #   Disk free space percentage threshold as 20%

    toEmail = ****@***.com
    fromEmail = ****@gmail.com # 
    fromEmailPassword = ****

    analyze_server(20, 20, 20, "/var/www/project/media/", True, toEmail, fromEmail, fromEmailPassword):

if __name__=="__main__":
    main()
```

**toEmail** - Any email address where you want to receive warning emails. <br/>
**fromEmail** - google email address that you own with ability to access by third party applications (unsecured); https://support.google.com/accounts/answer/6010255?hl=en <br/>
**fromEmailPassword** - password of the google email that you own <br/>

You can add a similar main method to server_health_monitor.py file and schedule a cron job to run periodically. By having ServerHealth.log file in a STATIC location (location where you can access from outside), will ease you to monitor the server. However, you will receive an email whenever the thresholds are reached. 

## Test the script before scheduling a cron job
Navigate to the location where the server_health_monitor.py is located.
```
sudo chmod -R 777 server_health_monitor.py
python server_health_monitor.py
```
In the case that the python libaries are mission install them as follows.
```
pip install library_name
```
If the execution is successfull, script will results nothing to the console but ServerHealth.log file. 

## How to schedule a cron job to run the script in every 15 min

Open ssh to server:<br/>
```
sudo crontab -e
```

Add following entry at the end of file and save.<br/>
```
0,15,30,45 * * * * /usr/bin/python2 /var/www/project/server_health_monitor.py
```
*note: <br/> python2 location can be different from /usr/bin/python2. Use the correct python2 location on your server.*