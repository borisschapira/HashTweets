import csv
import twitter
import os
import os.path

outfilename = os.path.dirname(os.path.realpath(__file__)) + '/tweets.csv'
tempfilename = os.path.dirname(os.path.realpath(__file__)) + '/temp.csv'

api = twitter.Api(
    consumer_key='consumer_key',
    consumer_secret='consumer_secret',
    access_token_key='access_token_key',
    access_token_secret='access_token_secret')

lines_seen = set()
tweets = api.GetSearch('#RendsLArgent',count=200)

if os.path.isfile(outfilename) and os.access(outfilename, os.R_OK):
    for line in open(outfilename, "r"):
        if line not in lines_seen: # not a duplicate
            lines_seen.add(line)
    mode='a'
else:
    mode='w+'

with open(tempfilename, mode) as csv_file:
    csv_writer = csv.writer(csv_file)
    for tweet in tweets:
        print(tweet.id)
        row = [tweet.id, tweet.user.screen_name, tweet.text]
        csv_writer.writerow(row)

# Remove dupes line from the CSV 
outfile = open(outfilename, "a")
for line in open(tempfilename, "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

os.remove(tempfilename)