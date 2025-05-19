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

    - If someone is genderqueer/genderquestionable but generally aligned with one gender over the other, I will mark them as their gender leaning as well as Other (ie "M | Other").

        > Ex. Technically genderless but strongly male/female coded characters (like the Crystal Gems from Steven Universe).

        > Ex. Casual gender switchers who usually go by one gender over the other (like Crowley from Good Omens or Sailor Uranus from Sailor Moon).

        > Ex. Characters who are treated as male/female in one adaptation while more nb in another (like Loki from Marvel).

        > Ex. Characters or real life people who use biased multi-pronoun sets in english (ie they/he, she/they, etc) or have otherwise stated to be binary-leaning nbs (like Gerard Way).

    - If a real human being is *majority* white (ie more than 1/2) and not obviously non-white-passing or (publicly visibly) very involved in the relevant community's advocacy/cultural practices/etc, I will tag them as "White (Multi)" instead of their non-white group.

    - The implied context of the character takes priority over the actor's attribute, reversing the order of OP's priority list, *where reasonable to.*

        - If the casting choice seems to have been made in line with the canon implied race rather than in contrast with it, I will tag it according to the implied race.

            > Ex. Real world historical context where it'd be highly unlikely for them to be the actor's specific config (like Hob (a random 14th century british white man turned immortal) from Sandman, whose actor is 1/4 south asian and who OP tagged as Asian because of that).

            > Ex. Fantasy setting where it's hard to explicitly state real world racial alignments (like Sanji One Piece).

        - If the casting choice was purposefully made with that contrast in mind, I will tag it according to the actor's race.
        
            > Ex. If the story implies that a character is white but they are played by an obviously non-white actor (like say in Hamilton), the actor's race obviously still takes priority.

    - If that actor is themself in the ranking, they'd be tagged according to the usual rules (hence may differ from their character's tags).

    > -> by using tags like "White (Multi)" or "M | Other" I can mark diversity where it exists without misrepresenting/overstating it (as I, as a minority person myself, do not appreciate when ppl do that while I'm still over here with no actual rep for the thing I am smh)

- Only if a character is canonically/a person irl is currently IDed as (middle-spec/non-leaning) nonbinary/genderless will I only tag them as "Other".

    > Ex. A character or real life person who only uses they/them / other languages' neutral pronouns / consistently omits gendered language (like some anime characters do in japanese) - (like Raine Whispers from Owl House).

    > Ex. A character who is canonically nb/gender-questionable/genderless and played by a nb-IDed actor (like Desire from Sandman).

    > Ex. A non-human character of a species without gender (like the Venom Symbiote).

- If it is a reader or player character they are tagged as "Ambig" unless OP's data or available wiki info specifies one gender over another.

    > Ex. "Female Shepard" for some ranks in the original data set.

    > Ex. The protagonist/player character of Persona 5 is male.

- The same logic applies to player characters' race: If their appearance can be customised, they will be tagged as "Ambig", if they have a set appearance, they will be tagged as appropriate.

    > Ex. Genshin Impact's Traveler, Fire Emblem's Byleth, and Persona 5's Amamiya Ren's appearances cannot be customised, hence are tagged according to the usual rules.

    > Ex. Dragon Age and Mass Effect's player characters can be customised, so they are tagged as "Ambig".

- If both male and female could be argued to be a correct labelling based on context they will be labelled as "M | F | Other".

    > Ex. Cis male drag queens in the femslash ranking.

- I added specificity for Asian and Indigenous folks.

    - For asian folks I differentiated between East ("E Asian"), South East ("SE Asian"), South ("S Asian"), and Central asians ("Central As") (as I think it's highly relevant to track this difference with this many east asian properties in the set).

    - For indigenous folks I differentiated between peoples from (so far I believe only north) America ("Am Ind"), Asia ("As Ind"), Europe ("Eu Ind"), and Polynesia ("Māori Ind", as they were all specifically Māori so far and I couldn't find a good way to shorten polynesian 😅).

- I relabelled "Latino" to "Latin" to make it genderneutral, as there are plenty of latin women in the set.

- According to the Oxford dictionary "Latin" as a group includes anyone from latin-language countries, so I'm including the south european ones in that (eg Portugal, Italy, etc), with the exception of the non-southern-aligned parts of say France and Switzerland.

    > Ex. Italian figure skater Sara from Yuri On ICE!! will be tagged as Latin (OP had tagged her as White).

    > Ex. Parisian Chat Noir from Miraculous will still be tagged as White as Paris is in northern France.

- I also added "Romani" as a label, for our romani characters.

    > Those being one of DC's Robins (who I believe was only in one of the early sets where race was not tracked yet) and Marvel's Scarlet Witch (who OP had tagged as white due to MCU casting).

- I also added "SE Eu" as a label, for the region around Greece, Turkey, etc.

    > As they are not latin-language countries, but also not in the middle east yet, but they are like right in between those other two mediterranean regions, and we have some folks with that ancestry in the set.

- For multiracial folks *(where information on their racial background is available)*:
    
    - If someone is white + non-white, and the non-white part is >= 1/2, and/or they are easily identifyable as their non-white group, they will be tagged as "< non-white group > (multi)", staying in line with OP's original method prioritising non-white ancestry.

        > Ex. The MCU's MJ (played by Zendaya) would be "Black (Multi)", because she is biracial (black & white).

    - If someone is majority white, they will be tagged as "White (multi)" (see above for more details).

    - If someone is less than 1/4 of a different group than their main one I am not counting it.

        > Ex. Josh Dun's great-great-great-grandmother was japanese. I am tagging him as "White", cause that is too many generations removed.

    - If we only know of one group and that they are multiracial of some variety, they will be tagged as "< group in question > (Multi)", same as above.

    - If someone is of multiple non-white groups (that can't reasonably be grouped together), they will be tagged as "< group a > / < group b > (Multi)", groups listed in alphabetical order.

        > Ex. "Am Ind / E Asian (Multi)", because those ancestries are from fully different continents.

    - If they can reasonably be grouped together under an umbrella term, they will be tagged as such instead of listing each group separately.
        
        > Ex. "Asian (Multi)" instead of say "E Asian / SE Asian / S Asian (Multi)".
    
    - I am leaving "Af Lat" folks as such, as to my understanding Latin is a largely cultural label encompassing lots of different ancestries, so someone who is afro-latin may just be black (ancestry-wise) & *from a latin country*, same as white latin folks, hence can't inherently be assumed to be multiracial.

        > For this same reason I also didn't add specifics to the Latin label, as I did with the Asian and Indig ones, as I couldn't come up with any meaningful logic by which to separate it into subgroups (with the available info), unlike region-specific asian & indigenous subgroups.

- If race isn't explicitly stated, there isn't a relevant live action adaptation, and context, voice actors, etc are conflicting to the point of me not knowing what to go with, the character's race will be tagged as "Ambig".

- If the character has never been portrayed in visual media and is not clearly implied or established to be of a specific group, their race will be tagged as "Unknown".

- If the character was alluded to being a certain highly underrepresented identity/label that is not established in the actual piece of media, casting, or *explicitly* confirmed by the creator (notably when there are plenty of actual canon [same or similar minority] characters in the piece of media in question), I will not count it.

    > Ex. Perfuma's character designer apparently said in a post that she was designed to be read as transgender, and Nate Stevenson liked a tweet once that called her a trans lesbian, but neither of these explicitly confirm her as canonically *being* trans, nor does the actual show or casting (she's voiced by a cis woman - the T-based first puberty needed to *look* trans (as per character design) also changes your voice, so voice plays a major role in any character audiovisually "reading" as a trans woman) establish it in any way. <br>
    -> I do not consider Perfuma to be trans for "Are there (binary/medically) trans characters in the data set?" analysis purposes as the only way to even find this out is via a niche reference on a wiki (not the actual show or casting), while other trans characters in the represented fandoms *are* actually explicitly, in-show-established, and even cast as trans, but those didn't make the ranking.

## Ships:

### Ship labels

- I used "x" as a delimiter for slash ships rather than "/", because I ended up using slashes in my name formatting and I wanted to avoid confusion (and I personally am more used to the x notation than the slash one).

- I am aware that some people use "x" as a means to indicate relationship dynamics via name order (ie who is a top or a bottom), I do not use it that way (Idk which order means which anyway 😅), so here they are all simply in alphabetical order, with no comment on dynamics intended by it.

- I kept OP's "&" notation for general/non-slash ships and listed all ships in my ship table file with both their slash- and their general-formatted label.

- I tagged all ships in the rankings with whether they were gen or slash ships, and extracted the eliminated gender combination to its own value on the ship table instead.

### Combo labels

- I collected the demographic combinations of the ships according to their new (alphabetical) order.

- For two character ships I collected their gender labels, regardless of contents.

    > Ex. Same-sex pairings are tagged as "M / M" or "F / F" and straight pairings as "F / M" or "M / F".

    > Ex. Eddie Brock and Venom are tagged as "M / Other" rather than just "Other".

    > Ex. Sailor Neptune and Sailor Uranus are tagged as "F / F | Other" rather than just "F / F" or "Other".

- If all characters were of the same racial group, I only tagged them once.

    > Ex. A 4-way ship of white minecraft youtubers will be tagged as "White", not "White / White / White / White" (cause that feels silly).

    > Ex. Princess Bubblegum and Marceline are tagged as "N.H." rather than "N.H. / N.H.".

- For same-sex poly ships, I kept it as "M / M" or "F / F".

    > Ex. The Amphibia girls' 3-way ship is tagged as "F / F".

- For any poly ships whose labels weren't all the same I collected all labels rather than consolidating repeats.

    > Ex. "Black / White / White" rather than "Black / White".

    > Ex. "M / M / F" rather than "Poly" or "M / F".



## Additional data:

### Geography:

- Countries were assigned based on where the fandom's (main) pieces of media, its author, or the real life humans being RPF shipped are from. 

- If there is an original version with later english/american adaptation, and no specification on which version is meant, the original version is counted, notably if the original's country of origin is under- or not yet represented.

    > Ex. The Witcher's original book version is by a Polish author and was written in Polish, so The Witcher franchise' country of origin is Poland, even though the games and live action show are not.

- If only a specific version is listed, only that version's country will be counted.

    > Ex. RuPaul's Drag Race has various versions, including the american original and the UK version, but only american queens made the ranking, so it is counted as american.

- If multiple countries collaborated on the piece of media, or the RPF fandom is made up of people from multiple countries, the fandom will be counted as belonging to all countries involved, regardless of how much or little they contributed.

    > Ex. One Direction has one irish member, so they count as Ireland / UK.

    > Ex. Power Rangers was a collaboration between America and Japan, so it is counted as Japan / USA.

- Languages are assigned based on countries of origin, even if the translation is more popular, unless the media in question is originally made/published in another language.

    > Ex. Final Fantasy enjoys international fame due to being translated into many other languages, but is counted as Japanese.

    > Ex. A french studio under a japanese company made Life is Strange, but the game was released in English, so its language is English.

- For continents, I did not bother differentiating between North, Middle, and South America, as only the US, Canada, and Mexico are represented to begin with, and the latter is only represented by a single youtuber (ie not even a whole fandom).

- The [world_population_by_countries.csv](data/reference_and_test_files/additional_data/world_population_by_countries.csv) file's info is taken from [wikipedia's list](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population). It only contains countries with populations over 1 million.

### Media Types:

- If a fandom has multiple media types, I counted as many as felt relevant, focusing on the most popular or those listed in this set.

    > Ex. BBC's Sherlock is obviously based on Sherlock Holmes by Sir Arthur Conan Doyle, but as only the show has been tagged across the entire data set, I am only counting it as "TV (live action)"

    > Ex. A lot of anime also have animated movies that either function as part of the show's canon (like Haikyuu) or independantly of it (like One Piece), but I did not bother counting these fandoms as "Movie (animated)", I only counted the show (and comic its based on where applicable). I also counted the One Piece live action netflix show, as I know it's the cause of the recent surge in popularity of that fandom (-> Our singular One Piece ship only made the annual ranking in 2023, the year the live action show was released. One Piece ships also made the tumblr ranking that year.), hence relevant to this data set.

- If it was not easily discernible which media types were meant (ie same character names across adaptations), I tried to scew as widely as possible.

    > Ex. I'm decently sure that the people writing Les Mis fanfic are seldomly only basing it on the french Victor Hugo original from the 19th century, presumably favouring the musical adaptation and 2012 movie among other english adaptations, but the characters have the same names in all instances, so I am including the original book as a media type as well.

- I grouped RPF by their own categories, including multiple where relevant or in addition to their fandom's existing media types.

    > Ex. Musicians who are shipped in association with a singing competition like American Idol or Super Vocal count as both "Music RPF" and "Unscripted TV RPF".

    > Ex. Live action shows like Supernatural or Merlin, whose actors are also RPF shipped, will be tagged as both "Actor RPF" and "TV (live action)".

### Canon, family, and orientation data:

- Any questionable/debatable status will be tagged as what seems most reasonable but with a "*" to acknowledge its non-definitive nature (more details below).

#### Canon pairings

- To be considered a canon pairing, the pairing must've have done at the very least one of the following in canon media:
    - confess (romantic) love/attraction to the other person
    - engage in romantic/sexual physical interactions such as kissing
    - be in an official relationship
    - be listed as love interests on their wiki (if there is a list of love interests)

- Merely flirting, vague expressions of affection, confirmations in non-canon media, and a variety of queerbaiting, no matter how egregious, are not enough to be counted

    > Ex. Hajime and Nagito, and Kokichi and Shuichi from Danganranpa seem to be like *this close* to being canon, including all of them but Hajime being canon mlm, but neither pairing goes far enough in canon media to be counted, despite egregious flirting, bait, and numerous pieces of evidence that could've counted in non-canon media. I have tagged both pairing as "No*".

- If they engaged in actions that would qualify but for reasons that do not indicate genuine attraction, those will not be counted

    > Ex. Fake dating or marriage for other motives, like Toni and Fangs marrying to get custody of their weird baby from their co-parent

    > Ex. Kissing for non-romantic reasons, like the Doctor kissing Rose to absorb Tardis energy or whatever to save her life

- If the action was one-sided, it will be tagged as "One-sided" instead of "Yes", as it is canonically one-sided.

    > Ex. Oswald Cobblepott canonically has a one-sided crush on Edward Nigma in Gotham.

#### Incest

- Blood-related pairings will be tagged as "Yes" for incest.

    > Why did Wincest rank so highly WHY

- Other kinds of relations will be tagged as such ("step"/"adopted"/"foster"/"in-law"), because that is still incest, albeit not blood-related.

    > Ex. Thor and Loki are adopted siblings/not blood-related but they are still brothers for all intents and purposes.

- If people are technically related by non-blood relations, but they're not directly connected, they will be tagged as "No*"

    > Ex. Kara Danvers' bio-aunt and adoptive sister are not blood- or directly related to each other, as they are on opposite sides of Kara's family, therefore merely related *via* Kara. They are not on par with directly related step/adoptive incest pairings like step parent/child or adoptive siblings.

- If a pairing was not related in the original work but was declared questionably related in another adaptation in an obvious attempt to erase a canon-queer relationship, they will be tagged as "No*"

    > Ex. Faraway Wanderers, as a danmei novel, has a mlm main pairing. In the TV adaptation Word of Honor they are not explicitly gay/together and later "revealed" to be each other's "junior/senior brother" despite not sharing parentage as far as I can tell from the TV show's wiki (I have not watched this show, I do not know the full details of how the show tried to justify this reveal). I am not counting that nonsense as incest as they are not related in the original danmei novel.

    > Ex. Sailor Neptune and Sailor Uranus are girlfriends in the japanese original, but the english dub decided to declare them cousins instead in order to hide the gayness. I am not counting that.

#### Orientation

- I am only tracking orientation as far as it is portrayed or specified in media

    > Ex. Someone of unspecified label who only ever had opposite-sex partners in media could well be bisexual, but I will have written "str8" in the data file, as only their hetero attraction is canonically confirmed

- If someone specified a label but has had love interests that do not align with that, the explicit label takes priority

    > Ex. Willow had male love interests but later explicitly came out as a lesbian, hence is tagged as "gay"

- If someone has listed love interests but their reciprocity is put in question, they will be counted but marked with a "*"

    > Ex. Princess Bubblegum has Finn and Mr Cream Puff listed as love interests, but she never explicitly reciprocated Finn's crush, and Mr Cream Puff happened when she was quite young and was arranged by another character for scheming purposes. Her only other love interest is Marceline, the only one she actually explicitly reciprocated and did stuff with. I have tagged her as "bi*" as her male love interests are questionable.

- If they usually have one type of orientation only but there's like one minor alternate version of the character that conflicts with it, they will also be tagged with the "*"

    > Ex. There's like one alternate universe in DC where Lex Luthor is gay and dates a big green man, but regular Lex seems to only ever have dated women, hence he is tagged as "str8*"

- If there are no known love interests or partners, they will be tagged as "unspecified"

    > Ex. The kpop industry doesn't want its idols to date or come out as queer, hence the various kpop idols in our rankings don't have any publicly known partners or confirmed identity labels. They are "unspecified".

- I am not bothering with a distinction between pan and bi, as we have like a single(1) character with a canonical unaligned nb partner, out of our total two(2) unaligned characters. Anyone who dates both men and women will be tagged as bi for simplicity's sake.

- Some characters may be able to be argued to be ace/aro or closeted gays in spite of having been in (any/hetero) relationships. Unless there is significant canon-support for this, I will disregard it, as the point of this exercise is less about determining the characters' actual labels and more about merely comparing what info on their potential orientation is canon vs what types of pairings they're put in by fans

    > Ex. Sansa Stark suffers through several arranged marriages, none of which she seems to enjoy particularly much, so she may well be ace, aro and/or gay, but we have no means of knowing that from what canon tells us, therefore she is still counted as str8 and canon-conflicting with being in a femslash ship, as she has not had any canon female lovers.

- If a character is explicitly fully unable to feel attraction (as opposed to folks on the wider ace/aro spectrum who may still have an orientation & romantic/sexual relationships), that will also qualify as a conflict with any slash ship they're in

    > Ex. Both Peridot and Yelena/White Widow are confirmed as ace-aro with specific reference to their lack of interest in relationships, so they are tagged as acearo and any slash ship containing them will be counted as conflicting with their canon lack of attraction.

    > Ex. Luffy is canonically established as not feeling any romantic or sexual attraction via being immune to Boa Hancock's devil fruit power, so if and when he is added to our data pool via tumblr's rankings (which I know contain Zolu among other ships that didn't make the AO3 rankings) he will also be counted as acearo and thereby conflicting in a slash ship.

- Any ace-aro spec character who does have an orientation will be counted as that orientation, not as their ace/aro status

    > Ex. Jughead ends up in a romantic and later even sexual relationship with Betty, despite being ace in the comics and portrayed as ace-spec in the show, so he is counted as str8 not ace.

## N.B.: 

There may remain inaccuracies in the data as it's a shitton of characters and while I looked up most of them & combed their wikis for relevant info I'm just one guy (same as OP is just one person) and I may have overlooked some details in any info I added/relabelled/completed.

However hopefully these discrepencies should be minor and not scew the general trends of the data.

