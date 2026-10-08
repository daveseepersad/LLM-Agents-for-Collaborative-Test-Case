# Paper figures and findings

## Paper (Groq archive)

`results`: 1 run(s), 28 experiments, 168 module results, 0 errors, 0 missing mutation scores.

Experiments per cell:

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 2 | 4 | 2 |
| Planner+ |  | 4 | 2 |
| Worker+ |  | 4 | 2 |
| Weak | 2 | 4 | 2 |

### Coverage by Architecture and Configuration

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 97.2 | 98.6 | 99.9 |
| Planner+ |  | 97.7 | 99.7 |
| Worker+ |  | 94.9 | 99.7 |
| Weak | 91.4 | 97.2 | 99.8 |

### Mutation Score by Architecture and Configuration

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 66.5 | 67.4 | 75.4 |
| Planner+ |  | 70.8 | 66.6 |
| Worker+ |  | 64.4 | 72.9 |
| Weak | 64.9 | 67.3 | 71.0 |

### Token Usage by Architecture and Configuration

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 2,200 | 12,121 | 18,476 |
| Planner+ |  | 16,043 | 29,168 |
| Worker+ |  | 17,064 | 35,150 |
| Weak | 4,155 | 23,270 | 28,721 |

### Coverage of module results (% of module results per band)

| architecture | module results | 100% | 90-99% | 60-89% | 1-59% | 0% |
|---|---|---|---|---|---|---|
| single | 24 | 70.8 | 12.5 | 12.5 | 4.2 | 0.0 |
| collaborative | 96 | 76.0 | 13.5 | 9.4 | 1.0 | 0.0 |
| competitive | 48 | 85.4 | 14.6 | 0.0 | 0.0 | 0.0 |

## Replication (Foundry, 3 runs)

`replication/foundry/rep*/results`: 3 run(s), 28 experiments, 504 module results, 0 errors, 4 missing mutation scores.

Experiments per cell:

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 2 | 4 | 2 |
| Planner+ |  | 4 | 2 |
| Worker+ |  | 4 | 2 |
| Weak | 2 | 4 | 2 |

### Coverage by Architecture and Configuration

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 95.9 | 91.2 | 99.7 |
| Planner+ |  | 96.4 | 99.8 |
| Worker+ |  | 96.4 | 99.8 |
| Weak | 97.1 | 92.2 | 98.9 |

Range of per-run means:

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 95.2 to 96.6 | 88.3 to 93.8 | 99.4 to 99.9 |
| Planner+ |  | 95.2 to 97.3 | 99.6 to 99.9 |
| Worker+ |  | 96.0 to 96.8 | 99.6 to 99.9 |
| Weak | 96.6 to 97.5 | 86.8 to 96.8 | 97.2 to 99.8 |

### Mutation Score by Architecture and Configuration

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 65.7 | 65.5 | 72.5 |
| Planner+ |  | 65.9 | 71.3 |
| Worker+ |  | 64.0 | 69.8 |
| Weak | 64.9 | 61.9 | 68.5 |

Range of per-run means:

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 65.0 to 66.6 | 62.0 to 68.0 | 69.6 to 74.3 |
| Planner+ |  | 65.3 to 67.1 | 66.9 to 75.4 |
| Worker+ |  | 62.7 to 65.2 | 68.6 to 70.4 |
| Weak | 63.1 to 66.5 | 60.7 to 63.2 | 65.3 to 71.7 |

### Token Usage by Architecture and Configuration

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 2,264 | 17,770 | 25,137 |
| Planner+ |  | 21,619 | 39,474 |
| Worker+ |  | 16,424 | 33,479 |
| Weak | 3,511 | 30,734 | 44,693 |

Range of per-run means:

| configuration | single | collaborative | competitive |
|---|---|---|---|
| Strong | 2,229 to 2,304 | 15,617 to 19,400 | 21,095 to 27,735 |
| Planner+ |  | 19,854 to 24,021 | 34,640 to 45,239 |
| Worker+ |  | 14,679 to 17,998 | 29,834 to 38,232 |
| Weak | 3,459 to 3,608 | 27,362 to 33,081 | 41,561 to 50,351 |

