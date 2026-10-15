# Simplified Chinese overlay for Do NOT Take This Cat Home PC 1.0.
# Original scripts and save data are not replaced.

translate zh_CN python:
    gui.text_font = "fonts/SourceHanSansCN-Regular.otf"
    gui.name_text_font = gui.text_font
    gui.interface_text_font = gui.text_font
    gui.button_text_font = gui.text_font
    gui.choice_button_text_font = gui.text_font
    gui.language = "japanese-normal"

init 999 python:
    # Default to Chinese on first launch of this overlay; later choices persist.
    if not persistent._zhcn_overlay_initialized:
        config.language = "zh_CN"
        persistent._zhcn_overlay_initialized = True

    # Original English puzzle answers are hidden for unrecognised languages.
    # Retain the original six-letter puzzle, timing, and success branches.
    _zhcn_puzzle_choices = 0
    for _zhcn_node in renpy.game.script.all_stmts:
        if isinstance(_zhcn_node, renpy.ast.Menu):
            _zhcn_items = []
            for _zhcn_caption, _zhcn_condition, _zhcn_block in _zhcn_node.items:
                if _zhcn_condition == '_preferences.language == "eng"':
                    _zhcn_condition = '_preferences.language in ("eng", "zh_CN")'
                    _zhcn_puzzle_choices += 1
                _zhcn_items.append((_zhcn_caption, _zhcn_condition, _zhcn_block))
            _zhcn_node.items = _zhcn_items
    config.always_shown_screens.append("zhcn_language_switch")
    _zhcn_previous_replace_text = config.replace_text
    def _zhcn_replace_text(text):
        if _zhcn_previous_replace_text is not None:
            text = _zhcn_previous_replace_text(text)
        if _preferences.language == "zh_CN":
            text = {"Do Not Take": "不要把", "This Cat Home": "这只猫带回家", "I T ": "它", " Home": "带回家"}.get(text, text)
        return renpy.translate_string(text)
    config.replace_text = _zhcn_replace_text

screen zhcn_language_switch():
    zorder 200
    if renpy.get_screen("preferences") or renpy.get_screen("languageselect"):
        hbox:
            xalign 0.97
            yalign 0.97
            spacing 18
            textbutton "简体中文" action [Language("zh_CN"), If(renpy.get_screen("languageselect"), Jump("afterLanguage"), NullAction())] text_font "fonts/SourceHanSansCN-Regular.otf" text_size 20
            textbutton "English" action [Language("eng"), If(renpy.get_screen("languageselect"), Jump("afterLanguage"), NullAction())] text_font "fonts/SourceHanSansCN-Regular.otf" text_size 20
