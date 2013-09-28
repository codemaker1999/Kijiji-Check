from urllib2 import urlopen
from xml.dom import minidom
from time import strptime,time,strftime
import os
# Cap number of lines in log
cap = 50
logfn='log.txt'
rss_url=''
# Make log file if it doesn't exist
cwd = os.getcwd()
logpath = os.path.join(cwd,logfn)
if not(os.path.isfile(logpath)):
    with open(logfn,'w') as log: pass
# Fetch XML (string) from RSS feed
xml_str = urlopen(rss_url).read()
# Parse and get pubDate tags
xml = minidom.parseString(xml_str)
# Get url to ad page
ad_url = xml.getElementsByTagName('link')[0].firstChild.nodeValue
# An 'item' is an ad
items = xml.getElementsByTagName('item')
# NOTE: items is a list of ads, sorted by time of posting
# Get date of ad posting from each item
item_dates = []
for i in items:
    date_DOM = i.getElementsByTagName('pubDate')[0]
    # EX:
    # date_str = 'Sun, 18 Aug 2013 20:30:04 GMT'
    date_str = date_DOM.firstChild.nodeValue
    # parse string into a time.struct_time
    fmt_kijiji='%a, %d %b %Y %H:%M:%S GMT' # (See time docs)
    timestruct = list(strptime(date_str,fmt_kijiji))
    item_dates.append(timestruct)

# Get old dates from the log
with open(logfn,'r') as log: # open log in read mode
    loglines = log.readlines()
    # Filter out log timestamps
    # EX: line=[Log Entry 2013-12-31 23:59:59]
    old_dates = filter(lambda x: not(x.startswith('[')),
                       loglines)    
    if len(old_dates) != 0:
        newest_old_date = old_dates[-1]
        # Helper
        def is_new(t):
            'Determine if t is a higher date than newest_old_date'
            global newest_old_date
            for i,j in zip(newest_old_date,t):
                if i<j: return True
                elif i>j: return False
            return False # If times are the same, False
        new_dates = filter(is_new, item_dates)
        # NOTE: new_dates is now a list of dates newer than the
        #   previous newest date in the log (still sorted)
    # If log is empty, everything is a new date
    else: new_dates = item_dates

# Open log for appending (if there is anything to append)
if len(new_dates): # If not empty
    with open(logfn,'a') as log: # open log in append mode
        # NOTE: log is open in append mode
        # Format current local time into string
        # EX: '2013-12-31 23:59:59'
        fmt_log = '%Y-%m-%d %H:%M:%S'
        cur_time = strftime(fmt_log) # Defaults to current time
        # Timestamp log entry
        log.write('[Log Entry %s]'%cur_time)
        log.write('\n')
        # Write new_dates to the end of log
        # order: prev dates -> oldest dates -> newest dates -> EOF
        # Thus we need to reverse new_dates
        new_dates.reverse()
        for date in new_dates:
            pretty_date=strftime(fmt_log,date)
            log.write(str(pretty_date))
            log.write('\n')
        # Launch the url to display the new ads
        # Empty string dummy arg is needed for window title
        os.system('start "" "%s"'%ad_url)

# Finally, trim log file
# Log file has potentially changed, get new lines
with open(logfn,'r') as log: # open log in read mode
    new_loglines = log.readlines()
    loglen = len(new_loglines)
# Check if beneath cap
if loglen>cap:
    with open(logfn,'w') as log:
        # NOTE: write mode erases previous log.txt
        # Trim from the top of the file (older entries)
        for line in new_loglines[loglen-cap:]:
            log.write(line)
            log.write('\n')
