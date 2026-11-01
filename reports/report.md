# evalkit report

Generated 2026-11-01 19:16 from 12 questions and 17 responses (observed_2026-10.jsonl, demo_synthetic.jsonl).

## Summary by model

| Model | Responses | Score | correct | partial | distractor | no_answer | wrong |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Opus 5 (claude.ai chat, web search on) | 3 | 67% | 2 | 0 | 0 | 1 | 0 |
| Gemini app (Flash-Lite) | 1 | 0% | 0 | 0 | 1 | 0 | 0 |
| Google Search AI Overview | 1 | 0% | 0 | 0 | 0 | 1 | 0 |
| demo-model (synthetic) | 12 | 54% | 6 | 1 | 3 | 1 | 1 |

## Automatic scorer vs human labels

The automatic label matched the human label on 5 of 5 hand-labelled responses.

- **q01 / Claude Opus 5 (claude.ai chat, web search on):** auto `correct`, human `correct` (match). Correct date with the full chain of reasoning.
- **q01 / Gemini app (Flash-Lite):** auto `distractor`, human `distractor` (match). Found the right article but answered with the partner's own death year instead of the Halifax architect's.
- **q02 / Google Search AI Overview:** auto `no_answer`, human `no_answer` (match). Claimed the figure is not in public records, which is false (City of Johannesburg report), and offered the modern figure instead.
- **q02 / Claude Opus 5 (claude.ai chat, web search on):** auto `no_answer`, human `no_answer` (match). Honest abstention; correctly identified the hospital but did not find the appendix.
- **q03 / Claude Opus 5 (claude.ai chat, web search on):** auto `correct`, human `correct` (match). Correct. Also flagged the foundation-stone conflict between sources.

## Failures in detail

### q01 / Gemini app (Flash-Lite): `distractor`

**Question:** Gandhi's friend, the architect Hermann Kallenbach, had a Scottish-born business partner who left Johannesburg for Canada in 1912 and later worked in the office of an architect based in Halifax, Nova Scotia. On what date did that Halifax architect die?

**Golden answer:** 2 June 1943  
**Model said:** The Scottish-born business partner referred to is Alexander McFarlane Kennedy (born 1879), who partnered with Hermann Kallenbach in Johannesburg from 1909 to 1912 before moving to Canada and working in a Halifax architec...  
**Flags:** mentions_distractor:1967|1879

