# Groupy
Example Bot hosted at: [@groupy@tomkahe.com](https://tomkahe.com/@groupy)

### Temporary Solution to lemmy/kbin/mbin/piefed federation on mastodon, specifically [this issue](https://github.com/LemmyNet/lemmy/issues/2606) or [this one](https://github.com/LemmyNet/lemmy/issues/2224) or [this](https://github.com/mastodon/mastodon/issues/18069) which will probably all be fixed by [this](https://github.com/mastodon/mastodon/pull/19059) but might [not be](https://github.com/mastodon/mastodon/issues/18069#issuecomment-1717307256). Unfortunately not a solution to [this](https://github.com/mastodon/mastodon/issues/17003).

Follows a set of link aggregator communities provided in the config.toml, checks every post to see if it is top-level (or *actually a post*), if it is a top-level post boost it to followers otherwise it is a comment and should be ignored. So you only have to follow your bot account and you'll just get the actual posts from the provided communities
