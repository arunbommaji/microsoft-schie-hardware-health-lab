# Microsoft SCHIE preparation — Hardware Health Monitoring Lab

**Status:** Educational prototype using simulated hardware telemetry. Not an Azure deployment, firmware implementation, real sensor integration, or production remediation system.

## Quick start (macOS or Linux)
```bash
make build
make test
make demo
python3 -m python.health_api
```
In a second terminal:
```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/telemetry
```
The C++17 app generates synthetic temperature and power telemetry concurrently across multiple threads, emits JSON Lines, and classifies threshold breaches. The Python standard-library HTTP service summarizes latest device health and *recommends* inspection, but never executes a repair action.

## Architecture
Simulated devices → multi-threaded C++ collector → JSONL file → Python HTTP service → health assessment and remediation recommendation.

## Important limitations
- Collector finishes threads before draining the thread-safe queue; this is a bounded demonstration, not streaming back-pressure.
- Synthetic telemetry is deterministic for reproducible tests. Thresholds are illustrative and are not hardware specifications.
- No SPI/I2C/GPIO/UART, kernel driver, firmware, cloud hosting, KQL connection, persistent database, authentication, or actual repair execution is implemented.
- Dockerfile requires an existing `telemetry.jsonl`; run `make demo` before building an image.

## Linux extension milestones
1. Run under Ubuntu Linux VM or container; measure process CPU/memory using `/proc/<pid>/status` and `/proc/stat`.
2. Replace the queue with bounded producer/consumer + condition variables; measure drop rate and throughput.
3. Add fault injection, retries, idempotent remediation simulation, timestamps, and health-history persistence.
4. Introduce Linux sysfs-based sensors **only on hardware you own/control**; document permissions and safety.
5. Evaluate a simulated I2C/UART device model using QEMU or mocks; distinguish simulation from real hardware access.
6. Add Azure Monitor ingestion and KQL queries only after securing a suitable Azure account and cost controls.

## Run evidence
See `docs/PROJECT_PLAN.md`. Never claim Azure or hardware deployment without testing it.
