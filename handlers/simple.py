from base import BaseHandler


class Home(BaseHandler):

    template_path = 'simple/home'

    def get(self, *args, **kwargs):
        self.response.out.write(self.loadtemplate())


class Section(object):
    title = None
    description = None

    def __init__(self):
        self.description = []


class About(BaseHandler):

    template_path = 'simple/about'

    def get(self, *args, **kwargs):
        """
        For now, we're just hard coding the about page.  To be fixed later.
        """
        sections = []

        section_one = Section()
        section_one.title = 'Goals'
        section_one.description.append("We want to have fun.")
        section_one.description.append(("We're really just a group of friends "
                                        "who want to hang out.  We don't struggle "
                                        "to be the best at anything, we don't have "
                                        "goals other than to screw around and have "
                                        "fun doing it."))
        section_one.description.append(("Whether we're participating in PvP, "
                                        "roleplaying, running story quests, "
                                        "farming, or any of the other thousand "
                                        "things GW2 lets you do - our aim is to "
                                        "have fun doing it."))

        sections.append(section_one)

        section_two = Section()
        section_two.title = 'Rules'
        section_two.description.append("Be courteous.")
        section_two.description.append("That's all.  Nothing more.")
        section_two.description.append(("There are no rules about activity, "
                                        "language, guild donations, or "
                                        "anything like that.  Although, I should "
                                        "say that if you're offline for long "
                                        "enough, we will assume that you have quit "
                                        "playing and you will be kicked.  But you "
                                        "can get right back in without going "
                                        "through any kind of application process "
                                        "- nothing about being inactive is wrong, "
                                        "we just hit the kick button when we're "
                                        "pretty sure someone isn't coming back.  "
                                        "If it turns out we're wrong about anyone, "
                                        "they are welcome right back."))
        section_two.description.append(("All that said, please note that you "
                                        "must use your common sense when dealing "
                                        "with other guild members.  If someone "
                                        "is having a bad day, try to cut them "
                                        "some slack.  If things start getting "
                                        "heated, be the one to back off - and, "
                                        "if necessary, log off for a while"))
        section_two.description.append(("Point is, don't be a jerk and you'll be "
                                        "just fine.  Heck, most people in this "
                                        "guild probably don't mind if you're a "
                                        "jerk, either - we've all dealt with the "
                                        "Arch linux community at least a little.  "
                                        "Be courteous and considerate, and "
                                        "help everyone in the guild (including "
                                        "you) have fun.  As long as everyone's "
                                        "having fun, we won't have any reason "
                                        "to lay out any discipline."))
        section_two.description.append(("Which would be awesome, because all of "
                                        "us are way to lazy to sit down and "
                                        "come up with punishments for breaking "
                                        "the rules."))

        sections.append(section_two)

        context = {
            'sections': sections,
            }

        self.response.out.write(self.loadtemplate(context))


