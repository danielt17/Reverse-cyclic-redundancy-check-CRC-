# Algorithm Flow

## High-level flow

```mermaid
flowchart LR
  A[Input packets data+crc] --> B[Split equal/unequal lengths]
  B --> C[Estimate polynomial candidates]
  C --> D[Estimate XorIn candidates]
  D --> E[Estimate XorOut + RefIn/RefOut]
  E --> F[Rank/filter combinations]
  F --> G[Final CRC parameter candidates]
```

## Steps

1. Use equal-length packet groups for polynomial inference (XOR-shift + GCD paths).
2. Merge and rank candidate polynomials.
3. Use unequal-length packets to solve for seed (`xor_in`) in GF(2).
4. Brute force reflection flags and recover `xor_out`.
5. Return the stable candidate set.

## Input quality recommendations

- Use packets where one field changes across samples.
- Include both equal-length and unequal-length examples.
- Provide enough samples (typically >= 10 gives better stability).
