# Shape, operator, build, or runtime failure investigation

> Template status: unexecuted. This report must reduce the failure to a public,
> minimal graph/input. Do not paste a private model, parser log, or customer
> error message.

## Report identity

| Field | Value |
| --- | --- |
| Report ID | `<YYYYMMDD-shape-op-short-name>` |
| Owner | `<name or public handle>` |
| Date / Git commit | `<UTC date>` / `<commit>` |
| Evidence level | `<E0 / E1 / E2 / E3 / E4>` |
| Failure phase | `<export / parse / build / deserialize / set-shape / enqueue>` |
| Status | `<open / root cause identified / fixed / regressed / inconclusive>` |

## One-sentence finding

`<The public minimal graph fails at ... when ... because ...>`

Use `Hypothesis:` if the mechanism has not been isolated.

## Symptom and expected behavior

- **Expected:** `<documented or deliberately defined behavior>`
- **Observed:** `<exact public-reproducer error/exit/status>`
- **First failing phase:** `<export, parser, builder, profile, runtime>`
- **Impact:** `<model cannot build, one shape fails, wrong output, etc.>`
- **Known-good boundary:** `<last phase/shape/version that succeeds>`
- **Known-bad boundary:** `<minimal phase/shape/version that fails>`

## Public asset provenance

| Asset | Public source | Revision | License | Integrity |
| --- | --- | --- | --- | --- |
| Original public model or synthetic graph | `<...>` | `<...>` | `<...>` | `<SHA-256>` |
| Minimal ONNX graph | `<repo path>` | `<commit>` | `<repo license>` | `<SHA-256>` |
| Input tensor(s) | `<public/synthetic origin>` | `<seed>` | `<terms>` | `<SHA-256>` |

Confirm the minimal graph is independently created or comes from a documented
public source, with no proprietary names, dimensions, constants, or metadata.

## Environment and compatibility matrix

Link: `<results/.../environment.json>`

| Component/device | Known good | Known bad | Not tested |
| --- | --- | --- | --- |
| TensorRT version | `<...>` | `<...>` | `<...>` |
| CUDA/driver | `<...>` | `<...>` | `<...>` |
| GPU/compute capability | `<...>` | `<...>` | `<...>` |
| ONNX/opset | `<...>` | `<...>` | `<...>` |
| Precision | `<...>` | `<...>` | `<...>` |
| Concrete shape/profile | `<...>` | `<...>` | `<...>` |

Do not imply compatibility outside tested cells.

## Graph and shape contract

```text
Input/output tensor names:
Rank, layout, dtype, and shape expressions:
Dynamic dimensions and shape tensors:
Optimization profile min / opt / max:
Operator domain, op type, and opset:
Operator attributes:
Plugin name/version/format, if any:
Expected output-shape calculation:
```

Explain whether the failure is in graph semantics, TensorRT support, profile
coverage, data-dependent shape handling, buffer sizing, or API ordering.

## Minimal reproduction

### Preconditions

`<public setup and asset verification>`

### Commands

```bash
# Include ONNX validation, trtexec build/run, and the custom runner when relevant.
<command>
```

### Exact public-reproducer output

```text
<short relevant excerpt; link the full unedited redacted log>
```

### Shape boundary table

| Input shape | Inside profile? | Build result | Runtime result | Output shape | Evidence |
| --- | --- | --- | --- | --- | --- |
| `<min>` | yes | `<...>` | `<...>` | `<...>` | `<...>` |
| `<opt>` | yes | `<...>` | `<...>` | `<...>` | `<...>` |
| `<max>` | yes | `<...>` | `<...>` | `<...>` | `<...>` |
| `<below min>` | no | `<...>` | `<expected diagnostic>` | n/a | `<...>` |
| `<above max>` | no | `<...>` | `<expected diagnostic>` | n/a | `<...>` |

## Reduction history

| Step | Removed/changed | Predicted outcome | Actual outcome | What it rules in/out |
| ---: | --- | --- | --- | --- |
| 1 | `<postprocessing nodes>` | `<...>` | `<...>` | `<...>` |
| 2 | `<operator attributes/input>` | `<...>` | `<...>` | `<...>` |
| 3 | `<dynamic to static dimension>` | `<...>` | `<...>` | `<...>` |

Retain the smallest graph that fails and a neighboring graph that succeeds.

## Investigation log

| Order | Hypothesis | Controlled test | Observation/evidence | Disposition |
| ---: | --- | --- | --- | --- |
| 1 | `<profile does not cover actual shape>` | `<...>` | `<...>` | `<...>` |
| 2 | `<unsupported op/opset/attribute>` | `<...>` | `<...>` | `<...>` |
| 3 | `<shape tensor vs execution tensor confusion>` | `<...>` | `<...>` | `<...>` |
| 4 | `<output buffer size/type mismatch>` | `<...>` | `<...>` | `<...>` |
| 5 | `<context API ordering or stale shape>` | `<...>` | `<...>` | `<...>` |

## Root cause and fix

### Root cause mechanism

`<precise failing contract and evidence that isolates it>`

### Fix or workaround

`<graph rewrite, supported operator, profile correction, plugin, buffer/API fix>`

### Trade-offs and ownership

`<temporary workaround vs upstream fix; performance/accuracy/maintenance cost>`

### Weakest evidence

`<remaining compatibility uncertainty and next falsification test>`

## Regression matrix

| Case | Expected | Before fix | After fix | Automated test/evidence |
| --- | --- | --- | --- | --- |
| Static known-good | pass | `<...>` | `<...>` | `<...>` |
| Dynamic min/opt/max | pass | `<...>` | `<...>` | `<...>` |
| Outside profile | actionable fail | `<...>` | `<...>` | `<...>` |
| Wrong dtype/rank | actionable fail | `<...>` | `<...>` | `<...>` |
| Repeated shape changes | stable/correct | `<...>` | `<...>` | `<...>` |

## Conclusion and limitations

`<Scope the finding to tested graph, versions, profiles, and device. Do not call
an unsupported operator a TensorRT defect without evidence and version review.>`

## Public release checklist

- [ ] Minimal graph/input is public or independently synthetic and license-safe.
- [ ] Full logs were reviewed for paths, hostnames, endpoints, and private symbols.
- [ ] Min/opt/max and out-of-profile behavior are explicitly tested.
- [ ] Root cause is isolated from exporter, parser, builder, runtime, and user-buffer alternatives.
- [ ] Workaround and durable fix are distinguished.
- [ ] Regression fails before and passes after the fix.
- [ ] No GPU/TensorRT validation is inferred from CPU CI.
