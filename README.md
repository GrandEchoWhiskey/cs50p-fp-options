# Options

### Classes
- option(short, long) -> option
- translation_table(option: list) -> table
- translation(in_args, prefix) -> list, dict

### Work
- x = option('alpha', 'a')
- translation(sys.argv, '-', x)