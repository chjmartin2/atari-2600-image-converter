import sys

if __name__ == "__main__":
    if '--setup-cartridge-support' in sys.argv:
        from chrono.standalone import setup_window
        setup_window()
    elif '--palette-self-test' in sys.argv:
        from chrono.standalone import palette_self_test
        palette_self_test(sys.argv[sys.argv.index('--palette-self-test')+1])
    elif '--self-test' in sys.argv:
        from chrono.standalone import self_test
        self_test(sys.argv[sys.argv.index('--self-test')+1])
    else:
        from chrono.gui import main
        main()
