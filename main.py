"""Cosmic Heat — entry point. Initializes display, loads assets, launches menu."""

if __name__ == '__main__':
    from classes import sound
    from classes.display import init_display
    from classes.assets import load_all_assets

    sound.init_audio()
    screen = init_display()
    sound.set_num_channels(20)

    load_all_assets(screen)  # loading screen shown here

    import menu
    menu.main()
