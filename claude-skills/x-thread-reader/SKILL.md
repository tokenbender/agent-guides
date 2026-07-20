---
name: x-thread-reader
description: Use when the user provides an X/Twitter status URL and needs the full thread, context beyond the first post, comparison, summary, intent analysis, title extraction, or reliable post text. Convert status links to Twitter Thread Reader URLs using the tweet id when X is blocked, incomplete, or thread context matters.
metadata:
  short-description: Read full X threads through Twitter Thread Reader
---

# X Thread Reader

Use this skill whenever an X/Twitter post may need more than the top-post text.

## Workflow

1. Extract the tweet id from the URL.
   - Match `x.com/<user>/status/<id>`, `twitter.com/<user>/status/<id>`, or equivalent status URLs.
   - Ignore query parameters such as `?s=20`.

2. Build the thread-reader URL:

   ```text
   https://twitter-thread.com/t/<tweet_id>
   ```

3. Fetch the Twitter Thread Reader page before drawing conclusions from a single X post.
   - Use it to recover the thread text, tweet count, linked media alt text, quoted/replied context, and embedded links when available.
   - Cite the thread-reader URL in the final answer when it shaped the answer.

4. Fall back only if Twitter Thread Reader fails or is missing tweets.
   - Try `api.fxtwitter.com`, `cdn.syndication.twimg.com/tweet-result`, X embed/oEmbed, web search, or browser-rendered inspection as appropriate.
   - State uncertainty when mirrors fail or only partial text is available.

## Output Rules

- Do not infer a thread's meaning from the opening tweet alone when a thread-reader page is available.
- When comparing a thread to a local project, read the thread first, then compare it against the relevant local docs or code.
- Preserve exact user output contracts. For title/capture tasks, return only the requested title format.
- Avoid guessed content. If the full thread cannot be verified, say what was verified and what was not.

## Example

```text
https://x.com/FredKSchott/status/2050274923852210397?s=20
-> https://twitter-thread.com/t/2050274923852210397
```
