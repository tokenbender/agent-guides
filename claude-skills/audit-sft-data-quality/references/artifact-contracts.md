# Artifact Contracts

## Contents

- [Purpose](#purpose)
- [Recommended directory layout](#recommended-directory-layout)
- [Evaluation contract](#evaluation-contract)
- [Evaluation health record](#evaluation-health-record)
- [Attempt and turn record](#attempt-and-turn-record)
- [Test reachability record](#test-reachability-record)
- [Task failure packet](#task-failure-packet)
- [Synthesis plan record](#synthesis-plan-record)
- [Row verification receipt](#row-verification-receipt)
- [Serialization receipt](#serialization-receipt)
- [Lineage and disposition record](#lineage-and-disposition-record)
- [Dataset manifest](#dataset-manifest)
- [Training diff](#training-diff)
- [Evaluation and promotion record](#evaluation-and-promotion-record)
- [Minimum summary tables](#minimum-summary-tables)

## Purpose

Use these field contracts as portable minimums. JSON, JSONL, CSV, Parquet, or a
database are all acceptable if the records remain immutable, hash-addressed,
and joinable. Add task-specific fields rather than deleting required evidence.

## Recommended directory layout

```text
iteration/
  contract/
    iteration.json
    evaluation.json
    hashes.json
  raw/
    trials/
    candidates/
    logs/
    feedback/
  audit/
    evaluation_health.jsonl
    accepted_runs.json
    attempts.jsonl
    tests.jsonl
    failure_packets.jsonl
    synthesis_plan.jsonl
    row_receipts.jsonl
    serialization_receipts.jsonl
    duplicates.jsonl
    contamination.jsonl
    dispositions.jsonl
  datasets/
    candidate.jsonl
    selected.jsonl
    review.jsonl
    rejected.jsonl
    eval_only.jsonl
    manifest.json
  training/
    control.json
    candidate.json
    diff.json
    canary_receipts.jsonl
  evaluation/
    trials.jsonl
    task_transitions.jsonl
    promotion.json
  reports/
    audit.md
    matrices/
```

Do not make downstream tools discover inputs with broad globs. Point them to
accepted manifests.

## Evaluation contract

```json
{
  "evaluation_id": "string",
  "created_at": "RFC-3339",
  "model": {
    "base_id": "string",
    "checkpoint_id": "string",
    "adapter_id": "string-or-null",
    "hashes": {},
    "tokenizer_id": "string",
    "tokenizer_hash": "sha256"
  },
  "harness": {
    "name": "string",
    "revision": "string",
    "repository_revision": "string",
    "overlay_hash": "sha256",
    "oracle_revision": "string"
  },
  "tasks": {
    "suite": "string",
    "expected_unique_count": 0,
    "task_manifest_hash": "sha256",
    "test_manifest_hash": "sha256",
    "exclusions": []
  },
  "inference": {
    "system_prompt_hash": "sha256",
    "chat_template_hash": "sha256",
    "reasoning_mode": "string",
    "temperature": 0.0,
    "top_p": 1.0,
    "max_tokens": 0,
    "seed_policy": "string"
  },
  "interaction": {
    "turn_limit": 1,
    "feedback_turn": null,
    "feedback_source": "none-or-oracle",
    "stop_rules": []
  },
  "runtime": {
    "environment_id": "string",
    "tool_policy": {},
    "sandbox": "string",
    "working_directory_policy": "string",
    "timeout_seconds": 0
  },
  "trial_plan": {
    "single_turn_trials": 0,
    "feedback_trials": 0,
    "independence_rule": "string"
  }
}
```

## Evaluation health record

```json
{
  "trial_id": "string",
  "evaluation_id": "string",
  "expected_tasks": 0,
  "observed_tasks": 0,
  "unique_terminal_tasks": 0,
  "duplicate_task_ids": [],
  "missing_task_ids": [],
  "checkpoint_loaded": true,
  "adapter_loaded": true,
  "candidate_artifacts_complete": true,
  "feedback_routing_valid": true,
  "channel_routing_valid": true,
  "oracle_completed": true,
  "health_verdict": "valid|invalid",
  "invalid_reasons": [],
  "artifact_hashes": {}
}
```

## Attempt and turn record

Store one record per turn:

```json
{
  "trial_id": "string",
  "task_id": "string",
  "attempt_id": "string",
  "turn_index": 1,
  "input_hash": "sha256",
  "response_hash": "sha256",
  "parsed_action_hash": "sha256-or-null",
  "applied_state_hash": "sha256-or-null",
  "feedback_hash": "sha256-or-null",
  "next_input_hash": "sha256-or-null",
  "terminal_stage": "format-or-apply|syntax|compile|link-or-odr|runtime-or-sanitizer|semantic-counterexample|resource-limit|pass|infrastructure-invalid",
  "terminal_status": "model-failure|model-pass|malformed-model-output|context-exhaustion|tool-or-sandbox-blocked|timeout-ambiguous|harness-error|oracle-error|missing-artifact",
  "diagnostic_refs": [],
  "tokens": {},
  "latency_ms": 0,
  "tool_calls": [],
  "artifact_refs": []
}
```

## Test reachability record

Store one record per declared test or assertion:

```json
{
  "trial_id": "string",
  "task_id": "string",
  "attempt_id": "string",
  "test_id": "string",
  "oracle_stage": "build|link|runtime|semantic|resource|final-state",
  "status": "passed-observed|failed-observed|not-reached-build-blocked|not-reached-runtime-blocked|not-run-harness-invalid",
  "blocker_ref": "string-or-null",
  "input_ref": "string-or-redacted-hash",
  "expected_ref": "string-or-redacted-hash",
  "observed_ref": "string-or-redacted-hash",
  "diagnostic_ref": "string-or-null"
}
```

## Task failure packet

```json
{
  "task_id": "string",
  "task_hash": "sha256",
  "accepted_attempt_ids": [],
  "terminal_stage_counts": {},
  "test_reachability_counts": {},
  "observed_counterexamples": [],
  "primary_mechanism": "string",
  "secondary_mechanisms": [],
  "evidence_tier": "observed|derived|strong-inference|weak-inference|hypothesis",
  "evidence_refs": [],
  "cross_attempt_finding": "string",
  "feedback_finding": "string",
  "rival_explanations": [],
  "next_probe": "string-or-null",
  "synthesis_disposition": "synthesize|probe-first|eval-repair|eval-only|reject"
}
```

## Synthesis plan record

```json
{
  "variant_id": "string",
  "parent_failure_packet": "string",
  "role": "foundation|api-contract|boundary|adversarial|state|representation|efficiency|genericity|composition|capstone|other",
  "latent_skill": "string",
  "observable_contract": [],
  "starter_artifacts": [],
  "editable_artifacts": [],
  "protected_artifacts": [],
  "oracle_delta": "string",
  "hidden_oracle_dimensions": [],
  "negative_controls": {
    "starter": "required",
    "failure_class": "required",
    "distinct_semantic": "required"
  },
  "heldout_exclusion_evidence": [],
  "provenance": {
    "kind": "synthetic-close-failure-conditioned",
    "generator": "string",
    "model": "string-or-null",
    "prompt_hash": "sha256",
    "seed": "string-or-null"
  }
}
```

## Row verification receipt

```json
{
  "row_id": "string",
  "row_hash": "sha256",
  "oracle_revision": "string",
  "environment_hash": "sha256",
  "commands": [],
  "target_passed": true,
  "starter_rejected": true,
  "failure_mutation_rejected": true,
  "semantic_mutation_rejected": true,
  "protected_artifacts_unchanged": true,
  "isolation_passed": true,
  "integration_passed": true,
  "sanitizer_or_invariant_passed": true,
  "inherited_tests_replayed": 0,
  "new_tests_added": 0,
  "new_oracle_dimensions": 0,
  "assertions_executed": 0,
  "logs": [],
  "verdict": "pass|fail|incomplete"
}
```

Mark inapplicable checks explicitly with a reason rather than silently setting
them to true.

## Serialization receipt

```json
{
  "row_id": "string",
  "messages_hash": "sha256",
  "role_order_valid": true,
  "loss_target_indices": [],
  "parsed_actions": [],
  "editable_scope_valid": true,
  "protected_scope_valid": true,
  "unchanged_emissions": [],
  "required_prose_valid": true,
  "hidden_artifact_leaks": [],
  "proved_target_hash_match": true,
  "tokenizer_id": "string",
  "tokenizer_hash": "sha256",
  "chat_template_hash": "sha256",
  "token_count": 0,
  "context_limit": 0,
  "truncation": false,
  "loss_mask_valid": true,
  "eos_valid": true,
  "replay_final_state_valid": true,
  "verdict": "pass|fail"
}
```

## Lineage and disposition record

```json
{
  "row_id": "string",
  "source_ids": [],
  "parent_ids": [],
  "revision_of": "string-or-null",
  "provenance_kind": "human|organic-trajectory|imported|model-generated|synthetic|repaired|synthetic-close-failure-conditioned",
  "duplicate_relations": [],
  "heldout_relations": [],
  "semantic_adjacency": [],
  "license": "string",
  "privacy_review": "pass|fail|review",
  "disposition": "train|replace-ancestor|review|repair-and-reverify|reject|eval-only",
  "reason_codes": [],
  "evidence_refs": []
}
```

## Dataset manifest

```json
{
  "dataset_id": "string",
  "dataset_version": "string",
  "dataset_sha256": "sha256",
  "row_count": 0,
  "unique_task_count": 0,
  "selected_row_ids_hash": "sha256",
  "parent_manifests": [],
  "excluded_ancestor_ids": [],
  "heldout_manifest_hash": "sha256",
  "verifier_contract_hash": "sha256",
  "row_receipts_hash": "sha256",
  "serialization_receipts_hash": "sha256",
  "tokenizer_hash": "sha256",
  "chat_template_hash": "sha256",
  "composition": {},
  "all_hard_gates_pass": true,
  "limitations": []
}
```

## Training diff

Compare control and candidate in a field-addressable record:

```json
{
  "control_run": "string",
  "candidate_run": "string",
  "authorized_changes": [],
  "unauthorized_changes": [],
  "differences": [
    {
      "field": "data.manifest_hash",
      "control": "sha256",
      "candidate": "sha256",
      "reason": "iteration intervention"
    }
  ],
  "comparison_valid": true
}
```

Include model lineage, trainer, optimizer, scheduler, precision, batch,
accumulation, sequence length, packing, updates, epochs, world size, hardware,
distributed strategy, seed, tokenizer, template, masking, reasoning mode, resume,
checkpoint saving, and evaluator routing.

## Evaluation and promotion record

```json
{
  "candidate_checkpoint": "string",
  "checkpoint_hash": "sha256",
  "evaluation_contract_hash": "sha256",
  "trial_ids": [],
  "single_turn": {
    "trial_scores": [],
    "mean": 0.0,
    "confidence_interval": []
  },
  "feedback": {
    "trial_scores": [],
    "mean": 0.0,
    "conditional_repair_rate": 0.0
  },
  "task_transitions": {},
  "format_and_harness_failures": {},
  "tokens_latency_context_cost": {},
  "regressions": [],
  "primary_gate_passed": false,
  "regression_gates_passed": false,
  "promotion_decision": "promote|reject|rerun-invalid-eval|continue-investigation",
  "decision_evidence": [],
  "next_probe": "string-or-null"
}
```

## Minimum summary tables

Produce these human-readable tables from the machine records:

1. evaluation health by trial;
2. terminal failure stage by task and attempt;
3. observed versus unreachable tests by task;
4. primary mechanism, evidence tier, and synthesis disposition by task;
5. variant role and oracle delta by generated row;
6. executable and serialization gate failures by row;
7. duplicate, revision, and held-out relations;
8. selected/replaced/review/rejected/eval-only counts;
9. corpus composition by family, provenance, difficulty, and token bucket;
10. control-versus-candidate training configuration diff;
11. task-by-trial evaluation matrix and task transitions;
12. promotion gates, verdict, limitations, and next probe.
