"""Create a plain text document in which each paragraph is a single line.

Usage: python create_text_document.py [output_path]
"""

import string
import sys
from pathlib import Path

DEFAULT_OUTPUT = Path(__file__).with_name("community-garden.txt")

# Paragraphs are wrapped here only to keep the source readable. Whitespace is
# collapsed on output, so each one is written as one unbroken line.
DOCUMENT = [
    ("title", "Starting a Community Garden"),
    ("heading", "Introduction"),
    ("paragraph", """
        A community garden is a shared piece of land where neighbours grow
        vegetables, herbs, fruit and flowers together. The idea is simple, but
        the benefits reach far beyond the harvest itself. People who have lived
        on the same street for years often meet for the first time over a
        raised bed, and children who have never seen a carrot pulled from the
        soil get to learn where their food comes from. Gardens also make good
        use of vacant lots, soften the look of a built-up area and give
        residents a quiet place to spend an evening outdoors. Starting one does
        take some patience, because land has to be found, permissions have to
        be granted and a group of volunteers has to agree on how the space will
        be run. None of these steps is especially difficult on its own, yet
        together they can feel overwhelming to a small group of enthusiasts
        with limited free time. This document describes the process from the
        first conversation to the first season of growing, so that a new group
        knows what to expect and what to tackle first. It is written for people
        with no earlier experience, and it assumes only an interest in
        gardening and a willingness to work with others.
    """),
    ("heading", "Getting Organised"),
    ("paragraph", """
        The most successful gardens tend to begin with people rather than with
        land. Before anyone looks at a site or buys a single seed, it is worth
        spending some time finding out who is interested and what they hope to
        get out of the project. Some members will want a private plot where
        they can grow food for their own household, while others may prefer to
        work on shared beds and split the produce between everyone who helped.
        Some will be drawn by the social side and will care more about benches
        and a place for coffee than about crop yields. These differences are
        not a problem as long as they are talked about openly at an early
        stage. A short meeting in a library, a school or someone's living room
        is usually enough to get started, and a simple notice on a local
        message board will often bring in more people than expected. Once a
        core group has formed, it should choose a contact person, keep a shared
        list of names and agree on how decisions will be made. A little
        structure at this point prevents a great deal of confusion later,
        particularly when money and land are involved.
    """),
    ("subheading", "First Steps for the Group"),
    ("paragraph", """
        The following steps work well as an agenda for the first few meetings.
        They are listed in the order in which most groups find it natural to
        take them.
    """),
    ("numbered", [
        "Invite neighbours, local associations and nearby schools to an open meeting.",
        "Write down what the group wants the garden to achieve in a few plain sentences.",
        "Choose a coordinator, a treasurer and someone to keep the meeting notes.",
        "Agree on how decisions are made and how new members can join.",
        "Draw up a rough budget and list the possible sources of funding.",
        "Make a list of candidate sites within easy walking distance for most members.",
    ]),
    ("heading", "Choosing a Site"),
    ("paragraph", """
        A good site does not need to be large, but it does need to meet a few
        basic requirements. Most vegetables want at least six hours of direct
        sunlight a day, so a plot shaded by tall buildings or mature trees will
        limit what can be grown. Access to water is just as important, because
        carrying cans over any distance quickly becomes tiresome during a dry
        summer. It is also wise to find out how the land was used in the past.
        Former industrial sites and old garages may have contaminated soil, and
        a simple laboratory test is a small price to pay for peace of mind. If
        the results are poor, raised beds filled with clean soil are a
        practical solution and they also make the garden easier to use for
        people who find bending difficult. Ownership is the next question to
        settle. Municipalities, churches, housing cooperatives and private
        landowners have all been known to lend out unused land, frequently at
        little or no cost. Whatever the arrangement turns out to be, it should
        be put in writing, with a clear statement of how long the group may
        stay and who is responsible for insurance, fencing and upkeep.
    """),
    ("subheading", "What to Check Before Signing"),
    ("paragraph", """
        Walk the site together at different times of day, and go through each
        of these points before any agreement is signed with the landowner.
    """),
    ("lettered", [
        "Hours of direct sunlight in both spring and high summer.",
        "Distance to the nearest water supply and who pays for the water used.",
        "Soil quality, including a test for lead and other common contaminants.",
        "Safe access for wheelchairs, prams and deliveries of soil or compost.",
        "Length of the lease and the notice required if the land is needed again.",
    ]),
    ("heading", "Planning the Layout"),
    ("paragraph", """
        With a site secured, the group can begin to draw up a plan. A sketch on
        paper is sufficient, as long as it shows the direction of the sun, the
        location of the water supply and the paths that will connect
        everything. Paths deserve more attention than they usually get. They
        should be wide enough for a wheelbarrow, and at least the main one
        should be firm and level so that everyone can use it regardless of
        mobility. Beds should be narrow enough to reach the centre from either
        side, which in practice means a width of around one metre and twenty
        centimetres. Tall crops such as beans and sweetcorn belong on the
        northern side, where they will not cast shade across their shorter
        neighbours. A shared compost area, a lockable shed and a seating area
        are worth including from the start, even if they are not built until
        later. Leaving a small part of the site unplanted is also a sensible
        choice, since new ideas will inevitably turn up once people begin
        working on the ground. Above all, the plan should be treated as a draft
        that the members can revise together as they learn what works on this
        particular patch of land.
    """),
    ("subheading", "Items to Include in the Plan"),
    ("lettered", [
        "Individual plots and shared beds, with their measurements.",
        "Main paths and narrower side paths between the beds.",
        "Taps, water butts and the route of any hoses.",
        "Compost bays, tool storage and a place for deliveries.",
    ]),
    ("heading", "The First Season"),
    ("paragraph", """
        It is tempting to try to do everything during the first year, but a
        modest start is far more likely to succeed. Choosing reliable crops
        such as potatoes, lettuce, radishes, beans and courgettes gives
        beginners an early reward and builds confidence for the seasons that
        follow. Regular work days help a great deal, because they spread the
        heavy tasks across many hands and give new members an easy way to get
        to know the others. A rota for watering is essential during the warmest
        weeks, when plants can suffer after only a few days of neglect, and
        holidays should be planned around it. The group should also keep simple
        records of what was planted, when it was sown and how well it did,
        since these notes become surprisingly valuable as the years go by.
        Finally, remember to celebrate. A harvest meal at the end of the summer
        rewards everyone who took part and shows the wider neighbourhood what
        has been accomplished, which is often the best way of attracting new
        members for the following year.
    """),
    ("subheading", "Tasks for the Year"),
    ("numbered", [
        "Prepare the beds and spread compost as soon as the ground has thawed.",
        "Sow hardy crops in early spring and more tender ones after the last frost.",
        "Set up the watering rota and hold a work day at least once a month.",
        "Harvest regularly and share any surplus with neighbours or a local food bank.",
        "Clear the beds in autumn and review the season together at a final meeting.",
    ]),
]


def render_block(kind, content):
    if kind == "title":
        return f"{content}\n{'=' * len(content)}"
    if kind == "heading":
        return f"{content}\n{'-' * len(content)}"
    if kind == "subheading":
        return content
    if kind == "paragraph":
        return " ".join(content.split())
    if kind == "numbered":
        return "\n".join(f"{i}. {item}" for i, item in enumerate(content, start=1))
    if kind == "lettered":
        return "\n".join(f"{letter}) {item}" for letter, item in zip(string.ascii_lowercase, content))
    raise ValueError(f"Unknown block kind: {kind}")


def main():
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    text = "\n\n".join(render_block(kind, content) for kind, content in DOCUMENT) + "\n"
    output.write_text(text, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
