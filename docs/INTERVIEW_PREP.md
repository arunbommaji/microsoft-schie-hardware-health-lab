# Microsoft SCHIE — interview preparation

## Coding practice (write code and test edge cases)
1. Implement a bounded, thread-safe C++ queue with `condition_variable` and clean shutdown.
2. Merge hardware telemetry sorted by timestamp using a priority queue. Complexity: explain O(N log k).
3. Detect a device whose heartbeat is missing for 30 seconds; support out-of-order events.
4. Design rate-limited retries and exponential backoff without duplicating remediation requests.
5. Implement moving-average temperature anomaly detection; compare it with a fixed threshold.

## Linux and systems questions
1. Process vs thread; virtual memory; page faults and context switches.
2. What do `strace`, `gdb`, `/proc`, `dmesg`, and `journalctl` reveal?
3. Explain an end-to-end system call from user space to kernel space.
4. Compare SPI, I2C, UART, and GPIO. What can be simulated on macOS vs Linux?
5. Describe U-Boot / UEFI, kernel boot, kernel modules, and device drivers; distinguish what you have only studied.

## Systems design practice
Design a 100,000-device fleet monitoring platform: data volume, durable queues, schema, deduplication, observability, SLOs, incident response, regional failover, and security boundaries. Explain health signal thresholds, remediation safety, and the rule that automation must fail safely.

## Verified behavioral stories from AKMA (prepare real details)
- MTTR reduced 55%: problem, measurement baseline, actions, postmortem.
- Recovery time reduced 25%: triggers, safeguards, rollbacks.
- 2M+ Kafka events/day: retries, lag monitoring, idempotency.
- 40% reduction in query latency: measurement and performance tradeoffs.
- 98% SLA compliance: service definition and monitoring.

## Interview strategy
Be clear that your experience is cloud production engineering, not firmware production engineering. Explain how you validated the synthetic project and where further real hardware work would be required.
