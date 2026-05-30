-- What are people asking across platforms?
SELECT
  'twitter' AS platform,
  t.text AS content,
  t.created_at,
  t.likes AS engagement
FROM twitter_local.tweets t
WHERE t.text LIKE '%?%'

UNION ALL

SELECT
  'discord' AS platform,
  d.content AS content,
  d.timestamp AS created_at,
  0 AS engagement
FROM discord.messages d
WHERE d.content LIKE '%?%'

ORDER BY created_at DESC
LIMIT 20;