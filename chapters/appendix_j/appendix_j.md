# Appendix J: Adversary Models

Every security claim is meaningless until you say what the adversary is allowed to do. "This scheme is
secure" is not a statement; "this scheme is indistinguishable under chosen-plaintext attack against a
probabilistic polynomial-time adversary" is. This appendix collects the adversary models used throughout
cryptography and secure computation into one reference, with the defining papers, worked numerical examples,
and exercises. It extends the formal-security material of Chapter 2 (Section 2.20), the threat-modeling
methods of Chapter 5 (Section 5.8), and the privacy-preserving computation of Chapter 17 (Section 17.4).

## J.1 The Three Layers of an Adversary Model

A complete adversary model answers three independent questions, and confusing them is the most common error
in threat-model write-ups. The layers compose: a system's threat model picks one item from each.

1. **Behavior.** How do the parties that hold key material act? Do they follow the protocol, deviate
   arbitrarily, or something in between?
2. **Corruption.** Which parties does the adversary control, when does it choose them, how many, and with
   what computational power?
3. **Game.** What must the adversary achieve to win, and what oracles does it get while trying?

```{mermaid}
flowchart TB
    T[Complete adversary model]
    T --> B[Layer 1: Behavior<br/>semi-honest, semi-malicious,<br/>covert, rational, malicious]
    T --> C[Layer 2: Corruption<br/>static or adaptive or mobile,<br/>threshold, computational power]
    T --> G[Layer 3: Game<br/>goal x capability,<br/>IND-CPA, IND-CCA2, IND-CPA-D]
    B --> S[Threat model statement]
    C --> S
    G --> S
```

Single-key encryption schemes usually need only Layer 3, because there is one key holder and no protocol.
Multi-party and multi-key systems need all three.

## J.2 Layer 1: Behavioral Models

The behavioral models form a ladder from a party that merely watches to one that is fully controlled by the
adversary. The two endpoints, semi-honest and malicious, are standard; the models between them exist because
those endpoints are respectively too optimistic and too expensive.

```{mermaid}
flowchart LR
    H[Fully honest] --> SH[Semi-honest<br/>passive]
    SH --> LZ[Lazy<br/>aborts, free-rides]
    LZ --> FS[Fail-stop<br/>omission]
    FS --> HL[Honest-looking]
    HL --> SM[Semi-malicious]
    SM --> CV[Covert]
    CV --> RA[Rational]
    RA --> MA[Malicious<br/>active, Byzantine]
```

**Fully honest.** The baseline: the party follows the protocol and protects its own view. Not an adversary,
but the reference point for everything below.

**Semi-honest (honest-but-curious, passive).** The party follows the protocol specification exactly, but the
adversary learns its entire internal state and tries to infer more than the output allows. Formally the
adversary learns the party's *view*: its input, its random tape, and every message it received. Security is
proved by exhibiting a simulator that reproduces that view from the party's input and output alone. This
model captures confidentiality against an insider who will not risk detection, and it is the standard
baseline in Chapter 17.

**Lazy (honest-but-lazy).** Formalized in two ways. In secure multi-party computation, a lazy party behaves
honestly but aborts partway through without colluding with corrupt parties; classical MPC lumps it in with
the adversary, which is unrealistic, so Badrinarayanan, Jain, Manohar, and Sahai gave it meaningful
guarantees in "Secure MPC: Laziness Leads to GOD" (ePrint 2018/580; ASIACRYPT 2020), introducing threshold
multi-key FHE and obtaining round-optimal MPC with guaranteed output delivery against a threshold mixed
adversary. In encryption, lazy parties are modeled as rational players unwilling to generate costly
randomness. The applied face in collaborative learning is the **free-rider**: a client that submits fabricated
model updates without training, to obtain the global model without contributing (including dynamic
free-riders that behave honestly early and switch later).

**Fail-stop, fail-corrupt, and omission.** Fail-corruption lets the adversary force a party to crash
irrevocably; omission corruption lets it selectively block messages to or from a party without reading them.
This is enforced laziness rather than chosen laziness.

**Honest-looking.** May deviate, but only in ways indistinguishable from honest execution (Canetti and
Ostrovsky, "Secure computation with honest-looking parties: What if nobody is truly honest?", STOC 1999,
pp. 255-264).