### Coverage of module results (% of module results per band)

| architecture | module results | 100% | 90-99% | 60-89% | 1-59% | 0% |
|---|---|---|---|---|---|---|
| single | 72 | 59.7 | 23.6 | 16.7 | 0.0 | 0.0 |
| collaborative | 288 | 75.3 | 13.9 | 4.2 | 4.2 | 2.4 |
| competitive | 144 | 88.9 | 10.4 | 0.7 | 0.0 | 0.0 |

## Findings of the paper

| Finding | Paper (Groq archive) | Replication (Foundry, 3 runs) |
|---|---|---|
| RQ1: Competitive coverage is near-complete (>= 99%) in every configuration | yes (min 99.7%) | no (min 98.9%) |
| RQ1: Multi-agent coverage >= Single-Agent coverage (Strong, Weak) | yes (Strong: 97.2 vs 98.6, Weak: 91.4 vs 97.2) | no (Strong: 95.9 vs 91.2, Weak: 97.1 vs 92.2) |
| RQ1: Competitive >= Collaborative coverage in every configuration | yes (Strong: 98.6/99.9, Planner+: 97.7/99.7, Worker+: 94.9/99.7, Weak: 97.2/99.8) | yes (Strong: 91.2/99.7, Planner+: 96.4/99.8, Worker+: 96.4/99.8, Weak: 92.2/98.9) |
| RQ1: Single-Agent coverage drops with the Weak configuration | yes (Strong 97.2 vs Weak 91.4) | no (Strong 95.9 vs Weak 97.1) |
| RQ1: Collaborative coverage is lowest in Worker+ | yes (Worker+ 94.9, min Worker+ 94.9) | no (Worker+ 96.4, min Strong 91.2) |
| RQ2: Mutation scores are well below coverage (every cell at least 15 points lower) | yes (smallest gap 24.5 points) | yes (smallest gap 25.6 points) |
| RQ2: Competitive has the highest mutation score in most configurations (>= 3 of 4) | yes (3 of 4 (Strong, Worker+, Weak)) | yes (4 of 4 (Strong, Planner+, Worker+, Weak)) |
| RQ2: Multi-agent mutation gains over Single-Agent are limited (< 10 points, Strong and Weak) | yes (Strong: +8.9, Weak: +6.2) | yes (Strong: +6.8, Weak: +3.5) |
| RQ3: Competitive uses the most tokens in every configuration | yes (Strong: competitive, Planner+: competitive, Worker+: competitive, Weak: competitive) | yes (Strong: competitive, Planner+: competitive, Worker+: competitive, Weak: competitive) |
| RQ3: Multi-agent uses several times the Single-Agent tokens with the same models (>= 3x, Strong and Weak) | yes (5.5x to 8.4x) | yes (7.8x to 12.7x) |
| RQ3: Single-Agent with Weak models uses more tokens than with Strong models | yes (Strong 2200 vs Weak 4155) | yes (Strong 2264 vs Weak 3511) |

## Paper (Groq archive) within the run-to-run range of Replication (Foundry, 3 runs)

Coverage by Architecture and Configuration: 3 of 10 cells in range.

| coverage: paper minus replication | single | collaborative | competitive |
|---|---|---|---|
| Strong | +1.4 | +7.4 | +0.2 (in range) |
| Planner+ |  | +1.3 | -0.1 (in range) |
| Worker+ |  | -1.5 | -0.1 (in range) |
| Weak | -5.7 | +5.0 | +0.9 |

Mutation Score by Architecture and Configuration: 5 of 10 cells in range.

