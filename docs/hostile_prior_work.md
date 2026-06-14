# Hostile Prior Work

The v3 hostile set was mostly scene-graph and vision-language metadata. For v4, the threat model is narrowed to papers and families that genuinely pressure the force-memory claim.

## Direct Threats

- Action Chunking Transformers / low-cost bimanual imitation learning: transformer policies already handle long-horizon manipulation from demonstrations. The paper must show that force-memory state is not just ordinary temporal context.
- Diffusion Policy: strong visuomotor policies already handle multimodal action distributions over manipulation benchmarks. The paper must show why persistent force memory is needed beyond action-distribution modeling.
- ContactNets and contact-dynamics learning: contact/stiction/discontinuity modeling is established. The paper must distinguish force-memory planning from learned contact dynamics.
- Visuo-Tactile Transformers: transformer representations over vision and touch already exist. The paper must show why the memory object is not merely adding tactile tokens.
- Conformal risk filtering and uncertainty-aware MPC: safety filters already reduce risk under uncertainty. The paper must show force memory improves success without becoming unsafe.
- Online residual system identification: adaptive baselines can infer hidden mechanical parameters. The paper must show force memory beats online ID in the hidden force regimes.
- Recent force-aware foundation-model and tactile representation work: the field is moving toward force/tactile policy learning, so local simulation evidence is not enough for main-conference readiness.

## v4 Evidence Against These Threats

The local benchmark includes recurrent memory, uncertainty, conformal risk, online residual ID, and robust force-threshold baselines. The proposed method beats the strongest non-oracle baseline, `online_residual_system_id`, by `0.160 +/- 0.010` success under combined stress, with lower force-limit violation and damage.

## Remaining Prior-Work Risk

The paper still needs a manual survey and external experiments against trained tactile/force-aware policies before it can be submitted.
