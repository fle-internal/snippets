import csv
import json
import os
import re
import sys
import time
import urllib2

def get_view_count(start_row, end_row, writer):
    with open('youtube_ids.txt', 'rb') as fp:
        reader = csv.reader(fp, delimiter=',')

        for count, read_row in enumerate(reader):
            if start_row is not None and count < start_row:
                continue
            elif end_row is not None and count <= end_row:
                continue

            youtube_id = read_row[0]
            print "%5d: %s" % (count, youtube_id)

            for retry_iter in range(5):
                try:
                    data = {}
                    string = 'http://gdata.youtube.com/feeds/api/videos/'+ youtube_id+'?v=2&alt=json'
                    response = urllib2.urlopen(string).read()
                    data     = json.loads(unicode(response, 'utf-8'))
                    import pdb; pdb.set_trace()
                    break
                except urllib2.HTTPError as e:
                    if e.code == 403 and "yt:quota" in e.read():
                        sleep_time = 15 # 4 minutes
                        sys.stderr.write("\t(%d) Hit the YouTube API limit; sleeping for %s seconds\n" % (retry_iter, sleep_time))
                        time.sleep(sleep_time)
                    else:
                        sys.stderr.write("\t(%d) HTTP error: %s (%s)\n" % (retry_iter, e, e.read()))
                        break  # don't waste requests retrying
                except Exception as e:
                        sys.stderr.write("\t(%d) non-HTTP error: %s\n" % (retry_iter, e))

            try:
                view_count      = data.get("entry").get("yt$statistics", {}).get("viewCount", "")
                fav_count       = data.get("entry").get("yt$statistics", {}).get("favoriteCount", "")
                video_title     = data.get("entry").get("title", {}).get("$t", "")
                author_name     = data.get("entry").get("author")[0].get("name", {}).get("$t", "")
                user_id         = data.get("entry").get("author")[0].get("yt$userId", {}).get("$t", "")
                upload_date     = data.get("entry").get("media$group", {}).get("yt$uploaded", {}).get("$t", "")
                rating_likes    = data.get("entry").get("yt$rating", {}).get("numLikes", "")
                rating_dislikes = data.get("entry").get("yt$rating", {}).get("numDislikes", "")
                average_rating  = data.get("entry").get("gd$rating", {}).get("average", "")


                out_row = [youtube_id,
                           view_count,
                           fav_count,
                           video_title,
                           author_name,
                           user_id,
                           upload_date,
                           rating_likes,
                           rating_dislikes,
                           average_rating]

            except Exception as e:
                sys.stderr.write("Error handling row: %s\n" % e)
                continue

            try:
                writer.writerow([unicode(l).encode('utf-8') for l in out_row])
            except Exception as e:
                try:
                    writer.writerow([l.decode('utf-8').encode('utf-8') for l in out_row])
                except Exception as e:
                    sys.stderr.write("Error writing row %s: %s" % (out_row, e))
                    continue

def download_youtube_data(out_file="youtube_stats.csv", start_row=None, end_row=None, append=None):

    if append is None and os.path.exists(out_file):
        append = True
        try:
            with open(out_file, "rb") as fp:
                reader = csv.reader(fp, delimiter=",")
                count = 0
                for count, row in enumerate(reader):
                    pass
                print
                start_row = count + 1 + 1  # cheat - extra one for assumed header row :(
        except:
            append = False

    if append:
        print "Appending previous results, starting at row %d" % start_row

    with open(out_file, '%sb' % 'a' if append else 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        if not append:
            writer.writerow(["YouTube ID" ,
                             "View Count",
                             "Favorite Count",
                             "Video Title",
                             "Author Name",
                             "User ID",
                             "Upload Date",
                             "Rating Likes",
                             "Rating Dislikes",
                             "Average Rating"])
        get_view_count(start_row, end_row, writer)


if __name__ == '__main__':
    download_youtube_data(start_row=1)  # skip the header row