| mutation: paper minus replication | single | collaborative | competitive |
|---|---|---|---|
| Strong | +0.8 (in range) | +1.9 (in range) | +2.9 |
| Planner+ |  | +4.9 | -4.6 |
| Worker+ |  | +0.5 (in range) | +3.1 |
| Weak | -0.1 (in range) | +5.5 | +2.5 (in range) |

Token Usage by Architecture and Configuration: 2 of 10 cells in range.

| tokens: paper minus replication | single | collaborative | competitive |
|---|---|---|---|
| Strong | -64 | -5,649 | -6,661 |
| Planner+ |  | -5,576 | -10,306 |
| Worker+ |  | +639 (in range) | +1,671 (in range) |
| Weak | +645 | -7,464 | -15,972 |


## Per experiment (mean over modules and runs)

| coverage | Paper (Groq archive) | Replication (Foundry, 3 runs) |
|---|---|---|
| collaborative_gptoss120B_gptoss120B | 99.8 | 99.8 |
| collaborative_gptoss120B_gptoss20B | 99.7 | 99.6 |
| collaborative_gptoss120B_llama70B | 98.3 | 95.6 |
| collaborative_gptoss120B_llamaScout17B | 96.7 | 90.7 |
| collaborative_gptoss20B_gptoss120B | 100.0 | 99.7 |
| collaborative_gptoss20B_gptoss20B | 100.0 | 99.7 |
| collaborative_gptoss20B_llama70B | 89.0 | 95.8 |
| collaborative_gptoss20B_llamaScout17B | 96.2 | 90.2 |
| collaborative_llama70B_gptoss120B | 99.7 | 93.9 |
| collaborative_llama70B_gptoss20B | 99.0 | 98.7 |
| collaborative_llama70B_llama70B | 96.5 | 75.3 |
| collaborative_llama70B_llamaScout17B | 95.5 | 96.7 |
| collaborative_llamaScout17B_gptoss120B | 99.2 | 99.2 |
| collaborative_llamaScout17B_gptoss20B | 96.5 | 94.1 |
| collaborative_llamaScout17B_llama70B | 91.5 | 91.1 |
| collaborative_llamaScout17B_llamaScout17B | 96.2 | 84.9 |
| competitive_gptoss120B_gptoss120B_llama70B | 100.0 | 100.0 |
| competitive_gptoss120B_gptoss20B_llamaScout17B | 99.8 | 99.9 |
| competitive_gptoss20B_gptoss120B_llama70b | 99.8 | 99.8 |
| competitive_gptoss20B_gptoss20B_llamaScout17B | 100.0 | 99.8 |
| competitive_llama70B_gptoss120B_llama70B | 99.8 | 99.3 |
| competitive_llama70B_gptoss20B_llamaScout17B | 99.5 | 99.7 |
| competitive_llamaScout17B_gptoss120B_llama70B | 99.5 | 99.8 |
| competitive_llamaScout17B_gptoss20B_llamaScout17B | 99.7 | 98.0 |
| single_gptoss120B | 97.3 | 97.7 |
| single_gptoss20B | 93.3 | 96.2 |
| single_llama70B | 97.2 | 94.1 |
| single_llamaScout17B | 89.5 | 98.1 |

