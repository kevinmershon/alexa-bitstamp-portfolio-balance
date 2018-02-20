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
1. Install PyAlgoTrade into the project directory using pip 2.x:

   ```shell
   pip install pyalgotrade -t ./
   ```

2. Install into AWS Lambda as a function with the following environment
   variables defined: `client_id`, `btc_api_key`, `btc_api_secret`,
   `eth_api_key`, `eth_api_secret`, `bch_api_key`, `bch_api_secret`,
   `xrp_api_key`, `xrp_api_secret`.

3. Configure API Gateway to use a LAMBDA_PROXY to the function with the
   following Model configuration:

   ```json
   {
     "$schema": "http://json-schema.org/draft-04/schema#",
     "title": "AlexaFlashBriefingSkill",
     "type": "object",
     "properties": {
       "mainText": {"type": "string"},
       "uid": {"type": "string"},
       "titleText": {"type": "string"},
       "updateDate": {
         "format": "date-time",
         "type": "string",
         "description": "Event
           date-time"
       }
     }
   }
   ```

Running the script
--

Once configured via API Gateway you should be able to hit the script via URL

Be sure to test that your script is accessible from the outside world.

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
