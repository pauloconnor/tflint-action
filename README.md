# TFLint action

A GitHub Action that runs tflint against a repository, with configurable rules [TFLint](https://github.com/terraform-linters/tflint) to catch stupid stuff that you may have missed in your reviews

## Inputs

| Parameter                        | Value              | Description                                                       |
| -------------------------------- | ------------------ | ----------------------------------------------------------------- |
| `TFLINT_PATH`                    | /github/workspace  | The path to run TFLint against, including /github/workspace       |
| `TFLINT_RECURSE`                 | false"             | Whether or not to recurse through directories                     |
| `TFLINT_CHANGED_ONLY`            | false"             | Run TFLint against changed files only                             |
| `TFLINT_CONFIG_FILE`             | false"             | Load the .tflint.hcl file in the root of the repo                 |
| `TFLINT_EXTRA_OPTIONS`           | null               | Extra options to pass to TFLint GitHub Action                     |
| `TFLINT_ENABLED_RULES`           | null               | Which extra rules to enable, one per line                         |
| `TFLINT_DISABLED_RULES`          | null               | Which standard rules to disable, one per line                     |
| `TFLINT_TAG_LINES`               | false              | Post a message at the fail that failed, with the error message    |

## Usage

```yaml
on: pull_request
name: tflint action
jobs:
  lint:
    name: Terraform Lint on PR
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
            # Full git history is needed to get a proper list of changed files
            fetch-depth: 0
      - uses: pauloconnor/tflint-action@v0.0.2 
        with:
            tflint_changed_only: false
            tflint_extra_options: --output json
            tflint_enabled_rules:
              terraform_required_providers
              terraform_standard_module_structure
            tflint_disabled_rules:
              terraform_deprecated_interpolation
```

Full example:

```yaml
jobs:
  tflint:
    name: TFLint
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: TFLint
        uses: pauloconnor/tflint-action@v0.0.2 
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
            tflint_path: environments/
            tflint_recurse: true
            tflint_changed_only: false
            tflint_extra_options: --output json
            tflint_enabled_rules:
              terraform_required_providers
              terraform_standard_module_structure
            tflint_disabled_rules:
              terraform_deprecated_interpolation
```

## License

Apache License. See [LICENSE](LICENSE) for full details.