| mutation | Paper (Groq archive) | Replication (Foundry, 3 runs) |
|---|---|---|
| collaborative_gptoss120B_gptoss120B | 74.9 | 75.7 |
| collaborative_gptoss120B_gptoss20B | 75.8 | 68.1 |
| collaborative_gptoss120B_llama70B | 64.3 | 66.5 |
| collaborative_gptoss120B_llamaScout17B | 68.9 | 62.8 |
| collaborative_gptoss20B_gptoss120B | 73.8 | 71.0 |
| collaborative_gptoss20B_gptoss20B | 71.5 | 68.8 |
| collaborative_gptoss20B_llama70B | 58.6 | 60.7 |
| collaborative_gptoss20B_llamaScout17B | 59.4 | 58.7 |
| collaborative_llama70B_gptoss120B | 69.4 | 67.9 |
| collaborative_llama70B_gptoss20B | 71.9 | 66.2 |
| collaborative_llama70B_llama70B | 61.0 | 51.2 |
| collaborative_llama70B_llamaScout17B | 66.7 | 66.4 |
| collaborative_llamaScout17B_gptoss120B | 69.5 | 66.2 |
| collaborative_llamaScout17B_gptoss20B | 71.1 | 64.9 |
| collaborative_llamaScout17B_llama70B | 55.9 | 57.9 |
| collaborative_llamaScout17B_llamaScout17B | 67.2 | 54.5 |
| competitive_gptoss120B_gptoss120B_llama70B | 76.1 | 72.1 |
| competitive_gptoss120B_gptoss20B_llamaScout17B | 68.6 | 72.7 |
| competitive_gptoss20B_gptoss120B_llama70b | 73.6 | 70.6 |
| competitive_gptoss20B_gptoss20B_llamaScout17B | 72.6 | 70.5 |
| competitive_llama70B_gptoss120B_llama70B | 74.7 | 72.8 |
| competitive_llama70B_gptoss20B_llamaScout17B | 64.7 | 69.8 |
| competitive_llamaScout17B_gptoss120B_llama70B | 72.3 | 69.0 |
| competitive_llamaScout17B_gptoss20B_llamaScout17B | 69.4 | 66.4 |
| single_gptoss120B | 68.8 | 70.4 |
| single_gptoss20B | 68.6 | 66.6 |
| single_llama70B | 64.2 | 61.0 |
| single_llamaScout17B | 61.1 | 63.3 |

| tokens | Paper (Groq archive) | Replication (Foundry, 3 runs) |
|---|---|---|
| collaborative_gptoss120B_gptoss120B | 12,394 | 12,282 |
| collaborative_gptoss120B_gptoss20B | 14,750 | 37,044 |
| collaborative_gptoss120B_llama70B | 11,246 | 16,001 |
| collaborative_gptoss120B_llamaScout17B | 14,031 | 13,535 |
| collaborative_gptoss20B_gptoss120B | 21,604 | 20,318 |
| collaborative_gptoss20B_gptoss20B | 29,268 | 48,620 |
| collaborative_gptoss20B_llama70B | 25,150 | 27,762 |
| collaborative_gptoss20B_llamaScout17B | 21,197 | 33,044 |
| collaborative_llama70B_gptoss120B | 10,578 | 21,209 |
| collaborative_llama70B_gptoss20B | 17,548 | 20,172 |
| collaborative_llama70B_llama70B | 14,266 | 21,588 |
| collaborative_llama70B_llamaScout17B | 17,844 | 15,725 |
| collaborative_llamaScout17B_gptoss120B | 7,309 | 6,952 |
| collaborative_llamaScout17B_gptoss20B | 21,490 | 24,883 |
| collaborative_llamaScout17B_llama70B | 14,191 | 10,665 |
| collaborative_llamaScout17B_llamaScout17B | 21,126 | 16,388 |
| competitive_gptoss120B_gptoss120B_llama70B | 13,665 | 22,562 |
| competitive_gptoss120B_gptoss20B_llamaScout17B | 24,263 | 35,757 |
| competitive_gptoss20B_gptoss120B_llama70b | 21,630 | 42,647 |
| competitive_gptoss20B_gptoss20B_llamaScout17B | 30,854 | 58,597 |
| competitive_llama70B_gptoss120B_llama70B | 23,287 | 27,712 |
| competitive_llama70B_gptoss20B_llamaScout17B | 34,073 | 43,192 |
| competitive_llamaScout17B_gptoss120B_llama70B | 48,669 | 24,310 |
| competitive_llamaScout17B_gptoss20B_llamaScout17B | 26,588 | 30,790 |
| single_gptoss120B | 2,560 | 2,660 |
| single_gptoss20B | 6,316 | 5,194 |
| single_llama70B | 1,840 | 1,868 |
| single_llamaScout17B | 1,995 | 1,828 |

