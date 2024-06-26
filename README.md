# Groupy

Example Bot hosted at: [@groupy@tomkahe.com](https://tomkahe.com/@groupy)

### Temporary Solution to Lemmy* federation on Mastodon, specifically [this issue](https://github.com/LemmyNet/lemmy/issues/2606) or [this one](https://github.com/LemmyNet/lemmy/issues/2224) or [this](https://github.com/mastodon/mastodon/issues/18069) which will probably all be fixed by [this](https://github.com/mastodon/mastodon/pull/19059) but might [not be](https://github.com/mastodon/mastodon/issues/18069#issuecomment-1717307256). Unfortunately not a solution to [this](https://github.com/mastodon/mastodon/issues/17003).

Follows a set of link aggregator communities provided in the config.toml, checks every status to see if it is *actually a post*, if it is a post boost it to followers otherwise it is a comment and should be ignored. You just follow your bot account and you'll just get the actual posts from the provided communities

*May also fix kbin/Mbin/PieFed federation, I am not certain if those experience the same issues. I tried testing with some federated kbin communities, but I'm not entirely certain how to differentiate between a community and a user from Mastodon. e.g. [@TodayILearned@kbin.social](https://kbin.social/search?q=%40todayilearned%40kbin.social) seems to reference both a user and a community and I can only follow the user from mastodon 

[![Follow @groupy@tomkahe.com](https://fedi-badge.deno.dev/@groupy@tomkahe.com/followers.svg?style=plastic)](https://tomkahe.com/@groupy)
