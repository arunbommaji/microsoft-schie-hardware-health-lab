Hardware Health Monitoring & Linux Systems Engineering Lab
C++17 | Python | Linux | Multithreading | Telemetry | I2C/SPI/UART Simulation | Docker | QEMU | GitHub Actions

An educational systems-engineering project focused on concurrent telemetry collection, device-health assessment, simulated fault remediation, hardware-interface modeling, and Linux debugging. Developed as a hands-on portfolio project aligned with cloud infrastructure and hardware-health engineering.
Scope: All telemetry and remediation are simulated. This project does not access physical sensors, modify firmware, deploy Azure infrastructure, or perform production repairs.

Verified results
Metric	Result
Automated regression tests	25 passed locally
GitHub Actions CI	Successful, 26 seconds, commit ede9678
Median collector throughput	141,915 synthetic readings/second
Benchmark workload	80,000 readings/run across 8 simulated devices; 5 runs
Median execution time	0.5637 seconds
ThreadSanitizer test	8,000 readings; no data races reported in tested execution
Hardware-interface models	I2C, SPI, UART
Linux environments	Ubuntu Docker, Alpine Linux ARM64 in QEMU


The benchmark includes JSONL generation and file writing in a local Ubuntu Docker environment. Results are not production hardware measurements.
Architecture
Simulated devices
      |
      v
Multithreaded C++17 collector
      |
      v
JSONL telemetry file
      |
      v
Python health HTTP service
      |
      +----> Device health classification
      |
      +----> Fault detection and simulated remediation
                 |-- Cooldown
                 |-- Quarantine
                 `-- Recovery verification

Separate educational device protocol labs:
  - I2C register and temperature model
  - SPI register command model
  - UART frame encoding/decoding and checksum
Features
C++ collector and Python API
- Concurrent generation of synthetic temperature and power readings in C++17.
- Thread-safe coordination and JSON Lines output.
- Python standard-library HTTP API with /health, /telemetry, and /remediation endpoints.
- Simulated fault detection, cooldown, quarantine, and recovery verification.
- No physical remediation is executed.
Hardware-interface simulations
- I2C: Register reads/writes, temperature decoding, overheating, sensor failure injection, and invalid-address handling.
- SPI: Device identity, configuration register reads/writes, and invalid-command handling.
- UART: Framed payload encoding/decoding, length checks, XOR checksum validation, and corrupted-frame rejection.
These are software models, not physical bus drivers.
Linux diagnostics and testing
- GDB: breakpoints, arguments, backtraces, and multithreaded inspection.
- strace: system calls, thread creation, and synchronization inspection.
- /proc: process status, memory usage, threads, and file descriptors.
- AddressSanitizer, UndefinedBehaviorSanitizer, and ThreadSanitizer exercises. An instrumented execution without an error does not prove absence of every possible defect.
- ARM64 QEMU/EDK2 virtual machine: Alpine Linux boot, CPU and GICv3 initialization, EFI variables, PCI enumeration, VirtIO GPU/storage, and guest kernel/device inspection.
The VM lab demonstrates virtual ARM64 Linux boot and diagnostics—not physical board bring-up, U-Boot development, or driver implementation.
Quick start
Requirements: C++17 compiler, Python 3, and Make. macOS or Linux.
make build
make test
make demo
python3 -m python.health_api
In another terminal:
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/telemetry
curl http://127.0.0.1:8080/remediation
The remediation endpoint reports synthetic events. The service port can be overridden with PORT, and the telemetry source with TELEMETRY_FILE.
Compile and run hardware-interface simulations
mkdir -p build
for source in cpp/i2c_sensor_sim.cpp cpp/spi_device_sim.cpp cpp/uart_frame_sim.cpp; do
  name="$(basename "$source" .cpp)"
  g++ -std=c++17 -O2 -Wall -Wextra -Werror -pedantic "$source" -o "build/$name"
done

./build/i2c_sensor_sim
./build/spi_device_sim
./build/uart_frame_sim
Automated tests and CI
Run the test suite locally:
make test
Latest verified local output:
Ran 25 tests

OK
The GitHub Actions workflow in .github/workflows/ci.yml checks out the source, builds the collector, compiles hardware simulators with strict warning flags, executes tests, validates generated telemetry, and runs simulator programs. The first GitHub Actions run succeeded for commit ede9678 in 26 seconds.
Benchmark
Five runs of the C++ collector inside Ubuntu Docker, each generating 80,000 simulated readings:
Run	Seconds
1	0.5521
2	0.5720
3	0.5543
4	0.5744
5	0.5637


Median time: 0.5637 seconds. Median throughput: 141,915 readings/second.

Numbers describe a particular local workload and environment, not service-level or physical-device performance.
Project structure
.github/workflows/ci.yml
cpp/collector.cpp
cpp/i2c_sensor_sim.cpp
cpp/spi_device_sim.cpp
cpp/uart_frame_sim.cpp
python/health_api.py
python/remediation.py
tests/test_collector_integration.py
tests/test_fault_injection.py
tests/test_health_api.py
tests/test_i2c_sensor.py
tests/test_remediation.py
tests/test_spi_device.py
tests/test_uart_frame.py
docs/PROJECT_PLAN.md
docs/INTERVIEW_PREP.md
docs/kql_examples.kql
Dockerfile
Makefile
README.md
Limitations and future work
- All sensor measurements, faults, health states, and remediation events are simulated.
- The API is a local educational demonstration without production-grade authentication or deployment hardening.
- No real I2C/SPI/UART hardware access, GPIO integration, kernel drivers, U-Boot modifications, or firmware development is claimed.
- No Azure or production deployment and no KQL-backed telemetry integration has been verified.
- Collector behavior and throughput should not be represented as a fully production-ready streaming back-pressure design without further review.
- Potential extensions: direct tests of malformed/truncated UART frames, hardware-authorized sysfs sensor experiments, persistence, observability metrics, virtual bootloader study, and controlled Azure ingestion with appropriate security and cost constraints.
Repository
https://github.com/arunbommaji/microsoft-schie-hardware-health-lab

Project category: Educational portfolio lab for Linux systems engineering, C++ concurrency, telemetry processing, hardware-protocol simulation, and automated testing.