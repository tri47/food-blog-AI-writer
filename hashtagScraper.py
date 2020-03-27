import json, re, requests
import datetime
import time
import pandas as pd
import boto3


def scrape_instagram(user,user_id,query_hash,MAX_PAGES=50):
    #MAX_PAGES = 50 # Number of extra infinite scroll loads to scrape (11 posts/page)
    print("Scraping post info for user ", user)

    captions, post_links, image_links, likes, post_dates =[], [], [], [], []
    has_next_page = True

    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'
        end_cursor = '' 
        count = 0

        # Use has_bext_page while loop to scrape all posts
        while ((count < MAX_PAGES) and (has_next_page) ): 
        #while has_next_page: #for count in range(1, 4):
            print('PAGE: ', count)
            if count == 1: # The profile page
                profile = 'https://www.instagram.com/' + user
            else: # subsequent infinite scroll requests
                profile = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash +'&variables={"id":"' + user_id + '","first":12,"after":"' +  end_cursor + '"}'
            r = s.get(profile)
            time.sleep(2)

            if count == 1: # Profile page
                data = re.search(
                    r'window._sharedData = (\{.+?});</script>', r.text).group(1)
                data = json.loads(data)
                data_point = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
            else: # subsequent infinite scroll requests
                data = json.loads(r.text)['data']
                data_point = data['user']['edge_owner_to_timeline_media']

            # Extract data and find the end cursor for the current page
            end_cursor = data_point['page_info']['end_cursor']
            has_next_page = data_point['page_info']['has_next_page']
            for link in data_point['edges']:
                post_link = 'https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/'
                caption = link['node']['edge_media_to_caption']['edges'][0]['node']['text']
                like = link['node']['edge_media_preview_like']['count']
                post_time = link['node']['taken_at_timestamp']
                image_link = link['node']['display_url']
                post_time = datetime.datetime.fromtimestamp(post_time).strftime('%Y-%m-%d %a %H:%M')
                captions.append(caption)
                likes.append(like)
                post_dates.append(post_time)
                image_links.append(image_link)
                post_links.append(post_link)
            count += 1
                
            captions.pop()
            likes.pop()
            post_dates.pop()
            image_links.pop()
            post_links.pop()

        data_tuples = list(zip(captions, likes, post_dates, post_links ) )
        df = pd.DataFrame(data_tuples)
    saved_data = df.to_csv('full_posts_cafe.csv',index=False)
    print('Top entries')
    print(df.head())
    return df

def lambda_handler(event, context):
  data = scrape_instagram()
  file_name = "instaposts.csv"
  save_file_to_s3('instareports', file_name, data)

users = [
  {'name':'NAME', 'user_id': 'ID', 'query_hash':'HASH'},
  {'name':'NAME', 'user_id': 'ID', 'query_hash':'HASH'}
]

df = None
for user in users:
    df_p = scrape_instagram(user['name'], user['user_id'], user['query_hash'])
    if df is None:
        df = df_p
    else:
        df = df.append(df_p)
    print(df.head())
    df.to_csv('captionsFinal.csv')
print(df)

#df.to_csv(user + '_insta_posts.csv')

   