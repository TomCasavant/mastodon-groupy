from mastodon import Mastodon
import toml
import time
from mastodon.streaming import CallbackStreamListener


class Bot:
  def __init__(self) -> None:
    with open('config.toml', 'r') as config_file:
      self.config = toml.load(config_file)
      self.bot_config = self.config.get('bot', {})
      self.mastodon_config = self.config.get('mastodon', {})
      self.mastodon = self.login()

  def login(self):
    server = self.mastodon_config.get('server')
    print(f"Logging into {server}")
    return Mastodon(access_token=self.mastodon_config.get('access_token'), api_base_url=server)

  '''
     Returns true if status is top level (a post), false otherwise (a comment)
  '''
  def is_post(self, status) -> bool:
    return status.get('reblog') and '/post/' in status.get('reblog').get('url')

  def follow_communities(self):
    users_to_follow = self.bot_config.get('communities')
    for user in users_to_follow:
      # Get account ID from username
      print(f"Attempting to follow {user}")
      account = self.mastodon.account_search(user)[0]
      account_id = account['id']
      # Follow the user
      self.mastodon.account_follow(account)

  def on_update(self, status):
    if (not status['reblogged'] and self.is_post(status)):
      print("Boosting status")
      print(status)
      self.mastodon.status_reblog(status['id'])

  def stream_timeline(self):
    listener = CallbackStreamListener(update_handler = self.on_update)
    self.mastodon.stream_user(listener, timeout=1200, reconnect_async=True)

if __name__ == "__main__":
  bot = Bot()
  bot.follow_communities()
  bot.stream_timeline()
