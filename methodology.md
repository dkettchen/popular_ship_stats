# METHODOLOGY

This document outlines the various methodologies I used to categorise, rename, and tag data from the original data sets as well as data I researched and added myself.

I shall refer to the original poster of the ao3 ship ranking data as "OP" in this document and any relevant notes.

Work in progress!


## Fandoms:

- If multiple fandoms are part of one franchise (adaptations, multiple installations, spinoffs, etc) or otherwise set in the same universe/multiverse they get grouped under one fandom label. 

    > Ex. DC characters appear across many different media types and storylines/series within them, so a fic tagged say "Batman/Joker" cannot be inferred to be about any specific instance, it can only be inferred that they are DC characters.

    > Ex. House of the Dragon is a Game of Thrones spin-off, so they both are set in the Game of Thrones Universe.

    > Ex. The One Piece manga, anime, and netflix live action series are all adaptations of the same story, so the fandom is One Piece, not any specific adaptation/release year.

- For non-english media, where possible and where OP hadn't already, I added the original title/spelling to the english translation, separated by a "|" (following OP's format). If OP's version was misspellt or formatted differently I corrected this.

    > Ex. Free! doesn't have a japanese title, so it remains as is.

    > Ex. My Hero Academia's japanese title was listed in roman characters by OP, so it gets changed to the actual kanji/kana version.

    > Ex. Omniscient Reader didn't have its korean title in OP's version, so it was added.

    > Ex. Heaven Official's Blessing did have its chinese title in the proper characters, but only had the roman letter version of said chinese title as a "translation" in OP's version. This was replaced with the actual english title.

- I also put the translation second, so fandoms could be sorted alphabetically without worrying about special characters getting in the way.

    > Ex. "Attack on Titan | 進撃の巨人" rather than "進撃の巨人 | Attack on Titan"

- If a media piece has two (or more) relevant titles (like f.e. a book's original title vs its TV adaptation's different title) both titles are included in the new fandom name, separated by a forward slash.

    > Ex. Game of Thrones is an adaptation of the A Song of Ice and Fire book series, so it becomes "A Song of Ice and Fire / Game of Thrones"

    > Ex. For media with multiple translated titles, this formatting still applies, merely grouping by language like so: "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令"

- Any inconsistent formatting, like added specified media types, release years, sub titles, or author names, was removed from the fandom names.

    > Ex. Author names were separated into their own attribute where present.

    > Ex. Anything in brackets (eg "Supernatural (TV 2005)") was removed.

    > Ex. Sub titles/roman numerals/numbers/etc denoting different instances of one franchise (eg "Final Fantasy X", "Persona 5" "Avatar: The Legend of Korra") were removed to group them together as a franchise instead.

- All Real Person Fic (RPF) was identified and tagged as such, as some of it was not explicitly labelled in the original data sets.

    > Ex. Most bands/musicians were not labelled as RPF, despite obviously referring to real people.

    > Ex. Youtuber/Online Creator RPF was not consistently labelled.

- RPF was grouped by fandom and category similarly to fictional fandoms. 

    > Ex. Various different bands/musicians have their own fandom, but are all Music RPF.

    > Ex. OP's various Women's soccer RPF spellings were grouped together under one label.

    > Ex. Actor RPF has been grouped by associated fandom, same as fictional part of that fandom.


## Characters:

### Names:

- Any inconsistent formatting, like brackets*, translations, etc were removed from character names.

    > *Brackets were re-included for Venom (Symbiote) from Marvel, and the two Connor models (RK800 & RK900) from Detroit: Become Human.

- Where aliases were obviously missing, like in any superhero property, they were looked up and added.

    > Ex. OP had Magneto simply as "Erik Lehnsherr", I have changed this to "Erik Lehnsherr | Magneto" for clarity and completeness

- All names were split into their parts, categorised (ie given name, surname, nickname, do they follow eastern or western order, etc), and saved in their individual parts. The util function `add_full_name` then reassembles these parts in order. 

    > `add_full_name` has some built in exceptions for characters like f.e. "Anakin Skywalker | Darth Vader", whose alias has a ""title"" (Darth) and his individual Sith ""name"" (Vader), hence does not follow the normal order of "Title Given-name Surname | Alias" the function would assume. Please consult the code for all of these exceptions.

### Demographic info (gender & race tags):

