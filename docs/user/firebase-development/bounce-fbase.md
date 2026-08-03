# bounce-fbase

Firebase emulator restart helper that discovers emulator ports from firebase.json, kills existing listeners, and starts emulators.

## Runtime Help Behavior

bounce-fbase does not provide argparse-style --help output. Running with --help currently executes normal startup validation and may return:

```text
Error: Could not find firebase.json
```

## Operational Flow

- Find firebase.json from current directory ancestry (or script parent fallback).
- Parse emulators.*.port values.
- Kill active processes on discovered ports.
- Run firebase emulators:start.

## Example

```bash
bounce-fbase
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/firebase-development/bounce-fbase.md from current script behavior. Keep runtime error examples brief and update operational flow steps if discovery or startup logic changes."
