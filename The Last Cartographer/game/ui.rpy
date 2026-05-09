################################
## Styles
################################

style button:
    activate_sound "audio/sfx/click.ogg"

style title_button is default:
    background None
    hover_background None
    padding (24, 12)

style title_button_text is default:
    size 26
    color "#c4a96b"
    hover_color "#ffffff"
    outlines [(1, "#000000", 0, 0)]

style hint_button is default:
    background "#2a2018bb"
    hover_background "#3a3020cc"
    padding (16, 10)

style hint_button_text is default:
    size 19
    color "#8a7a5a"
    hover_color "#c4a96b"
    italic True

style hint_button_bad is default:
    background "#221818bb"
    hover_background "#2e2020cc"
    padding (16, 10)

style hint_button_bad_text is default:
    size 19
    color "#7a6060"
    hover_color "#b89090"
    italic True

style hint_toggle is default:
    background "#1a150ecc"
    hover_background "#2a2018cc"
    padding (14, 8)

style hint_toggle_text is default:
    size 16
    color "#8a7a5a"
    hover_color "#c4a96b"
    italic True


################################
## Title Screen
################################

screen title_screen():
    # Full-screen background image
    add im.Scale("gui/main_menu.png", 1920, 1080)

    # Dark gradient overlay — heavier at bottom so text reads cleanly
    add "#00000055"

    frame:
        xfill True
        yfill True
        background "#00000000"
        padding (0, 0)

        # Top-left: small ornament
        text "* * *":
            xpos 48
            ypos 48
            size 16
            color "#c4a96b88"

        # Title block — upper third
        vbox:
            xalign 0.5
            yalign 0.28
            spacing 16

            text "THE LAST CARTOGRAPHER":
                xalign 0.5
                size 72
                color "#e8d5b0"
                kerning 6.0
                outlines [(3, "#07050a", 1, 1), (1, "#07050a", 0, 0)]

            text "— * —":
                xalign 0.5
                size 20
                color "#c4a96b"
                outlines [(1, "#00000099", 0, 0)]

            null height 6

            text "A town at the edge of empire.":
                xalign 0.5
                size 26
                color "#c4a96b"
                italic True
                outlines [(1, "#000000bb", 0, 0)]

            text "One woman who keeps the map in her head.":
                xalign 0.5
                size 26
                color "#c4a96b"
                italic True
                outlines [(1, "#000000bb", 0, 0)]

        # Bottom panel — frosted dark strip
        frame:
            xalign 0.5
            yalign 0.88
            xsize 460
            background "#0d0a07cc"
            padding (40, 24, 40, 24)

            vbox:
                spacing 14
                xalign 0.5

                textbutton "Begin":
                    style "title_button"
                    xalign 0.5
                    action Return()

                text "press enter or click":
                    xalign 0.5
                    size 15
                    color "#6a5c48"

        # Bottom-right version stamp
        text "The Last Cartographer  *  2026":
            xalign 0.98
            yalign 0.98
            size 13
            color "#3a3028"
            outlines [(1, "#00000099", 0, 0)]


################################
## Input Screen (overrides Ren'Py default)
################################

