Bitstamp Portfolio Balance Flash Briefing
==

This is a "Flash Briefing" skill for Amazon Alexa-compatible devices (Echo, Echo
Dot, etc.).

Dependencies
--
- Python 2.X (due to alterations in HMAC implementation required by PyAlgoTrade)
- PyAlgoTrade

Installation & Configuration
--
1. Install PyAlgoTrade using pip 2.x on a server exposed to the internet:

  ```shell
  pip install pyalgotrade
  ```

2. Set up a reverse proxy in Nginx or Apache. SSL *must* be enabled for Alexa's
   API to talk to the script. Use any port over 1024 that you want. Default is
   8081.

3. Edit `crypto_balance.py`'s configuration area at the top to specify your
   account client ID and API keys for each crypto pair you trade in. If all your
   coins are in one account you will still need to repeat the API key values for
   each coin/trade pair.

Running the script
--

You should run the script in the background so it's always available.

  ```shell
  nohup ./crypto_balance.py 8081 &
  ```

Be sure to test that your script is now accessible from the outside world and
that your connection is valid over HTTPS.

Connecting to your Alexa-compatible device
--

1. If you don't already have an Amazon Developer account, go to
   developer.amazon.com and set up your Alexa account as a developer one.
2. Go to the Alexa menu and then use the *Add a new Skill* button to add a
   *Flash Briefing Skill*.
3. Configure your Skill. Something similar to the following should work. For
   your convenience, the Bitstamp logo is included in this repo:

   ![Sample Configuration](/sample-configuration.png?raw=true "Sample Configuration")

4. Under the *Test* section, click the toggle to enable testing on your Alex
   app. Wait a few minutes for everything to sync up, then in the Alexa app you
   will need to go to your skills listing and enable the skill on your
   Alexa-compatible device.

License
--
MIT
