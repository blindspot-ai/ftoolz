if __name__ == '__main__':
    import sys
    import nose  # type: ignore

    sys.argv.append('--with-doctest')
    sys.argv.append('--with-coverage')
    sys.argv.append('--cover-branches')
    sys.argv.append('--cover-erase')
    sys.argv.append('--cover-package=ftoolz')

    nose.main(defaultTest=['ftoolz', '.'])