screen input(prompt):
    modal True
    zorder 200

    # Suggestion buttons — hidden behind a toggle
    $ _turn = getattr(store, "_hint_turn", 0)
    default show_hints = False

    frame:
        xalign 0.5
        yalign 0.76
        xsize 1500
        background "#00000000"
        padding (0, 0)

        vbox:
            spacing 8
            xalign 0.5

            textbutton ("hide suggestions" if show_hints else "not sure what to say?"):
                style "hint_toggle"
                xalign 0.5
                action ToggleLocalVariable("show_hints")

            if show_hints:
                hbox:
                    xalign 0.5
                    spacing 14

                    if _turn < 3:
                        textbutton "\"I need to cross the pass.\"" style "hint_button" action Return("I need to cross the Northern Pass. I was told you're the only one who knows the safe route.")
                        textbutton "\"How long have you been here?\"" style "hint_button" action Return("How long have you been the cartographer here?")
                        textbutton "\"Something's wrong with the trail signs.\"" style "hint_button" action Return("I heard the trail signs have been tampered with. Do you know anything about that?")
                    elif _turn < 6:
                        textbutton "\"Your apprentice —\"" style "hint_button" action Return("What happened to your apprentice? You didn't finish.")
                        textbutton "\"I've made mistakes with trust too.\"" style "hint_button" action Return("I've made mistakes with trust. Someone I relied on used information I gave them to hurt others. I've never fully forgiven myself.")
                        textbutton "\"Why is this town emptying?\"" style "hint_button" action Return("This town feels like it's draining out. What happened to it?")
                    else:
                        textbutton "\"That cost you more than a route.\"" style "hint_button" action Return("That sounds like it cost you more than just the route.")
                        textbutton "\"Why did you stay?\"" style "hint_button" action Return("Why did you stay here, when others left?")
                        textbutton "\"I should go.\"" style "hint_button" action Return("leave")

                hbox:
                    xalign 0.5
                    spacing 14

                    if _turn < 3:
                        textbutton "\"Just give me the route.\"" style "hint_button_bad" action Return("Just give me the pass route. I'll pay whatever you want.")
                        textbutton "\"My reasons are my own.\"" style "hint_button_bad" action Return("My reasons for crossing are none of your concern.")
                        textbutton "\"I've crossed worse passes alone.\"" style "hint_button_bad" action Return("I've crossed harder passes than this without a guide. I just need the map.")
                    elif _turn < 6:
                        textbutton "\"I don't have time for this.\"" style "hint_button_bad" action Return("I don't have time to sit here talking. Do you want payment or not?")
                        textbutton "\"I'm not alone — others sent me.\"" style "hint_button_bad" action Return("I'm not travelling alone. There are others waiting for this information.")
                        textbutton "\"A guild is paying me for this.\"" style "hint_button_bad" action Return("A merchant guild in the south hired me to chart this pass. They're paying well.")
                    else:
                        textbutton "\"You're being paranoid.\"" style "hint_button_bad" action Return("You're being paranoid. It's just a map.")
                        textbutton "\"I lied earlier.\"" style "hint_button_bad" action Return("I should tell you — I lied about why I'm here.")
                        textbutton "\"Tell someone else your story.\"" style "hint_button_bad" action Return("I don't need your confession. I just need the route.")

    # Text input frame
    frame:
        xalign 0.5
        yalign 0.88
        xsize 1500
        background "#000000e0"
        padding (40, 22, 40, 22)

        vbox:
            spacing 10

            text prompt:
                size 26
                color "#a08060"
                italic True

            hbox:
                spacing 10

                text "›":
                    color "#7a6040"
                    size 30
                    yalign 0.5

                input:
                    default ""
                    size 28
                    color "#e8d5b0"
                    xmaximum 1380
                    yalign 0.5


################################
## Thinking Overlay
################################

screen thinking_overlay():
    zorder 190

    frame:
        xalign 0.5
        yalign 0.88
        xsize 860
        background "#000000e0"
        padding (32, 18, 32, 18)

        hbox:
            spacing 10

            text "›":
                color "#8a7050"
                size 30
                yalign 0.5

            text "Mara considers...":
                color "#8a7050"
                size 28
                italic True
                yalign 0.5


################################
## Ending Title Card
################################

screen ending_card(quote):
    modal True
    add "#000000"

    vbox:
        xalign 0.5
        yalign 0.48
        spacing 30

        text "—":
            xalign 0.5
            size 18
            color "#2a2018"

        text "[quote]":
            xalign 0.5
            text_align 0.5
            size 30
            color "#c4a96b"
            italic True
            xmaximum 680

        text "—":
            xalign 0.5
            size 18
            color "#2a2018"

    text "[[ click to continue ]]":
        xalign 0.5
        yalign 0.84
        size 16
        color "#8a7a60"

    button:
        xfill True
        yfill True
        action Return()
        background None

    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
