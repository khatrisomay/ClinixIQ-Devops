# ==============================================================================
# ClinixIQ - TFLint Infrastructure Linter Configuration
# ==============================================================================

config {
  format              = "compact"
  plugin_dir          = "~/.tflint.d/plugins"
  module              = true
  force               = false
  disabled_by_default = false
}

# AWS Ruleset Plugin
plugin "aws" {
  enabled = true
  version = "0.30.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

# Standard Terraform Core Rules
rule "terraform_deprecated_interpolation" {
  enabled = true
}

rule "terraform_unused_declarations" {
  enabled = true
}

rule "terraform_comment_syntax" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_typed_variables" {
  enabled = true
}

rule "terraform_naming_convention" {
  enabled = true
}
