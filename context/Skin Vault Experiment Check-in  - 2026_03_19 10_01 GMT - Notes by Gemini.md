Mar 19, 2026

## Skin Vault Experiment Check-in 

Invited [Moritz Natalini](mailto:m.natalini@efg.gg) [Teodor Kuzmanov](mailto:t.kuzmanov@efg.gg) [Isabel Diezma Pérez](mailto:i.diezma-perez@efg.gg) ~~[Anouk Lubbers](mailto:a.lubbers@efg.gg)~~

Attachments [Skin Vault Experiment Check-in ](https://www.google.com/calendar/event?eid=M2syaTFnN2g3NTY5ZWc1MzNpZXU1cmxidnMgbS5uYXRhbGluaUBlZmcuZ2c) 

Meeting records [Transcript](?tab=t.2cvd5a9eq8sr) 

### Summary

Experiment launch review discussed low traffic and backend success with concerns for Steam rate limiting and user ID tracking.

**Experiment Status and Access**  
The experiment launched on 300 top-viewed player profiles, and internal users must be manually added to the database to expose their profiles for gradual inventory processing. Backend success was achieved due to extensive preparation, but potential future scalability limitations were noted.

**Steam Rate Limiting Concerns**  
Potential Steam rate limiting issues were identified, possibly due to Steam aggregating calls by IP address, which prompted the preparation of dashboards to monitor call volume. Low current traffic, only 626 users visited the page, was attributed to the experiment launching early in the week with traffic expected over the weekend.

**Tracking and Traffic Planning**  
Difficulty was noted in querying profile ID for tracking, leading to the suggestion of sending the entire page URL, which includes the user nickname as an identifier. The decision was made to gather feedback data from the 'feedback collector V1' and 'clicks V1' events and then determine the next steps.

### Details

* **Experiment Status and Internal User Access**: Moritz Natalini provided a recap of the experiment, which launched on Monday, noting that the top 300 most-viewed players have exposed the feature on their profiles. Isabel Diezma Pérez clarified that internal users who want their profiles exposed must be added manually to the database, even though the feature flag is enabled, to allow for gradual processing of inventory items. Teodor Kuzmanov confirmed that the manual addition is primarily for their profile to be exposed, not necessarily to see everyone else's profile ([00:01:07](?tab=t.2cvd5a9eq8sr#heading=h.3u7ffgbd0jt2)).

* **Concerns Regarding Steam Rate Limiting**: Isabel Diezma Pérez reported speaking with Lorenzo about potential rate limiting issues in Steam calls, even though the team uses public APIs and Lorenzo's team uses authenticated APIs. It is possible that Steam is aggregating calls by IP address, which could affect both teams' rate limiting, leading Isabel Diezma Pérez to start preparing dashboards for visibility into their team's call volume ([00:02:24](?tab=t.2cvd5a9eq8sr#heading=h.xpofsfs69mzl)). Moritz Natalini acknowledged this as an interesting find ([00:03:26](?tab=t.2cvd5a9eq8sr#heading=h.t88fu4rkahgj)).

* **Backend Success and Future Scalability**: Moritz Natalini expressed happiness with the backend's overall success, which they attributed to the extensive preparation by Isabel Diezma Pérez. However, Isabel Diezma Pérez expressed concern that if the feature is a success, they might not be able to expand it to more users due to limitations, which Moritz Natalini stated they would figure out later. Moritz Natalini then requested the feature flag name and information on where to track user sentiment and feedback ([00:03:26](?tab=t.2cvd5a9eq8sr#heading=h.t88fu4rkahgj)).

* **Monitoring Traffic and Querying Data**: Teodor Kuzmanov confirmed they would add the feature flag name to the tracking document. Moritz Natalini noted that traffic was currently low, with only 626 users having visited the page. Isabel Diezma Pérez suggested filtering or grouping by user ID to determine if a few specific users were driving the attention ([00:04:34](?tab=t.2cvd5a9eq8sr#heading=h.h5zaluo0y2ak)).

* **Challenges in Identifying Profile IDs for Tracking**: Moritz Natalini and Isabel Diezma Pérez discussed the difficulty in querying the profile ID, as they were only sending the user ID, which sometimes appears empty, potentially indicating anonymous users ([00:08:04](?tab=t.2cvd5a9eq8sr#heading=h.ip4zc5fnwp1f)). Teodor Kuzmanov suggested that they could send the whole page URL as part of the page view event, which includes the user nickname and acts as an identifier for the skin page ([00:09:12](?tab=t.2cvd5a9eq8sr#heading=h.zgkhlskjd820)). Moritz Natalini found that some users, likely internal ones, were viewing their own profiles repeatedly ([00:10:37](?tab=t.2cvd5a9eq8sr#heading=h.e0lqdpayyy2f)).

* **Low Traffic and Weekend Planning**: Isabel Diezma Pérez pointed out that the traffic is low partly because the experiment launched on Monday, and most of the traffic is expected on the weekend. Moritz Natalini agreed that they should consider publishing something to boost traffic over the weekend. Moritz Natalini planned to talk with Karen about ways to increase awareness, as putting a call to action (CTA) on the homepage is complicated because the feature is not released to 100% of users, and they do not know which users are in the experiment ([00:14:38](?tab=t.2cvd5a9eq8sr#heading=h.xw12mzkrgry8)).

* **Experiment Takeaways and Feedback Tracking**: Moritz Natalini concluded that the key takeaways were low traffic, noting it has only been three or four days, and they need to check traffic over the weekend, emphasizing that if traffic does not improve, the experiment is not working ([00:15:54](?tab=t.2cvd5a9eq8sr#heading=h.xif25azbn4in)). Teodor Kuzmanov identified two events for tracking user feedback: \`feedback collector V1\` and \`clicks V1\`. Moritz Natalini decided to gather the data from these sources and determine the next steps ([00:16:55](?tab=t.2cvd5a9eq8sr#heading=h.vqzj7qgtaefl)).

### Suggested next steps

- [ ] Moritz Natalini will think about adding more internal users to the database for testing.

- [ ] Teodor Kuzmanov will add the feature flag name to the tracking document.

- [ ] Moritz Natalini will talk with Karen to get their thoughts on addressing the low traffic.

- [ ] Moritz Natalini will gather the experiment data and follow up with the next steps.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=xXDNyGVez_meTqPIYmQWDxIVOAIIigIgABgDCA&detailid=standard)*