- Use OP's method for the most part (so we can reuse their tags) 

    > **OP's [2023 FAQ](https://archiveofourown.org/works/49183780/chapters/124101343) outlining their methodology** 

    > **Please note that in some cases even OP doesn't seem to keep to their own methodology:** Ex. Sanji One Piece's live action actor, Taz Skylar, is british-arab. One Piece is set in a fantasy world, hence has no means of explicitly stating Sanji's real-world race (I have watched all of One Piece, I would know if it had happened). According to OP's method that would mean tagging Sanji as MENA (because, without explicit mention in canon, non-white part of live action actor's race takes priority over both canon context implications and word of god), but he is still (imo correctly) tagged as white in their latest data sets.

- If there are multiple main canon adaptations of a thing, even if OP's data mostly was tagged as one over the rest, we will still consider the rest, unlike OP

    > Ex. Scarlet Witch is explicitly of romani origin in the comics, but was tagged as white due to her MCU casting. I'm retagging her as romani as the MCU is not explicit about her heritage (neither confirming nor denying it past her fictional east-european country of origin), so I'm defaulting to explicit canon mention of the character's (non-White) race (in line with OP's method), which happens to be in the comic version in this case, over the actress' real life category.

- I don't think it's useful/helpful, diversity-statistically, to imply someone is more explicit minority rep than they actually are

    - If a real human being is *majority* white (ie more than 1/2) and not obviously non-white-passing or (publicly visibly) very involved in the relevant community's advocacy/cultural practices/etc, I will tag them as "White (mixed)" instead of their non-white group.

    - If someone is genderqueer/genderquestionable but generally aligned with one gender over the other, I will mark them as their gender leaning as well as Other (ie "M | Other").

        > Ex. Technically genderless but strongly male/female coded characters (like the Crystal Gems from Steven Universe).

        > Ex. Shapeshifters who usually go by one gender over the other (like Crowley from Good Omens).

        > Ex. Characters who are treated as male/female in one adaptation while more nb in another (like Loki from Marvel).

        > Ex. Characters or real life people who use biased multi-pronoun sets in english (ie they/he, she/they, etc) or have otherwise stated to be binary-leaning nbs (like Gerard Way).

    - The implied context of the character takes priority over the actor's attribute, reversing the order of OP's priority list, *where reasonable to.*

        - If the casting choice seems to have been made in line with the canon implied race rather than in contrast with it, I will tag it according to the implied race.

            > Ex. Real world historical context where it'd be highly unlikely for them to be the actor's specific config (like Hob (a random 14th century british white man turned immortal) from Sandman, whose actor is 1/4 south asian and who OP tagged as Asian because of that).

            > Ex. Fantasy setting where it's hard to explicitly state real world racial alignments (like Sanji One Piece).

        - If the casting choice was purposefully made with that contrast in mind, I will tag it according to the actor's race.
        
            > Ex. If the story implies that a character is white but they are played by an obviously non-white actor (like say in Hamilton), the actor's race obviously still takes priority.

    - If that actor is themself in the ranking, they'd be tagged according to the usual rules 
    (hence may differ from their character's tags).

    > -> by using tags like "White (mixed)" or "M | Other" I can mark diversity where it exists without misrepresenting/overstating it (as I, as a minority person myself, do not appreciate when ppl do that while I'm still over here with no actual rep for the thing I am smh)

- Only if a character is canonically/a person irl is currently IDed as (middle-spec/non-leaning) nonbinary/genderless will I only tag them as "Other".

    > Ex. A character or real life person who only uses they/them / other languages' neutral pronouns / consistently omits gendered language (like some anime characters do in japanese) - (like Raine Whispers (they/them) from Owlhouse).

    > Ex. A character who is canonically nb/gender-questionable/genderless and played by a nb-IDed actor (like Desire from Sandman).

    > Ex. A non-human character of a species without gender (like the Venom Symbiote).

- If it is a reader or player character they are tagged as "Ambig" unless OP's data specifies one gender over another for a rank.

    > Ex. "Female Shepard" in the original data set.

- If both male and female could be argued to be a correct labelling based on context they will be labelled as "M | F | Other".

    > Ex. Cis male drag queens in the femslash ranking.

- If race isn't explicitly stated, there isn't a relevant live action adaptation, and context, voice actors, etc are conflicting to the point of me not knowing what to go with, the character's race will be tagged as "Ambig".

- If the character has never been portrayed in visual media and is not clearly implied or established to be of a specific group, their race will be tagged as "Unknown".

- According to oxford dictionary "Latin" includes anyone from latin-language countries, so I'm including the south european ones in that (eg Portugal, Italy, etc).


## N.B.: 

There may remain inaccuracies in the data as it's a shitton of characters and while I looked up most of them & combed their wikis for relevant info I'm just one guy (same as OP is just one person) and I may have overlooked some details in any info I added/relabelled/completed.

However hopefully these discrepencies should be minor and not scew the general trends of the data.

