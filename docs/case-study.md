# Case study: prompt-based phishing classification

## Problem and scope

I wanted to test whether an LLM could apply the reasoning I use during phishing triage: inspect available cues, consider pressure in context, and determine what action the sender wants. The assignment restricted the classifier to subject and body. It had no sender authentication, verified link destinations, rendered email view, attachment analysis, or recipient history.

The dataset contained 500 labeled examples. I used a stratified split of 400 development emails and 100 validation emails with seed 520. Four demonstrations, balanced across the two labels, came only from development data. Every configuration was compared on the same validation rows.

## Experiments and findings

The basic prompt achieved 0.782135 macro F1. Adding a structured cue/pressure/action strategy reduced it to 0.770833. That first hypothesis was not supported by the comparison.

A clearer spam/phishing boundary improved macro F1 to 0.793303. Adding four labeled development examples produced the strongest result: 0.899639 macro F1 and 90% accuracy. Relative to the boundary-only prompt, false positives fell from 19 to eight, while false negatives increased from one to two. The improvement involved a tradeoff.

A longer intent-focused revision helped the zero-shot setup but hurt the few-shot setup. The revised few-shot version reached 0.859098. More detailed instructions did not consistently improve classification.

With the intent-focused base held fixed, JSON label-only output reached 0.836801, compared with 0.826087 for integer output. Adding a SOC role or requiring a brief evidence explanation each produced 0.815271. These small differences need confirmation; the experiment does not establish universal benefits or disadvantages for those techniques.

## Error investigation

The best prompt produced eight false positives and two false negatives. Several class-0 messages contained promotions, urgent offers, forms, or information requests. Some would still deserve operational investigation. Agreement with a benchmark label is not equivalent to proving a message safe.

The two missed phishing messages resembled ordinary secure-message and file-transfer workflows. Their plausible business presentation is a possible explanation for the mistakes, not a claim about hidden model reasoning. The experiment lacked the technical evidence an analyst would normally use to resolve such ambiguity.

## Provider failure and recovery

During test export, Azure's content filter rejected one email. A second gateway model was also filtered. A Claude Haiku request using the same text, prompt, and demonstrations returned a valid binary response.

The export used a documented rule: only explicit provider content-filter blocks could use the fallback. Authentication failures, unrelated HTTP errors, and malformed responses did not receive default labels. Responses were cached separately by model policy, and the test audit recorded which model supplied each label.

The submitted pipeline contained 99 GPT 4.1 Mini responses and one Claude Haiku response. This was a conditional fallback, not a two-model ensemble or an independently validated accuracy improvement. The hidden test labels did not establish whether the fallback prediction was correct.

## Public result and limitations

Public Kaggle macro F1 was 0.79166 on 50 hidden-label emails, below local validation macro F1 of 0.899639 on 100 emails. Repeated validation-guided tuning, sampling differences, and corpus differences are possible contributors; their individual effects were not established.

Long inputs were consistently truncated to the beginning and end of the body, which could remove relevant middle content. Temperature 0 and cached reruns do not provide evidence of independent-run stability. The Enron/Nazario source mix may also permit corpus-specific shortcuts.

## Next steps

I would compare Claude Sonnet and GPT 4.1 Mini on the same validation emails with fixed prompts and demonstrations. I suspect model choice may have contributed to the lower public result, but the project did not test that explanation. Further work would reserve untouched evaluation data before tuning, vary development-example selection and order, isolate individual instruction changes, and evaluate the fallback on labeled blocked examples when available.

For SOC use, this project supports further research into analyst-assisted triage. It does not justify autonomous blocking or replacement of technical verification.

## References

- Dawkins, S., and Jacobs, J. (2023). *NIST Phish Scale User Guide*. NIST TN 2276. https://doi.org/10.6028/NIST.TN.2276
- Heiding, F., Schneier, B., Vishwanath, A., Bernstein, J., and Park, P. S. (2024). *Devising and Detecting Phishing Emails Using Large Language Models*. IEEE Access. https://doi.org/10.1109/ACCESS.2024.3375882
- Microsoft. *Content filtering for Microsoft Foundry Models (classic)*. https://learn.microsoft.com/en-us/azure/foundry-classic/foundry-models/concepts/content-filter

Coursework code and analysis should remain private unless the course permits sharing. No competition email text, hidden-label lookup, or prediction CSV is included in this case study.