class Lore(BaseHandler):

    template_path = 'simple/lore'

    def get(self, *args, **kwargs):
        """
        Again, our lore is simply hardcoded here.  I would like to make
        this a database call in the near future, so that we can edit
        it without making a code change, but for now, I'm just too lazy.
        """
        lore = []
        section_one = Section()
        section_one.title = "Author's Note"

        note = """
First, I want to tell you a bit about the writer of this lore.  It is
a member of the Order of Whispers who has come to us.  Remember that
much of what happened in the first game (fighting Abaddon) is legend,
and that inaccuracies may be rampant in his telling of the events.
This is how things work.  Our history may well be based on lies and
misinterpretation.  But it is still a valid interpretation of history,
and I won't be paying much attention to people who yell at me for
writing in the character of someone who has a twisted view of
Tyria's and Abaddon's history.

Second, to our members: This is not something you need to care
about to be part of our guild.  The fact of the matter is that
I (Sam/Valc) am a big fan of roleplaying games and love to
write stories.  When I make characters in games, I at least
come up with a detailed personality, and I usually write up
a long background.  The same goes for guilds.

So again, you do not need to care.  This is not a roleplaying guild.
Much as I like to roleplay from time to time, I'm not going to force
it on anyone else in the guild, ever.

If you do read through this background, I hope you enjoy it.
I spent quite a while digging through all of the old Guild Wars lore
before remembering just how out of place the background of Abaddon was.
So I developed a story around conspiracy theories and secret societies,
and I made it my goal to integrate our guild into the world in which
we would be inhabiting.

Personally, I think it worked out far better than I could have hoped.
Our story fits in with so many elements of the personal story of the
game so very well that I'm almost wondering if ArenaNet is planning
something very similar to the idea I've written down just below.

So without further ado, here is the story behind the Whispers of
Abaddon.  I hope you enjoy the read.
"""
        section_one.description.extend(note.split('\n\n'))
        lore.append(section_one)

        section_two = Section()
        section_two.title = "The Fall of Magic"
        body = """
At the beginning of time, there were six human gods.  Balthazar,
god of war; Dhuum, god of death - later overthrown by Grenth;
Dwayna, goddess of life; Lyssa, goddess of beauty;
Melandru, goddess of earth; and finally, Abaddon, greatest
of the gods, god of knowledge.

During our infancy as a race, the gods saw fit to grant us with
the powers of magic.  In their wisdom, the lesser gods chose
Abaddon, as the god of knowledge, to present this great gift
to the children of the gods.

Abaddon looked into humanity and, with all the knowledge he had
of things the other gods could not fathom, chose not to limit
this gift.

With all this power, humanity turned on itself.  Wars broke out.
Many people died in the horrifically destructive battles, powered
by magic unrestrained.  Evil dominated the world.

And Abaddon did nothing.

The other gods, horrified at the bloodshed and worried about what
the unrestrained use of magic would lead to, pleaded with Abaddon
to work with them to stop the flow of magic into the world, but
he refused.  So they decided to restrain it without him.

Each god worked on locks, forcing magic into small cages related
to the god who created the lock.  Grenth locked down the use of
reanimation and the cold touch of death; Lyssa, the magic of
illusion and misdirection; Balthazar the magic of might; and so
on.  Each one created their own brand of magic, limited in strength,
but still a powerful gift.
"""
        section_two.description.extend(body.split('\n\n'))
        lore.append(section_two)

        section_three = Section()
        section_three.title = "The Fall of Abaddon"
        body = """
Now, friends, I want you to pay attention here.  Because this next
part is where truly interesting events start to unfold.

Abaddon, known then as the god of knowledge and the keeper of secrets,
started a war.

Keep in mind, Abaddon was only as strong as any two other gods.  This
is not something that would be missed by one named the god of knowledge.
He knew.  There was no way he was going to win this war without a
massive struggle.  And yet, he was so very determined to keep all
magic unrestrained that he started a war, one that he had little hope
of winning, against five other gods.

Abaddon struggled and did his best.  He fought hard, but was beaten.
Eventually, he was imprisoned by Grenth, where he stayed until the
events of the Guild Wars, two hundred and fifty years ago.

But no one ever stopped to find out what piece of knowledge sitting
in the mind of the god of knowledge and the keeper of secrets had
caused him so very much fear.  Something so horrible that he would
start a hopeless war against five other gods, just to make sure that
humans had unrestrained use of magic.
"""
        section_three.description.extend(body.split('\n\n'))
        lore.append(section_three)

        section_four = Section()
        section_four.title = "The Death of Abaddon"
        body = """
For centuries, Abaddon built back his strength, trying to free himself
from Grenth's prison.  He employed the help of everyone from selfish
politicians looking for personal gain to genocidal maniacs, never
finding followers with a lick of sanity left in their brains.

When he finally broke free, ready to start his war anew, several so-called
heroes were waiting with the help of our old order, the Order of Whispers,
and one paragon whore named Kormir.  They faced off, and a great struggle ended
with Abaddon's defeat.  Kormir killed Abaddon, taking his powers for her own
selfish ends, becoming the false goddess of truth.
"""
        section_four.description.extend(body.split('\n\n'))
        lore.append(section_four)

        section_five = Section()
        section_five.title = "The Formation of the Whispers of Abaddon"
        body = """
Once again, Abaddon was the god of knowledge and keeper of secrets.  Why would
he put himself in such a situation for something that seems so very trivial?
If there were no reasons beyond his own ego for granting such immense magical
power to the human race, why would he start a war that he knew he had little
chance of winning over it?

No, it was obvious that something else was going on.  Abaddon knew something,
a fact so horrible that the massive slaughter resulting from unrestrained magic
was a minor afterthought.  The fact that the other gods couldn't see that is
disencouraging, to say the least.

Our founders, members of the Order of Whispers, began studying Abaddon's life
and death in depth.  At first, it was just an attempt to understand the fall of
a god - something that so very few people get to witness.  But the scholars
quickly realized that something was amiss.  Nothing in the story made sense.

Knowing how radical their developing theories were, they kept their secrets.
Initially just a pair of friends, the first members of the Whispers of
Abaddon worked silently, rarely exchanging information, and even then in code
that they were sure even the Order of Whispers would misinterpret.

But there was no denying it - logical deduction always lead down the same path,
toward some secret that Abaddon couldn't share.  And why didn't he bring it up
with the other gods?  Surely, if anyone could fathom such horror, it would be
his fellow gods - and surely, they could be trusted.  Or could they?  Were
the other gods implicated in Abaddon's great secret?

None of our answers are simple.  No one knows for sure what's going on.  But we
know that things just aren't adding up, and something horrible is coming.
Perhaps it already has - perhaps the awakening of the dragons is the precursor
to what Abaddon foresaw.

Whatever happens, we know our mission: Finish what our Lord, Abaddon, started.
We have been struggling to weaken the seals on magic for nearly two hundred
fifty years, and that struggle continues.  The power in magic is growing, and
we like to think that our struggle has been a major part of it.

The Order of Whispers will try to stop us.  The gods will try to stop us.  But
we will stop at nothing to prepare for whatever horror would terrify the
greatest of the gods.
"""
        section_five.description.extend(body.split('\n\n'))
        lore.append(section_five)

        context = {
            'lore': lore,
            }

        self.response.out.write(self.loadtemplate(context))
