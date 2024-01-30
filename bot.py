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
    #mastodon_config = self.config.get('mastodon')
    server = self.mastodon_config.get('server')
    print(f"Logging into {server}")
    return Mastodon(access_token=self.mastodon_config.get('access_token'), api_base_url=server)

  '''
     Returns true if status is top level (a post), false otherwise (a comment)
  '''
  def is_post(self, status) -> bool:
    print(status.get('in_reply_to_id'))
    return not status.get('reblog').get('in_reply_to_id')

#  def follow_config(self) -> None:
#    communities = self.bot_config.get('communities')
#    for community in communities:
#      print(f"Following {community}")
#      self.mastodon.status_post(f"Following {community}")
      #account_id = self.mastodon.account_search(community)[0]['id']
      #print(f"Found {account_id}")
#      self.mastodon.account_follow(community)
  def follow_config(self):
    #mastodon = self.login()
    users_to_follow = self.bot_config.get('communities')
    for user in users_to_follow:
      # Get account ID from username
      account = self.mastodon.account_search(user)[0]
      account_id = account['id']
      # Follow the user
      self.mastodon.account_follow(account_id)

  #def has_boosted_status(self, status_id):
      #mastodon = self.login()
   #   reblogged_by = self.mastodon.status_reblogged_by(status_id)
    #  print(reblogged_by)
     # authenticated_account_id = self.mastodon.account_verify_credentials()['id']
     # return authenticated_account_id in reblogged_by


  '''
    Loops through timeline and boosts all top-level posts, then sleeps
  '''
  def stream_timelines(self):
    # Follow all accounts from config
    self.follow_config()
    latest_status_id = None
    while True:
      all_statuses = []
      if (not latest_status_id):
        statuses = self.mastodon.timeline_home()
      else:
        satuses = self.mastodon.timeline_home(since_id=latest_status_id)

      all_statuses.extend(statuses)
      while self.mastodon.timeline_home(since_id=latest_status_id, max_id=statuses[-1]['id']):
         statuses = self.mastodon.timeline_home(since_id=latest_status_id, max_id=statuses[-1]['id'])
         all_statuses.extend(statuses)
      for status in all_statuses:
        if (not status['reblogged'] and self.is_post(status)):
          print(f"Boosting status {status}")
          self.mastodon.status_reblog(status['id'])
        else:
          print("Not boostable")
      if all_statuses:
        latest_status_id = all_statuses[0]['id']

      time.sleep(60*10)


  def on_update(status):
    if (not status['reblogged'] and self.is_post(status)):
      print("Boosting status")
      self.matodon.status_reblog(status['id'])
    else:
      print ("Not boostable")

  def stream_timeline(self):
    print(self.mastodon.retrieve_mastodon_version())
    print(self.mastodon._Mastodon__instance())
    listener = CallbackStreamListener(update_handler = self.on_update)
    #print(self.mastodon.retrieve_mastodon_version())
    #self.mastodon.stream_user( { 'update': self.on_update }, run_async=False)
    self.mastodon.stream_user(listener)

if __name__ == "__main__":
  bot = Bot()
  bot.stream_timeline()