**Semi-malicious.** Must follow the protocol specification, but may freely choose its input and random coins
in every round (Asharov, Jain, Lopez-Alt, Tromer, Vaikuntanathan, and Wichs, EUROCRYPT 2012, LNCS 7237,
pp. 483-501). It is now the standard model for multi-party and multi-key FHE constructions, because a client
that reports a fabricated value is exercising exactly this input-substitution power while still producing
protocol-conformant messages.

**Covert.** May deviate arbitrarily, but the protocol guarantees that cheating is detected with at least a
fixed probability epsilon, the **deterrence factor**, so adversaries who fear reputational or contractual
consequences refrain from cheating (Aumann and Lindell, TCC 2007; journal version, Journal of Cryptology,
2010). Covert security collapses to malicious security as epsilon approaches 1. The **publicly verifiable**
variant adds that a party detecting cheating receives a certificate it can publish to convince third parties,
without revealing its own input (Asharov and Orlandi, "Calling Out Cheaters: Covert Security with Public
Verifiability", ASIACRYPT 2012).

**Rational.** Utility-maximizing: cheats only when the expected payoff exceeds the expected penalty (Halpern
and Teague, "Rational secret sharing and multiparty computation", STOC 2004, pp. 623-632). The key structural
result is that protocols with a bounded, known number of iterations fall to backward induction and cannot be
considered rational, which is why rational protocols hide the reconstruction round. For rational and fully
adversarial players in one model, see Lysyanskaya and Triandopoulos, "Rationality and Adversarial Behavior in
Multi-Party Computation", CRYPTO 2006.

**Malicious (active, Byzantine).** Completely controlled by the adversary and free to deviate arbitrarily:
fabricated inputs, malformed keys, early aborts, and any message it likes.

**Mixed adversaries.** Simultaneously corrupt up to t_a parties actively, t_p passively, and t_f in a
fail-stop manner, filling the space between the pure settings in which passive corruption tolerates t < n/2
but active corruption only t < n/3 (Fitzi, Hirt, and Maurer, CRYPTO 1998).

**Friends-and-foes (FaF).** Additionally requires that honest parties' inputs stay hidden even from other,
curious honest parties who might receive the adversary's leaked view. It comes in weak and strong flavors,
and FaF security does not imply mixed-adversary security (Alon, Omri, and Paskin-Cherniavsky, "MPC with
Friends and Foes", CRYPTO 2020, pp. 677-706).

| Model | Follows protocol? | Distinctive power or limit | Canonical reference |
|---|---|---|---|
| Semi-honest | Yes | Learns from its full view only | Goldreich, *Foundations of Cryptography*, vol. 2 |
| Lazy | Yes, until it stops | Aborts or skips costly work, no collusion | Badrinarayanan et al., ePrint 2018/580 |
| Fail-stop / omission | Yes, until crashed | Crash or message blocking forced by adversary | Fitzi, Hirt, Maurer, CRYPTO 1998 |
| Honest-looking | Deviates undetectably | Deviations indistinguishable from honesty | Canetti, Ostrovsky, STOC 1999 |
| Semi-malicious | Yes | Arbitrary inputs and random coins | Asharov et al., EUROCRYPT 2012 |
| Covert | No, if unwatched | Deterred by detection probability epsilon | Aumann, Lindell, TCC 2007 |
| Rational | Depends on utility | Cheats only when payoff exceeds penalty | Halpern, Teague, STOC 2004 |
| Malicious | No | Arbitrary deviation, aborts, fake keys | Goldreich, *Foundations*, vol. 2 |
| Mixed | Varies per party | t_a active, t_p passive, t_f fail-stop at once | Fitzi, Hirt, Maurer, CRYPTO 1998 |
| Friends-and-foes | Adversary no, friends yes | Curious honest parties also constrained | Alon, Omri, Paskin-Cherniavsky, CRYPTO 2020 |

## J.3 Layer 2: Corruption Modifiers

These apply on top of any behavioral model.

**Timing.** A **static** adversary fixes its corruption set before the protocol begins. An **adaptive**
adversary chooses during execution, based on what it has already seen. A **mobile** adversary dynamically
corrupts and releases parties, keeping at most f corrupted at any moment while the set changes over time
(Ostrovsky and Yung, PODC 1991, pp. 51-59). **Proactive** protocols counter mobility by dividing execution
into phases and refreshing shares each phase, tolerating eventual corruption of every party as long as no
more than the threshold are corrupt within any single phase (Herzberg, Jarecki, Krawczyk, and Yung,
CRYPTO 1995).

**Scale and structure.** Either a threshold (honest versus dishonest majority, with the classical t < n/2
passive and t < n/3 active tolerances in the unconditional setting) or a **generalized adversary structure**
specifying arbitrary sets of actively and passively corruptible subsets rather than a simple count.

**Computational power.** Probabilistic polynomial-time (computational security) versus computationally
unbounded (information-theoretic or unconditional security).

**Scheduling.** A **rushing** adversary waits to see the honest parties' messages in a round before sending
its own, which matters whenever a protocol's security depends on simultaneity.

## J.4 Layer 3: Single-Key Game Models

The game layer crosses a **goal** (what counts as a break) with a **capability** (what oracles the adversary
may query).

**Goals**, from weakest break to strongest:

- **OW (one-wayness):** recover the plaintext of a given ciphertext.
- **IND (indistinguishability, equivalent to semantic security):** distinguish encryptions of two chosen
  messages.
- **NM (non-malleability):** produce a ciphertext whose plaintext is meaningfully related to a target
  plaintext.
- **KR (key recovery):** recover the secret key itself, the strongest break.
- For authenticated encryption, the integrity goals **INT-PTXT** and **INT-CTXT**, with the composition
  analysis in Bellare and Namprempre, "Authenticated Encryption: Relations among Notions and Analysis of the
  Generic Composition Paradigm", ASIACRYPT 2000, LNCS 1976, pp. 531-545.

**Capabilities**, in increasing order of power:

- **COA (ciphertext-only)** and **KPA (known-plaintext):** classical cryptanalytic settings.
- **CPA (chosen-plaintext):** the adversary obtains encryptions of plaintexts it chooses.
- **CCA1 (non-adaptive, the "lunchtime" attack):** a decryption oracle available only *before* the challenge
  ciphertext is issued.
- **CCA2 (adaptive):** a decryption oracle available before and after the challenge, on anything except the
  challenge itself.

Crossing goals with capabilities gives IND-CPA, IND-CCA1, IND-CCA2, NM-CPA, NM-CCA1, and NM-CCA2. The complete
map of implications and separations is due to Bellare, Desai, Pointcheval, and Rogaway, "Relations Among
Notions of Security for Public-Key Encryption Schemes", CRYPTO 1998, LNCS 1462, which proves either an
implication or a separation for every pair and also treats plaintext awareness in the random oracle model.

```{mermaid}
flowchart TB
    INDCCA2[IND-CCA2<br/>strongest] --> NMCCA2[NM-CCA2]
    INDCCA2 --> INDCCA1[IND-CCA1]
    NMCCA2 --> NMCCA1[NM-CCA1]
    INDCCA1 --> INDCPA[IND-CPA]
    NMCCA1 --> NMCPA[NM-CPA]
    NMCPA --> INDCPA
    INDCPA --> OW[OW-CPA<br/>weakest]
```

The headline facts to remember: IND-CCA2 implies every other notion in the diagram; IND-CCA1 does **not**
imply NM-CPA; NM-CPA does **not** imply IND-CCA1; and NM-CCA1 does **not** imply NM-CCA2. NM-CPA does imply
IND-CPA. This is why IND-CCA2 is the default target for general-purpose public-key encryption.

## J.5 Extended Single-Key Models

Real deployments hand adversaries powers the classical games do not model.

- **Related-key attacks (RKA).** The adversary requests encryptions under adversarially transformed keys.
  Bellare and Kohno gave the first formal treatment (EUROCRYPT 2003, LNCS 2656, pp. 491-506), parameterizing
  the adversary by a class of related-key-deriving functions and showing that RKA security is unachievable
  without restricting that class. The cryptanalytic origin is Biham, "New Types of Cryptanalytic Attacks Using
  Related Keys", EUROCRYPT 1993. In symmetric cryptanalysis, "single-key model" specifically means the
  absence of this power.
- **Key-dependent message (KDM) and circular security.** The adversary obtains encryptions of functions of
  the secret key. Circular security, which allows securely encrypting the secret key's own bits, is the most
  elementary form. This matters directly to fully homomorphic encryption, because bootstrapping publishes an
  encryption of the secret key under itself.
- **Leakage-resilient security.** Security when adversarially chosen functions of the secret key leak, the
  formal counterpart of side-channel attacks (Akavia, Goldwasser, and Vaikuntanathan, TCC 2009).
- **Selective-opening security (SOA).** The adversary sees many ciphertexts and then corrupts a subset of
  senders, learning their messages and random coins (Bellare, Hofheinz, and Yilek, EUROCRYPT 2009, LNCS 5479,
  pp. 1-35).

## J.6 Adversary Models for Homomorphic Encryption

Homomorphic encryption breaks the standard ladder, because malleability is the point of the scheme.

Since anyone can transform a ciphertext into a ciphertext of a related plaintext, non-malleability and
IND-CCA2 are unachievable by definition, so **IND-CCA1 is the classical ceiling**. The recent **vCCA** notion
of Manulis and Nguyen (EUROCRYPT 2024) pushes past IND-CCA1 by adding integrity through verifiability.

The passive story is subtler than IND-CPA, and this is where the modern literature concentrates:

- **IND-CPA-D** (CPA with decryption oracles on honestly evaluated ciphertexts). Li and Micciancio
  (EUROCRYPT 2021) presented passive attacks against the approximate scheme CKKS that run in expected
  polynomial time, achieve complete key recovery, and were implemented against HEAAN, SEAL, HElib, and
  PALISADE. The mechanism is that decryption outputs of approximate schemes leak the LWE noise in the
  ciphertext, which enables practical secret-key recovery, showing that plain IND-CPA does not adequately
  capture passive security for approximate schemes.
- **Noise flooding as countermeasure.** Adding Gaussian noise to the CKKS decryption output suffices for
  IND-CPA-D security, with nearly matching upper and lower bounds on the required noise (Li, Micciancio,
  Schultz, and Sorrell, CRYPTO 2022). However, noise tailored to the actual error in a given ciphertext rather
  than the worst-case error remains vulnerable, and Guo, Nabokov, Suvanto, and Johansson gave key-recovery
  attacks on non-worst-case noise-flooding countermeasures at USENIX Security 2024.
- **Exact schemes are not exempt.** Checri, Sirdey, Boudguiga, and Bultel (CRYPTO 2024) exhibited a CPA-D
  key-recovery attack on the linearly homomorphic Regev cryptosystem that generalizes to BFV, BGV, and TFHE,
  and Cheon, Choe, Passelegue, Stehle, and Suvanto independently attacked the IND-CPA-D security of exact FHE
  schemes at CCS 2024.
- **Bounded-query refinement.** q-IND-CPA-D bounds the number of decryption queries, so the attacker's
  advantage is governed by the failure probability of the scheme's noise bounds.

The practical lesson for anyone deploying FHE: quoting "IND-CPA secure" is not sufficient if any decryption
result, partial or full, ever reaches a party who also sees ciphertexts. State the model as IND-CPA-D and
state the smudging noise explicitly.

## J.7 Multi-Key Settings

"Multi-key" covers four genuinely different settings, each with its own adversary model.

**Multi-user (many independent keys, adversary attacks any one).** Motivated by Hastad-type attacks: the same
message encrypted under three RSA moduli with exponent 3 is recoverable by Chinese remaindering even though
each ciphertext is individually secure. Bellare, Boldyreva, and Micali, "Public-Key Encryption in a Multi-User
Setting: Security Proofs and Improvements" (EUROCRYPT 2000, LNCS 1807, pp. 259-274), proved that single-user
indistinguishability implies multi-user security, but the generic bound multiplies the single-instance
success probability by the number of keys, and at internet scale that factor materially erodes the claim.
Adjacent notions are key privacy (anonymity: a ciphertext should not reveal which public key was used) and
multi-recipient security with randomness reuse (Bellare, Boldyreva, and Staddon, PKC 2003).

**Multi-key FHE (independent keys, joint computation).** Lopez-Alt, Tromer, and Vaikuntanathan,
"On-the-fly multiparty computation on the cloud via multikey fully homomorphic encryption" (STOC 2012,
pp. 1219-1234): an untrusted but powerful cloud computes over data from dynamically chosen user sets, with
inputs and intermediate results hidden from the cloud and from other users. Its threat model composes a
passive or malicious evaluator with coalitions of users, and the joint decryption of the result is a protocol
analyzed under the Layer 1 models, typically semi-malicious.

**Threshold encryption and threshold FHE (one logical key, secret-shared t-of-n).** The adversary corrupts a
set of share holders below the reconstruction threshold, and the model must additionally state corruption
timing and behavior. Foundational constructions include Boneh et al., "Threshold Cryptosystems from Threshold
Fully Homomorphic Encryption" (CRYPTO 2018), and Boudgoust and Scholl (ASIACRYPT 2023). The distinctive attack
surface is the **partial decryption** itself: threshold variants of BFV, BGV, and CKKS are exposed to CPA-D
attackers and are insecure without smudging noise added after partial decryption. This is exactly the
situation in federated learning when clients collaboratively decrypt an aggregate (Chapter 17), and CPA-D
attacks in that setting have been extended to full key recovery.

**Identity-based, attribute-based, and functional encryption (one master key, many derived keys).** The
adversary gets a key-extraction oracle, and the central requirement is **collusion resistance**: users pooling
their decryption keys must not derive capability beyond what each holds individually. Orthogonally, the
target-commitment axis distinguishes **selective** security (the adversary commits in advance to the identity
it will attack, as in IND-sID-CPA) from **adaptive** security (it chooses the target during the game, as in
IND-ID-CCA2). **Complexity leveraging** converts a selective proof into an adaptive one at a 2^l cost in the
reduction, where l is the attribute or identity length.

## J.8 Composing a Complete Threat Model

A publishable threat model picks one item from each layer and states them in a single sentence. The template:

> [goal]-[capability] security of [scheme] against a [timing], [behavior] adversary corrupting [structure]
> parties with [computational power] and [oracle access].

Two worked instantiations:

- *Classical public-key deployment.* "IND-CCA2 security of the KEM against a probabilistic polynomial-time
  adversary with adaptive decryption-oracle access." Only Layer 3 is needed, because there is one key holder.
- *Federated learning with threshold CKKS.* "IND-CPA-D-style security of the threshold CKKS scheme against a
  static, semi-malicious coalition of up to K-1 clients, plus an honest-but-curious aggregation server holding
  the partial-decryption oracle, with the smudging noise variance stated explicitly." A client that
  misreports a training metric is handled separately at the protocol layer, where randomized verification
  converts it from malicious to covert with the audit rate as the deterrence factor epsilon.

Notice what the second statement does: it names the game (IND-CPA-D), the timing (static), the behavior
(semi-malicious clients, semi-honest server), the structure (up to K-1 of K), and the extra oracle (partial
decryption). Every one of those is a place where an unstated assumption could hide a break.

## J.9 Worked Numerical Examples

**Example J.1 (covert security: the minimum deterrence factor).** An adversary gains G = 100 units by cheating
and loses P = 1000 units if caught. With deterrence factor epsilon, its expected utility from cheating is

    E = (1 - epsilon) * G - epsilon * P

Cheating is irrational when E < 0, that is when G < epsilon * (G + P), so

    epsilon > G / (G + P) = 100 / 1100 = 0.0909

A detection probability above roughly 9.1 percent suffices. At the common epsilon = 1/2 the expected utility is
0.5 * 100 - 0.5 * 1000 = -450, comfortably negative. This is why covert security is attractive in practice:
deterrence needs only a modest audit rate, not the full cost of malicious security.

**Example J.2 (multi-user degradation).** A scheme has single-user advantage at most 2^-128. Deployed across
n = 2^30 users, the generic multi-user bound is n * 2^-128 = 2^30 * 2^-128 = 2^-98. The deployment therefore
offers about 98 bits, not 128: thirty bits of security are consumed by scale alone. To retain 128 bits across
2^30 users, the single-user target must be 2^-158.

**Example J.3 (corruption thresholds).** With n = 10 parties in the unconditional setting, passive security
requires t < n/2 = 5, so at most 4 corrupted parties; active security requires t < n/3 = 3.33, so at most 3. A
mixed adversary might be specified as t_a = 2 active plus t_p = 2 passive, which is feasible where t_a = 4
active would not be.

**Example J.4 (complexity leveraging).** An attribute-based scheme is proved selectively secure with advantage
2^-256, and identities are l = 128 bits. Complexity leveraging yields adaptive security with advantage
2^l * 2^-256 = 2^128 * 2^-256 = 2^-128. The selective proof must therefore be twice as strong as the adaptive
guarantee you want, which is precisely why the technique is considered expensive.

**Example J.5 (proactive refresh against a mobile adversary).** A system has n = 7 share holders, a
reconstruction threshold of t = 3, and tolerates f = 2 corruptions per phase. Over 10 phases the adversary can
touch up to 20 party-slots, and may well corrupt every party at some point, yet it never holds 3 valid shares
simultaneously because each refresh invalidates old shares. Security depends on the per-phase bound, not the
lifetime total.

## J.10 Exercises

1. A protocol is proved secure against semi-honest adversaries. A reviewer objects that a participant could
   submit a fabricated input. Which behavioral model does that objection invoke, and is the proof wrong?
2. Explain why IND-CCA2 is unachievable for any homomorphic encryption scheme, in two sentences.
3. An auditor cheats for a gain of 50 and faces a penalty of 200 if caught. What is the minimum deterrence
   factor that makes cheating irrational?
4. A scheme offers 2^-120 single-user advantage and is deployed to 2^20 users. What multi-user advantage does
   the generic bound give, and how many bits of security are lost?
5. Give one reason a designer might prefer covert security to malicious security, and one reason a regulator
   might reject that choice.
6. Which is stronger, NM-CPA or IND-CCA1? Justify your answer using the relations of Section J.4.
7. In a federated-learning system, clients jointly decrypt an aggregate. Name the oracle this creates and the
   security notion that must therefore be used instead of IND-CPA.
8. A protocol tolerates 2 corruptions per phase across 12 phases. Explain why it can survive an adversary that
   eventually corrupts all parties.
9. Write a complete threat-model sentence, using the Section J.8 template, for a two-party private set
   membership protocol in which only the client learns the answer and the server may choose its own inputs.
10. Why does a rational-adversary protocol avoid a fixed, publicly known number of rounds?

### Answer Key

1. It invokes the semi-malicious model (protocol-conformant messages, adversarially chosen input). The proof
   is not wrong; it is simply proved in a weaker model, and the claim must be restated or the protocol
   strengthened.
2. Anyone can maul a ciphertext into a ciphertext of a related plaintext, which is exactly the capability
   IND-CCA2 forbids. Since malleability is the intended functionality, the notion is unachievable and CCA1 is
   the ceiling.
3. epsilon > 50 / (50 + 200) = 0.2, so above 20 percent.
4. 2^20 * 2^-120 = 2^-100, so 20 bits are lost.
5. Covert security is far cheaper computationally and suffices where participants are identifiable and
   reputation-sensitive. A regulator may reject it because cheating still succeeds with probability
   1 - epsilon, which is unacceptable when the harm from a single undetected breach is severe.
6. Neither implies the other: Section J.4 records that IND-CCA1 does not imply NM-CPA and NM-CPA does not
   imply IND-CCA1. They are incomparable.
7. It creates a partial-decryption oracle, so the appropriate notion is IND-CPA-D (with smudging noise
   specified), not IND-CPA.
8. The adversary is mobile but bounded per phase, and proactive share refresh invalidates shares captured in
   earlier phases, so it never assembles a threshold set at one time.
9. For example: "IND-style privacy of the PSM protocol against a static, semi-malicious server and a
   probabilistic polynomial-time client, with one-sided simulation guaranteeing full simulation for the
   output-receiving client and privacy for the server."
10. Because a known final round enables backward induction: each party's optimal move in the last round is to
    withhold, which unravels the incentive to cooperate in every earlier round.
