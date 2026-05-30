-- What's my best performing content this week?
SELECT
  y.title,
  y.views,
  y.likes,
  t.text AS top_tweet,
  t.likes AS tweet_likes
FROM youtube_local.videos y
JOIN twitter_local.tweets t
  ON t.text LIKE '%video%'
ORDER BY y.views DESC
LIMIT 5;