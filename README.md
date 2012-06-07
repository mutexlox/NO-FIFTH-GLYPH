# No Fifth Glyph

That fifth glyph in our script is bad! This bot -v's (for a bit) any who say it.

To run: First modify config.py so it has what you want.

    python mainLoop.py [list of chans, " "-split]

For an illustration:

    python mainLoop.py "#foo"  # Runs, joining to #foo only
    python mainLoop.py "#foo" "#bar" "#baz"  # Runs, joining to #foo, #bar, #baz
    python mainLoop.py  # Runs, joining to no chans

Play with it, and **follow your IRC host's laws on bots.**
