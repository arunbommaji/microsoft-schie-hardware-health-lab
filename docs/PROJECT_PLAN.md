# Four-week execution checklist for Microsoft SCHIE SDE (Job 200057020)

## Week 1 — C++17 and Linux
- [ ] Build and run the baseline telemetry generator locally.
- [ ] Run Python unit tests and inspect both HTTP endpoints.
- [ ] Explain mutexes, race conditions, deadlocks, and thread lifecycle with code examples.
- [ ] On a Linux VM, collect `strace`, `gdb`, `top`, and `/proc` troubleshooting evidence.
- [ ] Upgrade the C++ collector to a bounded producer-consumer queue; benchmark messages/sec and memory.

## Week 2 — hardware concepts
- [ ] Simulate malformed, stale, overheating, and disconnected device signals.
- [ ] Research SPI vs I2C vs UART vs GPIO and document a safe mock implementation for one.
- [ ] Use QEMU to observe Linux boot logs and identify kernel vs user-space responsibility.
- [ ] Write a diagram of BIOS/UEFI, bootloader, Linux kernel, init process, and user space.

## Week 3 — cloud telemetry + reliability
- [ ] Add time stamps and structured log events.
- [ ] Add synthetic fleet-scale simulation, multiple fault classes, recovery recommendations, and metrics.
- [ ] Configure a CI pipeline on GitHub or translate included workflow to Bitbucket.
- [ ] Learn KQL in a Microsoft sample environment; adapt `docs/kql_examples.kql` to real table fields.
- [ ] Optional: deploy to Azure only with explicit cost control, credential safety, and user approval.

## Week 4 — evidence + interviews + application
- [ ] Capture actual test counts and benchmarks with commands, timestamps, and Git commit ID.
- [ ] Write one-page architecture doc showing measured limits and tradeoffs.
- [ ] Complete coding, systems design, Linux debugging, and behavioral practice prompts in `docs/INTERVIEW_PREP.md`.
- [ ] Update resume with *only implemented and verified* project work.
- [ ] Apply for job 200057020; verify role location, eligibility, and immigration/work authorization details through official channels.

## Evidence log template
Date | Git SHA | Test command/result | Benchmark method/result | Failure injected/result | Source link
