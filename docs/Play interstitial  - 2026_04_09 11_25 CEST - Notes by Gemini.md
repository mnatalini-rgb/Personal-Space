Apr 9, 2026

## Play interstitial 

Invited [Anouk Lubbers](mailto:a.lubbers@efg.gg) [Moritz Natalini](mailto:m.natalini@efg.gg)

Attachments [Play interstitial ](https://www.google.com/calendar/event?eid=MHZoNDFobjE1cWo5NDJjMDNsbTIyczNlMjMgYS5sdWJiZXJzQGVmZy5nZw) 

Meeting records [Transcript](?tab=t.rxqdbpop0dif) 

### Summary

Ad interstitial placement flow was finalized, with discussion focusing on user onboarding and A/B/C testing strategy with sound-on video requirements.

**Ad Interstitial Placement Confirmed**  
The interstitial ad spot before users enter a match was confirmed as the correct, less risky placement, following approval of the flow: Homepage \> Play \> Find a Match \> Video Interstitial Modal \> System searches for a match. The decision was made to have users watch the ad completely before starting the match queueing process to avoid user perception of longer wait times.

**Ad Onboarding and Skip Strategy**  
The team decided to offer users 1 skip per day, with ads beginning only from the second match onward to help build momentum. An A/B/C test is planned, comparing a control group, a group with no ads on the first match, and a group where ads begin after the first match to assess retention impact.

**MVP Requirements and Hub Feedback**  
The minimum viable product will feature an interstitial overlay with clear communication, sound-on playback, and UI elements showing remaining video time and the skip option transitioning to an upgrade button. The newly created centralized hub was positively received, with plans to automate data updates and create experiment templates.

### Details

* **Review of Ad Interstitial Placement**: Anouk Lubbers provided an update on the decision regarding ad placement, confirming that the interstitial spot—before users enter a match—was identified as the correct and less risky moment compared to other placements. This placement was determined after a meeting with Karen, Derek, and William, and the flow was approved by Derek. The decided flow is: Homepage \> Play \> Find a Match \> Video Interstitial Modal \> System searches for a match ([00:00:51](?tab=t.rxqdbpop0dif#heading=h.m8a12yidn21w)).

* **Matchmaking Queue Time and User Perception**: The team decided to have users watch the ad completely before starting the match queueing process, rather than showing the ad during the queue time. Concerns were raised that showing the ad during the queue time could lead to the user perceiving a longer wait time, or create complications for matchmaking with separate user pools. The average queue time is noted as 35 seconds in Europe and 9 seconds outside of Europe ([00:02:39](?tab=t.rxqdbpop0dif#heading=h.rwmtp21at9vs)).

* **Interstitial Video Flow Confirmation**: The flow was confirmed as the user pressing "Find Match," watching the video interstitial, and then automatically starting the match search once the video is completed. Moritz Natalini confirmed this sequence. Anouk Lubbers noted that the UI design is crucial for teaching users about this new system ([00:03:50](?tab=t.rxqdbpop0dif#heading=h.umtlz0xltq5b)).

* **Ad Skipping Mechanism and Behavior Onboarding**: The team is considering offering users one skip per day and suggested not showing the ad for the first match to build momentum ([00:03:50](?tab=t.rxqdbpop0dif#heading=h.umtlz0xltq5b)). The ad would start showing from the second match onward, and clear UI explaining the video duration and subsequent queuing is necessary ([00:04:58](?tab=t.rxqdbpop0dif#heading=h.83zbb8rzvwi7)). The skip button would eventually turn into an "upgrade" button after the user's daily skip is used ([00:06:05](?tab=t.rxqdbpop0dif#heading=h.autej96sp5hg)).

* **Justification for Ad Requirement**: Moritz Natalini suggested that tokens to skip the ads could eventually be sold, but Anouk Lubbers stated that the current focus is on onboarding users by helping them understand that servers require funding, and payment is made via user attention. This approach is seen as fair for paying for the servers ([00:06:05](?tab=t.rxqdbpop0dif#heading=h.autej96sp5hg)).

* **A/B/C Testing Strategy**: To evaluate the effectiveness of the ad placement, an A/B/C test is planned ([00:06:05](?tab=t.rxqdbpop0dif#heading=h.autej96sp5hg)). The test will include a control group with no ads, one group with no ads on the first match, and one group where ads begin after the first match to determine the impact of the first match experience on retention ([00:07:08](?tab=t.rxqdbpop0dif#heading=h.49pdd55je6q4)).

* **Discussion on Skip Button Strategy**: Moritz Natalini expressed concern that users may not play more than two matches and suggested thinking about whether a skip button is needed for users who reach the second match. Anouk Lubbers stated that the initial idea for the minimum viable product (MVP) is one skip per day, which can be fine-tuned later ([00:07:08](?tab=t.rxqdbpop0dif#heading=h.49pdd55je6q4)).

* **Integrating Smart System Features**: The possibility of developing a "smart" system for ad skipping was discussed, which could offer an additional free skip if a user has just lost a game or made a report. This would allow for a more scalable and interesting pattern by taking the user's mental state into consideration ([00:07:57](?tab=t.rxqdbpop0dif#heading=h.6bxtgsmu6tmw)).

* **Interstitial Sound and Resolution Requirements**: It was determined that the interstitial video must start playing with the sound on because the user initiates the action by clicking. Moritz Natalini noted that users could turn the sound off afterwards ([00:09:17](?tab=t.rxqdbpop0dif#heading=h.d72yjloxqmk2)). For the minimum resolution, Moritz Natalini recommended going as full screen as possible to ensure the user understands that they cannot interact until the video is completed ([00:10:28](?tab=t.rxqdbpop0dif#heading=h.c1esxp9ndx04)).

* **Advertising Partners and Diversity**: The ad content is intended to consist of partner ads, not in-house ads, for the interstitial. Moritz Natalini confirmed that a mix of advertisers, including endemic partners like Logitech and Trade It, would likely be used ([00:10:28](?tab=t.rxqdbpop0dif#heading=h.c1esxp9ndx04)). Derek was concerned about users seeing too many of the same ads, so ad diversification and capping the frequency were established as essential requirements for a positive user perception ([00:11:50](?tab=t.rxqdbpop0dif#heading=h.qt1xb3yop4xp)).

* **Summary of MVP Interstitial Concept and Next Steps**: The MVP will feature an interstitial overlay with clear upfront communication that the ad will play with sound on. The interstitial modal will include UI elements for turning off sound, showing the remaining video time, and explaining the skip option that transitions to an upgrade button. Anouk Lubbers will work on the concept design and share it for a follow-up meeting with Moritz Natalini and Karen ([00:12:49](?tab=t.rxqdbpop0dif#heading=h.suuxwiyq7kr7)).

* **Prioritization and Development Oversight**: Moritz Natalini emphasized that the interstitial feature is a P0 priority ([00:14:49](?tab=t.rxqdbpop0dif#heading=h.p4oyaeekhqvs)). They plan to work on the necessary guardrail metrics before development starts and will brief Theo once they are satisfied with the design ([00:16:19](?tab=t.rxqdbpop0dif#heading=h.2cw6enl0k4a2)).

* **Feedback on the AI-Created Hub**: Anouk Lubbers and Karen expressed positive feedback on the new hub, with Anouk Lubbers stating that they love it because it allows them to check data frequently and catch user feedback or make improvements during tests ([00:16:19](?tab=t.rxqdbpop0dif#heading=h.2cw6enl0k4a2)). Moritz Natalini confirmed that the hub needs team input for improvement, such as feedback on the layout, as it is intended to be a centralized, automated tool for everyone ([00:17:30](?tab=t.rxqdbpop0dif#heading=h.6jxkabtehg5g)).

* **Hub Functionality and Future Template Development**: The long-term plan for the hub includes centralization of project information, updates on ongoing projects, and a dashboard for checking the latest details. The goal is to create a template for experiments that provides a brief, links to the design dashboard, and the Figma file. Isabel will assist in automating data updates every 24 hours ([00:18:22](?tab=t.rxqdbpop0dif#heading=h.wqy0ewxz5l4)).

### Suggested next steps

- [ ] \[Anouk Lubbers\] Create Concept: Develop interstitial concept today. Share concept with Moritz Natalini today.

- [ ] \[Moritz Natalini\] Define Metrics: Develop guardrail metrics and related items. Ensure team alignment before development begins.

- [ ] \[The group\] Brief Theo: Brief Tio on final design concept. Wait for design approval before briefing Tio.

- [ ] \[Isabel\] Automate Data: Automate data updates for the project hub. Ensure data refreshes every 24 hours.

- [ ] \[Moritz Natalini\] Discuss Hosting: Discuss hub hosting location and method. Coordinate with Tio and Isa to finalize deployment strategy.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=OUuenL__DjKExcWqbmDVDxIQOAIIigIgABgDCA&detailid=standard)*