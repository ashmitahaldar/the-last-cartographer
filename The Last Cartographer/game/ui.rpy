################################
## Styles
################################

style title_button is default:
    background None
    hover_background None
    padding (24, 12)

style title_button_text is default:
    size 26
    color "#c4a96b"
    hover_color "#ffffff"
    outlines [(1, "#000000", 0, 0)]


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
        size 13
        color "#252018"

    button:
        xfill True
        yfill True
        action Return()
        background None

    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
