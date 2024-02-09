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
     Lemmy Post: /post/POST-ID
     Lemmy Comment: /comment/COMMENT-ID
     kbin/mbin post: /m/COMMUNITY/t/POST-ID/POST-NAME
     kbin/mbin comment:  /m/COMMUNITY/t/POST-ID/POST-NAME#entry-comment-COMMENTID
     Piefed Post: /post/POST-ID
     Piefed Comment: /post/POST-ID/comment/COMMENT-ID/
  '''
  def is_post(self, status) -> bool:
    if (not status.get('reblog')):
      # This was not boosted by a community account
      return False
    url = status.get('reblog').get('url')
    if '/comment/' in url or '#entry-comment-' in url:
      return False
    if not url.contains('post'):
      if not url.contains('/t/'):
        return False
    return True


  '''
    Loops through all communities from config, attempts to search for and follow account
  '''
  def follow_communities(self):
    users_to_follow = self.bot_config.get('communities')
    for user in users_to_follow:
      # Get account ID from username
      print(f"Attempting to follow {user}")
      account = self.mastodon.account_search(user, resolve=True)[0]
      account_id = account['id']
      print(account_id)
      # Follow the user
      print(self.mastodon.account_follow(account))

  """
    If status is a post, boost it. Otherwise ignore it
  """
  def on_update(self, status):
    if (not status['reblogged'] and self.is_post(status)):
      print("Boosting status")
      print(status)
      self.mastodon.status_reblog(status['id'])

  '''
    Creates a stream and attaches it to on_update
  '''
  def stream_timeline(self):
    print("Starting stream")
    listener = CallbackStreamListener(update_handler = self.on_update)
    self.mastodon.stream_user(listener, timeout=1200, reconnect_async=True)

  '''
    Uses config to update profile with display name, description, and profile fields
  '''
  def update_profile(self):
    display_name = self.mastodon_config.get('display_name')
    note_preface = self.mastodon_config.get('bio_preface')
    note_appendix = self.mastodon_config.get('bio_appendix')
    communities = '\n'.join(self.bot_config.get('communities'))
    note = f"{note_preface}\n{communities}\n\n{note_appendix}"
    print(self.mastodon_config)
    fields = [(field['descriptor'], field['value']) for field in self.mastodon_config.get('profile_field')]
    print(display_name, note, fields)
    self.mastodon.account_update_credentials(display_name=display_name, note=note, bot=True, fields=fields)

if __name__ == "__main__":
  bot = Bot()
  bot.update_profile()
  bot.follow_communities()
  bot.stream_timeline()