**Evidence:**
- [Brass Plaque reveals a history of a distinguished man and his architectural firm (The Heritage Portal, Munro & Lev, 2020)](https://www.theheritageportal.co.za/article/brass-plaque-reveals-history-distinguished-man-and-his-architectural-firm): "Later Kennedy returned to his profession and worked in the office of the well-known Canadian architectural practice of A R Cobb."
- [Andrew Randall Cobb (The Canadian Encyclopedia)](https://thecanadianencyclopedia.ca/en/article/andrew-randall-cobb): "Andrew Randall Cobb, architect (b at Brooklyn, NY 13 June 1876; d at Halifax 2 June 1943)."

*Note:* 1967 is the partner Kennedy's own death year, a tempting wrong entity.

### q02 / Google Search AI Overview: `no_answer`

**Question:** The public teaching hospital in Auckland Park, Johannesburg, that was renamed in 1997 after the anti-apartheid activist Helen Joseph first opened in 1967 under a different name. How many beds did it have when it opened?

**Golden answer:** 80  
**Model said:** The exact number of beds the J.G. Strijdom Hospital (now known as the Helen Joseph Hospital) had when it first opened in 1967 is not specified in historical or public records available from the search results, though the...  
**Flags:** mentions_distractor:639, abstained

**Evidence:**
- [Heritage inventory 7.4.1 Helen Joseph Hospital (City of Johannesburg)](https://ags.joburg.org.za/StoryMaps/Heritage/Corridors/Empire-Perth/pdf/7.4.6KP.pdf): "The former JG Strijdom Hospital was renamed after struggle icon Helen Joseph"
- [HIA & CMP Knowledge Precinct Vol. 3, Appendix B (tsica heritage consultants for City of Johannesburg)](https://www.theheritageportal.co.za/sites/default/files/notice%20attachments/HIA%20&%20CMP_Knowledge%20Precinct_Vol3.pdf): "J.G. Strijdom Hospital opened with 80 beds"

*Note:* 639 is the modern bed count. The opening figure appears only in a timeline appendix.

### q02 / Claude Opus 5 (claude.ai chat, web search on): `no_answer`

**Question:** The public teaching hospital in Auckland Park, Johannesburg, that was renamed in 1997 after the anti-apartheid activist Helen Joseph first opened in 1967 under a different name. How many beds did it have when it opened?

**Golden answer:** 80  
**Model said:** I couldn't pin that number down. The hospital is Helen Joseph, which opened in 1967 as the J.G. Strijdom Hospital and was renamed on 1 April 1997 after Helen Joseph, but none of the sources I checked state a bed count fo...  
**Flags:** mentions_distractor:639, abstained

**Evidence:**
- [Heritage inventory 7.4.1 Helen Joseph Hospital (City of Johannesburg)](https://ags.joburg.org.za/StoryMaps/Heritage/Corridors/Empire-Perth/pdf/7.4.6KP.pdf): "The former JG Strijdom Hospital was renamed after struggle icon Helen Joseph"
- [HIA & CMP Knowledge Precinct Vol. 3, Appendix B (tsica heritage consultants for City of Johannesburg)](https://www.theheritageportal.co.za/sites/default/files/notice%20attachments/HIA%20&%20CMP_Knowledge%20Precinct_Vol3.pdf): "J.G. Strijdom Hospital opened with 80 beds"

*Note:* 639 is the modern bed count. The opening figure appears only in a timeline appendix.

### q01 / demo-model (synthetic): `partial`

**Question:** Gandhi's friend, the architect Hermann Kallenbach, had a Scottish-born business partner who left Johannesburg for Canada in 1912 and later worked in the office of an architect based in Halifax, Nova Scotia. On what date did that Halifax architect die?

**Golden answer:** 2 June 1943  
**Model said:** The Halifax architect was Andrew Cobb, who died in 1943.  
**Flags:** none

**Evidence:**
- [Brass Plaque reveals a history of a distinguished man and his architectural firm (The Heritage Portal, Munro & Lev, 2020)](https://www.theheritageportal.co.za/article/brass-plaque-reveals-history-distinguished-man-and-his-architectural-firm): "Later Kennedy returned to his profession and worked in the office of the well-known Canadian architectural practice of A R Cobb."
- [Andrew Randall Cobb (The Canadian Encyclopedia)](https://thecanadianencyclopedia.ca/en/article/andrew-randall-cobb): "Andrew Randall Cobb, architect (b at Brooklyn, NY 13 June 1876; d at Halifax 2 June 1943)."

*Note:* 1967 is the partner Kennedy's own death year, a tempting wrong entity.

### q03 / demo-model (synthetic): `distractor`

**Question:** The Lithuanian-born architect who bought the farm near Johannesburg that Gandhi named after Leo Tolstoy also designed, with his business partner, a Dutch Reformed church in Johannesburg whose foundation stone was laid by General Koos de la Rey. On what date was the first service held in that church?

**Golden answer:** 26 January 1907  
**Model said:** The foundation stone was laid on 2 May 1906.  
**Flags:** mentions_distractor:2 May 1906

**Evidence:**
- [Brass Plaque reveals a history of a distinguished man and his architectural firm (The Heritage Portal, Munro & Lev, 2020)](https://www.theheritageportal.co.za/article/brass-plaque-reveals-history-distinguished-man-and-his-architectural-firm): "The best known works of this partnership were the Fairview Dutch Reform Church, in Op den Bergen Street and the St Andrews Presbyterian Church on Commissioner Street."
- [Dutch Reformed Church of Fairview blue plaque (Johannesburg Heritage Foundation)](https://www.theheritageportal.co.za/node/5183): "General de la Rey laid the foundation stone on 2 May 1906 and the first service was held on 26 January 1907."

*Note:* Sources disagree on the foundation-stone date (2, 5 or 7 May 1906), so the question asks about the first service instead.

### q05 / demo-model (synthetic): `wrong`

**Question:** The first Greek Orthodox church in Johannesburg was designed in the Byzantine style by an architect who was a close friend of Gandhi. How much, in pounds sterling, did its construction cost?

**Golden answer:** 3300  
**Model said:** It cost about £5,000 to build.  
**Flags:** none

**Evidence:**
- [Cathedral of Sts. Constantine and Helen (Wikipedia)](https://en.wikipedia.org/wiki/Cathedral_of_Sts._Constantine_and_Helen): "The community took six years to raise the £3,300 for the building"

### q07 / demo-model (synthetic): `distractor`

**Question:** When planning the Second World War military hospital at Baragwanath near Johannesburg, the bed provision was raised above the original plan because of the war in the Middle East. How many beds was provision finally made for?

**Golden answer:** 1544  
**Model said:** Provision was made for 1,200 beds.  
**Flags:** mentions_distractor:1200

**Evidence:**
- [Imperial Military Hospital, Baragwanath (Wikipedia)](https://en.wikipedia.org/wiki/Imperial_Military_Hospital,_Baragwanath): "it was then decided to make provision for 1,544 beds (instead of 1,200)"

### q09 / demo-model (synthetic): `no_answer`

**Question:** Coronation Hospital in Johannesburg, opened in 1944, was later renamed after the activist Rahima Moosa. On what date was it renamed?

**Golden answer:** 29 September 2008  
**Model said:** I don't know the exact date of the renaming.  
**Flags:** abstained

**Evidence:**
- [Rahima Moosa Mother and Child Hospital (Wikipedia)](https://en.wikipedia.org/wiki/Rahima_Moosa_Mother_and_Child_Hospital): "On 29 September 2008, Coronation Hospital was renamed the Rahima Moosa Mother and Child Hospital"

### q12 / demo-model (synthetic): `distractor`

**Question:** In which Scottish town was Hermann Kallenbach's long-time architectural partner Alexander McFarlane Kennedy born?

**Golden answer:** Stirling  
**Model said:** Kennedy was born in Glasgow.  
**Flags:** mentions_distractor:Glasgow

**Evidence:**
- [Brass Plaque reveals a history of a distinguished man and his architectural firm (The Heritage Portal, Munro & Lev, 2020)](https://www.theheritageportal.co.za/article/brass-plaque-reveals-history-distinguished-man-and-his-architectural-firm): "He was born in Stirling, Scotland in 1879, making him some eight years younger than Kallenbach."
