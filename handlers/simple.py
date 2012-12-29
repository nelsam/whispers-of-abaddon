from base import BaseHandler


class Home(BaseHandler):

    templatepath = 'simple/home'

    def get(self, *args, **kwargs):
        self.response.out.write(self.loadtemplate())


class Section(object):
    title = None
    description = None

    def __init__(self):
        self.description = []


class About(BaseHandler):

    templatepath = 'simple/about'

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

    templatepath = 'simple/lore'

    def get(self, *args, **kwargs):
        """
        Again, our lore is simply hardcoded here.  I would like to make
        this a database call in the near future, so that we can edit
        it without making a code change, but for now, I'm just too lazy.
        """
        from models.scribes import OrderedRecord
        query = OrderedRecord.query(OrderedRecord.section == 'lore')
        lore = query.order(OrderedRecord.rank)

        context = {
            'lore': lore,
            }

        self.response.out.write(self.loadtemplate(context))
